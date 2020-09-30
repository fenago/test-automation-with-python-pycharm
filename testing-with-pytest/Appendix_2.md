<img align="right" src="../logo.png">

**APPENDIX 2**

### pip

pip is the tool used to install Python packages, and it is installed as part of
your Python installation. pip supposedly is a recursive acronym that stands
for _pip install s Python_ or _pip install s Packages._ (Programmers can be pretty
nerdy with their humor.) If you have more than one version of Python installed
on your system, each version has its own pip package manager.

By default, when you run pip install something, pip will:

1. Connect to the PyPI repository at https://pypi.python.org/pypi.
2. Look for a package called something.
3. Download the appropriate version of something for your version of Python
and your system.
4. Install something into the site-packages directory of your Python installation
that was used to call pip. 

To check the version of pip and which version of Python it’s tied to, use pip --
version:


##### Step 1

#### (my_env) $ pip --version

```
pip 18.0 from /pytest-labs/testing-with-pytest/code/venv/lib/python3.7/site-packages/pip (python 3.7)
```

To list the packages you have currently installed with pip, use pip list. If there’s
something there you don’t want anymore, you can uninstall it with pip uninstall
something.

```
Package Version
---------- -------
pip 18.0
setuptools 39.0.1
```


##### Step 2

#### (my_env) $ pip install pytest

```
...
Installing collected packages: six, more-itertools, atomicwrites,
pluggy, attrs, py, pytest
Successfully installed atomicwrites-1.2.1 attrs-18.2.0
more-itertools-4.3.0 pluggy-0.7.1 py-1.6.0 pytest-3.8.0 six-1.11.0
```


##### Step 3

#### (my_env) $ pip list

```
Package Version
-------------- -------
Package Version
-------------- -------
atomicwrites 1.2.1
attrs 18.2.0
more-itertools 4.3.0
pip 18.0
pluggy 0.7.1
py 1.6.0
pytest 3.8.1
setuptools 39.0.1
six 1.11.0
```

As shown in this example, pip installs the package you want and also any
dependencies that aren’t already installed.

pip is pretty flexible. It can install things from other places, such as GitHub,
your own servers, a shared directory, or a local package you’re developing
yourself, and it always sticks the packages in site-packages unless you’re using
Python virtual environments.

You can use pip to install packages with version numbers from pypi.python.org
if it’s a release version PyPI knows about:


##### Step 4


##### $ pip install pytest==3.2.1


You can use pip to install a local package that has a setup.py file in it:


##### Step  5


##### $ pip install /path/to/package


Use ./package_name if you are in the same directory as the package to install it
locally:


##### Step 6


##### $ cd /path/just/above/package

##### $ pip install my_package # pip is looking in PyPI for "my_package"

##### $ pip install ./my_package # now pip looks locally


You can use pip to install packages that have been downloaded as zip files or
wheels without unpacking them.

You can also use pip to download a lot of files at once using a requirements.txt file:


##### Step 7

#### (my_env) $ cat requirements.txt

```
pytest==3.8.1
pytest-xdist==1.23.2
```


##### Step 8

#### (my_env) $ pip install -r requirements.txt


You can use pip to download a bunch of various versions into a local cache
of packages, and then point pip there instead of PyPI to install them into vir-
tual environments later, even when offline.

The following downloads pytest and all dependencies:


##### Step 9

#### (my_env) $ mkdir ~/.pipcache
#### (my_env) $ pip download -d ~/pipcache pytest

```
Collecting pytest
...
Successfully downloaded pytest atomicwrites pluggy
more-itertools setuptools py six attrs
```

Later, even if you’re offline, you can install from the cache:


##### Step 10

#### (my_env) $ pip install --no-index --find-links=~/pipcache pytest

```
Looking in links: /Users/okken/pipcache
Collecting pytest

...
Installing collected packages: attrs, six, more-itertools, atomicwrites,
py, pluggy, pytest
Successfully installed atomicwrites-1.x.y attrs-18.x.y
more-itertools-4.x.y pluggy-0.x.y py-1.x.y pytest-3.x.y six-1.x.y
```

This is great for situations like running tox or continuous integration test
suites without needing to grab packages from PyPI. I also use this method to
grab a bunch of packages before taking a trip so that I can code on the plane.


The Python Packaging Authority documentation is a great resource for more
information on pip.

1. https://pip.pypa.io



