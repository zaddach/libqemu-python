from llvmlite.binding.module import ModuleRef as LLVMLiteModuleRef
from llvmlite.binding.module import _Iterator
from .function import FunctionRef
from .basic_block import LLVMBasicBlockRef
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
