import llvmlite.binding.ffi as ffi
import llvmlite.binding.module as mod
import subprocess
import ctypes
import os
from ctypes import POINTER, c_uint

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
    lib.LLVMGetBasicBlockTerminator.restype= ffi.LLVMValueRef

    return lib

lib = _load_library()



