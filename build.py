import os
import subprocess
import glob
import shutil

CONFIGURE_PARAMS = ["--target-list=arm-lib", "--enable-lib"]

def main(args, env):
    
    src_dir = os.path.join(os.getcwd(), "src")
    configure = os.path.join(src_dir, "configure")
    build_dir = os.path.join(os.getcwd(), "build_ext")
    target_dir = os.path.join(os.getcwd(), "libqemu", "binding")

    CONFIGURE_PARAMS.append(("--clang=%s" % env["CLANG"])  if "CLANG" in env else "--clang=clang")
    CONFIGURE_PARAMS.append(("--cxx=%s" % env["CLANGXX"])  if "CLANGXX" in env else "--cxx=clang++")
    CONFIGURE_PARAMS.append(("--cc=%s" % env["CLANG"])  if "CLANG" in env else "--cc=clang")
    CONFIGURE_PARAMS.append(("--with-llvm-config=%s" % env["LLVM_CONFIG"])  if "LLVM_CONFIG" in env else "--with-llvm-config=llvm-config")

    
    #Make build dir if it does not exist
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    
    #Check out submodule, if not already done
    if not os.path.exists(configure):
        subprocess.check_call(["git", "submodule", "update", "--init", src_dir], cwd = os.getcwd())

    #Run configure
    if not os.path.exists(os.path.join(build_dir, "Makefile")):
        subprocess.check_call([configure] + CONFIGURE_PARAMS, cwd = build_dir)

    subprocess.check_call(["make", "-j4"], cwd = build_dir)

def parse_args():
    return None

if __name__ == "__main__":
    main(parse_args(), os.environ)
