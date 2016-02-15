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

