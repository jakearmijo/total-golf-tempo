import pytest
import numpy as np
from pathlib import Path

@pytest.fixture(autouse=True)
def mock_audio_device():
    """Mock sounddevice to avoid actual audio playback during tests"""
    import sounddevice as sd
    
    class MockOutputStream:
        def __init__(self, *args, **kwargs):
            self.closed = False
            
        def start(self):
            pass
            
        def stop(self):
            pass
            
        def close(self):
            self.closed = True
            
        def write(self, data):
            pass
    
    sd.OutputStream = MockOutputStream
    sd.play = lambda *args, **kwargs: None
    sd.wait = lambda: None
    
    return sd

@pytest.fixture
def sample_audio_data():
    """Generate sample audio data for testing"""
    return np.sin(2 * np.pi * 440 * np.linspace(0, 0.1, 4410)).astype(np.float32)

@pytest.fixture
def temp_cache_dir(tmp_path):
    """Create temporary directory for audio cache"""
    cache_dir = tmp_path / "audio_cache"
    cache_dir.mkdir()
    return cache_dir 