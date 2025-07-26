""" Tests """

import os
from subprocess import getstatusoutput
import re
import random
import string
from typing import NamedTuple


PRG = './fasta_parser.py'
INPUT1 = './tests/input1.fa'


# --------------------------------------------------
class Seq(NamedTuple):
    """ Copying Seq class here due to import restrictions """
    id: str
    seq: str


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{PRG} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_nonexistent_file():
    """ Fails on nonexistent file """

    random_str: str = ''
    for i in range(25):
        random_str += str(random.choice(string.ascii_letters))
    random_str += '.fa'

    retval, out = getstatusoutput(f'{PRG} {random_str}')
    assert retval != 0
    assert re.search('usage:', out)
    assert re.search(f"error: argument FILE: can\'t open '{random_str}'", out)


# --------------------------------------------------
def test_good_input1():
    """ Succeeds with good input """

    retval, out = getstatusoutput(f'{PRG} {INPUT1}')
    assert retval == 0

    assert out == (f'file = "{INPUT1}"\n'
    "[Seq(id='Sequence_A', seq='ATCG'), Seq(id='Sequence_B', seq='CCGGGA'), Seq(id='Sequence_C', seq='TCACTACTACCTGCCCCCCCCCCCCC')]")
