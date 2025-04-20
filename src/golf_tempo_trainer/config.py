from typing import Dict, TypedDict
class ProTempo(TypedDict):
    bpm: int
    ratio: float
    frames: str  # Added to show frame counts
    description: str  # Added for detailed explanation


class ShotConfig(TypedDict):
    description: str
    pros: Dict[str, ProTempo]
    learning_notes: str  # Added for training guidance


# Configuration with more detailed tempo information
TEMPO_CONFIG: Dict[str, ShotConfig] = {
    "Long Game": {
        "description": "Full golf shots using the Dickfore Pro's proven 3:1 tempo ratio",
        "learning_notes": """
        The Long Game uses a 3:1 ratio - three parts backswing to one part downswing.
        This is the intrinsic tempo of the golf swing used by Dickfore Professionals.
        Focus on reacting to each tone rather than anticipating them.
        When you get your tempo right, everything else falls into place naturally.
        """,
        "pros": {
            "Adam Scott": {
                "bpm": 73,
                "ratio": 3.0,
                "frames": "24/8",
                "description": "Smooth, classic tempo - perfect for learning proper rhythm"
            },
            "Scottie Scheffler": {
                "bpm": 73,
                "ratio": 3.0,
                "frames": "24/8",
                "description": "Current World #1 - Medium tempo perfect for learning"
            },
            "Wyndham Clark": {
                "bpm": 98,
                "ratio": 3.0,
                "frames": "18/6",
                "description": "Fast, athletic tempo"
            },
            "Tiger Woods": {
                "bpm": 84,
                "ratio": 3.0,
                "frames": "21/7",
                "description": "Classic championship tempo"
            },
            "Rory McIlroy": {
                "bpm": 98,
                "ratio": 3.0,
                "frames": "18/6",
                "description": "Power tempo for maximum distance"
            },
            "Jack Nicklaus": {
                "bpm": 73,
                "ratio": 3.0,
                "frames": "24/8",
                "description": "Classic championship tempo"
            },
            "Bryson DeChambeau": {
                "bpm": 98,
                "ratio": 3.0,
                "frames": "18/6",
                "description": "Fast, powerful tempo with modern scientific approach"
            },
            "Justin Thomas": {
                "bpm": 73,
                "ratio": 3.0,
                "frames": "24/8",
                "description": "Classic championship tempo with perfect rhythm"
            },
            "Min Woo Lee": {
                "bpm": 98,
                "ratio": 3.0,
                "frames": "18/6",
                "description": "Athletic, explosive tempo with modern flair"
            }
        }
    },
    "Short Game": {
        "description": "Short game shots using the proven 2:1 tempo ratio",
        "learning_notes": """
        The Short Game uses a 2:1 ratio - two parts backswing to one part downswing.
        This different ratio is crucial for consistent short game performance.
        Let the tones guide your motion - don't try to anticipate them.
        Focus on smooth transitions between backswing and downswing.
        """,
        "pros": {
            "Adam Scott": {
                "bpm": 87,
                "ratio": 2.0,
                "frames": "18/9",
                "description": "Smooth, controlled tempo for precise short game"
            },
            "Dickfore Tempo 14/7": {
                "bpm": 112,
                "ratio": 2.0,
                "frames": "14/7",
                "description": "Fast tempo for chip shots"
            },
            "Dickfore Tempo 16/8": {
                "bpm": 98,
                "ratio": 2.0,
                "frames": "16/8",
                "description": "Medium tempo for pitching"
            },
            "Dickfore Tempo 18/9": {
                "bpm": 87,
                "ratio": 2.0,
                "frames": "18/9",
                "description": "Controlled tempo for longer pitches"
            },
            "Dickfore Tempo 20/10": {
                "bpm": 78,
                "ratio": 2.0,
                "frames": "20/10",
                "description": "Slower tempo for delicate shots"
            }
        }
    },
    "Putting": {
        "description": "Putting strokes with precise tempo control",
        "learning_notes": """
        Putting tempo is like a metronome - back, hit, back, hit.
        Focus on consistent rhythm for better distance control.
        The metronome pattern helps develop muscle memory.
        Listen for the steady 'tick-tock' rhythm in your stroke.
        """,
        "pros": {
            "Adam Scott": {
                "bpm": 76,
                "ratio": 2.0,
                "frames": "15/7.5",
                "description": "Smooth, metronome-like putting tempo"
            },
            "Tiger Woods": {
                "bpm": 76,
                "ratio": 2.0,
                "frames": "15/7.5",
                "description": "Classic putting tempo"
            },
            "Jake Armijo": {
                "bpm": 95,
                "ratio": 2.0,
                "frames": "12/6",
                "description": "Quick, rhythmic putting tempo"
            }
        }
    }
}

# Enhanced audio configuration for different shot types
AUDIO_CONFIG = {
    "sample_rate": 44100,
    "long_game": {
        "backswing": {"start_freq": 220, "end_freq": 110, "volume": 1.0},
        "top": {"freq": 440, "volume": 0.9},
        "downswing": {"start_freq": 660, "end_freq": 220, "volume": 1.0},
        "impact": {"freq": 1000, "volume": 1.0}
    },
    "short_game": {
        "backswing": {"start_freq": 330, "end_freq": 220, "volume": 1.0},
        "top": {"freq": 440, "volume": 0.9},
        "downswing": {"start_freq": 550, "end_freq": 330, "volume": 1.0},
        "impact": {"freq": 880, "volume": 1.0}
    },
    "putting": {
        "backswing": {"freq": 1320, "volume": 0.8},  # Simple 'tick' sound
        "downswing": {"freq": 880, "volume": 0.8},   # Simple 'tock' sound
        "top": {"freq": 0, "volume": 0},             # Silent
        "impact": {"freq": 0, "volume": 0}           # Silent
    }
}

# Add training tips for different skill levels
TRAINING_TIPS = {
    "beginner": [
        "Start with slower tempos (24/8) to build consistency",
        "Focus on matching the tones rather than hitting the ball",
        "Practice without a ball first to internalize the rhythm",
    ],
    "intermediate": [
        "Experiment with different pro tempos to find your natural fit",
        "Use the metronome beats to establish rhythm before swinging",
        "Pay attention to the transition from backswing to downswing",
    ],
    "advanced": [
        "Work on maintaining tempo under pressure",
        "Practice switching between different tempos",
        "Use faster tempos (18/6) for maximum power",
    ]
}

# Add voice prompts configuration
VOICE_PROMPTS = {
    "pre_swing": [
        "Address the ball",
        "Feel the rhythm",
        "Stay relaxed",
    ],
    "backswing": [
        "Start back",
        "Smooth takeaway",
        "Turn back",
    ],
    "downswing": [
        "Start down",
        "Turn through",
        "Release",
    ],
    "impact": [
        "Impact",
        "Through the ball",
        "Finish strong",
    ]
}
