""" Tests for rna.py """

from subprocess import getstatusoutput
import platform
import os.path
import re
import string
import random
import shutil

PRG = './lengths.py'
RUN = f'python {PRG}' if platform.system() == 'Windows' else PRG
INPUT1 = './tests/inputs/input1.txt'
INPUT2 = './tests/inputs/input2.txt'
INPUT3 = './tests/inputs/input3.txt'


# --------------------------------------------------
def test_exists() -> None:
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage() -> None:
    """ Usage """

    for flag in ['-h', '--help']:
        retval, out = getstatusoutput(f'{RUN} {flag}')
        assert retval == 0
        assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_no_args() -> None:
    """ Dies on no args """

    retval, out = getstatusoutput(RUN)
    assert retval != 0
    assert out.lower().startswith('usage:')


# --------------------------------------------------
def test_bad_file() -> None:
    """ Die on missing input """

    bad = random_filename()
    retval, out = getstatusoutput(f'{RUN} {bad}')
    assert retval != 0
    assert re.match('usage:', out, re.IGNORECASE)
    assert re.search(f"No such file or directory: '{bad}'", out)


# --------------------------------------------------
def test_empty_file() -> None:
    """ Runs on empty file """

    out_dir = 'out'
    try:
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        empty_file = os.path.join(out_dir, "empty.txt")
        with open(empty_file, 'w') as f:
            pass

        retval, out = getstatusoutput(f'{RUN} {empty_file}')
        assert retval == 0
        assert out == 'Calculated length statistics for 0 sequences in 1 file to directory "out".'

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_good_input1() -> None:
    """ Runs on good input """

    out_dir = 'out'
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        retval, out = getstatusoutput(f'{RUN} {INPUT1}')
        assert retval == 0
        assert out == 'Calculated length statistics for 1 sequence in 1 file to directory "out".'
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir, 'input1.txt')
        assert os.path.isfile(out_file1)
        assert open(out_file1).read().rstrip() == '\n'.join(
            ['Maximum Length: 23', 'Minimum Length: 23', 'Average Length: 23.0'])
        out_file2 = os.path.join(out_dir, 'combined_data.txt')
        assert os.path.isfile(out_file2)
        assert open(out_file2).read().rstrip() == '\n'.join(
            ['Maximum Length: 23', 'Minimum Length: 23', 'Average Length: 23.0'])

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_good_input2() -> None:
    """ Runs on good input """

    out_dir = random_filename()
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        retval, out = getstatusoutput(f'{RUN} -o {out_dir} {INPUT2}')
        assert retval == 0
        assert out == (f'Calculated length statistics for 2 sequences in 1 file to '
                       f'directory "{out_dir}".')
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir, 'input2.txt')
        out_file2 = os.path.join(out_dir, 'combined_data.txt')
        assert os.path.isfile(out_file1)
        assert os.path.isfile(out_file2)
        assert open(out_file1).read().rstrip() == '\n'.join(
            ['Maximum Length: 20', 'Minimum Length: 18', 'Average Length: 19.0'])
        assert open(out_file2).read().rstrip() == '\n'.join(
            ['Maximum Length: 20', 'Minimum Length: 18', 'Average Length: 19.0'])

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def test_good_multiple_inputs():
    """ Runs on good inputs """

    out_dir = random_filename()
    try:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)

        retval, out = getstatusoutput(
            f'{RUN} --out_dir {out_dir} {INPUT1} {INPUT2} {INPUT3}')
        assert retval == 0
        assert out == (f'Calculated length statistics for 5 sequences in 3 files to '
                       f'directory "{out_dir}".')
        assert os.path.isdir(out_dir)
        out_file1 = os.path.join(out_dir, 'input1.txt')
        out_file2 = os.path.join(out_dir, 'input2.txt')
        out_file3 = os.path.join(out_dir, 'input3.txt')
        out_file4 = os.path.join(out_dir, 'combined_data.txt')
        assert os.path.isfile(out_file1)
        assert os.path.isfile(out_file2)
        assert os.path.isfile(out_file3)
        assert os.path.isfile(out_file4)
        assert open(out_file1).read().rstrip() == '\n'.join(
            ['Maximum Length: 23', 'Minimum Length: 23', 'Average Length: 23.0'])
        assert open(out_file2).read().rstrip() == '\n'.join(
            ['Maximum Length: 20', 'Minimum Length: 18', 'Average Length: 19.0'])
        assert open(out_file3).read().rstrip() == '\n'.join(
            ['Maximum Length: 967', 'Minimum Length: 919', 'Average Length: 943.0'])
        assert open(out_file4).read().rstrip() == '\n'.join(
            ['Maximum Length: 967', 'Minimum Length: 18', 'Average Length: 389.4'])

    finally:
        if os.path.isdir(out_dir):
            shutil.rmtree(out_dir)


# --------------------------------------------------
def random_filename() -> str:
    """ Generate a random filename """

    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
