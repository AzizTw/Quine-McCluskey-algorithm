# Quine-McCluskey algorithm

Python implementation of [Quine–McCluskey algorithm](https://en.wikipedia.org/wiki/Quine%E2%80%93McCluskey_algorithm) to find:

* The Prime Implicants
* The Essential Prime Implicants
* All minimum sum of products forms

## Up to 26 variables

_For any given function._

## How to use

You can choose whether you want to run it interactively or not.

To use the interactive mode, you should run it normally with the following command:
``python main.py``

For non-interactive use, you should run ``python main.py`` and specify the number of variables in the first argument, and then your minterms, and finally, the dont-cares which are optional.

For example:
``python main.py 4 0 1 2 3 4 -d 5 6 7 8``
**4** is the number of variables, the minterms are **{0,1,2,3,4}**, and the dont-cares are **{5,6,7,8}**.

<br>

## Sample runs

``python main.py``:

![](/imgs/Sample.jpg "Sample Run1")

``python main.py 4 0 1 2 3 4 -d 8 9 10 11``:

![](/imgs/Sample2.jpg "Sample Run2")

``python main.py 3 0 4 2 6 7``:

![](/imgs/Sample3.jpg "Sample Run3")
