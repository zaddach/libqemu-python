# Copyright (c) 2016 Jonas Zaddach <jonas.zaddach@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from llvmlite.binding.module import ModuleRef as LLVMLiteModuleRef
from llvmlite.binding.module import _Iterator
from .function import FunctionRef
from . import lib

class ModuleRef(LLVMLiteModuleRef):
    # Destructor needs to be overridden,
    # Module is destructed by libqemu and not llvmlite
    def _dispose(self):
        pass

    @property
    def functions(self):
        """
        Return an iterator over this module's functions.
        The iterator will yield a ValueRef for each function.
        """
        it = self._capi.LLVMPY_ModuleFunctionsIter(self)
        return _FunctionsIterator(it, module=self)

    def save(self, fd):
        if isinstance(fd, str):
            err = lib.LLVMWriteBitcodeToFile(self, fd)
        else:
            if not isinstance(fd, int):
                fd = fd.fileno()
            err = lib.LLVMWriteBitcodeToFD(self, fd, False, False)
        if err:
            raise IOError(0, "Unknown error writing bitcode to file")
        


class _FunctionsIterator(_Iterator):
    def _dispose(self):
        self._capi.LLVMPY_DisposeFunctionsIter(self)

    def _next(self):
        return self._capi.LLVMPY_FunctionsIterNext(self)

    def __next__(self):
        vp = self._next()
        if vp:
            return FunctionRef(vp, self._module)
        else:
            raise StopIteration
