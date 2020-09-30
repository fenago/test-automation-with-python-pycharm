<img align="right" src="../logo.png">


### Plugins

As powerful as pytest is right out of the box, it gets even better when you add
plugins to the mix. The pytest code base is structured with customization
and extensions, and there are hooks available to allow modifications and
improvements through plugins.

It might surprise you to know that you’ve already written some plugins if
you’ve worked through the previous labs in this course. Any time you put
fixtures and/or hook functions into a project’s top-level conftest.py file, you
created a local conftest plugin. It’s just a little bit of extra work to convert
these conftest.py files into installable plugins that you can share between
projects, with other people, or with the world.

We will start this lab looking at where to look for third-party plugins.
Quite a few plugins are available, so there’s a decent chance someone has
already written the change you want to make to pytest. Since we will be
looking at open source plugins, if a plugin does almost what you want to
do but not quite, you can fork it, or use it as a reference for creating your
own plugin. While this lab is about creating your own plugins, Appendix
3, Plugin Sampler Packis included to give you a taste of what’s
possible.

In this lab, you’ll learn how to create plugins, and I’ll point you in the
right direction to test, package, and distribute them. The full topic of Python
packaging and distribution is probably a book of its own, so we won’t cover
everything. But you’ll get far enough to be able to share plugins with your
team. I’ll also discuss some shortcuts to getting PyPI–distributed plugins up
with the least amount of work.

#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `/pytest-labs/testing-with-pytest/code` folder.


### Finding Plugins

You can find third-party pytest plugins in several places. The plugins listed
in Appendix 3, Plugin Sampler Packare all available for download
from PyPI. However, that’s not the only place to look for great pytest plugins.

```
_https://docs.pytest.org/en/latest/plugins.html_

```

The main pytest documentation site has a page that talks about installing
and using pytest plugins, and lists a few common plugins.

```
_https://pypi.python.org_
```
The Python Package Index (PyPI) is a great place to get lots of Python
packages, but it is also a great place to find pytest plugins. When looking
for pytest plugins, it should work pretty well to enter “pytest,” “pytest-,”
or “-pytest” into the search box, since most pytest plugins either start
with “pytest-,” or end in “-pytest.”

```
_https://github.com/pytest-dev_
```
The “pytest-dev” group on GitHub is where the pytest source code is kept.
It’s also where you can find some popular pytest plugins that are intended
to be maintained long-term by the pytest core team.


### Installing Plugins

pytest plugins are installed with pip, just like other Python packages. However,
you can use pip in several different ways to install plugins.

**Install from PyPI**

As PyPI is the default location for pip, installing plugins from PyPI is the easiest
method. Let’s install the pytest-cov plugin:


##### Step 1


##### $ pip install pytest-cov

This installs the latest stable version from PyPI.

**Install a Particular Version from PyPI**

If you want a particular version of a plugin, you can specify the version
after ‘==‘:


##### Step 2

##### $ pip install pytest-cov==2.5.1

**Install from a .tar.gz or .whl File**

Packages on PyPI are distributed as zipped files with the extensions .tar.gz
and/or .whl. These are often referred to as “tar balls” and “wheels.” If you’re



having trouble getting pip to work with PyPI directly (which can happen with
firewalls and other network complications), you can download either the .tar.gz
or the .whl and install from that.

You don’t have to unzip or anything; just point pip at it:


##### Step 3

##### $ pip install pytest-cov-2.5.1.tar.gz

_# or_


##### $ pip install pytest_cov-2.5.1-py2.py3-none-any.whl


**Install from a Local Directory**

You can keep a local stash of plugins (and other Python packages) in a local
or shared directory in .tar.gz or .whl format and use that instead of PyPI for
installing plugins:


##### Step 4


##### $ mkdirsome_plugins

##### $ cp pytest_cov-2.5.1-py2.py3-none-any.whlsome_plugins/

##### $ pip install --no-index--find-links=./some_plugins/pytest-cov**


The --no-index tells pip to not connect to PyPI. The --find-links=./some_plugins/ tells
pip to look in the directory called some_plugins. This technique is especially
useful if you have both third-party and your own custom plugins stored
locally, and also if you’re creating new virtual environments for continuous
integration or with tox. (We’ll talk about both tox and continuous integration
in Lab 7, Using pytest with Other Tools.)

