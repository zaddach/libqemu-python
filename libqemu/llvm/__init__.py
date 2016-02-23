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

import llvmlite.binding.ffi as ffi
import llvmlite.binding.module as mod
import subprocess
import ctypes
import os
from ctypes import POINTER, c_uint, c_char_p, c_int

REQUIRED_LLVM_VERSION = "3.5"

LLVMBasicBlockRef = ffi._make_opaque_ref("LLVMBasicBlock")

def _load_library():
    #TODO: Find .so in an elegant way
    libdir = subprocess.check_output(["llvm-config-" + REQUIRED_LLVM_VERSION, "--libdir"])
    lib = ctypes.CDLL(os.path.join(libdir.decode(encoding = "ISO-8859-1").strip(), "libLLVM-" + REQUIRED_LLVM_VERSION + ".so"))

    lib.LLVMCountBasicBlocks.argtypes = [ffi.LLVMValueRef]
    lib.LLVMCountBasicBlocks.restype = ctypes.c_uint

    lib.LLVMGetBasicBlocks.argtypes = [ffi.LLVMValueRef, POINTER(LLVMBasicBlockRef)]
    lib.LLVMGetBasicBlocks.restype = None

    lib.LLVMCountParams.argtypes = [ffi.LLVMValueRef]
    lib.LLVMCountParams.restype = c_uint

    lib.LLVMGetParams.argtypes = [ffi.LLVMValueRef, POINTER(ffi.LLVMValueRef)]
    lib.LLVMGetParams.restype = None

    lib.LLVMGetEntryBasicBlock.argtypes = [ffi.LLVMValueRef]
    lib.LLVMGetEntryBasicBlock.restype = ffi.LLVMValueRef

    lib.LLVMGetFirstInstruction.argtypes = [LLVMBasicBlockRef]
    lib.LLVMGetFirstInstruction.restype = ffi.LLVMValueRef

    lib.LLVMGetNextInstruction.argtypes = [ffi.LLVMValueRef]
    lib.LLVMGetNextInstruction.restype = ffi.LLVMValueRef

    lib.LLVMGetInstructionOpcode.argtypes = [ffi.LLVMValueRef]
    lib.LLVMGetInstructionOpcode.restypes = c_uint

    lib.LLVMGetBasicBlockTerminator.argtypes = [LLVMBasicBlockRef]
    lib.LLVMGetBasicBlockTerminator.restype = ffi.LLVMValueRef

    lib.LLVMWriteBitcodeToFile.argtypes = [ffi.LLVMModuleRef, c_char_p]
    lib.LLVMWriteBitcodeToFile.restype = c_int

    lib.LLVMWriteBitcodeToFD.argtypes = [ffi.LLVMModuleRef, c_int, c_int, c_int]
    lib.LLVMWriteBitcodeToFD.restype = c_int

    return lib

lib = _load_library()



