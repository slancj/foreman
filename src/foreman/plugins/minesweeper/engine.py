import random
from typing import List, Dict, Any, Optional, Tuple


class MinesweeperGame:
    """Class representing an active game of Minesweeper."""

    # Clear characters for 1:1 monospace grid alignment inside code blocks
    UNREVEALED_ICON = "."
    MINE_ICON = "*"

    def __init__(
        self,
        width: int = 8,
        height: int = 8,
        num_mines: int = 10,
        seed: Optional[int] = None,
    ):
        if width < 3 or width > 20:
            raise ValueError("Width must be between 3 and 20.")
        if height < 3 or height > 20:
            raise ValueError("Height must be between 3 and 20.")
        max_mines = (width * height) - 1
        if num_mines < 1 or num_mines > max_mines:
            raise ValueError(f"Number of mines must be between 1 and {max_mines}.")

        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.status = "IN_PROGRESS"  # "IN_PROGRESS", "WON", "LOST"
        self.grid_initialized = False
        self.moves_count = 0
        self.seed = seed

        # Initialize grid structure: board[row][col]
        self.grid: List[List[Dict[str, Any]]] = [
            [
                {"is_mine": False, "revealed": False, "neighbor_mines": 0}
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]

    def _in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def _get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if self._in_bounds(r, c):
                    neighbors.append((r, c))
        return neighbors

    def _place_mines(self, safe_row: int, safe_col: int) -> None:
        """Places mines randomly, ensuring (safe_row, safe_col) is not a mine (first-click safety)."""
        rng = random.Random(self.seed)
        all_coords = [
            (r, c)
            for r in range(self.height)
            for c in range(self.width)
            if not (r == safe_row and c == safe_col)
        ]

        mine_coords = set(rng.sample(all_coords, self.num_mines))

        for r, c in mine_coords:
            self.grid[r][c]["is_mine"] = True

        # Calculate neighbor mine counts
        for r in range(self.height):
            for c in range(self.width):
                if not self.grid[r][c]["is_mine"]:
                    count = sum(
                        1
                        for nr, nc in self._get_neighbors(r, c)
                        if self.grid[nr][nc]["is_mine"]
                    )
                    self.grid[r][c]["neighbor_mines"] = count

        self.grid_initialized = True

    def reveal_cell(self, row: int, col: int) -> Dict[str, Any]:
        """Reveals cell at (row, col)."""
        if self.status != "IN_PROGRESS":
            return {
                "error": f"Game is already over! Result: {self.status}.\n\n{self.render_board()}"
            }

        if not self._in_bounds(row, col):
            return {
                "error": f"Invalid coordinates ({row}, {col}). Row must be 0..{self.height-1}, Col must be 0..{self.width-1}."
            }

        cell = self.grid[row][col]
        if cell["revealed"]:
            return {
                "message": f"Cell ({row}, {col}) is already revealed.",
                "status": self.status,
                "board": self.render_board(),
            }

        # Initialize mines on first move for first-click safety
        if not self.grid_initialized:
            self._place_mines(row, col)

        self.moves_count += 1

        # Check if mine hit
        if cell["is_mine"]:
            self.status = "LOST"
            # Reveal all mines
            for r in range(self.height):
                for c in range(self.width):
                    if self.grid[r][c]["is_mine"]:
                        self.grid[r][c]["revealed"] = True

            return {
                "message": f"💥 BOOM! You stepped on a mine at ({row}, {col}). Game Over!",
                "status": self.status,
                "board": self.render_board(),
            }

        # Flood fill reveal for 0-neighbor empty cells
        self._flood_fill_reveal(row, col)

        # Check win condition: count unrevealed non-mine cells
        unrevealed_non_mines = sum(
            1
            for r in range(self.height)
            for c in range(self.width)
            if not self.grid[r][c]["is_mine"] and not self.grid[r][c]["revealed"]
        )

        if unrevealed_non_mines == 0:
            self.status = "WON"
            return {
                "message": f"🎉 Congratulations! You cleared all safe cells in {self.moves_count} moves!",
                "status": self.status,
                "board": self.render_board(),
            }

        return {
            "message": f"Revealed cell ({row}, {col}).",
            "status": self.status,
            "board": self.render_board(),
        }

    def _flood_fill_reveal(self, start_row: int, start_col: int) -> None:
        """Reveals cell and recursively expands empty 0-neighbor regions."""
        queue = [(start_row, start_col)]
        visited = set()

        while queue:
            r, c = queue.pop(0)
            if (r, c) in visited or not self._in_bounds(r, c):
                continue
            visited.add((r, c))

            cell = self.grid[r][c]
            if cell["is_mine"]:
                continue

            cell["revealed"] = True

            # If this cell has 0 neighboring mines, expand to unrevealed neighbors
            if cell["neighbor_mines"] == 0:
                for nr, nc in self._get_neighbors(r, c):
                    if not self.grid[nr][nc]["revealed"] and (nr, nc) not in visited:
                        queue.append((nr, nc))

    def render_board(self) -> str:
        """Renders string representation of the Minesweeper board wrapped in a markdown code block."""
        lines = ["```"]

        # Column header
        col_header = "   " + " ".join(f"{c:2d}" for c in range(self.width))
        lines.append(col_header)
        lines.append("  +" + "---" * self.width)

        for r in range(self.height):
            row_str = [f"{r:2d}|"]
            for c in range(self.width):
                cell = self.grid[r][c]
                if not cell["revealed"]:
                    row_str.append(f" {self.UNREVEALED_ICON} ")
                elif cell["is_mine"]:
                    row_str.append(f" {self.MINE_ICON} ")
                else:
                    val = " " if cell["neighbor_mines"] == 0 else str(cell["neighbor_mines"])
                    row_str.append(f" {val} ")
            lines.append("".join(row_str))

        lines.append("```")
        lines.append("Legend: '.' = unrevealed, ' ' = 0 adjacent, 1-8 = adjacent mines, '*' = mine")
        return "\n".join(lines)

    def get_state(self) -> Dict[str, Any]:
        """Returns board state summary."""
        revealed_count = sum(
            1 for r in range(self.height) for c in range(self.width) if self.grid[r][c]["revealed"]
        )
        return {
            "width": self.width,
            "height": self.height,
            "num_mines": self.num_mines,
            "status": self.status,
            "moves_count": self.moves_count,
            "revealed_cells": revealed_count,
            "total_cells": self.width * self.height,
            "board": self.render_board(),
        }
