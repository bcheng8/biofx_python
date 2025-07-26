#!/usr/bin/env python3
"""
Author : bcheng <bcheng@localhost>
Date   : 2025-07-25
Purpose: Hamming distance
"""

import argparse
from typing import NamedTuple, TextIO
import numpy as np


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Hamming distance but MORE!!',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        help='Input sequence(s) file')

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def hamming(str1: str, str2: str) -> int:
    """ Calculate Hamming distance """

    shorter = str1 if len(str1) <= len(str2) else str2
    hamming_dist: int = abs(len(str1) - len(str2))
    for index, _ in enumerate(shorter):
        if str1[index] != str2[index]:
            hamming_dist += 1
    
    return hamming_dist


# --------------------------------------------------
def multi_hamming(file: TextIO) -> np.ndarray:
    """ Calculate Hamming distance """

    lines = file.readlines()
    record = np.zeros((len(lines), len(lines)))

    for i in range(len(lines) - 1):
        str1 = lines[i].strip()
        print(f'Seq {i}: {str1}:')
        for j in range(i, len(lines)):
            if i == j:
                continue
            str2 = lines[j].strip()
            dist: int = hamming(str1, str2)
            record[i][j] = dist
            print(f'\tSeq {j}: {str2} - Dist: {dist}')

    return record


# --------------------------------------------------
def main() -> None:
    """ Main method """

    args = get_args()
    print(multi_hamming(args.file))


# --------------------------------------------------
if __name__ == '__main__':
    main()
