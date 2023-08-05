#######
numquad
#######

|build| |pyversions| |pypi| |license|

The Python package for numerical quadrature, i.e., numerical integration.

This package is simply a re-purposed mirror of one of the last open-sourced versions of the `quadpy <https://pypi.org/project/quadpy/>`_ Python package, `quadpy version 0.16.10 <https://zenodo.org/record/5541216>`_ (under the GNU GPLv3 license) in late December 2021/early January 2022. The only difference between ``numquad`` and `quadpy version 0.16.10 <https://zenodo.org/record/5541216>`_ is that ``numquad`` has no plotting clients -- plotting clients have been completely disabled. I do not intend to alter the contents of ``numquad`` whatsoever going forward.

************
Installation
************

This package can be installed using ``pip`` via the `Python Package Index <https://pypi.org/project/numquad/>`_ (PyPI),

::

    pip install numquad

Alternatively, a branch can be directly installed using

::

    pip install git+https://github.com/jasonmulderrig/numquad.git@<branch-name>

or after cloning a branch, moving to the main project directory (where the setup and configuration files are located), and executing ``pip install -e .`` for an editable installation or ``pip install .`` for a standard installation.

***********
Information
***********

- `License <https://github.com/jasonmulderrig/numquad/LICENSE>`__
- `Releases <https://github.com/jasonmulderrig/numquad/releases>`__
- `Repository <https://github.com/jasonmulderrig/numquad>`__

..
    Badges ========================================================================

.. |build| image:: https://img.shields.io/github/checks-status/jasonmulderrig/numquad/main?label=GitHub&logo=github
    :target: https://github.com/jasonmulderrig/numquad

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/numquad.svg?logo=python&logoColor=FBE072&color=4B8BBE&label=Python
    :target: https://pypi.org/project/numquad/

.. |pypi| image:: https://img.shields.io/pypi/v/numquad?logo=pypi&logoColor=FBE072&label=PyPI&color=4B8BBE
    :target: https://pypi.org/project/numquad/

.. |license| image:: https://img.shields.io/github/license/jasonmulderrig/numquad?label=License
    :target: https://github.com/jasonmulderrig/numquad/LICENSE