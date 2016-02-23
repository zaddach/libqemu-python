import os
import argparse
from libqemu import Libqemu, ArmCodeFlags, I386CodeFlags, CodeFlags
import struct

def parse_bytes(data):
    return bytes([int(x, 16) for x in data.split(" ")])
        

def main(args, env):
    endianness = {
        "little": "<",
        "big":    ">"}[args.endianness]
    data = parse_bytes(args.bytes)

    def mem_handler(self, env, addr, size, signed, code):
        offset = addr - args.address
        size_char = {
            1: "B",
            2: "H",
            4: "L",
            8: "Q"}[size]
        try:
            return struct.unpack("%s%s" % (endianness, size_char), data[offset : offset + size])[0]
        except IndexError:
            self.raise_error(0xdeadbeef)

    lq = Libqemu(mem_handler, args.arch)

    if args.arch == "arm":
        codeflags = {}
        for flag in args.flags:
            if flag in ["thumb"]:
                codeflags[flag] = True
            else:
                raise SystemError("Invalid flag argument for %s architecture: '%s'" % (args.arch, flag))
        flags = ArmCodeFlags(**codeflags)
    elif args.arch == "i386":
        codeflags = {}
        for flag in args.flags:
            if flags in []:
                codeflags[flag] = True
            else:
                raise SystemError("Invalid flag argument for %s architecture: '%s'" % (args.arch, flag))
        flags = I386CodeFlags(**codeflags)
    else:
        if args.flags:
            raise SystemError("Flags for architecture %s are not yet implemented" % args.arch)
        flags = CodeFlags()


    func = lq.gen_intermediate_code(args.address, flags)
    print(func)



def parse_args():
    parser = argparse.ArgumentParser(description = "Translate one binary opcode into LLVM instructions")
    parser.add_argument("--arch", type = str, default = "arm", help = "Instruction set architecture (i.e., arm, i386)")
    parser.add_argument("--address", type = int, default = 0, help = "Code address of instruction")
    parser.add_argument("--endianness", default = "little", choices = ["little", "big"])
    parser.add_argument("--flag", dest = "flags", action = "append", default = [], help = "Architecture specific disassembly flags (i.e., 'thumb' for the arm architecture)")
    parser.add_argument("bytes", type = str, default = None, help = "Binary opcode data written as hex bytes (i.e., \"ca fe ba be\")")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main(parse_args(), os.environ)
