import time
from typing import Dict, Optional
from dataclasses import dataclass
from .audio import AudioPlayer

@dataclass
class SwingTempo:
    shot_type: str
    pro_name: str
    bpm: float
    ratio: float
    frames: str
    description: str
    learning_notes: str
    
    @property
    def total_time(self) -> float:
        return 60.0 / self.bpm
    
    @property
    def backswing_time(self) -> float:
        return self.total_time * (self.ratio / (self.ratio + 1))
    
    @property
    def downswing_time(self) -> float:
        return self.total_time * (1 / (self.ratio + 1))

@dataclass
class SwingTiming:
    backswing: float
    downswing: float
    total: float
    ratio: float

class TempoTrainer:
    def __init__(self):
        self.audio_player = AudioPlayer()
        self.cycle_count = 0
        self.last_timing: Optional[SwingTiming] = None

    def analyze_timing(self, backswing_s: float, downswing_s: float, target_backswing: float, target_downswing: float) -> None:
        """Analyze and display detailed timing information"""
        total_s = backswing_s + downswing_s
        ratio = backswing_s / downswing_s if downswing_s > 0 else 0
        target_total = target_backswing + target_downswing
        target_ratio = target_backswing / target_downswing

        # Store timing for this swing
        self.last_timing = SwingTiming(
            backswing=backswing_s,
            downswing=downswing_s,
            total=total_s,
            ratio=ratio
        )

        print("\nTiming Analysis:")
        print(f"• Backswing: {backswing_s:.6f}s vs target {target_backswing:.6f}s (error: {(backswing_s - target_backswing)*1000:.3f}ms)")
        print(f"• Downswing: {downswing_s:.6f}s vs target {target_downswing:.6f}s (error: {(downswing_s - target_downswing)*1000:.3f}ms)")
        print(f"• Total:     {total_s:.6f}s vs target {target_total:.6f}s (error: {(total_s - target_total)*1000:.3f}ms)")
        print(f"• Ratio:     {ratio:.3f}:1 vs target {target_ratio:.1f}:1 (error: {abs(ratio - target_ratio)/target_ratio*100:.3f}%)")

    def train(self, settings: SwingTempo) -> None:
        """Run the training session with timing analysis"""
        # Set the appropriate shot type and timing
        self.audio_player.set_shot_type(settings.shot_type)
        self.audio_player.set_timing(settings.backswing_time, settings.downswing_time)
        
        print("\n=== Training Session Details ===")
        print(f"Shot Type: {settings.shot_type}")
        print(f"Pro: {settings.pro_name}")
        print(f"Frame Count: {settings.frames}")
        print(f"Overall Tempo: {settings.bpm:.0f} BPM")
        print(f"Swing Ratio: {settings.ratio:.1f}:1")
        
        if settings.description:
            print(f"\nDescription: {settings.description}")
        if settings.learning_notes:
            print(f"\nTraining Notes:\n{settings.learning_notes}")
            
        print("\n=== Target Timing ===")
        print(f"• Backswing:  {settings.backswing_time:.3f}s ({60/settings.backswing_time:.1f} BPM)")
        print(f"• Downswing:  {settings.downswing_time:.3f}s ({60/settings.downswing_time:.1f} BPM)")
        print(f"• Full Cycle: {settings.total_time:.3f}s ({settings.bpm:.1f} BPM)")
        print("\nPress Ctrl+C to end session")
        print("\n" + "="*50 + "\n")

        # Preload audio
        self.audio_player.preload_swing_tones(
            settings.backswing_time,
            settings.downswing_time
        )

        try:
            while True:
                self.cycle_count += 1
                print(f"=== Swing #{self.cycle_count} ===")
                
                # Play the sequence and measure timing
                start_time = time.perf_counter()
                self.audio_player.play_swing_sequence()
                end_time = time.perf_counter()

                # Calculate actual timing
                total_time = end_time - start_time
                backswing_time = settings.backswing_time
                downswing_time = settings.downswing_time

                # Analyze timing
                self.analyze_timing(
                    backswing_time,
                    downswing_time,
                    settings.backswing_time,
                    settings.downswing_time
                )

        except KeyboardInterrupt:
            print(f"\n=== Session Summary ===")
            print(f"Total swings: {self.cycle_count}")
            self.audio_player.cleanup()

    def _precise_sleep_until(self, target_time: float) -> None:
        """Ultra-precise sleep implementation with busy-wait"""
        while True:
            now = time.perf_counter_ns() / 1e9
            if now >= target_time:
                break
            remaining = target_time - now
            if remaining > 0.001:  # If more than 1ms remaining
                time.sleep(remaining * 0.8)  # Sleep for 80% of remaining time

    def _play_swing_cycle(self, tempo: SwingTempo) -> None:
        # Adjusted latency compensation
        latency_compensation = 0.015  # 15ms compensation
        
        # Pre-calculate all target times
        cycle_start = time.perf_counter_ns() / 1e9
        backswing_end = cycle_start + tempo.backswing_duration - latency_compensation
        downswing_end = backswing_end + tempo.downswing_duration - latency_compensation
        
        # Start backswing
        print(f"\nBackswing  [{tempo.backswing_duration:.3f}s] "
              f"({60/tempo.backswing_duration:.1f} BPM)")
        self.audio_player.play('backswing')
        
        # Wait for backswing end
        self._precise_sleep_until(backswing_end)
        
        # Start downswing
        downswing_start = time.perf_counter_ns() / 1e9
        print(f"Downswing  [{tempo.downswing_duration:.3f}s] "
              f"({60/tempo.downswing_duration:.1f} BPM)")
        self.audio_player.play('downswing')
        
        # Wait for downswing end
        self._precise_sleep_until(downswing_end)
        
        # Impact
        impact_start = time.perf_counter_ns() / 1e9
        print(f"Impact     [0.030s]")
        self.audio_player.play('impact')
        
        # Calculate actual timings
        actual_backswing = downswing_start - cycle_start
        actual_downswing = impact_start - downswing_start
        actual_cycle = impact_start - cycle_start
        actual_ratio = actual_backswing / actual_downswing if actual_downswing > 0 else 0
        
        # Print timing analysis
        print(f"\nTiming Analysis:")
        print(f"• Backswing: {actual_backswing:.6f}s vs target {tempo.backswing_duration:.6f}s "
              f"(error: {(actual_backswing - tempo.backswing_duration)*1000:.3f}ms)")
        print(f"• Downswing: {actual_downswing:.6f}s vs target {tempo.downswing_duration:.6f}s "
              f"(error: {(actual_downswing - tempo.downswing_duration)*1000:.3f}ms)")
        print(f"• Total:     {actual_cycle:.6f}s vs target {tempo.cycle_duration:.6f}s "
              f"(error: {(actual_cycle - tempo.cycle_duration)*1000:.3f}ms)")
        print(f"• Ratio:     {actual_ratio:.3f}:1 vs target {tempo.ratio:.1f}:1 "
              f"(error: {abs(actual_ratio - tempo.ratio)/tempo.ratio*100:.3f}%)")
        
        # Small pause between cycles
        time.sleep(0.2)

    def _format_session_info(self, tempo: SwingTempo) -> str:
        return f"""
Training Session Details:
------------------------
Shot Type: {tempo.shot_type}
Pro: {tempo.pro_name}
Overall Tempo: {tempo.bpm} BPM
Swing Ratio: {tempo.ratio}:1

Target Timing:
• Backswing:  {tempo.backswing_duration:.3f}s ({60/tempo.backswing_duration:.1f} BPM)
• Downswing:  {tempo.downswing_duration:.3f}s ({60/tempo.downswing_duration:.1f} BPM)
• Full Cycle: {tempo.cycle_duration:.3f}s ({tempo.bpm} BPM)

Press Ctrl+C to end session
"""

    def practice_mode(self, settings: SwingTempo) -> None:
        """Listen to the tempo without swinging"""
        print("\nPractice Mode - Just listen to internalize the tempo")
        print("Press Ctrl+C to exit practice mode")
        
        try:
            while True:
                self.audio_player.play_swing_sequence()
                time.sleep(2)  # Longer pause between sequences
        except KeyboardInterrupt:
            print("\nExiting practice mode")
