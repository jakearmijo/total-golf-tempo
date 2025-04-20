from typing import Optional, Tuple
from .config import TEMPO_CONFIG
from .trainer import SwingTempo, TempoTrainer

def get_user_selection(options: list[str], prompt: str) -> Optional[int]:
    print("\n" + prompt)
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    
    try:
        choice = int(input("\nEnter your choice (number): "))
        if 1 <= choice <= len(options):
            return choice - 1
        print("Invalid selection. Please choose a valid number.")
    except ValueError:
        print("Please enter a valid number.")
    return None

def get_tempo_settings() -> SwingTempo:
    # Get shot type selection
    shot_types = list(TEMPO_CONFIG.keys())
    print("\nSelect a shot type:")
    for i, shot_type in enumerate(shot_types, 1):
        print(f"{i}. {shot_type}")

    shot_choice = int(input("\nEnter your choice (number): ")) - 1
    selected_shot = shot_types[shot_choice]
    shot_config = TEMPO_CONFIG[selected_shot]

    # Get pro selection
    pros = list(shot_config["pros"].keys())
    print(f"\nSelect a pro for {selected_shot}:")
    for i, pro in enumerate(pros, 1):
        print(f"{i}. {pro}")

    pro_choice = int(input("\nEnter your choice (number): ")) - 1
    selected_pro = pros[pro_choice]
    pro_config = shot_config["pros"][selected_pro]

    return SwingTempo(
        shot_type=selected_shot,
        pro_name=selected_pro,
        bpm=pro_config["bpm"],
        ratio=pro_config["ratio"],
        frames=pro_config["frames"],
        description=pro_config["description"],
        learning_notes=shot_config["learning_notes"]
    )

def print_instructions() -> None:
    print("""
Dickfore Tempo Training System
-------------------------
You will hear three musical tones:
1. First tone  - Start your takeaway
2. Second tone - Start your downswing
3. Third tone  - Impact position

Simply react to each tone as it plays. Don't try to anticipate them.
The goal is to internalize this tempo until it becomes natural.

Remember:
- Long Game uses a 3:1 ratio (three parts backswing to one part downswing)
- Short Game uses a 2:1 ratio (two parts backswing to one part downswing)
    """)

def main() -> None:
    print("Welcome to Golf Tempo Trainer!")
    
    tempo_settings = get_tempo_settings()
    if tempo_settings is None:
        print("Error: Could not start training session.")
        return
    
    trainer = TempoTrainer()
    trainer.train(tempo_settings)

if __name__ == "__main__":
    main() 