import SwiftUI

struct TrainingView: View {
    @ObservedObject var viewModel: TempoTrainerViewModel
    @State private var progress: CGFloat = 0.0
    
    private var currentPhaseDuration: TimeInterval {
        guard let tempo = viewModel.currentTempo else { return 1.0 }
        
        switch viewModel.currentPhase {
        case .takeaway:
            return tempo.backswingDuration
        case .downswing:
            return tempo.downswingDuration
        case .impact:
            return 1.0 // Pause at impact
        case .idle:
            return 1.0
        case .metronome:
            return 1.0
        }
    }
    
    var body: some View {
        VStack(spacing: 30) {
            Text("Training Session")
                .font(.title)
                .fontWeight(.bold)
            
            // Phase indicator
            VStack(spacing: 15) {
                Text("Current Phase")
                    .font(.headline)
                
                Text(phaseText)
                    .font(.title2)
                    .foregroundColor(.blue)
                
                if let tempo = viewModel.currentTempo {
                    Text("\(Int(tempo.ratio)):1 Ratio")
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            .padding()
            .background(Color.blue.opacity(0.1))
            .cornerRadius(15)
            
            // Swing Feedback
            SwingFeedbackView(
                phase: viewModel.currentPhase,
                feedback: viewModel.lastSwingAccuracy.map { accuracy in
                    switch accuracy {
                    case .perfect:
                        return .good
                    case .good:
                        return .good
                    case .needsWork:
                        return .needsWork
                    }
                } ?? .waiting,
                progress: progress
            )
            
            // Learning Notes
            if let tempo = viewModel.currentTempo,
               let shotConfig = TempoConfig.shared.config[tempo.shotType],
               let proConfig = shotConfig.pros[tempo.proName] {
                VStack(alignment: .leading, spacing: 10) {
                    Text("Learning Focus")
                        .font(.headline)
                    
                    Text(proConfig.learningNotes)
                        .font(.body)
                        .foregroundColor(.secondary)
                }
                .padding()
                .background(Color.gray.opacity(0.1))
                .cornerRadius(15)
            }
            
            // Instructions
            VStack(alignment: .leading, spacing: 10) {
                Text("Instructions:")
                    .font(.headline)
                Text("1. First tone - Start your takeaway")
                Text("2. Second tone - Start your downswing")
                Text("3. Third tone - Impact position")
                
                if viewModel.currentTempo?.shotType == "Putting" {
                    Text("4. Maintain consistent tempo for distance control")
                        .foregroundColor(.blue)
                }
            }
            .padding()
            .background(Color.gray.opacity(0.1))
            .cornerRadius(15)
            
            // Stop button
            Button(action: {
                viewModel.stopTraining()
            }) {
                Text("Stop Training")
                    .font(.headline)
                    .foregroundColor(.white)
                    .frame(maxWidth: .infinity)
                    .padding()
                    .background(Color.red)
                    .cornerRadius(10)
            }
        }
        .padding()
        .onChange(of: viewModel.currentPhase) { oldPhase, newPhase in
            // Reset and animate progress when phase changes
            withAnimation(.linear(duration: currentPhaseDuration)) {
                progress = 0.0
            }
            withAnimation(.linear(duration: currentPhaseDuration)) {
                progress = 1.0
            }
        }
    }
    
    private var phaseText: String {
        switch viewModel.currentPhase {
        case .idle:
            return "Ready"
        case .takeaway:
            return "Takeaway"
        case .downswing:
            return "Downswing"
        case .impact:
            return "Impact"
        case .metronome:
            return "Metronome"
        }
    }
}

#Preview {
    TrainingView(viewModel: TempoTrainerViewModel())
} 