# brrt

**brrt** is a Python module to interface with old dot matrix printers using a Linux lpt device file. It's name is onomatopetic for the dot matrix printing sound. 

***NOTE*** This project is currently Work in Progress and the interface might change. A *lot*. 

## Usage 

The `printer_factory` should be the main entry point: It selects a formatter and printer dialect:

```python 
>>> from brrt import printer_factory
>>> printer = printer_factory("/dev/usb/lp0", "starlc10", "Aligned") 
```

## DotMatrixPrinter.print()

The resuling `DotMatrixPrinter` object can be used programmatically to print text using the `print` function. Text will automatically be formatted according to the selected formatter class.

```python 
>>> from brrt import printer_factory
>>> printer = printer_factory("/dev/usb/lp0", "starlc10", "Aligned") 
>>> printer.open()
>>> printer.print("Hello, world!")
>>> printer.close()
```

The `DotMatrixPrinter` also supports the context manager interface, so there is no need for manually open/close-ing the device file: 

```python 
>>> from brrt import printer_factory
>>> printer = printer_factory("/dev/usb/lp0", "starlc10", "Aligned") 
>>> with printer: 
>>>     printer.print("Hello, world!")
```

## DotMatrixPrinter.shell()

 An interacte shell is available using the `shell()` method: 
 
 ```python 
>>> printer.shell()
---------------------------------------------
Printer Shell Star LC-10 @ /dev/lp0

/dev/lp0 -> /set font Sanserif
  Set font Sanserif
/dev/lp0 ->   
  --> KTHXBYE!
```


## Script usage 

The `printer.py` file can also be used as a script executable, which will spawn an interactive printer shell.