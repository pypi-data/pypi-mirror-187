---

![Logo][Logo.img]

---
# **LoneDruid**

## Description:
Package with some functions to help you annoy people and mock on the python language.

## Built with:
---
[![Poetry][Poetry.img]][Poetry-url]

---

## Getting started:

### Installation:
Pip:
`pip install LoneDruid`

### Example of usage:

Right now there are only 3 functions:

`power_find(n: int)`
Can be used to deconstruct an integer into a list of powers of 2 (basically, a binary representation, but with a list)

`int_to_eso(n: int, eso: bool)`If eso==True (by default): Can be used to convert a **integer** into a esoteric representation of itself, that only includes -~int()'s, dunder `__add__`'s and `__pow__`'s (for negative integers it adds a `-` sign before the expression), else will convert it to a semi-normal `{sign}((2**i)+(2**j)...))` kind thing.

`multieso(nums: list[int], path: str, eso: bool)` Basically calls the int_to_eso() function on each element of the list `nums` and constructs a list with those elements inside a file specified in the `path` variable.

```python
import LoneDruid

print(LoneDruid.int_to_eso(42)
>>> ((-~int().__add__(-~int())).__pow__(-~int())).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int())))).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int()).__add__(-~int()).__add__(-~int()))))
```
Verify:
```py
print(((-~int().__add__(-~int())).__pow__(-~int())).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int())))).__add__(((-~int().__add__(-~int())).__pow__(-~int().__add__(-~int()).__add__(-~int()).__add__(-~int()).__add__(-~int())))))
>>> 42
```

## Credits:

* [Python discord community](https://discord.gg/python)  (specially **eivl#1134**)

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Poetry.img]: https://johnfraney.ca/blog/images/poetry.png
[Poetry-url]: https://python-poetry.org/
[Logo.img]: https://media.discordapp.net/attachments/470884583684964352/1066117775166283897/image.png?width=2000&height=662
[Logo.url]: https://discord.gg/python   