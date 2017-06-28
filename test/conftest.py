
import pytest




class TestValues:
    _name = "NA"
    op8 =  [ 1, 0xff ]
    op16 = [ 1, 0xffff ]
    op32 = [ 1, 0xffffffff]
    op64 = [ 1, 0xffffffffffffffff]
    someval8 = [ 0x2e, 0xa5 ]
    someval16 = [ 0x4b2e, 0xc68b ]
    someval32 = [ 0x5ed39a5f, 0xd2a173f6 ]
    someval64 = [ 0x27f4a35c5ed39a5f, 0xd2ac53201ca173f6 ]
    shift = [ 1, 32]
    x86carryop = [ "stc", "clc"]

class Large(TestValues):
    _name = "large"
    op8 = [ 0, 1, 2, 7, 8, 0xf, 0x10, 0x7f, 0x80, 0x81, 0xff]
    op16 = op8 +  [0x1234, 0x7fff, 0x8000, 0x8001, 0xfa72, 0xffff]
    op32 = op16 +  [0x12345678, 0x1812fada, 0x12a4b4cd,
                    0x7fffffff, 0x80000000, 0x80000001, 0xffffffff ]
    op64 = op32 +  [ 0x123456789, 0x100000000000,  0x65a227c6f24c562a,
                     0x7fffffffffffffff, 0x8000000000000000, 0x80000000000000001,
                     0xa812f8c42dec45ab, 0xffff123456789abc,  0xffffffffffffffff ]
    shift = [0, 1, 2, 3, 4, 5, 7, 8, 9, 15, 16, 17, 24, 31,
               32, 33, 48, 63, 64, 65, 127, 128, 129, 255 ]
    x86carryop = [ "stc", "clc" ]


class Medium(TestValues):
    _name = "medium"
    op8 =  [ 0, 1, 0x7f, 0x80, 0xff ]
    op16 = [ 0, 1, 0xff, 0x7fff, 0x8000, 0xffff ]
    op32 = [ 0, 1, 0x7fffffff, 0x80000000, 0xffffffff]
    op64 = [ 0, 1, 0x7fffffffffffffff, 0x8000000000000000, 0xffffffffffffffff]
    shift = [ 0, 1, 7, 8, 0xf, 0x7f, 0x80, 0x81, 0xff]
    x86carryop = [ "stc", "clc" ]

class Small(TestValues):
    _name = "small"
    x86carryop = [ "stc" ]

COVERAGES = [Large, Medium, Small]

def pytest_addoption(parser):
    parser.addoption("--coverage", choices=[x._name for x in COVERAGES],
                     default="medium", help="test more or less values")



def pytest_generate_tests(metafunc):
    fmap = {x._name:x for x in COVERAGES}[metafunc.config.option.coverage]
    for fn in metafunc.fixturenames:
        fnstr = fn.rstrip("_") # alias foo_, foo__, etc. to foo
        if hasattr(fmap, fnstr):
            metafunc.parametrize(fn, getattr(fmap, fnstr))
