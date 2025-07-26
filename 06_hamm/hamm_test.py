#!/usr/bin/env python3
""" Tests for hamm.py """

import os
import platform
from subprocess import getstatusoutput
from hamm import hamming


PRG = './hamm.py'
RUN = f'python {PRG}' if platform.system() == 'Windows' else PRG
INPUT1 = './tests/inputs/1.txt'
INPUT2 = './tests/inputs/2.txt'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{RUN} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def run(file: str) -> None:
    """ Run with input """

    assert os.path.isfile(file)
    with open(file, encoding='utf-8') as f:
        seq1, seq2, expected = f.read().splitlines()

    rv, out = getstatusoutput(f'{RUN} {seq1} {seq2}')
    assert rv == 0
    assert out.rstrip() == expected


# --------------------------------------------------
def test_hamming() -> None:
    """ Test hamming """

    assert hamming('', '') == 0
    assert hamming('A', 'A') == 0
    assert hamming('ACG', 'TCGA') == 2
    assert hamming('GAGCCTACTAACGGGAT', 'CATCGTAATGACGGCCT') == 7


# --------------------------------------------------
def test_input1() -> None:
    """ Test with input1 """

    run(INPUT1)


# --------------------------------------------------
def test_input2() -> None:
    """ Test with input2 """

    run(INPUT2)
