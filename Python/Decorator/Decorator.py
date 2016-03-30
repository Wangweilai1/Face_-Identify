# _*_ coding: utf-8
import functools
import inspect
from itertools import chain

def precessArg(value, annotation):
    try:
        return annotation(value)
    except ValueError as e:
        print('value:', value)
        raise TypeError('Expected: %s, got: %s' % (annotation.__name__,
                                                   type(value).__name__))

def typesafe(func):
    """
    Verify that the function is called with the right arguments types and that
    it returns a value of the right type, accordings to its annotations.
    """
    spec = inspect.getfullargspec(func)
    annotations = spec.annotations

    for name, annotation in annotations.items():
        if not isinstance(annotation, type):
            raise TypeError("The annotation for '%s' is not a type." % name)

    error = "Wrong type for %s: expected %s, got %s."
    # Deal with default parameters
    defaults = spec.defaults and list(spec.defaults) or []
    defaults_zip = zip(spec.args[-len(defaults):], defaults)
    i = 0
    for name, value in defaults_zip:
        if name in annotations:
            defaults[i] = precessArg(value, annotations[name])
        i += 1
    func.__defaults__ = tuple(defaults)

    kwonlydefaults = spec.kwonlydefaults or {}
    for name, value in kwonlydefaults.items():
        if name in annotations:
            kwonlydefaults[name] = precessArg(value, annotations[name])
    func.__kwdefaults__ = kwonlydefaults

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        keyword_args = kwargs.copy()
        new_args = args and list(args) or []
        new_kwargs = kwargs.copy()
        # Deal with explicit argument passed positionally
        i = 0
        for name, arg in zip(spec.args, args):
            if name in annotations:
                new_args[i] = precessArg(arg, annotations[name])
            i += 1

        # Add all explicit arguments passed by keyword
        for name in chain(spec.args, spec.kwonlyargs):
            poped_name = None
            if name in kwargs:
                poped_name = keyword_args.pop(name)
            if poped_name is not None and name in annotations:
                new_kwargs[name] = precessArg(poped_name, annotations[name]) 

        # Deal with variable positional arguments
        if spec.varargs and spec.varargs in annotations:
            annotation = annotations[spec.varargs]
            for i, arg in enumerate(args[len(spec.args):]):
                new_args[i] = precessArg(arg, annotation)

        # Deal with variable keyword argument
        if spec.varkw and spec.varkw in annotations:
            annotation = annotations[spec.varkw]
            for name, arg in keyword_args.items():
                new_kwargs[name] = precessArg(arg, annotation)

        # Deal with return value
        r = func(*new_args, **new_kwargs)
        if 'return' in annotations:
            r = precessArg(r, annotations['return'])
        return r

    return wrapper


if __name__ == '__main__':
    print("Begin test.")
    print("Test case 1:")
    try:
        @typesafe
        def testfun1(a:'This is a para.'):
            print('called OK!')
    except TypeError as e:
        print("TypeError: %s" % e)

    print("Test case 2:")
    try:
        @typesafe
        def testfun2(a:int,b:str = 'defaule'):
            print('called OK!')
        testfun2('str',1)
    except TypeError as e:
        print("TypeError: %s" % e)

    print("test case 3:")
    try:
        @typesafe
        def testfun3(a:int, b:int = 'str'):
            print('called OK')
    except TypeError as e:
        print('TypeError: %s' % e)

    print("Test case 4:")
    try:
        @typesafe
        def testfun4(a:int = '123', b:int = 1.2):
            print('called OK.')
            print(a, b)
        testfun4()
    except TypeError as e:
        print('TypeError: %s' % e)

    @typesafe
    def testfun5(a:int, b, c:int = 1, d = 2, *e:int, f:int, g, h:int = 3, i = 4, **j:int) -> str :
        print('called OK.')
        print(a, b, c, d, e, f, g, h, i, j)
        return 'OK'

    print("Test case 5:")
    try:
        testfun5(1.2, 'whatever', f = 2.3, g = 'whatever')
    except TypeError as e:
        print('TypeError: %s' % e)

    print("Test case 6:")
    try:
        testfun5(1.2, 'whatever', 2.2, 3.2, 'e1', f = '123', g = 'whatever')
    except TypeError as e:
        print('TypeError: %s' % e)

    print("Test case 7:")
    try:
        testfun5(1.2, 'whatever', 2.2, 3.2, 12, f = '123', g = 'whatever')
    except TypeError as e:
        print('TypeError: %s' % e)

    print("Test case 8:")
    try:
        testfun5(1.2, 'whatever', 2.2, 3.2, 12, f = '123', g = 'whatever', key1 = 'key1')
    except TypeError as e:
        print('TypeError: %s' % e)

    print("Test case 9:")
    try:
        testfun5(1.2, 'whatever', 2.2, 3.2, 12, f = '123', g = 'whatever', key1 = '111')
    except TypeError as e:
        print('TypeError: %s' % e)

    print('Test case 10:')
    @typesafe
    def testfun10(a) -> int:
        print('called OK.')
        return 'OK'
    try:
        testfun10(1)
    except TypeError as e:
        print('TypeError: %s' % e)