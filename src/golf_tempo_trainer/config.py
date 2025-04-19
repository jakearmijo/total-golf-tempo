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
        "description": "Full golf shots using the Tour Pro's proven 3:1 tempo ratio",
        "learning_notes": """
        The Long Game uses a 3:1 ratio - three parts backswing to one part downswing.
        This is the intrinsic tempo of the golf swing used by Tour Professionals.
        Practice these tempos until they become subconscious, eliminating the need
        to think about tempo during play.
        """,
        "pros": {
            "Tour Tempo 18/6": {
                "bpm": 98,
                "ratio": 3.0,
                "frames": "18/6",
                "description": "Fastest tempo - great for athletic players"
            },
            "Tour Tempo 21/7": {
                "bpm": 84,
                "ratio": 3.0,
                "frames": "21/7",
                "description": "Medium-fast tempo - most common among pros"
            },
            "Tour Tempo 24/8": {
                "bpm": 73,
                "ratio": 3.0,
                "frames": "24/8",
                "description": "Medium tempo - good for learning"
            },
            "Tour Tempo 27/9": {
                "bpm": 65,
                "ratio": 3.0,
                "frames": "27/9",
                "description": "Slower tempo - great for practice"
            }
        }
    },
    "Short Game": {
        "description": "Short game shots using the proven 2:1 tempo ratio",
        "learning_notes": """
        The Short Game uses a 2:1 ratio - two parts backswing to one part downswing.
        This different ratio is crucial for consistent short game performance and
        was discovered through study of top touring professionals.
        """,
        "pros": {
            "Tour Tempo 14/7": {
                "bpm": 112,
                "ratio": 2.0,
                "frames": "14/7",
                "description": "Fast tempo for chip shots"
            },
            "Tour Tempo 16/8": {
                "bpm": 98,
                "ratio": 2.0,
                "frames": "16/8",
                "description": "Medium tempo for pitching"
            },
            "Tour Tempo 18/9": {
                "bpm": 87,
                "ratio": 2.0,
                "frames": "18/9",
                "description": "Controlled tempo for longer pitches"
            },
            "Tour Tempo 20/10": {
                "bpm": 78,
                "ratio": 2.0,
                "frames": "20/10",
                "description": "Slower tempo for delicate shots"
            }
        }
    },
    "Putting": {
        "description": "Putting strokes with precise tempo control",
        "learning_notes": "Putting requires consistent tempo for distance control",
        "pros": {
            "Tiger Woods": {
                "bpm": 76,
                "ratio": 2.0,
                "frames": "15/7.5",
                "description": "Classic putting tempo"
            }
        }
    }
}

# Enhanced audio configuration for different shot types
AUDIO_CONFIG = {
    "sample_rate": 44100,
    "long_game": {
        "backswing": {"start_freq": 220, "end_freq": 110, "volume": 0.8},
        "top": {"freq": 440, "volume": 0.75},
        "downswing": {"start_freq": 660, "end_freq": 220, "volume": 0.8},
        "impact": {"freq": 1000, "volume": 0.9}
    },
    "short_game": {
        "backswing": {"start_freq": 330, "end_freq": 220, "volume": 0.8},
        "top": {"freq": 440, "volume": 0.75},
        "downswing": {"start_freq": 550, "end_freq": 330, "volume": 0.8},
        "impact": {"freq": 880, "volume": 0.85}
    },
    "putting": {
        "backswing": {"start_freq": 440, "end_freq": 330, "volume": 0.7},
        "top": {"freq": 550, "volume": 0.7},
        "downswing": {"start_freq": 660, "end_freq": 440, "volume": 0.7},
        "impact": {"freq": 770, "volume": 0.8}
    }
}
