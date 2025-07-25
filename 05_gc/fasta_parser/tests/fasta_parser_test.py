""" Tests """

import os
from subprocess import getstatusoutput
import re
import random
import string
from ..fasta_parser import Seq


PRG = './fasta_parser.py'
INPUT1 = './tests/input1.fa'

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

    assert out == [Seq('Sequence_A', 'ATCG'),
                   Seq('Sequence_B', 'CCGGGA'),
                   Seq('Sequence_C', 'TCACTACTACCTGCCCCCCCCCCCCC')]
