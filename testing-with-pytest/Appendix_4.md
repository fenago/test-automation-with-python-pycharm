<img align="right" src="../logo.png">


**APPENDIX 4**

### Packaging and Distributing Python Projects

The idea of packaging and distribution seems so serious. Most of Python has
a rather informal feeling about it, and now suddenly, we’re talking “packaging
and distribution.” However, sharing code is part of working with Python.
Therefore, it’s important to learn to share code properly with the builtin Python
tools. And while the topic is bigger than what I cover here, it needn’t be
intimidating. All I’m talking about is how to share code in a way that is more
traceable and consistent than emailing zipped directories of modules.

This lab is intended to give you a comfortable understanding of how to
set up a project so that it is installable with pip, how to create a source distribution, and how to create a wheel. This is enough for you to be able to share your code locally with a small team.

### Creating an Installable Module

We’ll start by learning how to make a small project installable with pip. For a
simple one-module project, the minimal configuration is small. I don’t recom-
mend you make it quite this small, but I want to show a minimal structure
in order to build up to something more maintainable, and also to show how
simple setup.py can be. Here’s a simple directory structure:

```
some_module_proj/
├──setup.py
└──some_module.py
```

The code we want to share is in some_module.py:

```
appendices/packaging/some_module_proj/some_module.py

def some_func():
    return 42
```

To make it installable with pip, we need a setup.py file. This is about as bare
bones as you can get:

```
appendices/packaging/some_module_proj/setup.py

    from setuptools import setup
    setup(
    name='some_module',
    py_modules=['some_module']
    )
```

One directory with one module and a setup.py file is enough to make it instal-
lable via pip:


##### Step 1


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/packaging

##### $ pip install ./some_module_proj

```
Processing ./some_module_proj
Installing collected packages: some-module
Running setup.py install for some-module ... done
Successfully installed some-module-0.0.0
```

And we can now use some_module from Python (or from a test):


##### Step 2


##### $ python

```
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.

>>> from some_module import some_func
>>> some_func()
42
>>> exit()
```

That’s a minimal setup, but it’s not realistic. If you’re sharing code, odds are
you are sharing a package. The next section builds on this to write a setup.py
file for a package.

### Creating an Installable Package

Let’s make this code a package by adding an `__init__.py` and putting the `__init__.py` file and module in a directory with a package name:


##### Step 3


##### $ tree some_package_proj/

```
some_package_proj/
├── setup.py
└── src
└── some_package
├── __init__.py
└── some_module.py
``` 


The content of some_module.py doesn’t change. The `__init__.py` needs to be written
to expose the module functionality to the outside world through the package
namespace. There are lots of choices for this. I recommend skimming the two
sections of the Python documentation that cover this topic.

If we do something like this in `__init__.py`:

```
import some_package.some_module
```
the client code will have to specify some_module:

```
import some_package
some_package.some_module.some_func()
```

However, I’m thinking that some_module.py is really our API for the package,
and we want everything in it to be exposed to the package level. Therefore,
we’ll use this form:

```
appendices/packaging/some_package_proj/src/some_package/__init__.py

from some_package.some_module import *
```

Now the client code can do this instead:

```
import some_package
some_package.some_func()
```

We also have to change the setup.py file, but not much:

```
appendices/packaging/some_package_proj/setup.py
fromsetuptoolsimport setup,find_packages

setup(
name='some_package',
packages=find_packages(where='src'),
package_dir={'': 'src'},
)
```

Instead of using py_modules, we specify packages.
This is now installable:


##### Step 4


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/packaging

##### $ pip install ./some_package_proj/

```
Processing ./some_package_proj
Installing collected packages: some-package
Running setup.py install for some-package ... done
Successfully installed some-package-0.0.0
```

1. https://docs.python.org/3/tutorial/modules.html#packages


and usable:


##### Step 5


##### $ python

```
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 26 2018, 23:26:24)
[Clang 6.0 (clang-600.0.57)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from some_package import some_func
>>> some_func()
42
```

Our project is now installable and in a structure that’s easy to build on. You
can add a tests directory at the same level of src to add our tests if you want.
However, the setup.py file is still missing some metadata needed to create a
proper source distribution or wheel. It’s just a little bit more work to make
that possible.

### Creating a Source Distribution and Wheel

For personal use, the configuration shown in the previous section is enough
to create a source distribution and a wheel. Let’s try it:


##### Step 6


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/packaging/some_package_proj/

##### $ pip install wheel

##### $ python setup.py sdist bdist_wheel

