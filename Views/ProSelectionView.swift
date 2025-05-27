import SwiftUI

struct ProSelectionView: View {
    @ObservedObject var viewModel: TempoTrainerViewModel
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Select Pro")
                .font(.title2)
                .fontWeight(.semibold)
            
            if let shotType = viewModel.selectedShotType,
               let shotConfig = TempoConfig.shared.config[shotType] {
                ScrollView {
                    VStack(spacing: 12) {
                        ForEach(Array(shotConfig.pros.keys.sorted()), id: \.self) { proName in
                            Button(action: {
                                viewModel.selectedPro = proName
                            }) {
                                VStack(alignment: .leading, spacing: 8) {
                                    Text(proName)
                                        .font(.headline)
                                    if let proConfig = shotConfig.pros[proName] {
                                        Text("BPM: \(proConfig.bpm) • Frames: \(proConfig.frames)")
                                            .font(.subheadline)
                                        Text(proConfig.description)
                                            .font(.caption)
                                            .foregroundColor(.gray)
                                    }
                                }
                                .padding()
                                .frame(maxWidth: .infinity, alignment: .leading)
                                .background(viewModel.selectedPro == proName ? Color.blue.opacity(0.2) : Color.blue.opacity(0.1))
                                .cornerRadius(10)
                            }
                        }
                    }
                }
                
                if let selectedPro = viewModel.selectedPro,
                   let proConfig = shotConfig.pros[selectedPro] {
                    NavigationLink(destination: TrainingView(viewModel: viewModel)) {
                        Text("Start Training")
                            .font(.headline)
                            .foregroundColor(.white)
                            .frame(maxWidth: .infinity)
                            .padding()
                            .background(Color.blue)
                            .cornerRadius(10)
                    }
                    .onAppear {
                        // Create SwingTempo instance when navigating
                        let tempo = SwingTempo(
                            shotType: shotType,
                            proName: selectedPro,
                            bpm: proConfig.bpm,
                            ratio: proConfig.ratio,
                            frames: proConfig.frames,
                            description: proConfig.description,
                            learningNotes: shotConfig.learningNotes
                        )
                        viewModel.startTraining(with: tempo)
                    }
                }
            }
        }
        .padding()
    }
}

#Preview {
    ProSelectionView(viewModel: TempoTrainerViewModel())
} 