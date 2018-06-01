seg = "Python decorator".center(40, "*")

#闭包: 外函数返回内函数的引用[函数名]
def outer(func):
    def inner(**kwargs):
        return func(**kwargs)
    return inner

def func(**kwargs):
    for v in kwargs.values():
        print(v)

args = {"desc": "Hello", "name": "My name is Losmli", "home": "I am from Hubei"}
f = outer(func)
f(**args)
#函数名是指向函数的变量,可以被赋值给其他变量
#函数被调用后才会执行
#outer(func)返回inner函数, inner函数被赋值给变量f, 调用函数f(**args)即执行inner(**args)

print(seg)

#闭包和装饰器
@outer
def test(**kwargs):
    for v in kwargs.values():
        print(v)

test(**args)

print(seg)

#装饰器: 在不修改原函数的情况下,装饰器可以在原函数调用前或调用后执行功能[装饰器就是给原函数添加功能]
"""
decorators are “wrappers”, which means that they let you execute code
before and after the function they decorate without modifying the function itself.
"""
#无参数装饰器
def hello(func):
    def wrapper():
        print("hello, %s" % func.__name__)
        func()
        print("goodbye, %s" % func.__name__)
    return wrapper

@hello
def foo():
    print("i am foo")

foo()
#等价于foo = hello(foo)
#hello()是一个decorator，hello(foo)返回函数wrapper，调用foo()将执行新函数wrapper()
#wrapper()函数内，首先打印，再紧接着调用原始函数func(),再打印

print(seg)

#多个装饰器: 给原函数添加多个功能, 但是原函数只执行一次
@hello
@hello
def bar():
    print("i am bar")

bar()
#等价于bar = hello(hello(bar))
#从上向下执行,但是原函数只执行一次
#可以将hello(bar)作为一个整体func, 先给func添加功能

print(seg)

#带参数的装饰器以及给被装饰的函数传递参数
def log(text):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("%s %s" % (text, func.__name__))
            func(*args, **kwargs)
        return wrapper
    return decorator

@log("hello")
def now(a):
    print("2018-5-26")
    print(a)

arg = "Learning python decorator"
now(arg)
#等价于now = log("hello")(now)
#首先执行log("hello")，返回的是decorator函数，再调用返回的decorator函数，参数是now函数，返回值最终是wrapper函数
#wrapper可以接受不定长的参数,*args通过tuple传递参数,**kwargs通过dict传递参数
#wrapper()函数内，首先打印，再紧接着调用原始函数func()

print(seg)

#将被装饰过的函数的函数名修正
import functools

def logger(arg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper():
            print("%s %s" % (arg, func.__name__))
            return func()
        return wrapper
    return decorator

@logger("goodbye")
def today():
    print("2018-5-26")

today()
print(today.__name__)
#被装饰过的原函数的函数名会变为wrapper
#@functools.wraps(func)等价于wrapper.__name__ = func.__name__

print(seg)

#给函数调用做缓存
def memo(func):
    cache = {}
    miss = object()

    @functools.wraps(func)
    def wrapper(*args):
        result = cache.get(args, miss)
        if result is miss:
            result = func(*args)
            cache[args] = result
        return result

    return wrapper

@memo
def fib(n):
    if n <= 2:
        return 1
    return fib(n - 1) + fib(n - 2)

print(fib(10))

print(seg)

#@property装饰器
class C(object):
    def __init__(self, name, age):
        self.name = name
        #age为私有属性, 不能直接被外界调用
        self.__age = age

    @property                     #装饰age函数, 使私有属性age能够被直接访问
    def age(self):                #函数名必须为私有属性的属性名
        return self.__age

    @age.setter                    #@属性名.setter, 使私有属性age能被修改
    def age(self, age):
        self.__age = age

    @age.deleter
    def age(self):
        del self.__age

c = C("somebody", 18)
# print(c.age)       #如果不定义被@property装饰的age函数, age属性不能被访问
print(c.__dict__)
c.age = 28
c.__age = 38         #动态绑定了一个新属性:__age
print(c.__dict__)

print(seg)

#内置装饰器classmethod和staticmethod
class Date(object):

    def __init__(self, day=0, month=0, year=0):
        self.day = day
        self.month = month
        self.year = year

    @classmethod
    def from_string(cls, date_as_string):
        """
        cls is an object that holds class itself, not an instance of the class.
        It's pretty cool because if we inherit our Date class, all children will have from_string defined also.
        :param date_as_string:
        :return:
        """
        day, month, year = map(int, date_as_string.split("-"))
        date1 = Date(day, month, year)
        return date1

    """
    staticmethod doesn't take any obligatory parameters
    (like a class method or instance method does).
    it's basically just a function
    without access to the object and it's internals (fields and another methods)
    """
    @staticmethod
    def is_date_valid(date_as_string):
        day, month, year = map(int, date_as_string.split("-"))
        return day <= 31 and month <= 12 and year <= 3999

date2 = Date.from_string("26-05-2018")
is_date = Date.is_date_valid("26-05-2018")
print(date2)
print(is_date)