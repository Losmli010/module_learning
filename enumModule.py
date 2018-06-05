from enum import Enum, IntEnum, unique

#枚举类型是一系列常量的集合

class Color(Enum):
    #枚举成员/枚举常量不能重复
    #枚举成员是单例类
    RED = 0
    GREEN = 1
    BLUE = 2
    # RED = 3

print(Color.RED)
print(type(Color.RED))
print(isinstance(Color.RED, Color))

@unique           #枚举常量的值不能重复
class Move(IntEnum):
    #IntEnum: 枚举常量的值必须为int或str(int)
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    # EAST = 4
    # WEAST = "a"

print(Move.UP)