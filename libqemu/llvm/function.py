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
