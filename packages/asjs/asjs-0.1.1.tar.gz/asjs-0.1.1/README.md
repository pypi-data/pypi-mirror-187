# asjs
 Python module for implement object with syntax from JavaScript

Implementing access to keys by `obj.path.to.your.key` notation as in JavaScript

## Installing

```
pip install asjs
```

or like this:

```
curl https://github.com/tankalxat34/pyasjs/raw/main/asjs.py -o asjs.py
```

## Using

Recommended import statement:

```py
from asjs import ObjectNotation
```

### Creating new object

Using dictionary:

```py
obj = ObjectNotation({"key1": "value1", "key2": "value2", "key3": {"a": "b", "lst": [14, 5, 6, 12]}})
```

Using arguments:

```py
obj = ObjectNotation(key1="value1", key2="value2", key3={"a": "b", "lst": [14, 5, 6, 12]})
```
### Getting values by keys or indexes
    >>> obj[0]
    value1
    >>> obj.key2
    value2
    >>> obj["key3"]
    [14, 5, 6, 12]

### Creating new keys in object
```py
obj.year = 2023
```

or:

```py
>>> obj.set("year", 2023)
```

or:

```py
>>> year = 2023
>>> obj.set(year)
```

or:

```py
>>> obj["year"] = 2023
```
### Saving functions in object
```py
>>> obj.fibonachi = lambda n: 1 if n <= 2 else obj.fibonachi(n - 1) + obj.fibonachi(n - 2)

>>> obj.fibonachi(7)
13
```

### Removing keys by string-names or indexes
    >>> del obj.year

or:
    
    >>> del obj[-1]

or:

    >>> del obj["year"]

### Changing value by key
    >>> obj.key1 = 123

or:

    >>> obj["key1"] = 123

### Cycle `for` by object

Indexes:
```py
>>> for i in range(len(obj)):
...     print(i)
0
1
2
```

Keys:
```py
>>> for k in obj:
...     print(k)
key1
key2
key3
fibonachi
```

Values:
```py
>>> for v in obj.values():
...     print(v)
123
value2
JSObject(a: 'b', lst: JSObject(0: 14, 1: 5, 2: 6, 3: 12))
<function <lambda> at 0x0000020189F19480>
```

### Boolean statements
```py
>>> "key3" in obj
True
>>> "fake_key" in obj
False
```