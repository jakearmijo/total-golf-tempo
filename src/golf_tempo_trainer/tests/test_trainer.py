import pytest
from unittest.mock import Mock, patch
from ..trainer import TempoTrainer, SwingTempo, SwingTiming

@pytest.fixture
def trainer():
    return TempoTrainer()

@pytest.fixture
def swing_tempo():
    return SwingTempo(
        shot_type="Long Game",
        pro_name="Tour Tempo 21/7",
        bpm=84,
        ratio=3.0,
        frames="21/7",
        description="Medium-fast tempo",
        learning_notes="Practice notes"
    )

class TestSwingTempo:
    def test_timing_calculations(self):
        """Test swing tempo timing calculations"""
        tempo = SwingTempo(
            shot_type="Long Game",
            pro_name="Test Pro",
            bpm=60,  # 1 second per beat
            ratio=3.0,
            frames="21/7",
            description="Test tempo",
            learning_notes="Test notes"
        )
        
        assert tempo.total_time == 1.0
        assert pytest.approx(tempo.backswing_time) == 0.75
        assert pytest.approx(tempo.downswing_time) == 0.25

    def test_invalid_values(self):
        """Test handling of invalid tempo values"""
        with pytest.raises(ValueError):
            SwingTempo(
                shot_type="Long Game",
                pro_name="Test Pro",
                bpm=-60,  # Invalid negative BPM
                ratio=3.0,
                frames="21/7",
                description="Test tempo",
                learning_notes="Test notes"
            )

class TestTempoTrainer:
    def test_initialization(self, trainer):
        """Test trainer initialization"""
        assert trainer.cycle_count == 0
        assert trainer.last_timing is None
        assert trainer.audio_player is not None

    def test_timing_analysis(self, trainer):
        """Test swing timing analysis"""
        trainer.analyze_timing(
            backswing_s=0.75,
            downswing_s=0.25,
            target_backswing=0.75,
            target_downswing=0.25
        )
        
        assert trainer.last_timing is not None
        assert trainer.last_timing.ratio == 3.0
        assert trainer.last_timing.total == 1.0

    @patch('time.perf_counter_ns')
    def test_precise_sleep(self, mock_time, trainer):
        """Test precise sleep implementation"""
        mock_time.return_value = 0
        
        with patch('time.sleep') as mock_sleep:
            trainer._precise_sleep_until(0.1)
            assert mock_sleep.called

    @patch('time.perf_counter_ns')
    def test_swing_cycle(self, mock_time, trainer, swing_tempo):
        """Test complete swing cycle execution"""
        mock_time.return_value = 0
        
        with patch.object(trainer.audio_player, 'play') as mock_play:
            trainer._play_swing_cycle(swing_tempo)
            
            # Verify correct sequence of tone playback
            expected_calls = ['backswing', 'downswing', 'impact']
            actual_calls = [call[0][0] for call in mock_play.call_args_list]
            assert actual_calls == expected_calls

    def test_practice_mode(self, trainer, swing_tempo):
        """Test practice mode execution"""
        with patch.object(trainer.audio_player, 'play_swing_sequence') as mock_play:
            with patch('time.sleep'):
                # Simulate KeyboardInterrupt after first cycle
                with pytest.raises(KeyboardInterrupt):
                    trainer.practice_mode(swing_tempo)
                
                assert mock_play.called

    def test_train_method(self, trainer, swing_tempo):
        """Test training session execution"""
        with patch.object(trainer.audio_player, 'set_shot_type') as mock_set_type:
            with patch.object(trainer.audio_player, 'set_timing') as mock_set_timing:
                with patch.object(trainer.audio_player, 'preload_swing_tones'):
                    # Simulate KeyboardInterrupt after setup
                    with pytest.raises(KeyboardInterrupt):
                        trainer.train(swing_tempo)
                    
                    mock_set_type.assert_called_once_with(swing_tempo.shot_type)
                    mock_set_timing.assert_called_once_with(
                        swing_tempo.backswing_time,
                        swing_tempo.downswing_time
                    ) 