Note that with the local directory install method, you can install multiple
versions and specify which version you want by adding == and the version
number:


##### Step  5

##### $ pip install --no-index--find-links=./some_plugins/pytest-cov==2.5.1


**Install from a Git Repository**

You can install plugins directly from a Git repository—in this case, GitHub:


##### Step 6

##### $ pip install git+https://github.com/pytest-dev/pytest-cov

You can also specify a version tag:


##### Step 7

##### $ pip install git+https://github.com/pytest-dev/pytest-cov@v2.5.1


Or you can specify a branch:


##### Step 8

##### $ pip install git+https://github.com/pytest-dev/pytest-cov@master


Installing from a Git repository is especially useful if you’re storing your own
work within Git, or if the plugin or plugin version you want isn’t on PyPI.


### Writing Your Own Plugins

Many third-party plugins contain quite a bit of code. That’s one of the reasons
we use them—to save us the time to develop all of that code ourselves.

For our example, we’ll create a plugin that changes the way the test status
looks. We’ll also include a command-line option to turn on this new behavior.
We’re also going to add some text to the output header. Specifically, we’ll
change all of the FAILED status indicators to “OPPORTUNITY for improve-
ment,” change F to O, and add “Thanks for running the tests” to the header.
We’ll use the --nice option to turn the behavior on.


Let’s go back to the Tasks project. In Expecting Exceptions, we
wrote some tests that made sure exceptions were raised if someone called an
API function incorrectly. Looks like we missed at least a few possible error
conditions.

1. https://docs.pytest.org/en/latest/reference.html#hooks


Here are a couple more tests:

```
ch5/a/tasks_proj/tests/func/test_api_exceptions.py

"""Test for expected exceptions from using the API wrong."""
import pytest
import tasks
from tasks import Task


@pytest.mark.usefixtures('tasks_db')
class TestAdd():
    """Tests related to tasks.add()."""

    def test_missing_summary(self):
        """Should raise an exception if summary missing."""
        with pytest.raises(ValueError):
            tasks.add(Task(owner='bob'))

    def test_done_not_bool(self):
        """Should raise an exception if done is not a bool."""
        with pytest.raises(ValueError):
            tasks.add(Task(summary='summary', done='True'))
```

Let’s run them to see if they pass:


##### Step  9


##### $ cd /pytest-labs/testing-with-pytest/code/ch5/a/tasks_proj

##### $ pytest

```
=================== test session starts ===================
plugins: cov-2.5.1
collected 57 items
tests/func/test_add.py ... [ 5%]
tests/func/test_add_variety.py .................... [ 40%]
........ [ 54%]
tests/func/test_add_variety2.py ............ [ 75%]
tests/func/test_api_exceptions.py .F....... [ 91%]
tests/func/test_unique_id.py . [ 92%]
tests/unit/test_task.py .... [100%]

======================== FAILURES =========================
_______________ TestAdd.test_done_not_bool ________________
self = <func.test_api_exceptions.TestAdd object at 0x103d82860>
    def test_done_not_bool(self):
        """Should raise an exception if done is not a bool."""
        with pytest.raises(ValueError):
>             tasks.add(Task(summary='summary', done='True'))
E             Failed: DID NOT RAISE <class 'ValueError'>
tests/func/test_api_exceptions.py:20: Failed

=========== 1 failed, 56 passed in 0.48 seconds ===========
```

Let’s run it again with -v for verbose. Since you’ve already seen the traceback,
you can turn that off with --tb=no .


And now let’s focus on the new tests with -k TestAdd, which works because
there aren’t any other tests with names that contain “TestAdd.”


##### Step 10


##### $ cd /pytest-labs/testing-with-pytest/code/ch5/a/tasks_proj/tests/func

##### $ pytest -v --tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
plugins:cov-2.5.1
collected 9 items/ 7 deselected

test_api_exceptions.py::TestAdd::test_missing_summaryPASSED[ 50%]
test_api_exceptions.py::TestAdd::test_done_not_bool FAILED[100%]

==== 1 failed, 1 passed,7 deselected in 0.10 seconds =====
```

We could go off and try to fix this test (and we should later), but now we are
focused on trying to make failures more pleasant for developers.

Let’s start by adding the “thank you” message to the header, which you can
do with a pytest hook called pytest_report_header().

```
ch5/b/tasks_proj/tests/conftest.py

