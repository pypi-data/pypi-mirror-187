# TMKTProcess

## How to install it

```sh
pip install tmktprocess
```

## How to import it

```py
from tmktprocess import Process
```

## How to use it

```py
def my_func(*args, **kwargs):
    # do some stuff
    pass
```

> To start your process you have to do this:

```py
process = Process(my_func)
process.start(my_args, my_kwargs)
result = process.join()
```

> The .start() will call your function and pass the args and kwargs, then the result will be return with the .join() method

### Use with Event

> You can also pass an Event from ```threading``` package in __init__ call.

```py
from threading import Event
my_event = Event()
process = Process(my_func, my_event)
```

> When the method will end, the event will be set
> 
> You can use it for everything you want