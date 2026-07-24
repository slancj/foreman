from typing import Optional
from langchain_core.tools import tool
from foreman.plugins.minesweeper.engine import MinesweeperGame

# Global active game session for the plugin
_active_game: Optional[MinesweeperGame] = None


@tool
def start_minesweeper_game(width: int = 8, height: int = 8, num_mines: int = 10) -> str:
    """Starts a new Minesweeper game session with specified grid dimensions (default 8x8) and mine count (default 10)."""
    global _active_game
    try:
        _active_game = MinesweeperGame(width=width, height=height, num_mines=num_mines)
        return (
            f"Started a new Minesweeper game ({width}x{height} grid with {num_mines} hidden mines).\n\n"
            f"Current Board:\n{_active_game.render_board()}\n\n"
            f"Use 'reveal_minesweeper_cell(row, col)' to reveal a cell."
        )
    except Exception as e:
        return f"Error starting Minesweeper game: {str(e)}"


@tool
def reveal_minesweeper_cell(row: int, col: int) -> str:
    """Reveals the cell at (row, col) in the active Minesweeper game board."""
    global _active_game
    if _active_game is None:
        return "No active Minesweeper game! Please start a game first using 'start_minesweeper_game'."

    result = _active_game.reveal_cell(row, col)
    if "error" in result:
        return result["error"]

    return f"{result['message']}\n\n{result['board']}"


@tool
def get_minesweeper_status() -> str:
    """Returns the current board state and status of the active Minesweeper game."""
    global _active_game
    if _active_game is None:
        return "No active Minesweeper game in progress."

    state = _active_game.get_state()
    lines = [
        f"Minesweeper Status: {state['status']} | Moves: {state['moves_count']} | Revealed: {state['revealed_cells']}/{state['total_cells']} | Total Mines: {state['num_mines']}",
        "",
        state["board"],
    ]
    return "\n".join(lines)


minesweeper_tools = [
    start_minesweeper_game,
    reveal_minesweeper_cell,
    get_minesweeper_status,
]
