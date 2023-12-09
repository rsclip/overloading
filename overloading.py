import inspect
from typing import Dict, List, Any, Callable, Tuple, Type
import ctypes

"""
A global function can be overloaded by defining multiple functions with the same name.

To do this, a dictionary of {"name": OverloadedFunction} is maintained in the relevant scope.
The scope will be the scope which the function is defined in. An attribute will be created on the scope:
```
scope.__overloaded_functions__ = {"name": OverloadedFunction}
```

To get the scope:
```
import inspect
scope = inspect.stack()[1].frame
```

When a function is wrapped with the @overload decorator:
- The scope is found
If its the first time the function is being overloaded:
- A new OverloadedFunction is created
- The function is bound to the OverloadedFunction
- The OverloadedFunction is added to the scope
- The function is replaced with the OverloadedFunction
If the function has already been overloaded:
- The function is bound to the OverloadedFunction
- The function is replaced with the OverloadedFunction
"""


class Signature:
    """
    Represents a function parameter signature, not including return.
    """
    def __init__(self, fn: Callable):
        self.sig = self.__signature(fn)
        self.optional = tuple(fn.__defaults__) if fn.__defaults__ else ()
        self.valid = self.__validate(fn)
        self.return_ty = fn.__annotations__.get("return", None)
        self.name = fn.__name__
    
    def __hash__(self) -> int:
        return hash(self.sig)
    
    def __eq__(self, __value: object) -> bool:
        return self.sig == __value
    
    def __signature(self, fn: Callable) -> Tuple[Type]:
        # a list of types of all arguments
        args = tuple(fn.__annotations__[name] for name in fn.__code__.co_varnames if name != "return")
        return args

    def __validate(self, fn: Callable) -> bool:
        """
        Whether the function has full annotations (not including return type)
        """
        annotationSize = len(list(name for name, _ in fn.__annotations__.items() if name != "return"))
        return annotationSize == fn.__code__.co_argcount
    
    #  signature
    def __str__(self) -> str:
        return f"sig<{self.name}({', '.join(arg.__name__ for arg in self.sig)}) -> {self.return_ty.__name__ if self.return_ty else None}>"
    
    def __repr__(self) -> str:
        return str(self.sig)


class OverloadedFunction:
    def __init__(self, name: str):
        self.name = name
        self.map = dict()
    
    def bind(self, name: str, fn: Callable):
        signature = Signature(fn)
        if not signature.valid:
            raise TypeError("All arguments must have type hints")

        self.map[signature] = fn
        
        # print(f"Bound {fn.__name__} to {self.name}: {signature}")
    
    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        """
        Get the matching function and call it, if it exists.
        """
        argsTypes = tuple(type(arg) for arg in args)
        # print(f"Calling {self.name.__name__} with {argsTypes} in {list(self.map.keys())}")

        # get the matching function
        matchingFn = self.map.get(argsTypes, None)
        if matchingFn is None:
            raise TypeError(f"Function {self.name} does not have matching signature")
        
        # call the matching function
        return matchingFn(*args, **kwargs)



class OverloadRegistry:
    def __init__(self):
        self.overloaded_functions: Dict[str, OverloadedFunction] = {}

    def overload(self, fn: Callable) -> Callable:
        # print(f"Overloading {fn.__name__} in {inspect.currentframe().f_back.f_globals['__name__']} with {fn.__annotations__}")
        # print(f"Current overloaded functions: {self.overloaded_functions}")

        name = fn.__name__
        overloaded_function = self.overloaded_functions.get(name, None)

        if overloaded_function is None:
            overloaded_function = OverloadedFunction(fn)
            self.overloaded_functions[name] = overloaded_function

        signature = tuple(inspect.signature(fn).parameters.values())
        overloaded_function.bind(signature, fn)

        return overloaded_function


# @overload decorator
def overload(fn: Callable) -> Callable:
    """
    Overload a function.
    """
    scope = inspect.currentframe().f_back.f_globals['__name__']
    overload_registry = getattr(__import__(scope), '__overload_registry__', None)

    if overload_registry is None:
        overload_registry = OverloadRegistry()
        setattr(__import__(scope), '__overload_registry__', overload_registry)

    return overload_registry.overload(fn)