import random

# A clean, curated list of 5-letter target words for Wordle
WORD_LIST = [
    "REACT", "CRANE", "SLATE", "APPLE", "SMART", "TRAIN", "HOUSE", "WORLD",
    "FLASH", "AGENT", "BUILD", "GRAPH", "CLOUD", "THINK", "SHARK", "PLANT",
    "BRAIN", "STORM", "LIGHT", "MUSIC", "PEACE", "MAGIC", "POWER", "SOLAR",
    "OCEAN", "SPACE", "STONE", "RIVER", "FLAME", "CROWN", "DREAM", "STORY",
    "MODEL", "LOGIC", "TOKEN", "PROMPT", "SNAKE", "ROBOT", "MATCH", "CLEAR"
]

def get_random_word() -> str:
    """Returns a random upper-case 5-letter target word."""
    return random.choice(WORD_LIST).upper()

def is_valid_word(word: str) -> bool:
    """Checks if a string is a 5-letter alphabetic word."""
    return len(word) == 5 and word.isalpha()
