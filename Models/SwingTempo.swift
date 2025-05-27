import Foundation

struct SwingTempo: Identifiable {
    let id = UUID()
    let shotType: String
    let proName: String
    let bpm: Int
    let ratio: Double
    let frames: String
    let description: String
    let learningNotes: String
    
    // Time intervals in seconds
    var backswingDuration: Double {
        return (60.0 / Double(bpm)) * ratio
    }
    
    var downswingDuration: Double {
        return (60.0 / Double(bpm))
    }
} 