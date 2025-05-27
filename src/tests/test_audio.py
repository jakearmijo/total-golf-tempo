import pytest
import numpy as np
import sounddevice as sd
from unittest.mock import Mock, patch, MagicMock, call
from pathlib import Path
from ..audio import AudioPlayer, AudioCache, Tone, ToneGenerator
import pyttsx3

# Fixtures
@pytest.fixture
def audio_player():
    player = AudioPlayer()
    yield player
    player.cleanup()

@pytest.fixture
def audio_cache(tmp_path):
    cache = AudioCache()
    cache.cache_dir = tmp_path / "audio_cache"
    cache.cache_dir.mkdir(exist_ok=True)
    return cache

@pytest.fixture
def tone_generator():
    return ToneGenerator(sample_rate=44100)

@pytest.fixture
def mock_tts_engine():
    with patch('pyttsx3.init') as mock_init:
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        yield mock_engine

# Test Tone Generation
class TestTone:
    def test_tone_generation(self):
        """
        Test basic tone generation with default parameters
        Time Complexity: O(n) where n is sample count
        """
        tone = Tone(frequency=440, duration_ms=100)
        audio = tone.generate()
        
        assert audio is not None
        assert len(audio) > 0
        
    def test_tone_volume(self):
        """Test volume adjustment"""
        tone1 = Tone(frequency=440, duration_ms=100, volume=0.5)
        tone2 = Tone(frequency=440, duration_ms=100, volume=1.0)
        
        audio1 = tone1.generate()
        audio2 = tone2.generate()
        
        # Check relative volumes
        assert abs(audio1.dBFS) < abs(audio2.dBFS)

# Test Audio Cache
class TestAudioCache:
    def test_cache_creation(self, audio_cache):
        """Test cache initialization"""
        assert audio_cache.cache_dir.exists()
        assert isinstance(audio_cache.cached_segments, dict)

    def test_tone_caching(self, audio_cache):
        """
        Test tone generation and caching
        Time Complexity: O(1) for retrieval after initial O(n) generation
        """
        tone = audio_cache.get_tone(
            name="test",
            freq=440,
            duration_s=0.1,
            volume=0.8,
            sample_rate=44100
        )
        
        # Verify tone properties
        assert isinstance(tone, np.ndarray)
        assert tone.dtype == np.float32
        
        # Test cache hit
        cached_tone = audio_cache.get_tone(
            name="test",
            freq=440,
            duration_s=0.1,
            volume=0.8,
            sample_rate=44100
        )
        assert np.array_equal(tone, cached_tone)

    def test_invalid_parameters(self, audio_cache):
        """Test error handling for invalid parameters"""
        with pytest.raises(ValueError):
            audio_cache.get_tone(
                name="test",
                freq=-440,  # Invalid frequency
                duration_s=0.1,
                volume=0.8,
                sample_rate=44100
            )

# Test Tone Generator
class TestToneGenerator:
    def test_impact_click(self, tone_generator):
        """Test impact click generation"""
        click = tone_generator.generate_impact_click()
        assert isinstance(click, np.ndarray)
        assert click.dtype == np.float32
        
    def test_sweep_generation(self, tone_generator):
        """Test frequency sweep generation"""
        sweep = tone_generator.generate_sweep(
            start_freq=440,
            end_freq=880,
            duration_s=0.5
        )
        assert isinstance(sweep, np.ndarray)
        assert sweep.dtype == np.float32

