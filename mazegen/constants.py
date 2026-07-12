#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   constants.py                                         :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: horarivo <horarivo@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/04 21:31:14 by horarivo            #+#    #+#            #
#   Updated: 2026/07/04 21:31:15 by horarivo           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Shared constants: wall bitmasks, keycodes, palettes, and "42" pattern."""

from typing import Final

# Chaque cellule est un entier 4 bits. Un bit a 1 signifie "mur ferme".
NORTH: Final[int] = 0b0001
EAST: Final[int] = 0b0010
SOUTH: Final[int] = 0b0100
WEST: Final[int] = 0b1000

# Direction opposee a chaque direction (utile pour percer un mur des
# deux cotes en meme temps).
OPPOSITE: Final[dict[int, int]] = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}
# Deplacement (dx, dy) associe a chaque direction.
DELTA: Final[dict[int, tuple[int, int]]] = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    EAST: (1, 0),
    WEST: (-1, 0),
}
# Lettre affichee dans le fichier de sortie pour chaque direction.
DIR_NAME: Final[dict[int, str]] = {
    NORTH: "N",
    EAST: "E",
    SOUTH: "S",
    WEST: "W",
}

# Codes clavier X11 utilises par MLX.
KEY_Q: Final[int] = 113
KEY_C: Final[int] = 99
KEY_P: Final[int] = 112
KEY_SPACE: Final[int] = 32
KEY_ESCAPE: Final[int] = 65307

# Dimensions du motif "42" (largeur x hauteur en cellules).
PAT_H: Final[int] = 7
PAT_W: Final[int] = 9

# Dessin du chiffre "4" (grille de 0/1, 1 = cellule pleine).
_D4: Final[list[list[int]]] = [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
]
# Dessin du chiffre "2" (meme principe).
_D2: Final[list[list[int]]] = [
    [1, 1, 1, 1],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
    [1, 1, 1, 1],
    [1, 0, 0, 0],
    [1, 0, 0, 0],
    [1, 1, 1, 1],
]


def _build_42() -> list[list[int]]:
    """Assemble les deux chiffres "4" et "2" en une seule grille.

    Returns:
        Grille 2D (PAT_H x PAT_W) ou 1 = cellule a garder pleine.
    """
    pat: list[list[int]] = [[0] * PAT_W for _ in range(PAT_H)]
    for r in range(PAT_H):
        for c in range(4):
            pat[r][c] = _D4[r][c]
            pat[r][5 + c] = _D2[r][c]
    return pat


PATTERN_42: Final[list[list[int]]] = _build_42()

_Palette = dict[str, tuple[int, int, int]]

# Trois jeux de couleurs (RGB) cyclables avec la touche C.
PALETTES: Final[list[_Palette]] = [
    {
        "wall": (220, 220, 220),
        "bg": (20, 20, 35),
        "visited": (28, 28, 52),
        "current": (255, 0, 0),
        "path": (255, 0, 0),
        "entry": (0, 0, 155),
        "exit": (255, 10, 10),
        "pattern": (70, 90, 255),
        "info_bg": (8, 8, 18),
        "hint": (80, 80, 110),
    },
    {
        "wall": (180, 140, 60),
        "bg": (15, 25, 15),
        "visited": (20, 40, 20),
        "current": (255, 200, 50),
        "path": (255, 0, 0),
        "entry": (80, 220, 120),
        "exit": (255, 80, 80),
        "pattern": (40, 50, 160),
        "info_bg": (5, 12, 5),
        "hint": (60, 90, 60),
    },
    {
        "wall": (150, 80, 120),
        "bg": (10, 10, 20),
        "visited": (28, 18, 42),
        "current": (255, 255, 100),
        "path": (255, 0, 0),
        "entry": (80, 55, 120),
        "exit": (255, 80, 80),
        "pattern": (222, 170, 127),
        "info_bg": (5, 5, 12),
        "hint": (90, 60, 100),
    },
]
