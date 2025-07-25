#!/usr/bin/env python3
"""
Author : bcheng <bcheng@localhost>
Date   : 2025-07-22
Purpose: Compute GC content
"""

import argparse
from typing import NamedTuple, TextIO
from Bio import SeqIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: TextIO


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Compute GC content',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        help='Input sequence file',
                        type=argparse.FileType('rt'),
                        nargs='+')

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> None:
    """ Report highest GC content in FASTA(s) """

    args: Args = get_args()
    file_arg: list[TextIO] = args.file  # type: ignore

    highest_gc_id: str = ""
    highest_gc: float = 0.0

    for file in file_arg:
        for record in SeqIO.parse(file, 'fasta'):
            # Protect against dividing by 0 length sequences
            if len(record.seq) == 0:
                continue

            # Protect against lowercase sequences ## necessary?
            record.seq = record.seq.upper()
            record_gc: float = (100 * (record.count("C") + record.count("G"))
                                / len(record.seq))
            if record_gc > highest_gc:
                highest_gc = record_gc
                highest_gc_id = record.id

    print(f'{highest_gc_id} {highest_gc:0.6f}')  # format to 6 decimal points


# --------------------------------------------------
if __name__ == '__main__':
    main()
