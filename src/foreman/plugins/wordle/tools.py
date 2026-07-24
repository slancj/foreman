from typing import Optional, Dict, Any
from langchain_core.tools import tool
from foreman.plugins.wordle.engine import WordleGame

# Global active game session for the plugin
_active_game: Optional[WordleGame] = None


@tool
def start_wordle_game(target_word: Optional[str] = None) -> str:
    """Starts a new Wordle game. Option to set a specific secret target word or pick randomly."""
    global _active_game
    try:
        _active_game = WordleGame(target_word=target_word)
        if target_word:
            return f"Started a new Wordle game with custom target word (hidden). 6 attempts remaining."
        return "Started a new Wordle game with a random 5-letter word. 6 attempts remaining. Make your first guess!"
    except Exception as e:
        return f"Error starting game: {str(e)}"


@tool
def make_wordle_guess(guess: str) -> str:
    """Submits a 5-letter word guess to the active Wordle game and returns tile feedback (🟩 = correct position, 🟨 = wrong position, ⬜ = not in word)."""
    global _active_game
    if _active_game is None:
        return "No active Wordle game! Please start a game first using 'start_wordle_game'."

    result = _active_game.evaluate_guess(guess)
    if "error" in result:
        return result["error"]

    return result["message"]


@tool
def get_wordle_status() -> str:
    """Returns the current state of the active Wordle board, including past guesses, feedback grid, and attempts remaining."""
    global _active_game
    if _active_game is None:
        return "No active Wordle game in progress."

    state = _active_game.get_state()
    lines = [f"Wordle Game Status: {state['status']} ({state['attempts_used']}/{state['max_attempts']} attempts)"]
    for g in state["history"]:
        lines.append(f"  Attempt {g['attempt']}: {g['guess']} -> {g['feedback']}")

    return "\n".join(lines)


wordle_tools = [start_wordle_game, make_wordle_guess, get_wordle_status]