def pytest_report_header():
    """Thank tester for running tests."""
    return "Thanks for running the tests."
```

Next, we’ll change the status reporting for tests to change F to O and FAILED to
OPPORTUNITY for improvement. There’s a hook function that allows for this type of
shenanigans: pytest_report_teststatus():

```
ch5/b/tasks_proj/tests/conftest.py

def pytest_report_teststatus(report):
    """Turn failures into opportunities."""
    if report.when == 'call' and report.failed:
            return (report.outcome, 'O', 'OPPORTUNITY for improvement')
```

And now we have just the output we were looking for. A test session with no
--verbose flag shows an O for failures, er, improvement opportunities:


##### Step 11


##### $ cd /pytest-labs/testing-with-pytest/code/ch5/b/tasks_proj/tests/func

##### $ pytest --tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
Thanksfor runningthe tests.
plugins:cov-2.5.1
collected 9 items/ 7 deselected

test_api_exceptions.py.O
```


```
====`1 failed, 1 passed,7 deselected in 0.10 seconds =====
```



And the -v or --verbose flag will be nicer also:


##### Step 12

##### $ pytest -v --tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
Thanksfor runningthe tests.
plugins:cov-2.5.1
collected 9 items/ 7 deselected

test_api_exceptions.py::TestAdd::test_missing_summaryPASSED[ 50%]
test_api_exceptions.py
::TestAdd::test_done_not_boolOPPORTUNITYfor improvement[100%]

==== 1 failed, 1 passed,7 deselected in 0.11 seconds =====
```

The last modification we’ll make is to add a command-line option, --nice, to
only have our status modifications occur if --nice is passed in:

```
ch5/c/tasks_proj/tests/conftest.py

def pytest_addoption(parser):
    """Turn nice features on with --nice option."""
    group = parser.getgroup('nice')
    group.addoption("--nice", action="store_true",
                    help="nice: turn failures into opportunities")


def pytest_report_header(config):
    """Thank tester for running tests."""
    if config.getoption('nice'):
        return "Thanks for running the tests."


def pytest_report_teststatus(report, config):
    """Turn failures into opportunities."""
    if report.when == 'call':
        if report.failed and config.getoption('nice'):
            return (report.outcome, 'O', 'OPPORTUNITY for improvement')
```

This is a good place to note that for this plugin, we are using just a couple of
hook functions. There are many more, which can be found on the main pytest
documentation site.

We can manually test our plugin just by running it against our example file.
First, with no --nice option, to make sure just the username shows up:


##### Step 13

##### $ cd /pytest-labs/testing-with-pytest/code/ch5/c/tasks_proj/tests/func

##### $ pytest --tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
plugins:cov-2.5.1
collected 9 items/ 7 deselected

test_api_exceptions.py.F [100%]
```

2. https://docs.pytest.org/en/latest/writing_plugins.html



```
==== 1 failed, 1 passed,7 deselected in 0.11 seconds =====
```

Now with --nice:


##### Step 14

##### $ pytest --nice--tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
Thanksfor runningthe tests.
plugins:cov-2.5.1
collected 9 items/ 7 deselected

test_api_exceptions.py.O [100%]

==== 1 failed, 1 passed,7 deselected in 0.12 seconds =====
```

And with --nice and --verbose:


##### Step 15


##### $ pytest -v --nice--tb=no test_api_exceptions.py -k TestAdd

```
=================== test session starts ===================
Thanks for running the tests.
plugins: cov-2.5.1
collected 9 items / 7 deselected
test_api_exceptions.py::TestAdd::test_missing_summary PASSED [ 50%]
test_api_exceptions.py
::TestAdd::test_done_not_bool OPPORTUNITY for improvement [100%]
==== 1 failed, 1 passed, 7 deselected in 0.10 seconds =====

```

Great! All of the changes we wanted are done with about a dozen lines of code
in a conftest.py file. Next, we’ll move this code into a plugin structure.

### Creating an Installable Plugin

The process for sharing plugins with others is well-defined.
First, we need to create a new directory to put our plugin code. It does not
matter what you call it, but since we are making a plugin for the “nice” flag,
let’s call it pytest-nice. We will have two files in this new directory: pytest_nice.py
and setup.py.

