import Foundation
#if os(iOS)
import AVFoundation
#else
import AVFAudio
#endif

class AudioService {
    static let shared = AudioService()
    private var audioPlayers: [URL: AVAudioPlayer] = [:]
    private var currentShotType: String?
    private var currentPro: String?
    private var backswingTime: TimeInterval = 1.0
    private var downswingTime: TimeInterval = 1.0
    private var speechSynthesizer: AVSpeechSynthesizer?
    private var isFirstSequence = true
    
    // Audio configuration matching Python implementation
    private let audioConfig: [String: [String: [String: Any]]] = [
        "long_game": [
            "backswing": ["start_freq": 220, "end_freq": 110, "volume": 1.0],
            "top": ["freq": 440, "volume": 0.9],
            "downswing": ["start_freq": 660, "end_freq": 220, "volume": 1.0],
            "impact": ["freq": 1000, "volume": 1.0]
        ],
        "short_game": [
            "backswing": ["start_freq": 330, "end_freq": 220, "volume": 1.0],
            "top": ["freq": 440, "volume": 0.9],
            "downswing": ["start_freq": 550, "end_freq": 330, "volume": 1.0],
            "impact": ["freq": 880, "volume": 1.0]
        ],
        "putting": [
            "backswing": ["freq": 1320, "volume": 0.8],
            "downswing": ["freq": 880, "volume": 0.8],
            "top": ["freq": 0, "volume": 0],
            "impact": ["freq": 0, "volume": 0]
        ]
    ]
    
    private init() {
        #if os(iOS)
        setupAudioSession()
        #endif
        speechSynthesizer = AVSpeechSynthesizer()
    }
    
    #if os(iOS)
    private func setupAudioSession() {
        do {
            try AVAudioSession.sharedInstance().setCategory(.playAndRecord, mode: .default)
            try AVAudioSession.sharedInstance().setActive(true)
        } catch {
            print("Failed to set up audio session: \(error)")
        }
    }
    #endif
    
    func setShotType(_ shotType: String) {
        currentShotType = shotType.lowercased().replacingOccurrences(of: " ", with: "_")
    }
    
    func setCurrentPro(_ proName: String) {
        currentPro = proName
        isFirstSequence = true
    }
    
    func setTiming(backswingTime: TimeInterval, downswingTime: TimeInterval) {
        self.backswingTime = backswingTime
        self.downswingTime = downswingTime
    }
    
    func playSwingSequence() {
        // Play pro name announcement only on first sequence
        if isFirstSequence, let proName = currentPro {
            speak("Starting \(proName)")
            Thread.sleep(forTimeInterval: 0.5)
            isFirstSequence = false
        }
        
        // Play "Address the ball" voice prompt
        speak("Address the ball")
        Thread.sleep(forTimeInterval: 1.0)
        
        // Play 4 metronome beats to establish rhythm
        let beatInterval = backswingTime / 3 // Divide backswing into 3 beats
        for _ in 0..<4 {
            playTone(for: .metronome)
            Thread.sleep(forTimeInterval: beatInterval)
        }
        
        // Play takeaway tone
        playTone(for: .takeaway)
        
        // Schedule downswing tone with precise timing
        DispatchQueue.main.asyncAfter(deadline: .now() + backswingTime) { [weak self] in
            self?.playTone(for: .downswing)
            
            // Schedule impact tone with precise timing
            DispatchQueue.main.asyncAfter(deadline: .now() + (self?.downswingTime ?? 1.0)) { [weak self] in
                self?.playTone(for: .impact)
            }
        }
    }
    
    private func speak(_ text: String) {
        let utterance = AVSpeechUtterance(string: text)
        utterance.rate = 0.5 // Slower rate for clarity
        utterance.volume = 1.0
        speechSynthesizer?.speak(utterance)
    }
    
    func playTone(for phase: SwingPhase) {
        let toneName: String
        let volume: Float
        
        switch phase {
        case .takeaway:
            toneName = "takeaway_tone"
            volume = 1.0
        case .downswing:
            toneName = "downswing_tone"
            volume = 1.0
        case .impact:
            toneName = "impact_tone"
            volume = 1.0
        case .metronome:
            toneName = "metronome_tone"
            volume = 0.5 // Softer volume for metronome
        case .idle:
            return
        }
        
        guard let url = Bundle.main.url(forResource: toneName, withExtension: "wav") else {
            print("Could not find audio file: \(toneName)")
            return
        }
        
        if let player = audioPlayers[url] {
            player.currentTime = 0
            player.volume = volume
            player.play()
        } else {
            do {
                let player = try AVAudioPlayer(contentsOf: url)
                player.volume = volume
                audioPlayers[url] = player
                player.play()
            } catch {
                print("Failed to play audio: \(error)")
            }
        }
    }
    
    func cleanup() {
        audioPlayers.removeAll()
        speechSynthesizer?.stopSpeaking(at: .immediate)
        isFirstSequence = true
    }
} 