import SwiftUI

struct ShotTypeSelectionView: View {
    @ObservedObject var viewModel: TempoTrainerViewModel
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Select Shot Type")
                .font(.title2)
                .fontWeight(.semibold)
            
            ForEach(Array(TempoConfig.shared.config.keys.sorted()), id: \.self) { shotType in
                Button(action: {
                    viewModel.selectedShotType = shotType
                }) {
                    HStack {
                        Text(shotType)
                            .font(.headline)
                        Spacer()
                        Image(systemName: "chevron.right")
                    }
                    .padding()
                    .background(Color.blue.opacity(0.1))
                    .cornerRadius(10)
                }
            }
            
            if let selectedShotType = viewModel.selectedShotType {
                NavigationLink(destination: ProSelectionView(viewModel: viewModel)) {
                    Text("Continue to \(selectedShotType) Pros")
                        .font(.headline)
                        .foregroundColor(.white)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .cornerRadius(10)
                }
            }
        }
        .padding()
    }
}

#Preview {
    ShotTypeSelectionView(viewModel: TempoTrainerViewModel())
} 