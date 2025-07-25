#!/usr/bin/env python3
"""
Author : bcheng <bcheng@localhost>
Date   : 2025-07-22
Purpose: Parse FASTA file(s)
"""

import argparse
from typing import NamedTuple, TextIO


class Args(NamedTuple):
    """ Command-line arguments """
    file: list[TextIO]


class Seq(NamedTuple):
    """ Sequence object """
    id: str
    seq: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Convert FASTA file into series of Seq objects',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        metavar='FILE',
                        type=argparse.FileType('rt'),
                        nargs='+',
                        help='FASTA file')

    args = parser.parse_args()

    return Args(args.file)


# --------------------------------------------------
def main() -> list[Seq]:
    """ Parse FASTA files """

    args = get_args()
    files: list[TextIO] = args.file
    seq_list: list[Seq] = []

    for file in files:
        print(f'file = "{file.name}"')

        with open(file.name, 'r', encoding='utf-8') as f:
            lines: list[str] = f.readlines()
            name: str = ''
            seq: str = ''
            for line in lines:
                if line.startswith('>'):
                    # New header means we're the prev sequence is complete
                    if name != '':  # protect against adding to seq_list on 1st iteration
                        seq_list.append(Seq(name, seq))
                    name = line[1:].strip()
                    seq = ''
                else:
                    seq = seq + line.strip()
            # Append final sequence (no new header at the end to trigger appending)
            seq_list.append(Seq(name, seq))

    print(seq_list)
    return seq_list


# --------------------------------------------------
if __name__ == '__main__':
    main()
