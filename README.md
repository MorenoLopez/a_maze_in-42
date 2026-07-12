*This project has been created as part of the 42 curriculum by horarivo, mandrini.*

# A-Maze-ing


## Description

A-Maze-ing is an interactive maze generator written in Python. From a plain-text
configuration file, it produces a randomly generated maze - perfect or imperfect -
displays it in a graphical MLX window with smooth animations, computes the shortest
path from entry to exit, and exports the result to a text file using a hexadecimal
wall representation.

The project is split into two parts:

- a standalone, pip-installable package (`mazegen`) holding all the reusable
  generation, solving, parsing and rendering logic,
- a thin executable (`a_maze_ing.py`) that wires that package to an MLX window and
  handles user interaction.

## Instructions

### Requirements

- Python 3.10 or higher
- the `mlx` module compatible with Python 3

The `mlx` wheel itself is not included in this repository: it is provided as an
attachment on the correction sheet (`mlx-2.2-py3-ubuntu-any.whl` /
`mlx-2.2-py3-fedora-any.whl`, or the `mlx-2.2-py3-none-any.whl` variant used during
development). Install whichever one matches your platform.

### Installation

1. Install Python 3.10+.
2. Install the lint/build dependencies:

```bash
python3 -m pip install -r requirements.txt
```

3. Install the MLX module from the wheel matching your platform:

```bash
python3 -m pip install mlx-2.2-py3-*-any.whl
```

4. (Optional) Install the `mazegen` package itself. Two prebuilt archives are
   already available at the root of this repository:

```bash
python3 -m pip install mazegen-1.0.0-py3-none-any.whl
# or
python3 -m pip install mazegen-1.0.0.tar.gz
```

### Rebuilding the mazegen package

The `mazegen` package can be rebuilt from source at any time:

```bash
make build
```

This runs `python3 -m build`, copies the resulting `mazegen-1.0.0.tar.gz` and
`mazegen-1.0.0-py3-none-any.whl` to the repository root, then removes the
temporary `dist/` and `mazegen.egg-info/` build artifacts.

### Execution

1. Edit `config.txt` or create a custom configuration file.
2. Run the application:

```bash
python3 a_maze_ing.py config.txt
```

### Keyboard controls

- `SPACE`: regenerate a new maze
- `P`: show/hide the shortest path
- `C`: cycle through color palettes
- `Q` or `ESC`: quit the application

## Configuration file

The configuration file contains one `KEY=VALUE` pair per line. Lines starting with
`#` are treated as comments and ignored. All keys below are mandatory.

| Key | Description | Example |
| --- | --- | --- |
| `WIDTH` | Maze width, in cells (integer, >= 5) | `WIDTH=20` |
| `HEIGHT` | Maze height, in cells (integer, >= 5) | `HEIGHT=15` |
| `ENTRY` | Entry coordinates, `x,y` format, inside bounds | `ENTRY=0,0` |
| `EXIT` | Exit coordinates, `x,y` format, inside bounds, different from `ENTRY` | `EXIT=19,14` |
| `OUTPUT_FILE` | Path of the generated output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | `True` for a perfect maze (single path), `False` to punch extra loops | `PERFECT=True` |
| `SEED` | Optional integer seed for reproducible generation | `SEED=42` |

Any malformed line (missing `=`, non-integer `WIDTH`/`HEIGHT`, invalid `x,y` tuple,
invalid `PERFECT` value, out-of-bounds or identical `ENTRY`/`EXIT`, missing
mandatory key) is reported with a clear error message on stderr, and the program
exits cleanly instead of crashing.

### Example configuration

```text
WIDTH=13
HEIGHT=11
ENTRY=0,0
EXIT=1,1
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

## Output file format

Once a maze is generated, it is written to `OUTPUT_FILE` as follows:

1. `HEIGHT` lines of `WIDTH` hexadecimal digits, one digit per cell. Each digit
   encodes which of the 4 walls of that cell are closed, using the bit layout
   `bit0=North, bit1=East, bit2=South, bit3=West` (`1` = wall closed, `0` = open).
2. An empty line.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit, written as a single line of direction
   letters (`N`, `E`, `S`, `W`).

All lines end with `\n`. This format matches the `output_validator.py` script
provided with the subject.

## Generation algorithm

The project uses the randomized Depth-First Search algorithm, also known as the
"Recursive Backtracker", to generate the maze.

### Why this algorithm?

- It is simple to implement and easy to reason about.
- It produces a perfect maze by construction (a spanning tree with no cycles),
  which also guarantees there is never a 3x3-or-larger fully open area.
- It fits naturally with step-by-step animated generation, since each step is a
  single "move to an unvisited neighbor or backtrack" operation.
- It composes well with post-processing: extra passages can be punched into the
  perfect maze afterward (see `PERFECT=False` below) without breaking the
  no-large-open-area constraint, since every candidate passage is checked against
  its 2x2 neighborhood before being carved.
- It is suitable for adding visual features such as the "42" pattern (cells
  reserved ahead of time and simply excluded from the walk) and path solving.

## Reusable module

The `mazegen` package is fully independent from the MLX/display layer and can be
reused in other maze, game, or graphical projects. It is distributed as a
pip-installable package (`mazegen-1.0.0.tar.gz` / `mazegen-1.0.0-py3-none-any.whl`,
both available at the root of this repository).

Reusable parts:

- `mazegen/config.py`: parses and validates a `KEY=VALUE` configuration file.
- `mazegen/generator.py`: `MazeGenerator`, the core maze generation class. Produces
  a grid of walls and passages, step-by-step or all at once.
- `mazegen/solver.py`: `MazeSolver`, a BFS solver returning the shortest path
  between entry and exit.
- `mazegen/renderer.py`: low-level pixel-drawing helpers and the output file
  writer, usable independently of MLX for the file-writing part.

### Basic usage example

```python
from mazegen import MazeGenerator, MazeSolver

