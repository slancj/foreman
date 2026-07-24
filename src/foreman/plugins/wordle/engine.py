from typing import List, Dict, Any, Optional
from foreman.plugins.wordle.words import get_random_word, is_valid_word


class WordleGame:
    """Class representing an active game of Wordle."""

    def __init__(self, target_word: Optional[str] = None, max_attempts: int = 6):
        if target_word:
            clean_target = target_word.strip().upper()
            if not is_valid_word(clean_target):
                raise ValueError("Target word must be a 5-letter alphabetic word.")
            self.target_word = clean_target
        else:
            self.target_word = get_random_word()

        self.max_attempts = max_attempts
        self.guesses: List[Dict[str, Any]] = []
        self.status = "IN_PROGRESS"  # "IN_PROGRESS", "WON", "LOST"

    def evaluate_guess(self, guess: str) -> Dict[str, Any]:
        """Evaluates a 5-letter guess against the target word."""
        guess = guess.strip().upper()

        if self.status != "IN_PROGRESS":
            return {
                "error": f"Game is already over! Result: {self.status}. Target word was '{self.target_word}'."
            }

        if not is_valid_word(guess):
            return {"error": "Invalid guess. Must be a 5-letter alphabetic word."}

        # Algorithm for Wordle letter evaluation with proper duplicate letter handling
        target_chars = list(self.target_word)
        result_colors = ["⬜"] * 5  # default absent

        # Pass 1: Mark exact matches (🟩 Green)
        target_counts: Dict[str, int] = {}
        for idx in range(5):
            g_char = guess[idx]
            t_char = target_chars[idx]
            if g_char == t_char:
                result_colors[idx] = "🟩"
            else:
                target_counts[t_char] = target_counts.get(t_char, 0) + 1

        # Pass 2: Mark present matches in wrong position (🟨 Yellow)
        for idx in range(5):
            if result_colors[idx] == "🟩":
                continue
            g_char = guess[idx]
            if target_counts.get(g_char, 0) > 0:
                result_colors[idx] = "🟨"
                target_counts[g_char] -= 1

        feedback_str = "".join(result_colors)
        
        attempt_record = {
            "attempt": len(self.guesses) + 1,
            "guess": guess,
            "feedback": feedback_str,
            "colors": result_colors
        }
        self.guesses.append(attempt_record)

        if guess == self.target_word:
            self.status = "WON"
        elif len(self.guesses) >= self.max_attempts:
            self.status = "LOST"

        return {
            "attempt": attempt_record["attempt"],
            "remaining_attempts": self.max_attempts - len(self.guesses),
            "guess": guess,
            "feedback": feedback_str,
            "status": self.status,
            "message": self._build_status_message(guess, feedback_str)
        }

    def _build_status_message(self, guess: str, feedback_str: str) -> str:
        if self.status == "WON":
            return f"🎉 Congratulations! You guessed '{guess}' correctly in {len(self.guesses)}/{self.max_attempts} attempts!"
        elif self.status == "LOST":
            return f"❌ Game Over! You used all {self.max_attempts} attempts. The secret word was '{self.target_word}'."
        else:
            remaining = self.max_attempts - len(self.guesses)
            return f"Guess '{guess}': {feedback_str} ({remaining} attempts remaining)"

    def get_state(self) -> Dict[str, Any]:
        """Returns current board summary."""
        return {
            "status": self.status,
            "attempts_used": len(self.guesses),
            "max_attempts": self.max_attempts,
            "history": self.guesses,
            "target_word": self.target_word if self.status != "IN_PROGRESS" else "?????",
        }
