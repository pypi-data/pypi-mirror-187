# [PyCpil](https://pypi.org/project/pycpil/)
[PyCpil](https://pypi.org/project/pycpil/) is a pip pkg to calculate isobaric heat capacity of ionic liquids and ionanofluids (nanofluids).

PyCpil pkg is a part of the research work and can be further used with a proper citation.

[1] [Carbon Nanotube-Based Ionanofluids for Efficient Energy Storage: Thermophysical Properties’ Determination and Advanced Data Analysis](https://pubs.acs.org/doi/abs/10.1021/acs.iecr.0c06008)

[2] [A study of changes in the heat capacity of carbon nanotube-based ionanofluids prepared from a series of imidazolium ionic liquids](https://pubs.rsc.org/en/content/articlelanding/2022/cp/d2cp02110b/unauth)

# Directions to use

1. Downloading the [PyCpil](https://pypi.org/project/pycpil/) pkg from PyPI.

```
$ pip install pycpil
```

2. Using python to import the PyCpil
```
>>> import pycpil as cp
```

3. Accessing help, info and the list of available ionic liquids and nanofluids in the pkg.
```
>>> cp.calculate.help()

>>> cp.calculate.info()

>>> cp.calculate.list()
```

4. Calculating isobaric heat capacity of ionic liquids or/and nanofluids (ionanofluids)

    1. Calculating heat capacity of ionic liquids. Find the name of ionic liquids from the pkg list.
    ```
    >>> cp.calculate.il('ionic liquid name', Temperature [C])
    ```



    2. Calculating heat capacity of nanofluids (ionanofluids). Find the name of ionic liquids, nano-particle and concentration of nano-particle from pkg list.
    ```
    >>> cp.calculate.inf('ionic liquid name', Concentration[wt.%], Temperature [C])
