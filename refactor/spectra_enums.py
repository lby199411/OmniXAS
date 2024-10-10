from enum import StrEnum


class MaterialIDPrefix(StrEnum):
    mp = "mp"
    mvc = "mvc"  # depricated in materials project


class Element(StrEnum):
    Ti = "Ti"
    V = "V"
    Cr = "Cr"
    Mn = "Mn"
    Fe = "Fe"
    Co = "Co"
    Ni = "Ni"
    Cu = "Cu"


class SpectrumType(StrEnum):
    VASP = "VASP"
    FEFF = "FEFF"


FEFF = SpectrumType.FEFF
VASP = SpectrumType.VASP

Ti = Element.Ti
V = Element.V
Cr = Element.Cr
Mn = Element.Mn
Fe = Element.Fe
Co = Element.Co
Ni = Element.Ni
Cu = Element.Cu
