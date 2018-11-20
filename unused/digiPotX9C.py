import ctypes
lib = ctypes.cdll.LoadLibrary('libDigiPotX9C.so')
class DigiPot(object):
    def __init__(self, incPin, udPin, csPin):
        lib.DigiPot_new.argtypes = [ctypes.c_ushort, ctypes.c_ushort, ctypes.c_ushort]
        lib.DigiPot_new.restype = ctypes.c_void_p
        
        lib.DigiPot_reset.argtypes = [ctypes.c_void_p]
        lib.DigiPot_reset.restype = ctypes.c_ushort
        
        lib.DigiPot_get.argtypes = [ctypes.c_void_p]
        lib.DigiPot_get.restype = ctypes.c_ushort
    
        lib.DigiPot_set.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        lib.DigiPot_set.restype = ctypes.c_ushort
    
        lib.DigiPot_increase.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        lib.DigiPot_increase.restype = ctypes.c_ushort
    
        lib.DigiPot_decrease.argtypes = [ctypes.c_void_p, ctypes.c_ushort]
        lib.DigiPot_decrease.restype = ctypes.c_ushort
    
        lib.DigiPot_change.argtypes = [ctypes.c_void_p, ctypes.c_ushort, ctypes.c_ushort]
        lib.DigiPot_change.restype = ctypes.c_ushort
    
        self.obj = lib.DigiPot_new(incPin, udPin, csPin)

    def reset(self):
        return lib.DigiPot_reset(self.obj)

    def get(self):
        return lib.DigiPot_get(self.obj)

    def set(self, val):
        return lib.DigiPot_set(self.obj, val)

    def increase(self, amount):
        return lib.DigiPot_increase(self.obj, amount)

    def decrease(self, amount):
        return lib.DigiPot_decrease(self.obj, amount)

    def change(self, dir, amount):
        return lib.DigiPot_change(self.obj, dir, amount)
