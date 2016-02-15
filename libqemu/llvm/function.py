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
from . import lib
from .basic_block import BasicBlockRef
from llvmlite.binding.ffi import LLVMValueRef

class FunctionRef(ValueRef):
    @property
    def basic_blocks(self):
        num_bbs = lib.LLVMCountBasicBlocks(self)
        bbs = (LLVMBasicBlockRef * num_bbs)()
        lib.LLVMGetBasicBlocks(self, bbs)
        return [BasicBlockRef(x, self.module, self) for x in bbs]

    @property
    def args(self):
        num_args = lib.LLVMCountParams(self)
        params = (LLVMValueRef * num_params)()
        lib.LLVMGetParams(self, params)
        return [ArgRef(x, self.module, self) for x in params]

    @property
    def entry_baslic_block(self):
        bb = lib.LLVMGetEntryBasicBlock(self)
        if bb:
            return BasicBlockRef(bb, self.module, self)
        else:
            return None
        
class ArgRef(ValueRef):
    def __init__(self, ptr, module, function):
        self.function = function
        super().__init__(ptr, module)
