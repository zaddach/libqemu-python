from llvmlite.binding.module import ValueRef
from llvmlite.binding.ffi import _make_opaque_ref
from . import lib
from .instruction import InstructionRef


LLVMBasicBlockRef = _make_opaque_ref("LLVMBasicBlock")

class BasicBlockRef(ValueRef):
    def __init__(self, ptr, module, function):
        self.function = function
        super().__init__(ptr, module)

    @property
    def instructions(self):
        return _InstructionIterator(self.module, self) 

    @property
    def terminator(self):
        inst = lib.LLVMGetBasicBlockTerminator(self)
        return InstructionRef(inst, self.module, self) if inst else None

class _InstructionIterator:
    def __init__(self, module, bb):
        self._inst = lib.LLVMGetFirstInstruction(bb)
        self._module = module
        self._bb = bb

    def __next__(self):
        v = self._inst
        if v:
            self._inst = lib.LLVMGetNextInstruction(v)
            return InstructionRef(v, self._module, self._bb)
        raise StopIteration

    next = __next__

    def __iter__(self):
        return self

