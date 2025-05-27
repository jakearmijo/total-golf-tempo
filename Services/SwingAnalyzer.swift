import Foundation
#if os(iOS)
import AVFoundation
#else
import CoreAudio
import CoreAudioKit
#endif
import Accelerate

class SwingAnalyzer: NSObject, ObservableObject {
    @Published var swingFeedback: SwingFeedback = .waiting
    @Published var timingAccuracy: [Double] = []  // Store timing accuracy for each phase
    
    #if os(iOS)
    private var audioEngine: AVAudioEngine?
    private var inputNode: AVAudioInputNode?
    #else
    private var audioQueue: AudioQueueRef?
    #endif
    
    private var isAnalyzing = false
    
    private let bufferSize = 1024
    private let sampleRate: Double = 44100.0
    private var audioBuffer: [Float] = []
    private var lastPeakTime: Date?
    private var analysisCallback: ((SwingAccuracy, Double) -> Void)?
    
    enum SwingFeedback {
        case waiting
        case good
        case close
        case needsWork
    }
    
    override init() {
        super.init()
        setupAudioEngine()
    }
    
    private func setupAudioEngine() {
        #if os(iOS)
        audioEngine = AVAudioEngine()
        inputNode = audioEngine?.inputNode
        
        let inputFormat = inputNode?.outputFormat(forBus: 0)
        
        inputNode?.installTap(onBus: 0, bufferSize: AVAudioFrameCount(bufferSize), format: inputFormat) { [weak self] buffer, time in
            self?.processAudioBuffer(buffer)
        }
        
        do {
            try audioEngine?.start()
        } catch {
            print("Failed to start audio engine: \(error)")
        }
        #else
        // macOS implementation using CoreAudio
        var streamFormat = AudioStreamBasicDescription(
            mSampleRate: sampleRate,
            mFormatID: kAudioFormatLinearPCM,
            mFormatFlags: kAudioFormatFlagIsFloat | kAudioFormatFlagIsPacked,
            mBytesPerPacket: 4,
            mFramesPerPacket: 1,
            mBytesPerFrame: 4,
            mChannelsPerFrame: 1,
            mBitsPerChannel: 32,
            mReserved: 0
        )
        
        let userData = UnsafeMutableRawPointer(Unmanaged.passUnretained(self).toOpaque())
        
        AudioQueueNewInput(
            &streamFormat,
            { (userData, queue, buffer, startTime, numPackets, packetDesc) in
                let analyzer = Unmanaged<SwingAnalyzer>.fromOpaque(userData!).takeUnretainedValue()
                analyzer.processAudioBuffer(buffer)
            },
            userData,
            nil,
            nil,
            0,
            &audioQueue
        )
        
        if let queue = audioQueue {
            AudioQueueStart(queue, nil)
        }
        #endif
    }
    
    private func processAudioBuffer(_ buffer: AudioQueueBufferRef) {
        #if os(iOS)
        guard let channelData = buffer.floatChannelData?[0] else { return }
        let frameCount = Int(buffer.frameLength)
        
        // Convert buffer to array
        let samples = Array(UnsafeBufferPointer(start: channelData, count: frameCount))
        audioBuffer.append(contentsOf: samples)
        #else
        let frameCount = Int(buffer.pointee.mAudioDataByteSize) / MemoryLayout<Float>.size
        let samples = Array(UnsafeBufferPointer(start: buffer.pointee.mAudioData.assumingMemoryBound(to: Float.self),
                                              count: frameCount))
        audioBuffer.append(contentsOf: samples)
        #endif
        
        // Keep buffer size manageable
        if audioBuffer.count > Int(sampleRate * 2) { // 2 seconds of audio
            audioBuffer.removeFirst(samples.count)
        }
        
        // Detect peaks in the audio
        detectPeaks()
    }
    
    private func detectPeaks() {
        guard audioBuffer.count >= bufferSize else { return }
        
        // Calculate RMS value for the current buffer
        var rms: Float = 0
        vDSP_rmsqv(audioBuffer.suffix(bufferSize), 1, &rms, vDSP_Length(bufferSize))
        
        // If we detect a significant peak
        if rms > 0.1 { // Adjust threshold as needed
            let now = Date()
            if let lastPeak = lastPeakTime {
                let timeSinceLastPeak = now.timeIntervalSince(lastPeak)
                analyzeTiming(timeSinceLastPeak)
            }
            lastPeakTime = now
        }
    }
    
    private func analyzeTiming(_ timeInterval: Double) {
        // Compare the detected timing with expected timing
        let expectedInterval = 0.5 // Example expected interval
        let accuracy = abs(timeInterval - expectedInterval)
        
        timingAccuracy.append(accuracy)
        if timingAccuracy.count > 3 {
            timingAccuracy.removeFirst()
        }
        
        // Update feedback based on accuracy
        let feedback: SwingAccuracy
        if accuracy < 0.05 {
            feedback = .perfect
        } else if accuracy < 0.1 {
            feedback = .good
        } else {
            feedback = .needsWork
        }
        
        DispatchQueue.main.async {
            self.analysisCallback?(feedback, accuracy)
        }
    }
    
    func startAnalysis(completion: @escaping (SwingAccuracy, Double) -> Void) {
        isAnalyzing = true
        timingAccuracy.removeAll()
        swingFeedback = .waiting
        analysisCallback = completion
    }
    
    func stopAnalysis() {
        isAnalyzing = false
        #if os(iOS)
        audioEngine?.stop()
        audioEngine?.inputNode.removeTap(onBus: 0)
        #else
        if let queue = audioQueue {
            AudioQueueStop(queue, true)
            AudioQueueDispose(queue, true)
        }
        #endif
        analysisCallback = nil
    }
    
    deinit {
        stopAnalysis()
    }
} 