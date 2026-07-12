#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   generator.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/04 21:31:50 by horarivo            #+#    #+#            #
#   Updated: 2026/07/04 21:31:51 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Maze generation using the randomized recursive backtracker."""

import random
import sys
from typing import Optional

from .constants import (
    DELTA,
    EAST,
    OPPOSITE,
    PAT_H,
    PAT_W,
    PATTERN_42,
    SOUTH,
    WEST,
)


class MazeGenerator:
    """Generate a maze using the randomized recursive backtracker.

    Each cell is a 4-bit integer (see constants.py) indicating which
    walls are closed. Generation can happen step by step (step) or
    all at once (generate_all), which enables animation in app.py.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        seed: Optional[int] = None,
        perfect: bool = True,
    ) -> None:
        """Initialize the grid and start the walk from the entry.

        Args:
            width: maze width in cells.
            height: maze height in cells.
            entry: (x, y) coordinates of the entry.
            exit_: (x, y) coordinates of the exit.
            seed: random seed, used to reproduce the same maze.
            perfect: if False, extra passages are carved after
                generation completes.
        """
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.perfect = perfect
        self.seed: int = (
            seed if seed is not None else random.randint(0, 999_999)
        )
        random.seed(self.seed)

        # Toutes les cellules commencent avec leurs 4 murs fermes.
        self.grid: list[list[int]] = [
            [0xF] * width for _ in range(height)
        ]
        self.visited: list[list[bool]] = [
            [False] * width for _ in range(height)
        ]
        # Cellules reservees au motif "42", jamais creusees.
        self.is_42: list[list[bool]] = [
            [False] * width for _ in range(height)
        ]

        self.current: Optional[tuple[int, int]] = None
        self.done: bool = False
        self.pattern_skipped: bool = False
        self._stack: list[tuple[int, int]] = []

        self._stamp_42()
        self._start_walk()

    def _stamp_42(self) -> None:
        """Reserve the "42" pattern cells at the center of the maze.

        If the maze is too small to fit the pattern, a message is
        printed on the console and the pattern is skipped.
        """
        if self.width < PAT_W + 4 or self.height < PAT_H + 4:
            print(
                "[Info] Maze too small for pattern '42' "
                f"(minimum {PAT_W + 4}x{PAT_H + 4}, "
                f"current {self.width}x{self.height}).",
                file=sys.stderr,
            )
            self.pattern_skipped = True
            return

        ox = (self.width - PAT_W) // 2
        oy = (self.height - PAT_H) // 2

        for r in range(PAT_H):
            for c in range(PAT_W):
                if PATTERN_42[r][c] == 1:
                    gx, gy = ox + c, oy + r
                    self.visited[gy][gx] = True
                    self.is_42[gy][gx] = True

    def _start_walk(self) -> None:
        """Mark the entry as visited and initialize the stack."""
        sx, sy = self.entry
        self.visited[sy][sx] = True
        self._stack = [(sx, sy)]
        self.current = (sx, sy)

    def step(self, n: int = 1) -> None:
        """Advance the backtracker generation by n steps.

        At each step, try to move to an unvisited neighbor in a
        random direction. If no neighbor is available, backtrack by
        popping the stack.

        Args:
            n: number of steps to perform.
        """
        for _ in range(n):
            if not self._stack:
                self._finish()
                return

            x, y = self._stack[-1]
            self.current = (x, y)

            dirs = list(DELTA.keys())
            random.shuffle(dirs)
            moved = False

            for direction in dirs:
                dx, dy = DELTA[direction]
                nx, ny = x + dx, y + dy
                in_bounds = (
                    0 <= nx < self.width and 0 <= ny < self.height
                )
                if in_bounds and not self.visited[ny][nx]:
                    # Open the wall on both sides at once to keep neighboring
                    # cells consistent.
                    self.grid[y][x] &= ~direction
                    self.grid[ny][nx] &= ~OPPOSITE[direction]
                    self.visited[ny][nx] = True
                    self._stack.append((nx, ny))
                    moved = True
                    break

            if not moved:
                self._stack.pop()

        if not self._stack:
            self._finish()

    def generate_all(self) -> None:
        """Generate the full maze at once (without animation)."""
        while not self.done:
            self.step(256)

    def _finish(self) -> None:
        """Mark generation as finished.

        If the maze should not be perfect, extra passages are then
        added.
        """
        self.done = True
        self.current = None
        if not self.perfect:
            self._add_loops()

    def _add_loops(self) -> None:
        """Carve extra passages for an imperfect maze.

        Each candidate passage is checked before being carved, to
        never create a fully open 3x3-or-larger area (forbidden by
        the subject).
        """
        extra = max(1, (self.width * self.height) // 10)
        max_attempts = extra * 20
        added = 0
        attempts = 0

        while added < extra and attempts < max_attempts:
            attempts += 1
            x = random.randint(0, self.width - 2)
            y = random.randint(0, self.height - 2)

            if self.is_42[y][x] or self.is_42[y][x + 1]:
                continue
            if not (self.grid[y][x] & EAST):
                continue
            if self._would_create_large_opening(x, y):
                continue

            self.grid[y][x] &= ~EAST
            self.grid[y][x + 1] &= ~WEST
            added += 1

    def _would_create_large_opening(self, x: int, y: int) -> bool:
        """Check if carving the East wall of (x, y) opens a 2x2 block.

        A fully open 2x2 block of cells amounts to a 3x3+ open area
        in practice.

        Args:
            x: column of the cell whose East wall would be carved.
            y: row of the cell.

        Returns:
            True if carving is unsafe and must be avoided.
        """
        y_min = max(0, y - 1)
        y_max = min(self.height - 2, y + 1)
        x_min = max(0, x - 1)
        x_max = min(self.width - 2, x)

        for oy in range(y_min, y_max + 1):
            for ox in range(x_min, x_max + 1):
                if self._block_is_open(ox, oy, ox == x and oy == y):
                    return True
        return False

    def _block_is_open(
        self,
        x: int,
        y: int,
        simulate_east: bool,
    ) -> bool:
        """Check if the 2x2 block starting at (x, y) is already open.

        Args:
            x: column of the top-left corner of the 2x2 block.
            y: row of the top-left corner of the 2x2 block.
            simulate_east: if True, simulate the East wall of (x, y)
                as already carved (used to test before carving).

        Returns:
            True if the block's 4 internal walls are already open.
        """
        east_top = simulate_east or not (self.grid[y][x] & EAST)
        east_bottom = not (self.grid[y + 1][x] & EAST)
        south_left = not (self.grid[y][x] & SOUTH)
        south_right = not (self.grid[y][x + 1] & SOUTH)
        return east_top and east_bottom and south_left and south_right
