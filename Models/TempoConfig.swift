import Foundation

struct ProConfig: Codable {
    let bpm: Int
    let ratio: Double
    let frames: String  // Changed to String to match Python config
    let description: String
    let learningNotes: String
}

struct ShotConfig: Codable {
    let description: String
    let pros: [String: ProConfig]
    let learningNotes: String
}

struct TempoConfig {
    static let shared = TempoConfig()
    
    let config: [String: ShotConfig] = [
        "Long Game": ShotConfig(
            description: "Full golf shots using the Dickfore Pro's proven 3:1 tempo ratio",
            pros: [
                "Adam Scott": ProConfig(
                    bpm: 73,
                    ratio: 3.0,
                    frames: "24/8",
                    description: "Smooth, classic tempo - perfect for learning proper rhythm",
                    learningNotes: "Focus on the 3:1 ratio. Let the backswing match the tone, then let the downswing happen naturally."
                ),
                "Scottie Scheffler": ProConfig(
                    bpm: 73,
                    ratio: 3.0,
                    frames: "24/8",
                    description: "Current World #1 - Medium tempo perfect for learning",
                    learningNotes: "Maintain the 3:1 ratio throughout. Focus on the smooth transition from backswing to downswing."
                ),
                "Wyndham Clark": ProConfig(
                    bpm: 98,
                    ratio: 3.0,
                    frames: "18/6",
                    description: "Fast, athletic tempo",
                    learningNotes: "Keep the rhythm quick but controlled. Focus on maintaining the 3:1 ratio at higher speed."
                ),
                "Tiger Woods": ProConfig(
                    bpm: 84,
                    ratio: 3.0,
                    frames: "21/7",
                    description: "Classic championship tempo",
                    learningNotes: "Study the master's tempo. Notice how he maintains the 3:1 ratio even under pressure."
                ),
                "Rory McIlroy": ProConfig(
                    bpm: 98,
                    ratio: 3.0,
                    frames: "18/6",
                    description: "Power tempo for maximum distance",
                    learningNotes: "Fast but controlled. Let the 3:1 ratio guide your power generation."
                ),
                "Jack Nicklaus": ProConfig(
                    bpm: 73,
                    ratio: 3.0,
                    frames: "24/8",
                    description: "Classic championship tempo",
                    learningNotes: "The Golden Bear's tempo is timeless. Focus on the smooth 3:1 rhythm."
                ),
                "Bryson DeChambeau": ProConfig(
                    bpm: 98,
                    ratio: 3.0,
                    frames: "18/6",
                    description: "Fast, powerful tempo with modern scientific approach",
                    learningNotes: "Combine scientific precision with the 3:1 ratio for maximum power."
                ),
                "Justin Thomas": ProConfig(
                    bpm: 73,
                    ratio: 3.0,
                    frames: "24/8",
                    description: "Classic championship tempo with perfect rhythm",
                    learningNotes: "Study JT's smooth transition while maintaining the 3:1 ratio."
                ),
                "Min Woo Lee": ProConfig(
                    bpm: 98,
                    ratio: 3.0,
                    frames: "18/6",
                    description: "Athletic, explosive tempo with modern flair",
                    learningNotes: "Combine athleticism with the 3:1 ratio for a powerful, modern swing."
                )
            ],
            learningNotes: "The Long Game uses a 3:1 ratio - three parts backswing to one part downswing. This is the intrinsic tempo of the golf swing used by Dickfore Professionals. Focus on reacting to each tone rather than anticipating them. When you get your tempo right, everything else falls into place naturally."
        ),
        "Short Game": ShotConfig(
            description: "Short game shots using the proven 2:1 tempo ratio",
            pros: [
                "Adam Scott": ProConfig(
                    bpm: 87,
                    ratio: 2.0,
                    frames: "18/9",
                    description: "Smooth, controlled tempo for precise short game",
                    learningNotes: "Use the 2:1 ratio for better control. Keep the rhythm consistent and focus on smooth transitions."
                ),
                "Dickfore Tempo 14/7": ProConfig(
                    bpm: 112,
                    ratio: 2.0,
                    frames: "14/7",
                    description: "Fast tempo for chip shots",
                    learningNotes: "Quick, crisp tempo perfect for chip shots. Maintain the 2:1 ratio for consistency."
                ),
                "Dickfore Tempo 16/8": ProConfig(
                    bpm: 98,
                    ratio: 2.0,
                    frames: "16/8",
                    description: "Medium tempo for pitching",
                    learningNotes: "Balanced tempo for standard pitch shots. Focus on the 2:1 ratio for distance control."
                ),
                "Dickfore Tempo 18/9": ProConfig(
                    bpm: 87,
                    ratio: 2.0,
                    frames: "18/9",
                    description: "Controlled tempo for longer pitches",
                    learningNotes: "Slower, more controlled tempo for longer pitch shots. Maintain the 2:1 ratio for consistency."
                ),
                "Dickfore Tempo 20/10": ProConfig(
                    bpm: 78,
                    ratio: 2.0,
                    frames: "20/10",
                    description: "Slower tempo for delicate shots",
                    learningNotes: "Very controlled tempo for delicate shots. Focus on maintaining the 2:1 ratio for precision."
                )
            ],
            learningNotes: "The Short Game uses a 2:1 ratio - two parts backswing to one part downswing. This different ratio is crucial for consistent short game performance. Let the tones guide your motion - don't try to anticipate them. Focus on smooth transitions between backswing and downswing."
        ),
        "Putting": ShotConfig(
            description: "Putting strokes with precise tempo control",
            pros: [
                "Adam Scott": ProConfig(
                    bpm: 76,
                    ratio: 2.0,
                    frames: "15/7.5",
                    description: "Smooth, metronome-like putting tempo",
                    learningNotes: "Think 'tick-tock' like a metronome. Use the rhythm for distance control."
                ),
                "Tiger Woods": ProConfig(
                    bpm: 76,
                    ratio: 2.0,
                    frames: "15/7.5",
                    description: "Classic putting tempo",
                    learningNotes: "Study Tiger's consistent putting tempo. Focus on the metronome-like rhythm."
                ),
                "Jake Armijo": ProConfig(
                    bpm: 85,
                    ratio: 2.0,
                    frames: "12/6",
                    description: "Quick, rhythmic putting tempo",
                    learningNotes: "Faster tempo for confident putting. Maintain the rhythm for distance control."
                )
            ],
            learningNotes: "Putting tempo is like a metronome - back, hit, back, hit. Focus on consistent rhythm for better distance control. The metronome pattern helps develop muscle memory. Listen for the steady 'tick-tock' rhythm in your stroke."
        )
    ]
} 
} 