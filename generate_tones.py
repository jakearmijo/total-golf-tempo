import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class Tone:
    frequency: int
    duration_ms: int
    volume: float = 0.8
    sample_rate: int = 44100

    def generate(self) -> np.ndarray:
        # Generate time array
        t = np.linspace(0, self.duration_ms / 1000.0,
                        int(self.sample_rate * self.duration_ms / 1000.0))

        # Generate sine wave
        samples = np.sin(2.0 * np.pi * self.frequency * t)

        # Apply envelope for smooth start/end
        envelope = np.ones_like(samples)
        attack_samples = int(0.005 * self.sample_rate)  # 5ms attack
        decay_samples = int(0.005 * self.sample_rate)   # 5ms decay
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)

        # Apply volume and convert to float32
        return (samples * envelope * self.volume).astype(np.float32)

class AudioCache:
    """
    Cache for audio segments to improve performance and reduce CPU usage
    Time Complexity: O(1) for retrievals, O(n) for initial generation
    Space Complexity: O(n) where n is number of unique tones
    """
    def __init__(self):
        self.cache_dir = Path("audio_cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.cached_segments: Dict[str, np.ndarray] = {}

    def get_tone(self, name: str, freq: float, duration_s: float, volume: float, sample_rate: int) -> np.ndarray:
        """Retrieve or generate a tone with specific parameters"""
        key = f"{name}_{freq}_{duration_s}_{volume}"

        if key not in self.cached_segments:
            cache_file = self.cache_dir / f"{key}.npy"

            if cache_file.exists():
                self.cached_segments[key] = np.load(str(cache_file))
            else:
                # Generate time array
                t = np.linspace(0, duration_s, int(sample_rate * duration_s))

                # Generate sine wave
                tone = np.sin(2 * np.pi * freq * t)

                # Apply envelope for smooth start/end
                envelope = np.ones_like(tone)
                attack_samples = int(0.005 * sample_rate)  # 5ms attack
                decay_samples = int(0.005 * sample_rate)   # 5ms decay
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)

                # Apply volume and convert to float32
                tone = (tone * envelope * volume).astype(np.float32)

                # Cache the tone
                np.save(str(cache_file), tone)
                self.cached_segments[key] = tone

        return self.cached_segments[key]

    def get_sweep(self, name: str, start_freq: float, end_freq: float, duration_s: float, volume: float, sample_rate: int) -> np.ndarray:
        """Generate a frequency sweep tone"""
        key = f"{name}_sweep_{start_freq}_{end_freq}_{duration_s}_{volume}"

        if key not in self.cached_segments:
            cache_file = self.cache_dir / f"{key}.npy"

            if cache_file.exists():
                self.cached_segments[key] = np.load(str(cache_file))
            else:
                # Generate time array
                t = np.linspace(0, duration_s, int(sample_rate * duration_s))

                # Generate frequency sweep
                freq = np.exp(np.linspace(np.log(start_freq), np.log(end_freq), len(t)))
                phase = 2 * np.pi * freq.cumsum() / sample_rate
                tone = np.sin(phase)

                # Apply envelope for smooth start/end
                envelope = np.ones_like(tone)
                attack_samples = int(0.005 * sample_rate)  # 5ms attack
                decay_samples = int(0.005 * sample_rate)   # 5ms decay
                envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
                envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)

                # Apply volume and convert to float32
                tone = (tone * envelope * volume).astype(np.float32)

                # Cache the tone
                np.save(str(cache_file), tone)
                self.cached_segments[key] = tone

        return self.cached_segments[key]

    def get_impact_click(self, volume: float = 0.9, sample_rate: int = 44100) -> np.ndarray:
        """Generate an impact click sound with harmonics"""
        key = f"impact_click_{volume}"

        if key not in self.cached_segments:
            cache_file = self.cache_dir / f"{key}.npy"

            if cache_file.exists():
                self.cached_segments[key] = np.load(str(cache_file))
            else:
                duration_s = 0.030  # 30ms duration
                t = np.linspace(0, duration_s, int(sample_rate * duration_s))

                # Generate harmonics
                harmonics = [1000, 2000, 3000]
                weights = [1.0, 0.5, 0.25]
                click = np.zeros_like(t)

                for freq, weight in zip(harmonics, weights):
                    click += weight * np.sin(2 * np.pi * freq * t)

                # Apply exponential decay envelope
                envelope = np.exp(-t * 50)  # Fast decay for impact sound
                tone = (click * envelope * volume).astype(np.float32)

                # Cache the tone
                np.save(str(cache_file), tone)
                self.cached_segments[key] = tone

        return self.cached_segments[key]

def main():
    # Create output directory
    output_dir = Path("tones")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize audio cache
    audio_cache = AudioCache()
    sample_rate = 44100

    # Generate metronome tone (E4 note - 330Hz)
    metronome_tone = audio_cache.get_tone(
        "metronome",
        freq=330.0,    # E4 note
        duration_s=0.050,  # 50ms duration
        volume=0.5,    # Half volume
        sample_rate=sample_rate
    )
    sf.write(str(output_dir / "metronome_tone.wav"), metronome_tone, sample_rate)

    # Generate backswing tone (A4 note - 440Hz)
    backswing_tone = audio_cache.get_tone(
        "backswing",
        freq=440.0,    # A4 note
        duration_s=0.100,  # 100ms duration
        volume=0.8,    # 80% volume
        sample_rate=sample_rate
    )
    sf.write(str(output_dir / "backswing_tone.wav"), backswing_tone, sample_rate)

    # Generate downswing tone (C#5 note - 554.37Hz)
    downswing_tone = audio_cache.get_tone(
        "downswing",
        freq=554.37,   # C#5 note
        duration_s=0.100,  # 100ms duration
        volume=0.8,    # 80% volume
        sample_rate=sample_rate
    )
    sf.write(str(output_dir / "downswing_tone.wav"), downswing_tone, sample_rate)

    # Generate impact tone (E5 note - 659.25Hz)
    impact_tone = audio_cache.get_tone(
        "impact",
        freq=659.25,   # E5 note
        duration_s=0.100,  # 100ms duration
        volume=0.8,    # 80% volume
        sample_rate=sample_rate
    )
    sf.write(str(output_dir / "impact_tone.wav"), impact_tone, sample_rate)
    
    print("Generated all tones:")
    print("- metronome_tone.wav (E4 note - 330Hz)")
    print("- backswing_tone.wav (A4 note - 440Hz)")
    print("- downswing_tone.wav (C#5 note - 554.37Hz)")
    print("- impact_tone.wav (E5 note - 659.25Hz)")

if __name__ == "__main__":
    main() 