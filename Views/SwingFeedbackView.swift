import SwiftUI

struct SwingFeedbackView: View {
    let phase: SwingPhase
    let feedback: SwingAnalyzer.SwingFeedback
    let progress: CGFloat
    
    var body: some View {
        VStack(spacing: 15) {
            // Circular progress indicator
            ZStack {
                Circle()
                    .stroke(Color.gray.opacity(0.2), lineWidth: 8)
                    .frame(width: 120, height: 120)
                
                Circle()
                    .trim(from: 0, to: progress)
                    .stroke(feedbackColor, lineWidth: 8)
                    .frame(width: 120, height: 120)
                    .rotationEffect(.degrees(-90))
                
                // Phase markers
                ForEach(0..<3) { index in
                    Circle()
                        .fill(feedbackColor)
                        .frame(width: 8, height: 8)
                        .offset(y: -60)
                        .rotationEffect(.degrees(Double(index) * 120))
                }
                
                // Center text
                Text(phaseText)
                    .font(.headline)
                    .foregroundColor(feedbackColor)
            }
            
            // Feedback text
            Text(feedbackText)
                .font(.subheadline)
                .foregroundColor(feedbackColor)
        }
    }
    
    private var feedbackColor: Color {
        switch feedback {
        case .good:
            return .green
        case .close:
            return .yellow
        case .needsWork:
            return .red
        case .waiting:
            return .gray
        }
    }
    
    private var phaseText: String {
        switch phase {
        case .takeaway:
            return "1"
        case .downswing:
            return "2"
        case .impact:
            return "3"
        case .idle:
            return "Ready"
        case .metronome:
            return "♪"
        }
    }
    
    private var feedbackText: String {
        switch feedback {
        case .good:
            return "Perfect Timing!"
        case .close:
            return "Almost There"
        case .needsWork:
            return "Try Again"
        case .waiting:
            return "Waiting..."
        }
    }
}

#Preview {
    SwingFeedbackView(
        phase: .takeaway,
        feedback: .good,
        progress: 0.75
    )
} 