```
running sdist
...
warning: sdist: standard file not found:
should have one of README, README.rst, README.txt, README.md
running check
warning: check: missing required meta-data: url
warning: check: missing meta-data:
either (author and author_email)
or (maintainer and maintainer_email) must be supplied
running bdist_wheel
```

##### Step 7


##### $ ls dist

```
some_package-0.0.0-py3-none-any.whl some_package-0.0.0.tar.gz
```

Well, with some warnings, a .whl and a .tar.gz file are created. Let’s get rid of
those warnings.

To do that, we need to:

- Add one of these files: README, README.rst, or README.txt.
- Add metadata for url.
- Add metadata for either (author and author_email) or (maintainer and maintain-
    er_email).


Let’s also add:

- A version number
- A license
- A change log

It makes sense that you’d want these things. Including some kind of README
allows people to know how to use the package. The url, author, and author_email
(or maintainer) information makes sense to let users know who to contact if they
have issues or questions about the package. A license is important to let
people know how they can distribute, contribute, and reuse the package. And
if it’s not open source, say so in the license data. To choose a license for open
source projects, I recommend looking at https://choosealicense.com.

Those extra bits don’t add too much work. Here’s what I’ve come up with for
a minimal default.

The setup.py:

```
appendices/packaging/some_package_proj_v2/setup.py

from setuptools import setup, find_packages

setup(
name='some_package',
description='Demonstrate packaging and distribution',
version='1.0',
author='Fenago',
author_email='brian@pythontesting.net',
url='https://pragprog.com/book/bopytest/python-testing-with-pytest',
packages=find_packages(where='src'),
package_dir={'': 'src'},
)

```


Here’s the README.rst:

```
appendices/packaging/some_package_proj_v2/README.rst


====================================================
some_package: Demonstrate packaging and distribution
====================================================
``some_package`` is the Python package to demostrate how easy it is
to create installable, maintainable, shareable packages and distributions.
It does contain one function, called ``some_func()``.
.. code-block
>>> import some_package
>>> some_package.some_func()
42
```

That's it, really.

The README.rst is formatted in reStructuredText. I’ve done what many have
done before me: I copied a README.rst from an open source project, removed
everything I didn’t like, and changed everything else to reflect this project.

You can also use a markdown formated README.md, or an ASCII-formatted
README.txt or README, but I’m okay with copy/paste/edit in this instance.

I recommend also adding a change log. Here’s the start of one:

```
appendices/packaging/some_package_proj_v2/CHANGELOG.rst

Changelog
=========
------------------------------------------------------
1.0
---
Changes:
~~~~~~~~
- Initial version.
```

See [http://keepachangelog.com](http://keepachangelog.com) for some great advice on what to put in your change log. All of the changes to tasks_proj over the course of this course have been logged
into a CHANGELOG.rst file.

Let’s see if this was enough to remove the warnings:


##### Step 8


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/packaging/some_package_proj_v2

##### $ python setup.py sdist bdist_wheel

```
running sdist
running build
```

2. [http://docutils.sourceforge.net/rst.html](http://docutils.sourceforge.net/rst.html)


```
running build_py
creating build
creating build/lib
creating build/lib/some_package
...
```

##### Step 9


##### $ ls dist

```
some_package-1.0-py3-none-any.whl some_package-1.0.tar.gz
```

Yep. No warnings.

Now, we can put the .whl and/or .tar.gz files in a local shared directory and pip
install to our heart’s content:


##### Step 10


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/packaging/some_package_proj_v2

##### $ mkdir ~/packages/

##### $ cp dist/some_package-1.0-py3-none-any.whl ~/packages

##### $ cp dist/some_package-1.0.tar.gz ~/packages

##### $ pip install --no-index --find-links=~/packages some_package

```
Collecting some_package
Installing collected packages: some-package
Successfully installed some-package-1.0
```


##### Step 11


##### $ pip install --no-index --find-links=./dist some_package==1.0

```
Requirement already satisfied: some_package==1.0 in
/path/to/venv/lib/python3.6/site-packages
```

Now you can create your own stash of local project packages from your team,
including multiple versions of each, and install them almost as easily as
packages from PyPI.

### Creating a PyPI-Installable Package

You need to add more metadata to your setup.py to get a package ready to
distribute on PyPI. You also need to use a tool such as Twine to push pack-
ages to PyPI. (Twine is a collection of utilities to help make interacting with
PyPI easy and secure. It handles authentication over HTTPS to keep your PyPI
credentials secure, and handles the uploading of packages to PyPI.)
