# SympyAdd
Расширение возможностей sympy

## Класс I - единичная матрица

Разложение на элементарные
``` python
from sympy import Matrix
from sympy_add import *

M = Matrix([
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
    ])
I.decompose(M)
```