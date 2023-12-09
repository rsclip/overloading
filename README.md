# Python function overloading

## What is function overloading?
In various programming languages, function overloading is the ability to create multiple functions of the same name with different implementations. Calls to an overloaded function will run a specific implementation of that function appropriate to the context of the call, allowing one function call to perform different tasks depending on context.

## How to overload a function in Python?
Python does not support function overloading. The closest you can get natively is to use default arguments in the function definition, overwrite the function with a new definition, or to use the `*args` and `**kwargs` arguments to capture any number of arguments passed to the function.

This project introduces a decorator that allows you to overload a function in Python simply by decorating it with `@overload`. The decorator will automatically select the correct implementation of the function based on the types of the arguments passed to the function.

## The decorator

### Installation
Copying the `overload.py` file into your project will allow you to use the decorator.  
There are no external dependencies, but the decorator requires Python 3.9 or higher.

### How to use
The decorator can be used as follows:

```python
from overload import overload

@overload
def log(msg: str) -> None:
    """
    Log with a single message parameter
    """
    print(f"{msg}")

@overload
def log(msg: str, level: int) -> None:
    """
    Log with a message and integer level parameter
    """
    print(f"[{level}] {msg}")

@overload
def log(msg: str, level: str) -> None:
    """
    Log with a message and string level parameter
    """
    print(f"[STR-{level}] {msg}")
```

The decorator will automatically select the correct implementation of the function based on the types of the arguments passed to the function:

```python
log("Hello, world!") # Prints "Hello, world!"
log("Hello, world!", 1) # Prints "[1] Hello, world!"
log("Hello, world!", "INFO") # Prints "[STR-INFO] Hello, world!"
```

If no implementation matches the types of the arguments passed to the function, a `TypeError` will be raised:

```python
>>> log(1, 2, 3)

TypeError:
No matching function found for (int, int, int). Valid signatures:
log:
        log(str) -> None
        log(str, int) -> None
        log(str, str) -> None
```

## How does it work?

### The `OverloadRegistry` class
The `OverloadRegistry` class is responsible for storing the implementations of all overloaded functions. It is a singleton class, meaning that only one instance of the class can exist at any given time. This ensures that all overloaded functions are stored in the same registry.

The class is stored on the current stack frame, so it will respect scope access.

The `OverloadRegistry` contains a dictionary mapping various function names to an `OverloadedFunction`. This contains all implementations of a given function with varying signatures.

### The `OverloadedFunction` class
The `OverloadedFunction` class is responsible for storing all implementations of a given function, and upon being called mapping the arguments passed to the function to the correct implementation.

The class contains a dictionary of `Signature` objects, which contain the signature of the function and a reference to the function itself.

### The `Signature` class
The `Signature` class represents a given signature (no default arguments) of a function. It contains the types of the arguments and the return type of the function.

### The `@overload` decorator
The `@overload` decorator is responsible for registering a function with the `OverloadRegistry`. It will create an `OverloadedFunction` object for the function if it does not exist yet, and add the function to the `OverloadedFunction` object.

The `OverloadRegistry` will be attached to the current stack frame if it doesn't exist.

The original function defined will be stored in the `OverloadedFunction` object, and the `OverloadedFunction` component will be returned. This allows the decorator to be used as a function call, which will then return the correct implementation of the function based on the types of the arguments passed to the function.

## Constraints

### Default arguments
The decorator does not support default arguments. This is because the decorator will only be called once, when the function is defined. This means that the decorator cannot know which implementation to return when the function is called, as it does not know the values of the default arguments.

### `*args` and `**kwargs`
Due to the way the decorator works, it is not possible to use `*args` and `**kwargs` in the function definition. 

We cannot determine the types of arguments passed into the function, so it may cause bugs.

### `@overload` decorator
The `@overload` decorator can only be used on functions. It cannot be used on methods, as the decorator will not be able to determine the type of the `self` argument.

### Type hints

#### Type hints in the function definition
Overloaded functions **must** have type hints in the function definition. This is because the decorator will use the type hints to determine which implementation to return.

The return type hint is not required.

#### Advanced type hinting
The decorator currently does not support advanced type hinting, such as `typing.Union` or `typing.Optional`.