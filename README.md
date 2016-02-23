# libqemu-python
Python interface to libqemu library

This repository provides a Python interface to the [libqemu library](https://github.com/zaddach/libqemu). 
It allows for easy transformation of binary executable code to the LLVM intermediate language.
The LLVM IR can then be inspected using this library and [llvmlite](https://github.com/numba/llvmlite).

==== Installation ====

If your distribution does not have a package for llvm 3.5, add the [LLVM nightly repo](http://llvm.org/apt/) to your sources list.
Before compiling, some packets need to be installed. On Ubuntu, those are:

  sudo apt-get install llvm-3.5 clang-3.5 libedit-dev zlib1g-dev libffi-dev libtinfo-dev

Afterwards, the module's installation should work:

  python3 setup.py install

You can test your setup with:

 python3 -m libqemu.disassemble --arch arm --flag thumb --address 4096 "08 1D"

That should translate an ARM Thumb instruction set "add r0, r1, #4" to LLVM IR.




