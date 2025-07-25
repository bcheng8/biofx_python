#!/usr/bin/env python3
"""
Author : bcheng <bcheng@localhost>
Date   : 2025-07-21
Purpose: Fibonacci Exercise
"""

import argparse
from typing import NamedTuple, Callable
from pathlib import Path


class Args(NamedTuple):
    """ Command-line arguments """
    generations: int
    litter: int
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Fibonacci Exercise',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('generations',
                        metavar='generations',
                        help='Number of generations',
                        type=int)

    parser.add_argument('litter',
                        metavar='litter',
                        help='Size of litter per generation',
                        type=int)

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='OUT_DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    if args.generations < 1 or args.generations > 40:
        parser.error(f'fib.py: error: generations "{args.generations}" '
                     f'must be between 1 and 40')
    if args.litter < 1 or args.litter > 5:
        parser.error(f'fib.py: error: litter "{args.litter}" '
                     f'must be between 1 and 5')

    return Args(args.generations, args.litter, args.out_dir)


# --------------------------------------------------
def memoize(f: Callable) -> Callable:
    """ Memoize a function """

    cache = {}

    def memo(x):
        if x not in cache:
            cache[x] = f(x)
        return cache[x]

    return memo


# --------------------------------------------------
def main() -> None:
    """ Produce number of pairs of rabbits after
    n generations and k litter size per pair """

    args = get_args()
    gen: int = args.generations
    litter: int = args.litter
    out: str = args.out_dir

    if not Path(out).is_dir():
        Path.mkdir(Path(out))

    # Define fibonacci function internally
    # Decorate fib with memoize (aka fib = memoize(fib))
    @memoize
    def fib(gen):
        if gen == 1 or gen == 2:
            return 1
        return fib(gen-1) + fib(gen-2)*litter

    solution = fib(gen)

    print(solution)

    with open(Path(out) / 'solution.txt', 'w', encoding='utf-8') as f:
        f.write(str(solution))


# --------------------------------------------------
if __name__ == '__main__':
    main()
