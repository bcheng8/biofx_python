#!/usr/bin/env python3
"""
Author : bcheng <bcheng@localhost>
Date   : 2025-07-16
Purpose: Report DNA length statistics
"""

import argparse
from typing import NamedTuple, TextIO
import os
from pathlib import Path


class Args(NamedTuple):
    """ Command-line arguments """
    file: list[TextIO]
    out_dir: str


# --------------------------------------------------
def get_args() -> Args:
    """ Get command-line arguments """

    parser = argparse.ArgumentParser(
        description='Transcribe DNA to RNA',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file',
                        help='Input DNA file(s)',
                        metavar='FILE',
                        nargs='+',
                        type=argparse.FileType('rt'))

    parser.add_argument('-o',
                        '--out_dir',
                        help='Output directory',
                        metavar='OUT_DIR',
                        type=str,
                        default='out')

    args = parser.parse_args()

    return Args(file=args.file, out_dir=args.out_dir)


# --------------------------------------------------
def main() -> None:
    """ Produce out_dir populated with files containing DNA seq length info"""

    args = get_args()

    if not os.path.isdir(args.out_dir):
        os.makedirs(args.out_dir)

    #? Assumption that each file line only has one sequence
    num_seqs, num_files = 0, 0
    combined_max, combined_min, combined_avg = None, None, 0

    for file in args.file:
        num_files += 1

        # Initialize file statistics variables
        num_local_seqs, len_max, len_min, len_avg = 0, None, None, 0

        lines = file.readlines()

        with open(Path(args.out_dir) / Path(file.name).name, 'w', encoding='utf-8') as out_file:
            # Check if file is empty
            if len(lines) == 0:
                continue

            for line in lines:
                line = line.strip()
                num_seqs += 1
                num_local_seqs += 1

                # Update sequence length info
                if len_max is None or len(line) > len_max:
                    len_max = len(line)
                if len_min is None or len(line) < len_min:
                    len_min = len(line)
                len_avg += len(line)

            # combined_avg will be divided by num_seq after all files are read
            combined_avg += len_avg
            len_avg /= num_local_seqs

            out_file.write(f'Maximum Length: {len_max}\n'
                           f'Minimum Length: {len_min}\n'
                           f'Average Length: {len_avg}')

        # Compare file statistics to combined ones
        if combined_max is None or len_max > combined_max: # type: ignore
            combined_max = len_max
        if combined_min is None or len_min < combined_min: # type: ignore
            combined_min = len_min

    # Final combined length data calculations and creation of combined_data.txt
    if num_seqs == 0:
        combined_avg = 'N/A'
    else:
        combined_avg /= num_seqs

    with open(Path(args.out_dir) / 'combined_data.txt', 'w', encoding='utf-8') as f:
        f.write(f'Maximum Length: {combined_max}\n'
                f'Minimum Length: {combined_min}\n'
                f'Average Length: {combined_avg}')

    # Formatting output message
    print(f'Calculated length statistics for {num_seqs} '
          f'sequence{"" if num_seqs == 1 else "s"} in {num_files} '
          f'file{"" if num_files == 1 else "s"} to directory "{args.out_dir}".')


# --------------------------------------------------
if __name__ == '__main__':
    main()
