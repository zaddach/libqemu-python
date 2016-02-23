# libqemu-python
Python interface to libqemu library

This repository provides a Python interface to the [libqemu library](https://github.com/zaddach/libqemu). 
It allows for easy transformation of binary executable code to the LLVM intermediate language.
The LLVM IR can then be inspected using this library and [llvmlite](https://github.com/numba/llvmlite).

==== Installation ====

If your distribution does not have a package for llvm 3.5, add the [LLVM nightly repo](http://llvm.org/apt/) to your sources list.
Before compiling, some packets need to be installed. On Ubuntu, those are:

  sudo apt-get install llvm-3.5 clang-3.5 libedit-dev

Afterwards, you should be good to go!

  python3 setup.py install