# Test Audio Player
class TestAudioPlayer:
    def test_shot_type_setting(self, audio_player):
        """Test shot type configuration"""
        audio_player.set_shot_type("long_game")
        assert audio_player.shot_type == "long_game"
        
        # Test invalid shot type fallback
        audio_player.set_shot_type("invalid_type")
        assert audio_player.shot_type == "long_game"

    @patch('sounddevice.OutputStream')
    def test_preload_swing_tones(self, mock_output_stream, audio_player):
        """Test tone preloading"""
        audio_player.preload_swing_tones(0.9, 0.3)
        
        # Verify all required tones are cached
        required_tones = ['metronome', 'backswing_start', 'downswing_start', 'impact']
        for tone in required_tones:
            assert tone in audio_player.cached_tones
            
    def test_timing_setup(self, audio_player):
        """Test timing configuration"""
        backswing = 0.9
        downswing = 0.3
        
        audio_player.set_timing(backswing, downswing)
        assert audio_player.backswing_time == backswing
        assert audio_player.downswing_time == downswing

    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_swing_sequence(self, mock_wait, mock_play, audio_player):
        """Test complete swing sequence playback"""
        audio_player.set_timing(0.9, 0.3)
        audio_player.preload_swing_tones(0.9, 0.3)
        
        # Mock time.sleep to speed up test
        with patch('time.sleep'):
            audio_player.play_swing_sequence()
            
        # Verify proper sequence of tone playback
        assert mock_play.call_count > 0
        assert mock_wait.call_count > 0

    def test_cleanup(self, audio_player):
        """Test resource cleanup"""
        audio_player.preload_swing_tones(0.9, 0.3)
        audio_player.cleanup()
        assert len(audio_player._streams) == 0

    @patch('time.sleep')
    def test_play_swing_sequence_with_speech(self, mock_sleep, audio_player, mock_tts_engine):
        """
        Test complete swing sequence with speech integration
        Time Complexity: O(1)
        """
        audio_player.set_timing(0.9, 0.3)
        audio_player.preload_swing_tones(0.9, 0.3)
        
        with patch.object(audio_player, 'play') as mock_play:
            audio_player.play_swing_sequence()
            
            # Verify speech prompts
            expected_speech_calls = [
                call("Address the ball"),
                call("Start backswing"),
                call("Start downswing"),
                call("Impact")
            ]
            actual_speech_calls = [
                call(args[0]) for args, _ in mock_tts_engine.say.call_args_list
            ]
            assert actual_speech_calls == expected_speech_calls
            
            # Verify tone playback sequence
            expected_tone_calls = [
                call('metronome'),
                call('metronome'),
                call('metronome'),
                call('metronome'),
                call('backswing_start'),
                call('downswing_start'),
                call('impact')
            ]
            assert mock_play.call_args_list == expected_tone_calls

    def test_error_handling_tts(self, audio_player, mock_tts_engine):
        """
        Test TTS error handling
        Time Complexity: O(1)
        """
        mock_tts_engine.say.side_effect = Exception("TTS Error")
        
        # Should not raise exception but log error
        with pytest.warns(UserWarning):
            audio_player.speak("Test speech")

    @pytest.mark.parametrize("text,expected_delay", [
        ("Short text", 0.5),
        ("This is a longer piece of text that should take more time", 1.5)
    ])
    def test_speech_timing(self, text, expected_delay, audio_player, mock_tts_engine):
        """
        Test speech timing adaptation
        Time Complexity: O(1)
        """
        with patch('time.sleep') as mock_sleep:
            audio_player.speak(text)
            # Verify appropriate delays based on text length
            assert mock_tts_engine.say.called
            assert mock_tts_engine.runAndWait.called

    def test_concurrent_audio_speech(self, audio_player, mock_tts_engine):
        """
        Test handling of concurrent audio and speech
        Time Complexity: O(1)
        """
        with patch.object(audio_player, 'play') as mock_play:
            # Simulate concurrent audio and speech
            audio_player.play('metronome')
            audio_player.speak("Test")
            
            # Verify proper sequencing
            mock_play.assert_called_once_with('metronome')
            mock_tts_engine.say.assert_called_once_with("Test")

# Add new test class for TTS functionality
class TestTextToSpeech:
    def test_tts_initialization(self, audio_player, mock_tts_engine):
        """
        Test TTS engine initialization and configuration
        Time Complexity: O(1)
        """
        assert audio_player.tts_engine is not None
        mock_tts_engine.setProperty.assert_has_calls([
            call('rate', 150),
            call('volume', 0.9)
        ])

    def test_speak_method(self, audio_player, mock_tts_engine):
        """
        Test speak method execution
        Time Complexity: O(1)
        """
        test_text = "Test speech"
        audio_player.speak(test_text)
        
        mock_tts_engine.say.assert_called_once_with(test_text)
        mock_tts_engine.runAndWait.assert_called_once()

    def test_cleanup_includes_tts(self, audio_player, mock_tts_engine):
        """
        Test TTS cleanup during AudioPlayer cleanup
        Time Complexity: O(1)
        """
        audio_player.cleanup()
        mock_tts_engine.stop.assert_called_once() 