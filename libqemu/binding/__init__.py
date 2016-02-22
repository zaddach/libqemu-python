from ctypes import CDLL
import os

#_architectures = ["arm"]
#_libs = {}

_package_path = os.path.dirname(__file__)

def _get_library(arch):
    
    return CDLL(os.path.join(_package_path, "libqemu-%s.so" % arch))

#for arch in _architectures:
#    try:
#        _libs[arch] = CDLL("libqemu-%s.so" % arch)
#    except:
#        raise
#}
