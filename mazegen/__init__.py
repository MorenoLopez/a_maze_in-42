#!/usr/bin/env python3
# ########################################################################### #
#   shebang: 1                                                                #
#                                                          :::      ::::::::  #
#   __init__.py                                          :+:      :+:    :+:  #
#                                                      +:+ +:+         +:+    #
#   By: mandrini <mandrini@student.42antananarivo.   +#+  +:+       +#+       #
#                                                  +#+#+#+#+#+   +#+          #
#   Created: 2026/07/04 21:22:34 by mandrini            #+#    #+#            #
#   Updated: 2026/07/04 21:51:41 by mandrini           ###   ########.fr      #
#                                                                             #
# ########################################################################### #

"""Public API of the mazegen package.

Only the classes and functions listed in ``__all__`` are intended to
be imported from outside (mazegen.app remains an internal detail).
"""

from .config import Config, die
from .generator import MazeGenerator
from .solver import MazeSolver

__all__ = [
    "Config",
    "die",
    "MazeGenerator",
    "MazeSolver",
]
