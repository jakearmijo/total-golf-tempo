import Foundation
import AVFoundation

class TempoTrainerViewModel: ObservableObject {
    // MARK: - Published Properties
    @Published var currentPhase: SwingPhase = .idle
    @Published var isTraining = false
    @Published var lastSwingAccuracy: SwingAccuracy?
    @Published var lastSwingTiming: Double?
    @Published var selectedShotType: String?
    @Published var selectedPro: String?
    @Published var currentTempo: SwingTempo?
    
    // MARK: - Private Properties
    private var swingAnalyzer: SwingAnalyzer?
    private var currentPhaseTimer: Timer?
    
    // MARK: - Public Methods
    func startTraining(with tempo: SwingTempo) {
        isTraining = true
        currentTempo = tempo
        
        // Initialize analyzer
        swingAnalyzer = SwingAnalyzer()
        
        // Configure audio service
        AudioService.shared.setShotType(tempo.shotType)
        AudioService.shared.setCurrentPro(tempo.proName)
        AudioService.shared.setTiming(
            backswingTime: tempo.backswingDuration,
            downswingTime: tempo.downswingDuration
        )
        
        // Start swing analysis
        swingAnalyzer?.startAnalysis { [weak self] accuracy, timing in
            DispatchQueue.main.async {
                self?.lastSwingAccuracy = accuracy
                self?.lastSwingTiming = timing
            }
        }
        
        // Start training sequence
        startTrainingSequence()
    }
    
    func stopTraining() {
        isTraining = false
        currentPhase = .idle
        currentTempo = nil
        
        // Cleanup
        currentPhaseTimer?.invalidate()
        currentPhaseTimer = nil
        AudioService.shared.cleanup()
        swingAnalyzer?.stopAnalysis()
    }
    
    // MARK: - Private Methods
    private func startTrainingSequence() {
        // Start with a delay to allow setup
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) { [weak self] in
            self?.playNextPhase()
        }
    }
    
    private func playNextPhase() {
        guard isTraining else { return }
        
        switch currentPhase {
        case .idle:
            currentPhase = .takeaway
            AudioService.shared.playSwingSequence()
            startPhaseTimer(duration: 1.0)
            
        case .takeaway:
            currentPhase = .downswing
            startPhaseTimer(duration: 1.0)
            
        case .downswing:
            currentPhase = .impact
            startPhaseTimer(duration: 1.0)
            
        case .impact:
            currentPhase = .idle
            // Wait before next sequence
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
                self?.playNextPhase()
            }
            
        case .metronome:
            // Metronome is handled within the AudioService.playSwingSequence()
            // No need to handle it here as it's part of the sequence
            break
        }
    }
    
    private func startPhaseTimer(duration: TimeInterval) {
        currentPhaseTimer?.invalidate()
        currentPhaseTimer = Timer.scheduledTimer(withTimeInterval: duration, repeats: false) { [weak self] _ in
            self?.playNextPhase()
        }
    }
} 