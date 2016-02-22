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
from enum import Enum

# instruction opcodes (from include/llvm/Instruction.def)
class Opcode(Enum):
    RET            = 1
    BR             = 2
    SWITCH         = 3
    INDIRECT_BR    = 4
    INVOKE         = 5
    RESUME         = 6
    UNREACHABLE    = 7
    ADD            = 8
    FADD           = 9
    SUB            = 10
    FSUB           = 11
    MUL            = 12
    FMUL           = 13
    UDIV           = 14
    SDIV           = 15
    FDIV           = 16
    UREM           = 17
    SREM           = 18
    FREM           = 19
    SHL            = 20
    LSHR           = 21
    ASHR           = 22
    AND            = 23
    OR             = 24
    XOR            = 25
    ALLOCA         = 26
    LOAD           = 27
    STORE          = 28
    GETELEMENTPTR  = 29
    FENCE          = 30
    ATOMICCMPXCHG  = 31
    ATOMICRMW      = 32
    TRUNC          = 33
    ZEXT           = 34
    SEXT           = 35
    FPTOUI         = 36
    FPTOSI         = 37
    UITOFP         = 38
    SITOFP         = 39
    FPTRUNC        = 40
    FPEXT          = 41
    PTRTOINT       = 42
    INTTOPTR       = 43
    BITCAST        = 44
    ICMP           = 45
    FCMP           = 46
    PHI            = 47
    CALL           = 48
    SELECT         = 49
    USEROP1        = 50
    USEROP2        = 51
    VAARG          = 52
    EXTRACTELEMENT = 53
    INSERTELEMENT  = 54
    SHUFFLEVECTOR  = 55
    EXTRACTVALUE   = 56
    INSERTVALUE    = 57
    LANDINGPAD     = 58

def _get_opcode(value_ref):
    return Opcode(lib.LLVMGetInstructionOpcode(value_ref))

def _get_instruction(value_ref, module, bb):
    try:
        opcode = _get_opcode(value_ref)
        return {
            Opcode.PHI: PHINodeRef,
            Opcode.CALL: CallOrInvokeInstructionRef,
            Opcode.INVOKE: CallOrInvokeInstructionRef,        
            Opcode.SWITCH: SwitchInstructionRef,
            Opcode.ALLOCA: AllocaInstructionRef,
            Opcode.FCMP: CompareInstructionRef,
            Opcode.ICMP: CompareInstructionRef,
        }[opcode](value_ref, module, bb)
    except KeyError:
        return InstructionRef(value_ref, module, bb)

class InstructionRef(ValueRef):
    def __init__(self, ptr, module, bb):
        self.basic_block = bb
        super().__init__(ptr, module)

    @property
    def opcode(self):
        return _get_opcode(self)

class PHINodeRef(InstructionRef):
    pass

class CallOrInvokeInstructionRef(InstructionRef):
    pass

class SwitchInstructionRef(InstructionRef):
    pass

class CompareInstructionRef(InstructionRef):
    pass

class AllocaInstructionRef(InstructionRef):
    pass


