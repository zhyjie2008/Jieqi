#!/usr/bin/env pypy
# -*- coding: utf-8 -*-

from __future__ import print_function
import re, sys, time
from itertools import count
from collections import namedtuple

piece = { 'P': 44, 'N': 108, 'B': 23, 'R': 233, 'A': 23, 'C': 101, 'K': 2500}
put = lambda board, i, p: board[:i] + p + board[i+1:]
# 子力价值表参考“象眼”

pst = {
    "P": ( #兵
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  9, 12, 15, 17, 22, 17, 15, 12,  9,  0,  0,  0,  0,
      0,  0,  0, 19, 24, 39, 51, 72, 51, 39, 24, 19,  0,  0,  0,  0,
      0,  0,  0, 19, 24, 32, 49, 57, 49, 32, 24, 19,  0,  0,  0,  0,
      0,  0,  0, 19, 23, 27, 29, 30, 29, 27, 23, 19,  0,  0,  0,  0,
      0,  0,  0, 14, 18, 20, 27, 29, 27, 20, 18, 14,  0,  0,  0,  0,
      0,  0,  0,  7,  9, 13, 14, 16, 14, 13,  9,  7,  0,  0,  0,  0,
      0,  0,  0,  7,  7,  7, 11, 15, 11,  7,  7,  7,  0,  0,  0,  0,
      0,  0,  0,  5,  5,  6,  4,  5,  4,  6,  5,  5,  0,  0,  0,  0,
      0,  0,  0,  4,  4,  5, -6, -10, -6, 5,  4,  4,  0,  0,  0,  0,
      0,  0,  0,  2,  2,  3, -9, -12, -9, 3,  2,  2,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "B": ( #相
    # *   *   *   a   b   c   d   e   f   g   h   i   *   *   *   *
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0, 70, 39, 12, 35, 72, 35, 12, 39, 70,  0,  0,  0,  0,  #  对方底线
      0,  0,  0, 65, 15, 15, 20, 68, 20, 15, 15, 65,  0,  0,  0,  0,
      0,  0,  0, 12, 41, 75, 41,  6, 41, 75, 41, 12,  0,  0,  0,  0,
      0,  0,  0, 27, 31, 70, 30, 25, 30, 70, 31, 27,  0,  0,  0,  0,  #  a6/i6相可以阻挡暗车
      0,  0,  0, 65, 35, 12, 35, 70, 35, 12, 35, 65,  0,  0,  0,  0,
      0,  0,  0, 60, 30, 31, 30, 65, 30, 31, 30, 60,  0,  0,  0,  0,
      0,  0,  0, 10, 35, 65, 35, 10, 35, 65, 35, 10,  0,  0,  0,  0,
      0,  0,  0, 35, 30, 49, 30, 43, 30, 49, 30, 35,  0,  0,  0,  0,
      0,  0,  0, 55, 27,  6, 27, 30, 27,  6, 27, 55,  0,  0,  0,  0,
      0,  0,  0, 35, 16, 40, 16, 20, 16, 40, 16, 35,  0,  0,  0,  0,  #  本方底线
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "A": ( #士
    # *   *   *   a   b   c   d   e   f   g   h   i   *   *   *   *
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0, 58, 59, 50, 55, 50, 55, 50, 59, 58,  0,  0,  0,  0,
      0,  0,  0, 58, 63, 62, 85, 70, 85, 62, 63, 58,  0,  0,  0,  0,  #  对方底线
      0,  0,  0, 58, 58, 69, 79, 76, 79, 69, 58, 58,  0,  0,  0,  0,
      0,  0,  0, 55, 59, 58, 61, 58, 61, 58, 59, 55,  0,  0,  0,  0,
      0,  0,  0, 53, 55, 58, 56, 58, 56, 58, 55, 53,  0,  0,  0,  0,
      0,  0,  0, 51, 52, 55, 52, 55, 52, 55, 52, 51,  0,  0,  0,  0,
      0,  0,  0, 43, 55, 45, 55, 45, 55, 45, 55, 43,  0,  0,  0,  0,
      0,  0,  0, 52, 39, 59, 39, 63, 39, 59, 39, 52,  0,  0,  0,  0,
      0,  0,  0, 29, 60, 35, 70, 31, 70, 35, 60, 29,  0,  0,  0,  0,
      0,  0,  0, 35, 27, 65, 39, 75, 39, 65, 27, 35,  0,  0,  0,  0,
      0,  0,  0, 25, 54, 27, 74, 25, 74, 27, 54, 25,  0,  0,  0,  0,  #  本方底线
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "N": ( #马
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0, 90, 90, 90, 96, 90, 96, 90, 90, 90,  0,  0,  0,  0,
      0,  0,  0, 80, 86,103, 87, 94, 87,103, 86, 80,  0,  0,  0,  0,
      0,  0,  0, 87, 83, 84, 95, 99, 95, 84, 83, 87,  0,  0,  0,  0,
      0,  0,  0, 83, 98, 92, 97, 90, 97, 92, 98, 83,  0,  0,  0,  0,
      0,  0,  0, 80, 90, 89,103,104,103, 89, 90, 80,  0,  0,  0,  0,
      0,  0,  0, 80, 88, 91, 92, 93, 92, 91, 88, 80,  0,  0,  0,  0,
      0,  0,  0, 82, 84, 88, 85, 88, 85, 88, 84, 82,  0,  0,  0,  0,
      0,  0,  0, 83, 83, 84, 85, 95, 85, 84, 83, 83,  0,  0,  0,  0,
      0,  0,  0, 80, 80, 82, 83, 78, 83, 82, 80, 80,  0,  0,  0,  0,
      0,  0,  0, 68, 75, 75, 75, 65, 75, 75, 75, 68,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "R": (#车
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,246,248,247,256,254,256,247,248,246,  0,  0,  0,  0,
      0,  0,  0,246,252,252,259,273,259,252,252,246,  0,  0,  0,  0,
      0,  0,  0,246,252,252,259,266,259,252,252,246,  0,  0,  0,  0,
      0,  0,  0,246,253,253,259,256,259,253,253,246,  0,  0,  0,  0,
      0,  0,  0,248,251,251,257,255,257,251,251,248,  0,  0,  0,  0,
      0,  0,  0,248,242,252,257,255,257,252,242,248,  0,  0,  0,  0,
      0,  0,  0,244,244,244,257,254,257,244,244,244,  0,  0,  0,  0,
      0,  0,  0,238,244,244,259,242,259,244,244,238,  0,  0,  0,  0,
      0,  0,  0,240,248,246,259,230,259,246,248,240,  0,  0,  0,  0,
      0,  0,  0,244,246,244,252,220,252,244,246,244,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "C": (
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,145,145,132,132,120,132,132,145,145,  0,  0,  0,  0,
      0,  0,  0,128,128,126,122,129,122,126,128,128,  0,  0,  0,  0,
      0,  0,  0,127,127,126,121,122,121,126,127,127,  0,  0,  0,  0,
      0,  0,  0,126,129,129,128,130,128,129,129,126,  0,  0,  0,  0,
      0,  0,  0,126,126,126,126,130,126,126,126,126,  0,  0,  0,  0,
      0,  0,  0,125,126,129,126,130,126,129,126,125,  0,  0,  0,  0,
      0,  0,  0,126,126,126,126,140,126,126,126,126,  0,  0,  0,  0,
      0,  0,  0,127,126,100,129,140,129,100,126,127,  0,  0,  0,  0,
      0,  0,  0,126,127,128,128,135,128,128,127,126,  0,  0,  0,  0,
      0,  0,  0,126,126,127,129,129,129,127,126,126,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "K": ( #帅
    # *   *   *   a   b   c   d   e   f   g   h   i   *   *   *   *
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  2460,  2470,  2460,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  2470,  2480,  2470,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  2490,  2500,  2490,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    ),
    "0": ( #Bonus
    # *   *   *   a   b   c   d   e   f   g   h   i   *   *   *   *
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  100,  0,  0,  0,  0,  0,  0,  0,  100,  0,  0,  0,  0, #  对方底线
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  30,  0,  30,  0, 30,  0, 30,  0, 30,  0,  0,  0,  0, #翻动暗兵有奖励
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  -100,  0,  0,  0,  0,  0,  0,  0,  -100,  0,  0,  0,  0, #  本方底线
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
      0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0
    )
}


A0, I0, A9, I9 = 12 * 16 + 3,12 * 16 + 11, 3 * 16 + 3,  3 * 16 + 11

'''
D: 暗车
E: 暗马
F: 暗相
G: 暗士
H: 暗炮
I: 暗车
'''

initial = (
    '               \n'  #0
    '               \n'  #1
    '               \n'  #2
    '   rnbakabnr   \n'  #3
    '   .........   \n'  #4
    '   .c.....c.   \n'  #5
    '   p.p.p.p.p   \n'  #6
    '   .........   \n'  #7
    '   .........   \n'  #8
    '   P.P.P.P.P   \n'  #9
    '   .C.....C.   \n'  #10
    '   .........   \n'  #11
    '   RNBAKABNR   \n'  #12
    '               \n'  #13
    '               \n'  #14
    '               \n'  #15
)

initial_covered = (
    '               \n'  #0
    '               \n'  #1
    '               \n'  #2
    '   defgkgfed   \n'  #3
    '   .........   \n'  #4
    '   .h.....h.   \n'  #5
    '   i.i.i.i.i   \n'  #6
    '   .........   \n'  #7
    '   .........   \n'  #8
    '   I.I.I.I.I   \n'  #9
    '   .H.....H.   \n'  #10
    '   .........   \n'  #11
    '   DEFGKGFED   \n'  #12
    '               \n'  #13
    '               \n'  #14
    '               \n'  #15
)


# Lists of possible moves for each piece type.
N, E, S, W = -16, 1, 16, -1
directions = {
    'P': (N, W, E),
    'I': (N, ), #暗兵
    'N': (N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W),
    'E': (N+N+E, E+N+E, W+N+W, N+N+W), #暗马
    'B': (2 * N + 2 * E, 2 * S + 2 * E, 2 * S + 2 * W, 2 * N + 2 * W),
    'F': (2 * N + 2 * E, 2 * N + 2 * W), #暗相
    'R': (N, E, S, W),
    'D': (N, E, W), #暗车
    'C': (N, E, S, W),
    'H': (N, E, S, W), #暗炮
    'A': (N+E, S+E, S+W, N+W),
    'G': (N+E, N+W), #暗士
    'K': (N, E, S, W)
}

MATE_LOWER = piece['K'] - (2*piece['R'] + 2*piece['N'] + 2*piece['B'] + 2*piece['A'] + 2*piece['C'] + 5*piece['P'])
MATE_UPPER = piece['K'] + (2*piece['R'] + 2*piece['N'] + 2*piece['B'] + 2*piece['A'] + 2*piece['C'] + 5*piece['P'])

# The table size is the maximum number of elements in the transposition table.
TABLE_SIZE = 1e7

# Constants for tuning search
QS_LIMIT = 219
EVAL_ROUGHNESS = 13
DRAW_TEST = True
THINK_TIME = 0.5

###############################################################################
# Chess logic
###############################################################################

class Position(namedtuple('Position', 'board score')):
    """ A state of a chess game
    board -- a 256 char representation of the board
    score -- the board evaluation
    """
    def gen_moves(self):
        # For each of our pieces, iterate through each possible 'ray' of moves,
        # as defined in the 'directions' map. The rays are broken e.g. by
        # captures or immediately in case of pieces such as knights.
        for i, p in enumerate(self.board):
            if p == 'K': 
                for scanpos in range(i - 16,A9,-16):
                    if self.board[scanpos] == 'k':
                        yield (i,scanpos)
                    elif self.board[scanpos] != '.':
                        break

            if not p.isupper(): continue

            if p in ('C', 'H'): #明暗炮
                for d in directions[p]:
                    cfoot = 0
                    for j in count(i+d, d):
                        q = self.board[j]
                        if q.isspace():break
                        if cfoot == 0 and q == '.':yield (i,j)
                        elif cfoot == 0 and q != '.':cfoot += 1
                        elif cfoot == 1 and q.islower(): yield (i,j);break
                        elif cfoot == 1 and q.isupper(): break;
                continue

            for d in directions[p]:
                for j in count(i+d, d):
                    q = self.board[j]
                    # Stay inside the board, and off friendly pieces
                    if q.isspace() or q.isupper(): break
                    # 过河的卒/兵才能横着走
                    if p == 'P' and d in (E, W) and i > 128: break
                    # j & 15 等价于 j % 16但是更快
                    elif p in ('A','K') and (j < 160 or j & 15 > 8 or j & 15 < 6): break
                    elif p == 'G' and j != 183: break #暗士, 花心坐标: (11, 7), 11 * 16 + 7 = 183
                    elif p == 'B' and j < 128: break
                    elif p in ('N', 'E'): #暗马
                        n_diff_x = (j - i) & 15
                        if n_diff_x == 14 or n_diff_x == 2:
                            if self.board[i + (1 if n_diff_x == 2 else -1)] != '.': break
                        else:
                            if j > i and self.board[i + 16] != '.': break
                            elif j < i and self.board[i - 16] != '.': break
                    elif p in ('B', 'F') and self.board[i + d // 2] != '.':break
                    # Move it
                    yield (i, j)
                    # Stop crawlers from sliding, and sliding after captures
                    if p in 'PNBAKIEFG' or q.islower(): break

    def rotate(self):
        ''' Rotates the board, preserving enpassant '''
        return Position(
            self.board[-2::-1].swapcase() + " ", -self.score)

    def nullmove(self):
        ''' Like rotate, but clears ep and kp '''
        return self.rotate()

    def move(self, move):
        i, j = move
        # Copy variables and reset ep and kp
        board = self.board
        score = self.score + self.value(move)
        # Actual move
        board = put(board, j, board[i])
        board = put(board, i, '.')
        return Position(board, score).rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        # Actual move
        score = pst[p][j] - pst[p][i]
        # Capture
        if q.islower():
            score += pst[q.upper()][255-j-1]
        return score

###############################################################################
# Search logic
###############################################################################

# lower <= s(pos) <= upper
Entry = namedtuple('Entry', 'lower upper')

class Searcher:
    def __init__(self):
        self.tp_score = {}
        self.tp_move = {}
        self.history = set()
        self.nodes = 0

    def alphabet(self, pos, alpha, beta, depth, root=True):
        """ returns r where
                s(pos) <= r < gamma    if gamma > s(pos)
                gamma <= r <= s(pos)   if gamma <= s(pos)"""
        self.nodes += 1

        # Depth <= 0 is QSearch. Here any position is searched as deeply as is needed for
        # calmness, and from this point on there is no difference in behaviour depending on
        # depth, so so there is no reason to keep different depths in the transposition table.
        depth = max(depth, 0)

        # Sunfish is a king-capture engine, so we should always check if we
        # still have a king. Notice since this is the only termination check,
        # the remaining code has to be comfortable with being mated, stalemated
        # or able to capture the opponent king.
        if pos.score <= -MATE_LOWER:
            return -MATE_UPPER

        # We detect 3-fold captures by comparing against previously
        # _actually played_ positions.
        # Note that we need to do this before we look in the table, as the
        # position may have been previously reached with a different score.
        # This is what prevents a search instability.
        # FIXME: This is not true, since other positions will be affected by
        # the new values for all the drawn positions.
        if DRAW_TEST:
            if not root and pos in self.history:
                return 0

        # Look in the table if we have already searched this position before.
        # We also need to be sure, that the stored search was over the same
        # nodes as the current search.
        entry = self.tp_score.get((pos, depth, root), Entry(-MATE_UPPER, MATE_UPPER))
        if entry.lower >= beta and (not root or self.tp_move.get(pos) is not None):
            return entry.lower
        if entry.upper < alpha:
            return entry.upper

        # Here extensions may be added
        # Such as 'if in_check: depth += 1'

        # Generator of moves to search in order.
        # This allows us to define the moves, but only calculate them if needed.
            # First try not moving at all. We only do this if there is at least one major
            # piece left on the board, since otherwise zugzwangs are too dangerous.
        if depth > 0 and not root and any(c in pos.board for c in 'RNC'):
            val = -self.alphabet(pos.nullmove(), -beta,1-beta, depth-3, root=False)
            if val >= beta and self.alphabet(pos,alpha,beta,depth - 3,root=False): return val
        # For QSearch we have a different kind of null-move, namely we can just stop
        # and not capture anythign else.
        if depth == 0:
            return pos.score
        # Then killer move. We search it twice, but the tp will fix things for us.
        # Note, we don't have to check for legality, since we've already done it
        # before. Also note that in QS the killer must be a capture, otherwise we
        # will be non deterministic.
        best = -MATE_UPPER
        killer = self.tp_move.get(pos)

        # Then all the other moves
        mvBest = None
        for move in [killer] + sorted(pos.gen_moves(), key=pos.value, reverse=True):
        #for val, move in sorted(((pos.value(move), move) for move in pos.gen_moves()), reverse=True):
            # If depth == 0 we only try moves with high intrinsic score (captures and
            # promotions). Otherwise we do all moves.
            if (move is not None) and (depth > 0):
                if best == -MATE_UPPER:
                    val = -self.alphabet(pos.move(move), -beta, -alpha, depth - 1, root=False)
                else:
                    val = -self.alphabet(pos.move(move), -alpha - 1, -alpha, depth - 1, root=False)
                    if val > alpha and val < beta:
                        val = -self.alphabet(pos.move(move), -beta, -alpha, depth - 1, root=False)
                if val > best:
                    best = val
                    if val > beta:
                        mvBest = move
                        break;
                    if val > alpha:
                        alpha = val
                        mvBest = move
        if mvBest is not None:
            # Clear before setting, so we always have a value
            # Save the move for pv construction and killer heuristic
            if len(self.tp_move) > TABLE_SIZE: self.tp_move.clear()
            self.tp_move[pos] = mvBest

        # Stalemate checking is a bit tricky: Say we failed low, because
        # we can't (legally) move and so the (real) score is -infty.
        # At the next depth we are allowed to just return r, -infty <= r < gamma,
        # which is normally fine.
        # However, what if gamma = -10 and we don't have any legal moves?
        # Then the score is actaully a draw and we should fail high!
        # Thus, if best < gamma and best < 0 we need to double check what we are doing.
        # This doesn't prevent sunfish from making a move that results in stalemate,
        # but only if depth == 1, so that's probably fair enough.
        # (Btw, at depth 1 we can also mate without realizing.)
        if best < alpha and best < 0 and depth > 0:
            is_dead = lambda pos: any(pos.value(m) >= MATE_LOWER for m in pos.gen_moves())
            if all(is_dead(pos.move(m)) for m in pos.gen_moves()):
                in_check = is_dead(pos.nullmove())
                best = -MATE_UPPER if in_check else 0

        # Clear before setting, so we always have a value
        if len(self.tp_score) > TABLE_SIZE: self.tp_score.clear()
        # Table part 2
        if best >= beta:
            self.tp_score[pos, depth, root] = Entry(best, entry.upper)
        if best < alpha:
            self.tp_score[pos, depth, root] = Entry(entry.lower, best)

        return best

    def search(self, pos, history=()):
        """ Iterative deepening MTD-bi search """
        self.nodes = 0
        if DRAW_TEST:
            self.history = set(history)
            # print('# Clearing table due to new history')
            self.tp_score.clear()

        # In finished games, we could potentially go far enough to cause a recursion
        # limit exception. Hence we bound the ply.
        for depth in range(1, 1000):
            # The inner loop is a binary search on the score of the position.
            # Inv: lower <= score <= upper
            # 'while lower != upper' would work, but play tests show a margin of 20 plays
            # better.
            lower, upper = -MATE_UPPER, MATE_UPPER
            self.alphabet(pos, lower,upper, depth)
            yield depth, self.tp_move.get(pos), self.tp_score.get((pos, depth, True),Entry(-MATE_UPPER, MATE_UPPER)).lower

###############################################################################
# User interface
###############################################################################

# Python 2 compatability
if sys.version_info[0] == 2:
    input = raw_input


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1])
    return A0 + fil - 16*rank


def render(i):
    rank, fil = divmod(i - A0, 16)
    return chr(fil + ord('a')) + str(-rank)

def print_pos(pos):
    print()
    uni_pieces = {'R':'车', 'N':'马', 'B':'相', 'A':'仕', 'K':'帅', 'P':'兵', 'C':'炮',
                  'r':'俥', 'n':'傌', 'b':'象', 'a':'士', 'k':'将', 'p':'卒', 'c':'砲', '.':'．'}
    for i, row in enumerate(pos.board.split()):
        print(' ', 9-i, ''.join(uni_pieces.get(p, p) for p in row))
    print('    ａｂｃｄｅｆｇｈｉ\n\n')

def main():
    hist = [Position(initial, 0)]
    searcher = Searcher()
    while True:
        print_pos(hist[-1])

        if hist[-1].score <= -MATE_LOWER:
            print("You lost")
            break

        # We query the user until she enters a (pseudo) legal move.
        move = None
        while move not in hist[-1].gen_moves():
            match = re.match('([a-i][0-9])'*2, input('Your move: '))
            if match:
                move = parse(match.group(1)), parse(match.group(2))
            else:
                # Inform the user when invalid input (e.g. "help") is entered
                print("Please enter a move like h2e2")
        hist.append(hist[-1].move(move))

        # After our move we rotate the board and print it again.
        # This allows us to see the effect of our move.
        print("Before Rotate!")
        print_pos(hist[-1].rotate())
        print("After Rotate!")

        if hist[-1].score <= -MATE_LOWER:
            print("You won")
            break

        # Fire up the engine to look for a move.
        start = time.time()
        for _depth, move, score in searcher.search(hist[-1], hist):
            if time.time() - start > THINK_TIME:
                break

        if score == MATE_UPPER:
            print("Checkmate!")

        # The black player moves from a rotated position, so we have to
        # 'back rotate' the move before printing it.
        print("Think depth: {} My move: {}".format(_depth, render(255-move[0] - 1) + render(255-move[1]-1)))
        hist.append(hist[-1].move(move))


if __name__ == '__main__':
    main()