# Instantiate the generator with custom parameters (size, entry/exit, seed,
# perfect flag)
gen = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit_=(19, 14),
    seed=42,
    perfect=True,
)
gen.generate_all()

# Access the generated structure: gen.grid[y][x] holds a 4-bit wall mask
# (bit0=N, bit1=E, bit2=S, bit3=W ; 1 = wall closed)
print(gen.grid[0][0])

# Access a solution (shortest path) via the BFS solver
solver = MazeSolver(gen)
print(solver.solve())         # e.g. ['E', 'E', 'S', ...]
print(solver.path_cells())    # {(0, 0), (1, 0), ...}
```

## Advanced features

- Central "42" pattern: some cells remain fully walled to draw the pattern. If the
  maze is too small to fit it, a message is printed on the terminal and the
  pattern is skipped.
- Interactive shortest path display, with an animated tracing line and a
  following avatar.
- Animated maze generation, with a light trail and a pulsing "current cell"
  effect.
- Three different color palettes, cyclable at runtime.
- `PERFECT=False` option to generate imperfect mazes with extra loops, while
  still preventing any 3x3-or-larger fully open area.
- Export of the result as a text file in the expected format.

## Project structure

```text
a-maze-ing/
├── a_maze_ing.py                   - main executable
├── config.txt                      - example configuration
├── Makefile                        - install / run / debug / clean / lint / build
├── pyproject.toml                  - package configuration
├── requirements.txt                - lint and build dependencies
├── mazegen-1.0.0.tar.gz            - prebuilt reusable package (sdist)
├── mazegen-1.0.0-py3-none-any.whl  - prebuilt reusable package (wheel)
└── mazegen/
    ├── __init__.py                 - public API of the package
    ├── app.py                      - MLX interface, rendering, event handling
    ├── config.py                   - configuration parsing and validation
    ├── constants.py                - wall bitmasks, keycodes, palettes, 42 pattern
    ├── generator.py                - maze generation (MazeGenerator)
    ├── renderer.py                 - pixel drawing helpers and output writer
    ├── solver.py                   - maze solving (MazeSolver)
    └── assets/
        └── flash.xpm               - avatar sprite used by the MLX renderer
```

## Project management

### Team and roles

- `horarivo`: maze generation algorithm (recursive backtracker, "42" pattern, animation, loop punching), overall design.
- `mandrini`: path finding algorithm (BFS solver), rendering, testing, and documentation.

### Planning

1. Analyze the project requirements and define the expected features.
2. Implement the configuration parser and its error handling.
3. Develop the maze generator (recursive backtracker, "42" pattern).
4. Add the BFS solver and the MLX rendering layer.
5. Integrate color palettes, keyboard controls, and generation/path animations.
6. Package `mazegen` as a reusable, pip-installable module.
7. Test the output file format, edge cases, and package reinstallation in a
   fresh virtual environment.

The plan evolved mainly around the packaging step: separating the reusable
`mazegen` package from the MLX/display layer was planned from the start, but the
anti-large-open-area check for `PERFECT=False` was added later, once testing
revealed the initial loop-punching logic had no protection against it.

### What worked well

- The modular project structure (config / generator / solver / renderer / app)
  simplified implementation and testing.
- Separating generation logic from rendering made the code reusable as a
  standalone package with no MLX dependency.
- The "42" pattern and the animated generation add a strong visual identity to
  the project.

### Improvements possible

- Support multiple generation algorithms (Prim, Kruskal, Aldous-Broder) and let
  the configuration file select one.
- Allow dynamic reloading of a new configuration file without restarting the
  program.
- Add more advanced rendering options (zoom, grid overlay, step-by-step solver
  animation).

### Tools used

- Python 3.10+
- `pip` and `build` for dependency management and packaging
- `mlx` / MiniLibX for graphical output
- `flake8` and `mypy` for style and static type checking
- Git for version control

## Resources

- Maze generation algorithm: depth-first search / recursive backtracker
- Breadth-first search (BFS) for shortest path solving
- MLX / MiniLibX documentation for graphical output
- Classic maze-related references: "Maze generation algorithm" and
  "Depth-first search maze" articles

### AI usage

AI assistance was used during this project for the following tasks:

- **Code review**: reviewing the generator, solver, and rendering modules for
  bugs, in particular the missing anti-large-open-area check in the
  `PERFECT=False` loop-punching logic, and the non-portable icon path that broke
  once the package was installed outside of the source repository.
- **Packaging guidance**: clarifying how to correctly bundle a non-Python asset
  (`flash.xpm`) inside the `mazegen` wheel using `package-data` and
  `importlib.resources`.

All AI-generated suggestions were reviewed, tested, and adapted by the team
before being integrated into the project.