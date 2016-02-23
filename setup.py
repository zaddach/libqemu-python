try:
    from setuptools import setup, Extension
    from setuptools.command.build_py import build_py as build
    from setuptools.command.build_ext import build_ext
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup, Extension
    from distutils.command.build import build
    from distutils.command.build_ext import build_ext
    from distutils.command.install import install
from distutils.spawn import spawn
import os
import sys
import glob

if os.environ.get('READTHEDOCS', None) == 'True':
    sys.exit("setup.py disabled on readthedocs: called with %s"
             % (sys.argv,))

import versioneer

versioneer.VCS = 'git'
versioneer.versionfile_source = 'libqemu/_version.py'
versioneer.versionfile_build = 'libqemu/_version.py'
versioneer.tag_prefix = 'v' # tags are like v1.2.0
versioneer.parentdir_prefix = 'llvmlite-' # dirname like 'myproject-1.2.0'


here_dir = os.path.dirname(__file__)
build_dir = "%s%sbuild_ext" % (here_dir, "/" if here_dir else "")


cmdclass = versioneer.get_cmdclass()
build = cmdclass.get('build', build)
build_ext = cmdclass.get('build_ext', build_ext)

def get_sosuffix():
    if os.name == 'posix':
        if sys.platform == 'darwin':
            return "dylib"
        else:
            return 'so'
    else:
        assert os.name == 'nt'
        return 'dll'


def get_library_files():
    architectures = ["arm"]
    soext = get_sosuffix()
    return ["%s/%s-lib/libqemu-%s.%s" % (build_dir, x, x, soext) for x in architectures]

class LibqemuBuild(build):

    def finalize_options(self):
        build.finalize_options(self)
        # The build isn't platform-independent
        if self.build_lib == self.build_purelib:
            self.build_lib = self.build_platlib

    def get_sub_commands(self):
        # Force "build_ext" invocation.
        commands = build.get_sub_commands(self)
        for c in commands:
            if c == 'build_ext':
                return commands
        return ['build_ext'] + commands


class LibqemuBuildExt(build_ext):

    def run(self):
        build_ext.run(self)
        cmd = [sys.executable, os.path.join(here_dir, 'build.py')]
        spawn(cmd, dry_run=self.dry_run)
        # HACK: this makes sure the library file (which is large) is only
        # included in binary builds, not source builds.
        self.distribution.package_data = {
            "libqemu.binding": ["*.dll", "*.so", "*.dylib"]
        }


class LibqemuInstall(install):
    # Ensure install see the libllvmlite shared library
    # This seems to only be necessary on OSX.
    def run(self):
        self.distribution.package_data = {
            "libqemu.binding": ["*.dll", "*.so", "*.dylib"]
        }
        install.run(self)


cmdclass.update({'build': LibqemuBuild,
                 'build_ext': LibqemuBuildExt,
                 'install': LibqemuInstall,
                 })

packages = ['libqemu',
            'libqemu.llvm',
            'libqemu.binding',
            'libqemu.disassemble'
            ]

install_requires = ["llvmlite <= 0.5.1"]

setup(name='libqemu',
      description="Python wrapper for libqemu",
      version=versioneer.get_version(),
      classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Compilers",
      ],
      # Include the separately-compiled shared library
      author="Jonas Zaddach",
      author_email="jonas.zaddach@gmail.com",
      url="http://github.com/zaddach/libqemu-python",
      download_url="https://github.com/zaddach/libqemu-python",
      packages=packages,
      install_requires=install_requires,
      license="BSD",
      cmdclass=cmdclass,
      )