3. [http://python-packaging.readthedocs.io](http://python-packaging.readthedocs.io)
4. https://www.pypa.io


```
pytest-nice
├──LICENCE
├──README.rst
├──pytest_nice.py
├──setup.py
└──tests
├──conftest.py
└──test_nice.py
```

In pytest_nice.py, we’ll put the exact contents of our conftest.py that were related
to this feature (and take it out of the tasks_proj/tests/conftest.py):

```
ch5/pytest-nice/pytest_nice.py

"""Code for pytest-nice plugin."""

import pytest


def pytest_addoption(parser):
    """Turn nice features on with --nice option."""
    group = parser.getgroup('nice')
    group.addoption("--nice", action="store_true",
                    help="nice: turn FAILED into OPPORTUNITY for improvement")


def pytest_report_header(config):
    """Thank tester for running tests."""
    if config.getoption('nice'):
        return "Thanks for running the tests."


def pytest_report_teststatus(report, config):
    """Turn failures into opportunities."""
    if report.when == 'call':
        if report.failed and config.getoption('nice'):
            return (report.outcome, 'O', 'OPPORTUNITY for improvement')
```


In setup.py, we need a very minimal call to setup():

```
ch5/pytest-nice/setup.py

"""Setup for pytest-nice plugin."""

from setuptools import setup

setup(
    name='pytest-nice',
    version='0.1.0',
    description='A pytest plugin to turn FAILURE into OPPORTUNITY',
    url='https://wherever/you/have/info/on/this/package',
    author='Your Name',
    author_email='your_email@somewhere.com',
    license='proprietary',
    py_modules=['pytest_nice'],
    install_requires=['pytest'],
    entry_points={'pytest11': ['nice = pytest_nice', ], },
)
```


So far, all of the parameters to setup() are standard and used for all Python
installers. The piece that is different for pytest plugins is the entry_points
parameter. We have listed entry_points={'pytest11':['nice = pytest_nice',], },. The
entry_points feature is standard for setuptools, but pytest11 is a special identifier
that pytest looks for. With this line, we are telling pytest that nice is the name
of our plugin, and pytest_nice is the name of the module where our plugin lives.
If we had used a package, our entry here would be:

```
entry_points={'pytest11': ['name_of_plugin = myproject.pluginmodule',], },

```

I haven’t talked about the README.rst file yet. Some form of README is a
requirement by setuptools. If you leave it out, you’ll get this:

```
...
warning: sdist: standard file not found: should have one of README,
README.rst, README.txt, README.md
...

```

Keeping a README around as a standard way to include some information
about a project is a good idea anyway. Here’s what I’ve put in the file for
pytest-nice:

```
ch5/pytest-nice/README.rst**

pytest-nice: A pytestplugin
=============================

Makespytestoutputjusta bit nicerduringfailures.

Features
--------

- Adds``--nice``optionthat:
    - turns``F``to ``O``
```

```
- with``-v``,turns``FAILURE``to ``OPPORTUNITYfor improvement``

Installation
------------

Giventhatour pytestpluginsare beingsavedin .tar.gzformin the
shareddirectoryPATH,theninstalllikethis:

::
```


##### Step 16


##### $ pip install PATH/pytest-nice-0.1.0.tar.gz

##### $ pip install --no-index--find-linksPATHpytest-nice

```
Usage
-----

::
```


##### Step 17

##### $ pytest --nice


There are lots of opinions about what should be in a README. This is a rather
minimal version, but it works.

### Testing Plugins

Plugins are code that needs to be tested just like any other code. However,
testing a change to a testing tool is a little tricky. When we developed the
plugin code in Writing Your Own Plugins, we tested it manually
by using a sample test file, running pytest against it, and looking at the output
to make sure it was right. We can do the same thing in an automated way
using a plugin called pytester that ships with pytest but is disabled by default.

Our test directory for pytest-nice has two files: conftest.py and test_nice.py. To use
pytester, we need to add just one line to conftest.py:

```
ch5/pytest-nice/tests/conftest.py

"""pytester is needed for testing plugins."""
pytest_plugins = 'pytester'

```

This turns on the pytester plugin. We will be using a fixture called testdir that
becomes available when pytester is enabled.

Often, tests for plugins take on the form we’ve described in manual steps:

1. Make an example test file.
2. Run pytest with or without some options in the directory that contains
our example file.
3. Examine the output.
4. Possibly check the result code—0 for all passing, 1 for some failing.

Let’s look at one example:


```
ch5/pytest-nice/tests/test_nice.py

def test_pass_fail(testdir):

    # create a temporary pytest test module
    testdir.makepyfile("""
        def test_pass():
            assert 1 == 1

        def test_fail():
            assert 1 == 2
    """)

    # run pytest
    result = testdir.runpytest()

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        '*.F*',  # . for Pass, F for Fail
    ])

    # make sure that that we get a '1' exit code for the testsuite
    assert result.ret == 1
```

The testdir fixture automatically creates a temporary directory for us to put test
files. It has a method called makepyfile() that allows us to put in the contents of a
test file. In this case, we are creating two tests: one that passes and one that fails.

We run pytest against the new test file with testdir.runpytest(). You can pass in
options if you want. The return value can then be examined further, and is
of type RunResult.

Usually, I look at stdout and ret. For checking the output like we did manually,
use fnmatch_lines, passing in a list of strings that we want to see in the output,
and then making sure that ret is 0 for passing sessions and 1 for failing sessions.
The strings passed into fnmatch_lines can include glob wildcards. We can use our
example file for more tests. Instead of duplicating that code, let’s make a fixture:

```
ch5/pytest-nice/tests/test_nice.py

@pytest.fixture()
def sample_test(testdir):
    testdir.makepyfile("""
        def test_pass():
            assert 1 == 1

        def test_fail():
            assert 1 == 2
    """)
    return testdir
```

5. https://docs.pytest.org/en/latest/writing_plugins.html#_pytest.pytester.RunResult



Now, for the rest of the tests, we can use sample_test as a directory that already
contains our sample test file. Here are the tests for the other option variants:

```
ch5/pytest-nice/tests/test_nice.py

def test_with_nice(sample_test):
    result = sample_test.runpytest('--nice')
    result.stdout.fnmatch_lines(['*.O*', ])  # . for Pass, O for Fail
    assert result.ret == 1


def test_with_nice_verbose(sample_test):
    result = sample_test.runpytest('-v', '--nice')
    result.stdout.fnmatch_lines([
        '*::test_fail OPPORTUNITY for improvement*',
    ])
    assert result.ret == 1


def test_not_nice_verbose(sample_test):
    result = sample_test.runpytest('-v')
    result.stdout.fnmatch_lines(['*::test_fail FAILED*'])
    assert result.ret == 1
```   

Just a couple more tests to write. Let’s make sure our thank-you message is
in the header:

```
ch5/pytest-nice/tests/test_nice.py

def test_header(sample_test):
    result = sample_test.runpytest('--nice')
    result.stdout.fnmatch_lines(['Thanks for running the tests.'])


def test_header_not_nice(sample_test):
    result = sample_test.runpytest()
    thanks_message = 'Thanks for running the tests.'
    assert thanks_message not in result.stdout.str()
```

This could have been part of the other tests also, but I like to have it in a
separate test so that one test checks one thing.

Finally, let’s check the help text:

```
ch5/pytest -nice/tests/test_nice.py

def test_help_message(testdir):
    result = testdir.runpytest('--help')

    # fnmatch_lines does an assertion internally
    result.stdout.fnmatch_lines([
        'nice:',
        '*--nice*nice: turn FAILED into OPPORTUNITY for improvement',
    ])
```

I think that’s a pretty good check to make sure our plugin works.



To run the tests, let’s start in our pytest-nice directory and make sure our plugin
is installed. We do this either by installing the .zip.gz file or installing the cur-
rent directory in editable mode:


##### Step 18


##### $ cd /pytest-labs/testing-with-pytest/code/ch5/pytest -nice/

##### $ pip install .

```
Processing /pytest-labs/testing-with-pytest/code/ch5/pytest -nice
...

Runningsetup.pybdist_wheelfor pytest-nice... done
...

Successfullybuiltpytest-nice
Installingcollected packages:pytest-nice
Successfullyinstalledpytest-nice-0.1.0
```

Now that it’s installed, let’s run the tests:


##### Step 19

##### $ pytest -v

```
=================== test session starts ===================
plugins:nice-0.1.0,cov-2.5.1
collected 7 items

test_nice.py::test_pass_fail PASSED            [ 14%]
test_nice.py::test_with_nice PASSED            [ 28%]
test_nice.py::test_with_nice_verbose PASSED            [ 42%]
test_nice.py::test_not_nice_verbose PASSED            [ 57%]
test_nice.py::test_header PASSED            [ 71%]
test_nice.py::test_header_not_nice PASSED            [ 85%]
test_nice.py::test_help_message PASSED            [100%]

================ 7 passed in 0.57 seconds =================
```

Yay! All the tests pass. We can uninstall it just like any other Python package
or pytest plugin:


##### Step 20

##### $ pip uninstallpytest-nice

```
Uninstallingpytest-nice-0.1.0:
...

Proceed(y/n)?y
Successfullyuninstalledpytest-nice-0.1.0
```

A great way to learn more about plugin testing is to look at the tests contained
in other pytest plugins available through PyPI.

### Creating a Distribution

Believe it or not, we are almost done with our plugin. From the command
line, we can use this setup.py file to create a distribution:


##### Step 21


##### $ cd /pytest-labs/testing-with-pytest/code/ch5/pytest -nice

##### $ pythonsetup.pysdist

```
runningsdist
runningegg_info
```

```
creatingpytest_nice.egg-info
...

runningcheck
creatingpytest-nice-0.1.0
...

creating dist
Creating tar archive
...
```


##### Step 22


##### $ ls dist

```
pytest-nice-0.1.0.tar.gz
```

(Note that sdist stands for “source distribution.”)

Within pytest-nice, a dist directory contains a new file called pytest-nice-0.1.0.tar.gz.
This file can now be used anywhere to install our plugin, even in place:


##### Step 23


##### $ pip install dist/pytest-nice-0.1.0.tar.gz


```
Processing ./dist/pytest-nice-0.1.0.tar.gz
...
Installing collected packages: pytest-nice
Successfully installed pytest-nice-0.1.0
```

However, you can put your .tar.gz files anywhere you’ll be able to get at them
to use and share.

**Distributing Plugins Through a Shared Directory**

pip already supports installing packages from shared directories, so all we
have to do to distribute our plugin through a shared directory is pick a location
we can remember and put the .tar.gz files for our plugins there. Let’s say we
put pytest-nice-0.1.0.tar.gz into a directory called myplugins.

To install pytest-nice from myplugins:


##### Step 24

##### $ pip install --no-index --find-links myplugins pytest-nice


The --no-index tells pip to not go out to PyPI to look for what you want to install.
The --find-linksmyplugins tells PyPI to look in myplugins for packages to install. And
of course, pytest-nice is what we want to install.

If you’ve done some bug fixes and there are newer versions in myplugins, you
can upgrade by adding --upgrade:


##### Step 25

##### $ pip install --upgrade --no-index --find-links myplugins pytest-nice


This is just like any other use of pip, but with the ---no-index --find-links myplugins added.

**Distributing Plugins Through PyPI**
When you are contributing a pytest plugin, another great place to start is by
using the cookiecutter-pytest-plugin :


##### Step 26


##### $ pip install cookiecutter 


##### $ cookiecutter https://github.com/pytest-dev/cookiecutter-pytest-plugin



### Exercises

In ch4/cache/test_slower.py, there is an autouse fixture called check_duration(). You
used it in the Lab 4 exercises as well. Now, let’s make a plugin out of it.

1. Create a directory named pytest-slower that will hold the code for the new
plugin, similar to the directory described in Creating an Installable Plugin.
2. Fill out all the files of the directory to make pytest-slower an installable plugin.
3. Write some test code for the plugin.
4. Take a look at the Python Package Index and search for “pytest-.” Find
a pytest plugin that looks interesting to you.
5. Install the plugin you chose and try it out on Tasks tests.

### What’s Next

You’ve used conftest.py a lot so far in this course. There are also configuration
files that affect how pytest runs, such as pytest.ini. In the next lab, you’ll
run through the different configuration files and learn what you can do there
to make your testing life easier.

6. https://packaging.python.org/distributing
7. https://github.com/pytest-dev/cookiecutter-pytest-plugin
8. https://pypi.python.org/pypi

