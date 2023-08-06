# Ycolor<br>
made by Yourouchour<br>
My English is not good,so the following content comes from my translation software.<br>
### Description<br>
Ycolor is a conventional color text printing tool.<br>
### How to use<br>
Ycolor 1.0.x uses four functions to print color text.<br>
```python
from ycolor import *
printcolor('Hello, world',fore=Fore.RED,back=Back.WHITE)
printcolor_text('Hello, world',color='RED+WHITE')
printcolor_int('Hello, world',color='0xfe')
```
### Historical version<br>
v1.0.1 Two functions are created to print color text.<br>
v1.0.2 Some modules are hidden to make the display more concise.<br>
v1.0.3 Added function printcolor_int.<br>