#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   renderer.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mandrini <mandrini@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/04 21:58:13 by mandrini            #+#    #+#            #
#   Updated: 2026/07/04 21:58:15 by mandrini           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Low-level helpers: pixel drawing in the MLX buffer and output writer."""

from .config import die
from .generator import MazeGenerator


def to_bytes(r: int, g: int, b: int) -> bytes:
    """Convert an RGB color to 4 ARGB bytes (MLX buffer format).

    Args:
        r: red component (0-255).
        g: green component (0-255).
        b: blue component (0-255).

    Returns:
        4 bytes in the format expected by the MLX image buffer.
    """
    return (0xFF000000 | (r << 16) | (g << 8) | b).to_bytes(4, "little")


def to_int(r: int, g: int, b: int) -> int:
    """Convert an RGB color to a 0xAARRGGBB integer for mlx_string_put.

    Args:
        r: red component (0-255).
        g: green component (0-255).
        b: blue component (0-255).

    Returns:
        Integer color value, in the format expected by MLX.
    """
    return 0xFF000000 | (r << 16) | (g << 8) | b


def fill_rect(
    data: memoryview,
    sl: int,
    x: int,
    y: int,
    w: int,
    h: int,
    cb: bytes,
) -> None:
    """Fill a pixel rectangle in the image buffer.

    Args:
        data: memory buffer of the MLX image.
        sl: size of one buffer line (size_line).
        x: x coordinate of the top-left corner.
        y: y coordinate of the top-left corner.
        w: rectangle width in pixels.
        h: rectangle height in pixels.
        cb: color to apply, as 4 bytes.
    """
    row_bytes = cb * w
    for dy in range(h):
        start = (y + dy) * sl + x * 4
        data[start:start + w * 4] = row_bytes


def draw_hline(
    data: memoryview,
    sl: int,
    x: int,
    y: int,
    length: int,
    thick: int,
    cb: bytes,
) -> None:
    """Draw a thick horizontal line in the buffer.

    Args:
        data: memory buffer of the MLX image.
        sl: size of one buffer line.
        x: starting x coordinate.
        y: starting y coordinate.
        length: line length in pixels.
        thick: line thickness in pixels.
        cb: color to apply.
    """
    fill_rect(data, sl, x, y, length, thick, cb)


def draw_vline(
    data: memoryview,
    sl: int,
    x: int,
    y: int,
    length: int,
    thick: int,
    cb: bytes,
) -> None:
    """Draw a thick vertical line in the buffer.

    Args:
        data: memory buffer of the MLX image.
        sl: size of one buffer line.
        x: starting x coordinate.
        y: starting y coordinate.
        length: line length in pixels.
        thick: line thickness in pixels.
        cb: color to apply.
    """
    fill_rect(data, sl, x, y, thick, length, cb)


def write_output(
    gen: MazeGenerator,
    solution: list[str],
    filepath: str,
) -> None:
    """Write the maze to the output file in the expected format.

    Format: one row per line (hex digits), an empty line, the entry,
    the exit, then the path (N/E/S/W letters).

    Args:
        gen: generator holding the maze to export.
        solution: shortest path, as a list of direction letters.
        filepath: path of the file to write.
    """
    try:
        with open(filepath, "w") as f:
            for row in gen.grid:
                f.write(
                    "".join(format(cell, "X") for cell in row) + "\n"
                )
            f.write("\n")
            ex, ey = gen.entry
            xx, xy = gen.exit_
            f.write(f"{ex},{ey}\n")
            f.write(f"{xx},{xy}\n")
            f.write("".join(solution) + "\n")
        print(f"[OK] File written: {filepath!r}")
    except OSError as exc:
        die(f"Unable to write {filepath!r}: {exc}")
