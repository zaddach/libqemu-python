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

from llvmlite.binding.ffi import LLVMModuleRef, LLVMValueRef
from ctypes import c_uint64, c_void_p, c_uint, c_bool, \
    POINTER, byref, c_char_p, c_int, CFUNCTYPE, CDLL
from .llvm.module import ModuleRef
from .llvm.function import FunctionRef, ArgRef
from .llvm.basic_block import BasicBlockRef

class ArmCodeFlags():
    thumb = False

    def __init__(self, *args, **kwargs):
        for arg in kwargs:
            setattr(self, arg, kwargs[arg])

    @property
    def _value(self):
        return int(self.thumb) << 0

_libqemu_load_func = CFUNCTYPE(c_uint64, c_void_p, c_uint64, c_uint, c_bool, c_bool)
_libqemu_store_func = CFUNCTYPE(None, c_void_p, c_uint64, c_uint, c_bool, c_bool, c_uint64)

class LibqemuError(RuntimeError):
    def __init__(self, errorcode):
        self.code = errorcode

class Libqemu():
    def __init__(self, load_callback, library):
        self._handle = CDLL(library)
        
        self._handle.libqemu_init.argtypes = [_libqemu_load_func, _libqemu_store_func]
        self._handle.libqemu_init.restype = c_int 
        
        self._handle.libqemu_get_module.argtypes = []
        self._handle.libqemu_get_module.restype = LLVMModuleRef
        
        self._handle.libqemu_gen_intermediate_code.argtypes = [c_uint64, c_uint64, c_bool, POINTER(LLVMValueRef)]
        self._handle.libqemu_gen_intermediate_code.restype = c_int 
        
        self._handle.libqemu_raise_error.argtypes = [c_void_p, c_int]
        self._handle.libqemu_raise_error.restype = None
        
        self._handle.libqemu_get_target_name.argtypes = []
        self._handle.libqemu_get_target_name.restype = c_char_p

        self._load_callback = _libqemu_load_func(lambda env, addr, size, signed, code: load_callback(self, env, addr, size, signed, code))
        error = self._handle.libqemu_init(self._load_callback, _libqemu_store_func())
        if error != 0:
            raise LibqemuError(error)
        self.module = ModuleRef(self._handle.libqemu_get_module())

    def gen_intermediate_code(self, pc, code_flags, single_inst = True):
        llvm_func = LLVMValueRef()
        error = self._handle.libqemu_gen_intermediate_code(pc, code_flags._value, single_inst, byref(llvm_func))
        if error != 0:
            raise LibqemuError(error)
        return FunctionRef(llvm_func, module = self.module)

    def raise_error(self, env, error_code):
        self._handle.libqemu_raise_error(env, error_code)

    @property
    def target_name(self):
        return self._handle.libqemu_get_target_name().decode(encoding = "ISO-8859-1")
