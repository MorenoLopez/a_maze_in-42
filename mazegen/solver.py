#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   solver.py                                            :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mandrini <mandrini@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/04 21:34:14 by mandrini            #+#    #+#            #
#   Updated: 2026/07/04 21:50:45 by mandrini           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Shortest-path search using breadth-first search (BFS)."""

from collections import deque
from typing import Optional

from .constants import DELTA, DIR_NAME
from .generator import MazeGenerator

# Movement associated with each direction letter of the output file.
_DELTA_MAP: dict[str, tuple[int, int]] = {
    "N": (0, -1), "E": (1, 0), "S": (0, 1), "W": (-1, 0),
}


class MazeSolver:
    """Compute the shortest path between the entry and the exit.

    BFS guarantees the shortest path since moving between two cells
    always costs exactly 1 step. The result is cached after the
    first call to solve().
    """

    def __init__(self, gen: MazeGenerator) -> None:
        """Attach the solver to a maze, already generated or in progress.

        Args:
            gen: maze generator to solve.
        """
        self._gen = gen
        self._path: Optional[list[str]] = None
        self._bfs_order: list[tuple[int, int]] = []

    def solve(self) -> list[str]:
        """Find the shortest path from the entry to the exit.

        Returns:
            List of N/E/S/W letters describing the path, in the
            order to follow from the entry.
        """
        if self._path is not None:
            return self._path

        gen = self._gen
        ex, ey = gen.exit_

        self._bfs_order = [gen.entry]

        queue: deque[tuple[tuple[int, int], list[str]]] = deque(
            [(gen.entry, [])]
        )
        seen: set[tuple[int, int]] = {gen.entry}

        while queue:
            (cx, cy), path = queue.popleft()
            if (cx, cy) == (ex, ey):
                self._path = path
                return path

            for direction, (dx, dy) in DELTA.items():
                nx, ny = cx + dx, cy + dy
                in_bounds = (
                    0 <= nx < gen.width and 0 <= ny < gen.height
                )
                wall_open = not (gen.grid[cy][cx] & direction)
                if in_bounds and (nx, ny) not in seen and wall_open:
                    seen.add((nx, ny))
                    self._bfs_order.append((nx, ny))
                    queue.append(
                        ((nx, ny), path + [DIR_NAME[direction]])
                    )

        self._path = []
        return self._path

    def path_cells(self) -> set[tuple[int, int]]:
        """Return the set of (x, y) cells located on the path.

        Returns:
            A set of coordinates, including the entry and the exit.
        """
        cells: set[tuple[int, int]] = {self._gen.entry}
        x, y = self._gen.entry
        for d in self.solve():
            dx, dy = _DELTA_MAP[d]
            x, y = x + dx, y + dy
            cells.add((x, y))
        return cells

    def path_list(self) -> list[tuple[int, int]]:
        """Return the path as an ordered list from entry to exit.

        Used to animate the solution line in app.py.

        Returns:
            List of (x, y) coordinates, in traversal order.
        """
        result: list[tuple[int, int]] = [self._gen.entry]
        x, y = self._gen.entry
        for d in self.solve():
            dx, dy = _DELTA_MAP[d]
            x, y = x + dx, y + dy
            result.append((x, y))
        return result

    def bfs_order(self) -> list[tuple[int, int]]:
        """Return the cells in BFS discovery order.

        Returns:
            List of coordinates, with the entry discovered first.
        """
        self.solve()
        return self._bfs_order
