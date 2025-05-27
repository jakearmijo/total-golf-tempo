import Foundation
import AVFoundation

class AudioPlayer {
    private var audioEngine: AVAudioEngine?
    private var playerNode: AVAudioPlayerNode?
    private var currentShotType: String?
    private var currentPro: String?
    private var backswingTime: TimeInterval = 1.0
    private var downswingTime: TimeInterval = 1.0
    
    func setShotType(_ shotType: String) {
        currentShotType = shotType
    }
    
    func setCurrentPro(_ proName: String) {
        currentPro = proName
    }
    
    func setTiming(backswingTime: TimeInterval, downswingTime: TimeInterval) {
        self.backswingTime = backswingTime
        self.downswingTime = downswingTime
    }
    
    func playSwingSequence() {
        // Play takeaway tone
        playTone(for: .takeaway)
        
        // Schedule downswing tone
        DispatchQueue.main.asyncAfter(deadline: .now() + backswingTime) { [weak self] in
            self?.playTone(for: .downswing)
            
            // Schedule impact tone
            DispatchQueue.main.asyncAfter(deadline: .now() + (self?.downswingTime ?? 1.0)) { [weak self] in
                self?.playTone(for: .impact)
            }
        }
    }
    
    private func playTone(for phase: SwingPhase) {
        let toneName: String
        switch phase {
        case .takeaway:
            toneName = "takeaway_tone"
        case .downswing:
            toneName = "downswing_tone"
        case .impact:
            toneName = "impact_tone"
        case .idle:
            return
        }
        
        guard let url = Bundle.main.url(forResource: toneName, withExtension: "wav") else {
            print("Could not find audio file: \(toneName)")
            return
        }
        
        do {
            let player = try AVAudioPlayer(contentsOf: url)
            player.play()
        } catch {
            print("Failed to play audio: \(error)")
        }
    }
    
    func cleanup() {
        audioEngine?.stop()
        audioEngine = nil
        playerNode = nil
    }
} 