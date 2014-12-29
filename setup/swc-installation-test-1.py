#!/usr/bin/env python

"""Test script to check required Python version.

Execute this code at the command line by typing:

  python swc-installation-test-1.py

How to get a command line:

- On OSX run this with the Terminal application.

- On Windows, go to the Start menu, select 'Run' and type 'cmd'
(without the quotes) to run the 'cmd.exe' Windows Command Prompt.

- On Linux, either use your login shell directly, or run one of a
  number of graphical terminals (e.g. 'xterm', 'gnome-terminal', ...).

For some screen shots, see:

  http://software-carpentry.org/setup/terminal.html

Run the script and follow the instructions it prints at the end.  If
you see an error saying that the 'python' command was not found, than
you may not have any version of Python installed.  See:

  http://www.python.org/download/releases/2.7.3/#download

for installation instructions.

This test is separate to avoid Python syntax errors parsing the more
elaborate `swc-installation-test-2.py`.
"""

import sys as _sys


__version__ = '0.1'


def check_python_version():
    if _sys.version_info < (2, 6):
        print('check for Python version (python):')
        print('outdated version of Python: ' + _sys.version)
        return False
    return True

def check_numpy_version():
    try:
        import numpy
    except ImportError:
        print('Please install Anaconda or update your numpy package')
        print('https://store.continuum.io/cshop/anaconda/')
        return False
    numpy_ver = numpy.__version__
    if numpy_ver != '1.9.1':
        print('outdated version (numpy): '+numpy_ver)
        return False
    return True

def check_scipy_version():
    try:
        import scipy
    except ImportError:
        print('Please install Anaconda or update your scipy package')
        print('https://store.continuum.io/cshop/anaconda/')
        return False
    scipy_ver = scipy.__version__
    if scipy_ver != '0.14.0':
        print('outdated version (scipy): '+scipy_ver)
        return False
    return True

def check_astropy_version():
    try:
        import astropy
    except ImportError:
        print('Please install Anaconda or update your astropy package')
        print('https://store.continuum.io/cshop/anaconda/')
        return False
    astropy_ver = astropy.__version__
    if astropy_ver != '0.4.2':
        print('outdated version (astropy): '+astropy_ver)
        return False
    return True

def check_matplotlib_version():
    try:
        import matplotlib
    except ImportError:
        print('Please install Anaconda or update your matplotlib package')
        print('https://store.continuum.io/cshop/anaconda/')
        return False
    matplotlib_ver = matplotlib.__version__
    if matplotlib_ver != '1.4.2':
        print('outdated version (matplotlib): '+matplotlib_ver)
        return False
    return True

if __name__ == '__main__':
    print('-------------------')
    if check_python_version():
        print('Python Version Passed')
    else:
        print('Python Version Failed')
        print('Install a current version of Python (2.7)!')
        print('https://store.continuum.io/cshop/anaconda/')
        _sys.exit(1)
    print('-------------------')
    if check_numpy_version():
        print('Numpy Version Passed')
    else:
        print('Please update numpy to version 1.9.1')
        print('type: conda update numpy')
        _sys.exit(1)
    print('-------------------')
    if check_scipy_version():
        print('Scipy Version Passed')
    else:
        print('Please update scipy to version 0.14.0')
        print('type: conda update scipy')
        _sys.exit(1)
    print('-------------------')
    if check_matplotlib_version():
        print('Matplotlib Version Passed')
    else:
        print('Please update matplotlib to version 1.4.2')
        print('type: conda update matplotlib')
        _sys.exit(1)
    print('-------------------')
    if check_astropy_version():
        print('Astropy Version Passed')
    else:
        print('Please update astropy to version 0.4.2')
        print('type: conda update astropy')
        _sys.exit(1)
    print('-------------------')