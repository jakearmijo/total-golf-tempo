import SwiftUI

struct ContentView: View {
    @StateObject private var viewModel = TempoTrainerViewModel()
    
    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                Text("Total Tempo")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                
                if viewModel.isTraining {
                    TrainingView(viewModel: viewModel)
                } else {
                    ShotTypeSelectionView(viewModel: viewModel)
                }
            }
            .padding()
        }
    }
}

#Preview {
    ContentView()
} 