import os
import numpy as np
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, Optional
from pydub import AudioSegment
from pydub.playback import play as pydub_play
from .config import AUDIO_CONFIG
import time
import pyttsx3


@dataclass
class Tone:
    frequency: int
    duration_ms: int
    volume: float = 0.8  # Default volume
    sample_rate: int = AUDIO_CONFIG["sample_rate"]

    def generate(self) -> AudioSegment:
        # Generate time array
        t = np.linspace(0, self.duration_ms / 1000.0,
                        int(self.sample_rate * self.duration_ms / 1000.0))

        # Generate sine wave
        samples = np.sin(2.0 * np.pi * self.frequency * t)

        # Convert to 16-bit PCM
        samples = (samples * 32767).astype(np.int16)

        # Create AudioSegment from raw PCM data
        audio = AudioSegment(
            samples.tobytes(),
            frame_rate=self.sample_rate,
            sample_width=2,  # 16-bit = 2 bytes
            channels=1       # mono
        )

        # Apply volume adjustment
        return audio.apply_gain(self.volume)


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

    def get_tone(self,
                 name: str,
                 freq: float,
                 duration_s: float,
                 volume: float,
                 sample_rate: int) -> np.ndarray:
        """
        Retrieve or generate a tone with specific parameters
        """
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


class ToneGenerator:
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def generate_sweep(self, start_freq: float, end_freq: float, duration_s: float, volume: float = 0.8) -> np.ndarray:
        """Generate a frequency sweep"""
        t = np.linspace(0, duration_s, int(self.sample_rate * duration_s))
        freq = np.exp(np.linspace(
            np.log(start_freq), np.log(end_freq), len(t)))
        tone = np.sin(2 * np.pi * freq.cumsum() / self.sample_rate)
        envelope = np.ones_like(tone)
        attack_samples = int(0.01 * self.sample_rate)
        decay_samples = int(0.01 * self.sample_rate)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
        return (tone * envelope * volume).astype(np.float32)

    def generate_impact_click(self, volume: float = 0.9) -> np.ndarray:
        """Generate an impact click sound"""
        duration_s = 0.030
        t = np.linspace(0, duration_s, int(self.sample_rate * duration_s))
        harmonics = [1000, 2000, 3000]
        weights = [1.0, 0.5, 0.25]
        click = np.zeros_like(t)
        for freq, weight in zip(harmonics, weights):
            click += weight * np.sin(2 * np.pi * freq * t)
        envelope = np.exp(-t * 50)
        return (click * envelope * volume).astype(np.float32)


class AudioPlayer:
    def __init__(self):
        self.generator = ToneGenerator()
        self._streams: Dict[str, sd.OutputStream] = {}
        self._buffer_size = 128
        self.cached_tones = {}
        self.shot_type = "long_game"
        self.backswing_time = 0
        self.downswing_time = 0
        self.audio_cache = AudioCache()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level

    def set_shot_type(self, shot_type: str) -> None:
        """Set the shot type to use appropriate tones"""
        self.shot_type = shot_type.lower().replace(" ", "_")
        if self.shot_type not in AUDIO_CONFIG:
            self.shot_type = "long_game"

    def preload_swing_tones(self, backswing_s: float, downswing_s: float) -> None:
        """Preload all tones including the new metronome tone"""
        config = AUDIO_CONFIG[self.shot_type]
        sample_rate = AUDIO_CONFIG["sample_rate"]

        # Add metronome tone to cached_tones
        self.cached_tones = {
            'metronome': self.audio_cache.get_tone(
                'metronome',
                freq=330,    # E4 note - softer than main tones
                duration_s=0.050,  # Short duration for rhythm
                volume=0.5,   # Lower volume than swing tones
                sample_rate=sample_rate
            ),
            'backswing_start': self.audio_cache.get_tone(
                'backswing',
                freq=440,    # A4 note
                duration_s=0.100,
                volume=config['backswing']['volume'],
                sample_rate=sample_rate
            ),
            'downswing_start': self.audio_cache.get_tone(
                'downswing',
                freq=554.37,  # C#5 note
                duration_s=0.100,
                volume=config['downswing']['volume'],
                sample_rate=sample_rate
            ),
            'impact': self.audio_cache.get_tone(
                'impact',
                freq=659.25,  # E5 note
                duration_s=0.100,
                volume=config['impact']['volume'],
                sample_rate=sample_rate
            )
        }

        # Initialize audio streams for each tone
        for tone_name, tone_data in self.cached_tones.items():
            if tone_name not in self._streams or self._streams[tone_name].closed:
                self._streams[tone_name] = sd.OutputStream(
                    samplerate=sample_rate,
                    channels=1,
                    dtype=np.float32,
                    blocksize=self._buffer_size
                )
                self._streams[tone_name].start()

    def play(self, tone_name: str) -> None:
        """Play a specific tone"""
        if tone_name in self.cached_tones:
            if tone_name not in self._streams or self._streams[tone_name].closed:
                self._streams[tone_name] = sd.OutputStream(
                    samplerate=AUDIO_CONFIG["sample_rate"],
                    channels=1,
                    dtype=np.float32,
                    blocksize=self._buffer_size
                )
                self._streams[tone_name].start()

            self._streams[tone_name].write(self.cached_tones[tone_name])
            sd.play(self.cached_tones[tone_name], AUDIO_CONFIG["sample_rate"])
            sd.wait()  # Wait for the sound to finish playing

    def speak(self, text: str) -> None:
        """Speak the given text using text-to-speech"""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def play_swing_sequence(self) -> None:
        """Play a complete swing sequence with preparation rhythm"""
        # Play pro name announcement
        if hasattr(self, 'current_pro'):
            self.speak(f"Starting {self.current_pro}")
            time.sleep(0.5)  # Brief pause after pro announcement
        
        # Play "Address the ball" voice prompt
        self.speak("Address the ball")
        time.sleep(1)  # Brief pause after the voice prompt
        
        # Play 4 metronome beats to establish rhythm
        beat_interval = self.backswing_time / 3  # Divide backswing into 3 beats
        for _ in range(4):
            self.play('metronome')
            time.sleep(beat_interval)

        # First tone - Start takeaway
        self.play('backswing_start')
        
        # Wait for backswing duration
        time.sleep(self.backswing_time)

        # Second tone - Start downswing
        self.play('downswing_start')

        # Third tone - Impact
        time.sleep(self.downswing_time)
        self.play('impact')

        # Rest before next sequence
        time.sleep(1.5)

    def cleanup(self) -> None:
        """Clean up audio resources"""
        for stream in self._streams.values():
            stream.stop()
            stream.close()
        self._streams.clear()
        
        # Stop and close the TTS engine
        self.tts_engine.stop()

    def set_timing(self, backswing_time: float, downswing_time: float) -> None:
        """Set the timing values for the swing sequence"""
        self.backswing_time = backswing_time
        self.downswing_time = downswing_time

    def set_current_pro(self, pro_name: str) -> None:
        """Set the current pro name for announcements"""
        self.current_pro = pro_name
