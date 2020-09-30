<img align="right" src="../logo.png">


### Builtin Fixtures

The builtin fixtures that come prepackaged with pytest can help you do some
pretty useful things in your tests easily and consistently. For example, in
addition to handling temporary files, pytest includes builtin fixtures to access
command-line options, communicate between tests sessions, validate output
streams, modify environmental variables, and interrogate warnings. The
builtin fixtures are extensions to the core functionality of pytest. Let’s now 
take a look at several of the most often used builtin fixtures one by one.


#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `/pytest-labs/testing-with-pytest/code` folder.


### Using tmpdir and tmpdir_factory

The tmpdir and tmpdir_factory builtin fixtures are used to create a temporary file
system directory before your test runs, and remove the directory when your
test is finished. Here’s a simple example using tmpdir:

```
ch4/test_tmpdir.py

def test_tmpdir(tmpdir):
    # tmpdir already has a path name associated with it
    # join() extends the path to include a filename
    # the file is created when it's written to
    a_file = tmpdir.join('something.txt')

    # you can create directories
    a_sub_dir = tmpdir.mkdir('anything')

    # you can create files in directories (created when written)
    another_file = a_sub_dir.join('something_else.txt')

    # this write creates 'something.txt'
    a_file.write('contents may settle during shipping')

    # this write creates 'anything/something_else.txt'
    another_file.write('something different')

    # you can read the files as well
    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
```

The value returned from tmpdir is an object of type py.path.local. Because the tmpdir fixture is defined as function scope, you can’t use
tmpdir to create folders or files that should stay in place longer than one test
function. For fixtures with scope other than function (class, module, session),
tmpdir_factory is available.

To see how similar tmpdir and tmpdir_factory are, I’ll modify the tmpdir example
just enough to use tmpdir_factory instead:

```
ch4/test_tmpdir.py

def test_tmpdir_factory(tmpdir_factory):
    # you should start with making a directory
    # a_dir acts like the object returned from the tmpdir fixture
    a_dir = tmpdir_factory.mktemp('mydir')

    # base_temp will be the parent dir of 'mydir'
    # you don't have to use getbasetemp()
    # using it here just to show that it's available
    base_temp = tmpdir_factory.getbasetemp()
    print('base:', base_temp)

    # the rest of this test looks the same as the 'test_tmpdir()'
    # example except I'm using a_dir instead of tmpdir

    a_file = a_dir.join('something.txt')
    a_sub_dir = a_dir.mkdir('anything')
    another_file = a_sub_dir.join('something_else.txt')

    a_file.write('contents may settle during shipping')
    another_file.write('something different')

    assert a_file.read() == 'contents may settle during shipping'
    assert another_file.read() == 'something different'
```

The first line uses mktemp('mydir') to create a directory and saves it in a_dir. For
the rest of the function, you can use a_dir just like the tmpdir returned from
the tmpdir fixture.

In the second line of the tmpdir_factory example, the getbasetemp() function returns
the base directory used for this session. The print statement is in the example
so you can see where the directory is on your system. Let’s see where it is:


##### Step 1


##### $ cd /pytest-labs/testing-with-pytest/code/ch4

##### $ pytest -q -s test_tmpdir.py::test_tmpdir_factory

```
base:/private/var/folders/53/zv4j_zc506x2xq25l31qxvxm0000gn\
/T/pytest-of-okken/pytest-732
.
1 passed in 0.04seconds
```

You can also specify your own base directory if you need to with pytest --
`basetemp=mydir`.

**Using Temporary Directories for Other Scopes**


Suppose we have a module full of tests, and many of them need
to be able to read some data from a json file. We could put a module scope
fixture in either the module itself, or in a conftest.py file that sets up the data
file like this:

```
ch4/authors/conftest.py

"""Demonstrate tmpdir_factory."""

import json
import pytest


@pytest.fixture(scope='module')
def author_file_json(tmpdir_factory):
    """Write some authors to a data file."""
    python_author_data = {
        'Ned': {'City': 'Boston'},
        'Brian': {'City': 'Portland'},
        'Luciano': {'City': 'Sau Paulo'}
    }

    file_ = tmpdir_factory.mktemp('data').join('author_file.json')
    print('file:{}'.format(str(file_)))

    with file.open('w') as f:
        json.dump(python_author_data, f)
    return file
```

The author_file_json() fixture creates a temporary directory called data and creates
a file called author_file.json within the data directory. It then writes the
python_author_data dictionary as json. Because this is a module scope fixture,
the json file will only be created once per module that has a test using it:


```
ch4/authors/test_authors.py

"""Some tests that use temp data files."""
import json


def test_brian_in_portland(author_file_json):
    """A test that uses a data file."""
    with author_file_json.open() as f:
        authors = json.load(f)
    assert authors['Brian']['City'] == 'Portland'


def test_all_have_cities(author_file_json):
    """Same file is used for both tests."""
    with author_file_json.open() as f:
        authors = json.load(f)
    for a in authors:
        assert len(authors[a]['City']) > 0
```

Both tests will use the same json file. If one test data file works for multiple
tests, there’s no use recreating it for both.

### Using pytestconfig

With the pytestconfig builtin fixture, you can control how pytest runs through
command-line arguments and options, configuration files, plugins, and the
directory from which you launched pytest. The pytestconfig fixture is a shortcut
to request.config, and is sometimes referred to in the pytest documentation as
“the pytest config object.”

To see how pytestconfig works, you’ll look at how to add a custom command-
line option and read the option value from within a test. You can read the
value of command-line options directly from pytestconfig, but to add the option
and have pytest parse it, you need to add a hook function. _Hook functions_ ,
which I cover in more detail in Lab 5, Plugins, are another
way to control how pytest behaves and are used frequently in plugins. How-
ever, adding a custom command-line option and reading it from pytestconfig is
common enough that I want to cover it here.

We’ll use the pytest hook pytest_addoption to add a couple of options to the
options already available in the pytest command line:

```
ch4/pytestconfig/conftest.py

def pytest_addoption(parser):
    parser.addoption("--myopt", action="store_true",
                     help="some boolean option")
    parser.addoption("--foo", action="store", default="bar",
                     help="foo: bar or baz")
```

Adding command-line options via pytest_addoption should be done via plugins
or in the conftest.py file at the top of your project directory structure. You
shouldn’t do it in a test subdirectory.

The options --myopt and --foo <value> were added to the previous code, and the
help string was modified, as shown here:


##### Step 2


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/pytestconfig

##### $ pytest --help

```
usage:pytest[options][file_or_dir][file_or_dir][...]
...

customoptions:
--myopt somebooleanoption
--foo=FOO foo:bar or baz
...

```

Now we can access those options from a test:

```
ch4/pytestconfig/test_config.py

import pytest


def test_option(pytestconfig):
    print('"foo" set to:', pytestconfig.getoption('foo'))
    print('"myopt" set to:', pytestconfig.getoption('myopt'))
```

Let’s see how this works:


##### Step 3


##### $ pytest-s -q test_config.py::test_option

```
"foo"set to: bar
"myopt"set to: False
.
1 passed in 0.01seconds
```


##### $ pytest-s -q --myopttest_config.py::test_option

```
"foo"set to: bar
"myopt"set to: True
.
1 passed in 0.01seconds
```


##### $ pytest-s -q --myopt--foobaz test_config.py::test_option

```
"foo"set to: baz
"myopt"set to: True
.
1 passed in 0.01seconds
```

Because pytestconfig is a fixture, it can also be accessed from other fixtures.
You can make fixtures for the option names, if you like, like this:

```
ch4/pytestconfig/test_config.py

@pytest.fixture()
def foo(pytestconfig):
    return pytestconfig.option.foo


@pytest.fixture()
def myopt(pytestconfig):
    return pytestconfig.option.myopt


def test_fixtures_for_options(foo, myopt):
    print('"foo" set to:', foo)
    print('"myopt" set to:', myopt)
```

You can also access builtin options, not just options you add, as well as
information about how pytest was started (the directory, the arguments, and
so on).




Here’s an example of a few configuration values and options:

```
ch4/pytestconfig/test_config.py

def test_pytestconfig(pytestconfig):
    print('args            :', pytestconfig.args)
    print('inifile         :', pytestconfig.inifile)
    print('invocation_dir  :', pytestconfig.invocation_dir)
    print('rootdir         :', pytestconfig.rootdir)
    print('-k EXPRESSION   :', pytestconfig.getoption('keyword'))
    print('-v, --verbose   :', pytestconfig.getoption('verbose'))
    print('-q, --quiet     :', pytestconfig.getoption('quiet'))
    print('-l, --showlocals:', pytestconfig.getoption('showlocals'))
    print('--tb=style      :', pytestconfig.getoption('tbstyle'))
```

You’ll use pytestconfig again when I demonstrate ini files in Lab 6, Config-
uration

### Using cache

Usually we testers like to think about each test as being as independent as
possible from other tests. We want to make sure other dependencies don’t
creep in. We want to be able to run or rerun any test in any order and get the
same result. We also want test sessions to be repeatable and to not change
behavior based on previous test sessions.

However, sometimes passing information from one test session to the next
can be quite useful. When we do want to pass information to future test ses-
sions, we can do it with the cache builtin fixture.

The cache fixture is all about storing information about one test session and
retrieving it in the next. A great example of using the powers of cache for good
is the builtin functionality of --last-failed and --failed-first. Let’s take a look at how
the data for these flags is stored using cache.

Here’s the help text for the --last-failed and --failed-first options, as well as a couple
of cache options:


##### Step 4


##### $ pytest --help

```
...
--lf, --last-failed rerun only the tests that failed at the last run (or
all if none failed)
--ff, --failed-first run all tests but run the last failures first. This
may re-order tests and thus lead to repeated fixture
setup/teardown
--nf, --new-first run tests from new files first, then the rest of the
tests sorted by file mtime
--cache-show show cache contents, don't perform collection or tests
--cache-clear remove all cache contents at start of test run.
...
```


To see these in action, we’ll use these two tests:

```
ch4/cache/test_pass_fail.py

def test_this_passes():
    assert 1 == 1


def test_this_fails():
    assert 1 == 2
```

Let’s run them using --verbose to see the function names, and --tb=no to hide
the stack trace:


##### Step 5


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/cache

##### $ pytest --verbose --tb=no test_pass_fail.py

```
=================== test session starts ===================
collected 2 items

test_pass_fail.py::test_this_passes PASSED            [ 50%]
test_pass_fail.py::test_this_fails FAILED [100%]

=========== 1 failed, 1 passed in 0.06 seconds ============
```

If you run them again with the --ff or --failed-first flag, the tests that failed previ-
ously will be run first, followed by the rest of the session:


##### Step 6


##### $ pytest --verbose --tb=no --fftest_pass_fail.py

```
=================== test session starts ===================
collected 2 items
run-last-failure:rerunprevious1 failurefirst

test_pass_fail.py::test_this_fails FAILED [ 50%]
test_pass_fail.py::test_this_passes PASSED            [100%]

=========== 1 failed, 1 passed in 0.06 seconds ============
```

Or you can use --lf or --last-failed to just run the tests that failed the last time:


##### Step 7

#### venv) $ pytest --verbose --tb=no --lf test_pass_fail.py

```
=================== test session starts ===================
collected 2 items/ 1 deselected
run-last-failure:rerunprevious1 failure

test_pass_fail.py::test_this_fails FAILED [100%]

========= 1 failed, 1 deselected in 0.06 seconds ==========
```

Before we look at how the failure data is being saved and how you can use
the same mechanism, let’s look at another example that makes the value of
--lf and --ff even more obvious.

Here’s a parametrized test with one failure:



```
ch4/cache/test_few_failures.py

"""Demonstrate -lf and -ff with failing tests."""

import pytest
from pytest import approx


testdata = [
    # x, y, expected
    (1.01, 2.01, 3.02),
    (1e25, 1e23, 1.1e25),
    (1.23, 3.21, 4.44),
    (0.1, 0.2, 0.3),
    (1e25, 1e24, 1.1e25)
]


@pytest.mark.parametrize("x,y,expected", testdata)
def test_a(x, y, expected):
    """Demo approx()."""
    sum_ = x + y
    assert sum_ == approx(expected)
```

And the output:


##### Step 8


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/cache

##### $ pytest -q test_few_failures.py

```
.F... [100%]

========================FAILURES=========================
_______________test_a[1e+25-1e+23-1.1e+25]_______________

x = 1e+25,y = 1e+23,expected= 1.1e+25

@pytest.mark.parametrize("x,y,expected",testdata)
def test_a(x,y, expected):
"""Demoapprox()."""
sum_= x + y
> assertsum_== approx(expected)
E assert1.01e+25== 1.1e+25± 1.1e+19
E + where1.1e+25± 1.1e+19= approx(1.1e+25)

test_few_failures.py:21:AssertionError
1 failed, 4 passed in 0.10seconds
```

Maybe you can spot the problem right off the bat. But let’s pretend the test
is longer and more complicated, and it’s not obvious what’s wrong. Let’s run
the test again to see the failure again. You can specify the test case on the
command line:


##### Step 9


##### $ pytest -q "test_few_failures.py::test_a[1e+25-1e+23-1.1e+25]"


If you don’t want to copy/paste or there are multiple failed cases you’d like
to rerun, --lf is much easier. And if you’re really debugging a test failure,
another flag that might make things easier is --showlocals, or -l for short:


##### Step 10


##### $ pytest -q --lf -l test_few_failures.py

```
run-last-failure:rerunprevious1 failure
F [100%]

========================FAILURES=========================
_______________test_a[1e+25-1e+23-1.1e+25]_______________

x = 1e+25,y = 1e+23,expected= 1.1e+25

@pytest.mark.parametrize("x,y,expected",testdata)
def test_a(x,y, expected):
"""Demoapprox()."""
sum_= x + y

> assertsum_== approx(expected)
E assert1.01e+25== 1.1e+25± 1.1e+19
E + where1.1e+25± 1.1e+19= approx(1.1e+25)

expected = 1.1e+25
sum_ = 1.01e+25
x = 1e+25
y = 1e+23

test_few_failures.py:21:AssertionError
1 failed, 4 deselected in 0.06seconds
```

The reason for the failure should be more obvious now.

To pull off the trick of remembering what test failed last time, pytest stores
test failure information from the last test session. You can see the stored
information with --cache-show:


##### Step 11


##### $ pytest --cache-show

```
===================== test session starts ======================
-------------------------cachevalues-------------------------
cache/lastfailedcontains:
{'test_few_failures.py::test_a[1e+25-1e+23-1.1e+25]':True}

================= no tests ran in 0.00 seconds =================
```


##### $ pytest --cache-show

```
=================== test session starts ===================
----------------------cachevalues-----------------------
cache/lastfailedcontains:
{'test_few_failures.py::test_a[1e+25-1e+23-1.1e+25]':True}
...

==============no tests ran in 0.00 seconds ===============
```

Or you can look in the cache dir:


##### Step 12


##### $ cat .pytest_cache/v/cache/lastfailed

```
{
"test_few_failures.py::test_a[1e+25-1e+23-1.1e+25]":true
}
```

You can pass in --cache-clear to clear the cache before the session.



The cache can be used for more than just --lf and --ff. Let’s make a fixture that
records how long tests take, saves the times, and on the next run, reports an
error on tests that take longer than, say, twice as long as last time.

The interface for the cache fixture is simply

```
cache.get(key,default)
cache.set(key,value)
```


Here’s our fixture used to time tests:

```
ch4/cache/test_slower.py

@pytest.fixture(autouse=True)
def check_duration(request, cache):
    key = 'duration/' + request.node.nodeid.replace(':', '_')
    # nodeid's can have colons
    # keys become filenames within .cache
    # replace colons with something filename safe
    start_time = datetime.datetime.now()
    yield
    stop_time = datetime.datetime.now()
    this_duration = (stop_time - start_time).total_seconds()
    last_duration = cache.get(key, None)
    cache.set(key, this_duration)
    if last_duration is not None:
        errorstring = "test duration over 2x last duration"
        assert this_duration <= last_duration * 2, errorstring
```


Now we need some tests that take different amounts of time:

```
ch4/cache/test_slower.py

@pytest.mark.parametrize('i', range(5))
def test_slow_stuff(i):
    time.sleep(random.random())
```

We are using
random and parametrization to easily generate some tests that sleep for a
random amount of time, all shorter than a second. Let’s see it run a couple
of times:


##### Step 13


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/cache

##### $ pytest -q --tb=linetest_slower.py

```
..... [100%]
5 passed in 1.40seconds
```


##### Step 14

##### $ pytest -q --tb=linetest_slower.py

```
..E.E.. [100%]

=========================ERRORS==========================
_________ERRORat teardownof test_slow_stuff[1]_________
E AssertionError:testdurationover2x lastduration
assert0.125103<= (0.009833* 2)
_________ERRORat teardownof test_slow_stuff[2]_________
E AssertionError:testdurationover2x lastduration
assert0.28841<= (0.086302* 2)
5 passed,2 error in 1.77seconds
```

Well, that was fun. Let’s see what’s in the cache:


##### Step 15


##### $ pytest -q --cache-show

```
----------------------cachevalues-----------------------
cache/lastfailedcontains:
{'test_slower.py::test_slow_stuff[1]':True,
'test_slower.py::test_slow_stuff[2]':True}
...

duration/test_slower.py__test_slow_stuff[0]contains:
0.958503
duration/test_slower.py__test_slow_stuff[1]contains:
0.125103
duration/test_slower.py__test_slow_stuff[2]contains:
0.28841
duration/test_slower.py__test_slow_stuff[3]contains:
0.170382
duration/test_slower.py__test_slow_stuff[4]contains:
0.148116

no tests ran in 0.01seconds
```

We are reading and writing to the cache for every test. We could split up the
fixture into a function scope fixture to measure durations and a session scope
fixture to read and write to the cache. However, if we do this, we can’t use
the cache fixture because it has function scope. Fortunately, a quick peek at
the implementation on GitHub reveals that the cache fixture is simply
returning request.config.cache. This is available in any scope.

2. https://github.com/pytest-dev/pytest/blob/master/_pytest/cacheprovider.py



Here’s one possible refactoring of the same functionality:

```
ch4/cache/test_slower_2.py

@pytest.fixture(scope='session')
def duration_cache(request):
    key = 'duration/testdurations'
    d = Duration({}, request.config.cache.get(key, {}))
    yield d
    request.config.cache.set(key, d.current)


@pytest.fixture(autouse=True)
def check_duration(request, duration_cache):
    d = duration_cache
    nodeid = request.node.nodeid
    start_time = datetime.datetime.now()
    yield
    duration = (datetime.datetime.now() - start_time).total_seconds()
    d.current[nodeid] = duration
    if d.last.get(nodeid, None) is not None:
        errorstring = "test duration over 2x last duration"
        assert duration <= (d.last[nodeid] * 2), errorstring
```

The duration_cache fixture is session scope. It reads the previous entry or an empty
dictionary if there is no previous cached data, before any tests are run. In the
previous code, we saved both the retrieved dictionary and an empty one in a
namedtuple called Duration with accessors current and last. We then passed that
namedtuple to the check_duration fixture, which is function scope and runs for every
test function. As the test runs, the same named tuple is passed to each test, and
the times for the current test runs are stored in the d.current dictionary. At the
end of the test session, the collected current dictionary is saved in the cache.

After running it a couple of times, let’s look at the saved cache:


##### Step 16


##### $ pytest -q --cache-cleartest_slower_2.py

```
..... [100%]
5 passed in 2.27seconds
```


##### $ pytest -q --tb=no test_slower_2.py

```
.E.E...E [100%]
5 passed,3 error in 3.65 seconds
```


##### $ pytest -q --cache-show

```
---------------------- cache values -----------------------
cache/lastfailedcontains:
{'test_slower_2.py::test_slow_stuff[0]':True,
'test_slower_2.py::test_slow_stuff[1]':True,
'test_slower_2.py::test_slow_stuff[4]':True}
...

duration/testdurationscontains:
{'test_slower_2.py::test_slow_stuff[0]':0.701514,
```


```
'test_slower_2.py::test_slow_stuff[1]':0.89724,
'test_slower_2.py::test_slow_stuff[2]':0.997875,
'test_slower_2.py::test_slow_stuff[3]':0.271242,
'test_slower_2.py::test_slow_stuff[4]':0.689478}

no tests ran in 0.00seconds
```

That looks better.

### Using capsys

The capsys builtin fixture provides two bits of functionality: it allows you to
retrieve stdout and stderr from some code, and it disables output capture tem-
porarily. Let’s take a look at retrieving stdout and stderr.

Suppose you have a function to print a greeting to stdout:

```
ch4/cap/test_capsys.py

def greeting(name):
    print('Hi, {}'.format(name))
```

You can’t test it by checking the return value. You have to test stdout somehow.
You can test the output by using capsys:

```
ch4/cap/test_capsys.py

def test_greeting(capsys):
    greeting('Earthling')
    out, err = capsys.readouterr()
    assert out == 'Hi, Earthling\n'
    assert err == ''

    greeting('Brian')
    greeting('Nerd')
    out, err = capsys.readouterr()
    assert out == 'Hi, Brian\nHi, Nerd\n'
    assert err == ''
```

The captured stdout and stderr are retrieved from capsys.redouterr(). The return
value is whatever has been captured since the beginning of the function, or
from the last time it was called.

The previous example only used stdout. Let’s look at an example using stderr:

```
ch4/cap/test_capsys.py

def yikes(problem):
    print('YIKES! {}'.format(problem), file=sys.stderr)


def test_yikes(capsys):
    yikes('Out of coffee!')
    out, err = capsys.readouterr()
    assert out == ''
    assert 'Out of coffee!' in err
```


pytest usually captures the output from your tests and the code under test.
This includes print statements. The captured output is displayed for failing
tests only after the full test session is complete. The -s option turns off this
feature, and output is sent to stdout while the tests are running. You can use capsys.disabled() to temporarily let output get past the capture mechanism.

Here’s an example:

```
ch4/cap/test_capsys.py

def test_capsys_disabled(capsys):
    with capsys.disabled():
    print('\nalways print this')
    print('normal print, usually captured')

```

Now, 'always print this' will always be output:


##### Step  17


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/cap

##### $ pytest -q test_capsys.py::test_capsys_disabled

```
alwaysprintthis

. [100%]
1 passed in 0.02seconds
```


##### $ pytest -q -s test_capsys.py::test_capsys_disabled

```

always print this
normal print, usually captured

1 passed in 0.01 seconds
```

As you can see, alwaysprintthis shows up with or without output capturing, since
it’s being printed from within a with capsys.disabled() block. The other print state-
ment is just a normal print statement, so normal print, usuallycaptured is only seen
in the output when we pass in the -s flag, which is a shortcut for --capture=no,
turning off output capture.

### Using monkeypatch

A “monkey patch” is a dynamic modification of a class or module during
runtime. During testing, “monkey patching” is a convenient way to take over
part of the runtime environment of the code under test and replace either
input dependencies or output dependencies with objects or functions that
are more convenient for testing. The monkeypatch builtin fixture allows you to
do this in the context of a single test.

The monkeypatch fixture provides the following functions:

- setattr(target, name,value=`<notset>`,raising=True): Set an attribute.
- delattr(target, name=`<notset>`,raising=True): Delete an attribute.
- setitem(dic,name,value): Set a dictionary entry.
- delitem(dic,name,raising=True): Delete a dictionary entry.
- setenv(name,value,prepend=None): Set an environmental variable.
- delenv(name,raising=True): Delete an environmental variable.
- syspath_prepend(path): Prepend path to sys.path, which is Python’s list of import
    locations.
- chdir(path): Change the current working directory.


To see monkeypatch in action, let’s look at code that writes a dot configuration
file. The behavior of some programs can be changed with preferences and
values set in a dot file in a user’s home directory. Here’s a bit of code that
reads and writes a cheese preferences file:

```
ch4/monkey/cheese.py

import os
import json


def read_cheese_preferences():
    full_path = os.path.expanduser('~/.cheese.json')
    with open(full_path, 'r') as f:
        prefs = json.load(f)
    return prefs


def write_cheese_preferences(prefs):
    full_path = os.path.expanduser('~/.cheese.json')
    with open(full_path, 'w') as f:
        json.dump(prefs, f, indent=4)


def write_default_cheese_preferences():
    write_cheese_preferences(_default_prefs)

_default_prefs = {
    'slicing': ['manchego', 'sharp cheddar'],
    'spreadable': ['Saint Andre', 'camembert',
                   'bucheron', 'goat', 'humbolt fog', 'cambozola'],
    'salads': ['crumbled feta']
}
```

Let’s take a look at how we could test write_default_cheese_preferences(). It’s a
function that takes no parameters and doesn’t return anything. But it does
have a side effect that we can test. It writes a file to the current user’s home
directory.

One approach is to just let it run normally and check the side effect. Suppose
I already have tests for read_cheese_preferences() and I trust them, so I can use
them in the testing of write_default_cheese_preferences():

```
ch4/monkey/test_cheese.py

def test_def_prefs_full():
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual
```

One problem with this is that anyone who runs this test code will overwrite
their own cheese preferences file. That’s not good.

If a user has HOME set, os.path.expanduser() replaces ~ with whatever is in a user’s
HOME environmental variable. Let’s create a temporary directory and redirect
HOME to point to that new temporary directory:

```
ch4/monkey/test_cheese.py

def test_def_prefs_change_home(tmpdir, monkeypatch):
    monkeypatch.setenv('HOME', tmpdir.mkdir('home'))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual
```

Instead of patching the HOME environmental variable, let’s patch expanduser:

```
ch4/monkey/test_cheese.py

def test_def_prefs_change_expanduser(tmpdir, monkeypatch):
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(cheese.os.path, 'expanduser',
                        (lambda x: x.replace('~', str(fake_home_dir))))
    cheese.write_default_cheese_preferences()
    expected = cheese._default_prefs
    actual = cheese.read_cheese_preferences()
    assert expected == actual
```


Let’s say we’re worried about what happens if the file already exists. We want
to be sure it gets overwritten with the defaults when write_default_cheese_prefer-
ences() is called:

```
ch4/monkey/test_cheese.py

def test_def_prefs_change_defaults(tmpdir, monkeypatch):
    # write the file once
    fake_home_dir = tmpdir.mkdir('home')
    monkeypatch.setattr(cheese.os.path, 'expanduser',
                        (lambda x: x.replace('~', str(fake_home_dir))))
    cheese.write_default_cheese_preferences()
    defaults_before = copy.deepcopy(cheese._default_prefs)

    # change the defaults
    monkeypatch.setitem(cheese._default_prefs, 'slicing', ['provolone'])
    monkeypatch.setitem(cheese._default_prefs, 'spreadable', ['brie'])
    monkeypatch.setitem(cheese._default_prefs, 'salads', ['pepper jack'])
    defaults_modified = cheese._default_prefs

    # write it again with modified defaults
    cheese.write_default_cheese_preferences()

    # read, and check
    actual = cheese.read_cheese_preferences()
    assert defaults_modified == actual
    assert defaults_modified != defaults_before
```

Because _default_prefs is a dictionary, we can use monkeypatch.setitem() to change
dictionary items just for the duration of the test.

We’ve used setenv(), setattr(), and setitem(). The del forms are pretty similar. They
just delete an environmental variable, attribute, or dictionary item instead of
setting something.
You can also use the monkeypatch fixture functions in conjunction with
unittest.mock to temporarily replace attributes with mock objects.

### Using doctest_namespace

Let’s play with an example. Let’s say we have a module named unneces-
sary_math.py with multiply() and divide() methods that we really want to make sure
everyone understands clearly. So we throw some usage examples in both the
file docstring and the docstrings of the functions:

```
ch4/dt/1/unnecessary_math.py

"""
This module defines multiply(a, b) and divide(a, b).

>>> import unnecessary_math as um

Here's how you use multiply:

>>> um.multiply(4, 3)
12
>>> um.multiply('a', 3)
'aaa'


Here's how you use divide:

>>> um.divide(10, 5)
2.0
"""


def multiply(a, b):
    """
    Returns a multiplied by b.

    >>> um.multiply(4, 3)
    12
    >>> um.multiply('a', 3)
    'aaa'
    """
    return a * b


def divide(a, b):
    """
    Returns a divided by b.

    >>> um.divide(10, 5)
    2.0
    """
    return a / b
```

Since the name unnecessary_math is long, we decide to use um instead by using
import unnecessary_math as um in the top docstring. The code in the docstrings of
the functions doesn’t include the import statement, but continue with the um
convention.


##### Step 18


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/dt/1

##### $ pytest -v --doctest-modules--tb=shortunnecessary_math.py

```
=================== test session starts ===================
collected 3 items

unnecessary_math.py::unnecessary_math PASSED            [ 33%]
unnecessary_math.py::unnecessary_math.divide FAILED[ 66%]
unnecessary_math.py::unnecessary_math.multiply FAILED[100%]

========================FAILURES=========================
____________[doctest]unnecessary_math.divide ____________
034
035 Returnsa dividedby b.
036
037 >>> um.divide(10,5)
UNEXPECTEDEXCEPTION:NameError("name'um'is not defined")
Traceback(mostrecentcalllast):
...

File"<doctestunnecessary_math.divide[0]>", line1, in <module>

NameError:name'um'is not defined

/pytest-labs/testing-with-pytest/code/ch4/dt/1/unnecessary_math.py:37:UnexpectedException

___________[doctest]unnecessary_math.multiply___________
022
023 Returnsa multipliedby b.
024
025 >>> um.multiply(4,3)
UNEXPECTEDEXCEPTION:NameError("name'um'is not defined")
Traceback(mostrecentcalllast):
...

File"<doctestunnecessary_math.multiply[0]>",line1, in <module>

NameError:name'um'is not defined

/pytest-labs/testing-with-pytest/code/ch4/dt/1/unnecessary_math.py:25:UnexpectedException

=========== 2 failed, 1 passed in 0.12 seconds ============
```


One way to fix it is to put the import statement in each docstring:

```
ch4/dt/2/unnecessary_math.py

def multiply(a, b):
    """
    Returns a multiplied by b.

    >>> import unnecessary_math as um
    >>> um.multiply(4, 3)
    12
    >>> um.multiply('a', 3)
    'aaa'
    """
    return a * b


def divide(a, b):
    """
    Returns a divided by b.

    >>> import unnecessary_math as um
    >>> um.divide(10, 5)
    2.0
    """
    return a / b
```

This definitely fixes the problem:


##### Step 19


##### $ cd /pytest-labs/testing-with-pytest/code/ch4/dt/2

##### $ pytest -v --doctest-modules--tb=shortunnecessary_math.py

```
=================== test session starts ===================
collected 3 items

unnecessary_math.py::unnecessary_math PASSED            [ 33%]
unnecessary_math.py::unnecessary_math.dividePASSED[ 66%]
unnecessary_math.py::unnecessary_math.multiplyPASSED[100%]

================ 3 passed in 0.03 seconds =================
```



However, it also clutters the docstrings, and doesn’t add any real value to
readers of the code.
The builtin fixture doctest_namespace, used in an autouse fixture at a top-level
conftest.py file, will fix the problem without changing the source code:

```
ch4/dt/3/conftest.py

import pytest
import unnecessary_math


@pytest.fixture(autouse=True)
def add_um(doctest_namespace):
    doctest_namespace['um'] = unnecessary_math
```

This tells pytest to add the um name to the doctest_namespace and have it
be the value of the imported unnecessary_math module. With this in place in the
conftest.py file, any doctests found within the scope of this conftest.py file will
have the um symbol defined.

### Using recwarn

The recwarn builtin fixture is used to examine warnings generated by code
under test. In Python, you can add warnings that work a lot like assertions,
but are used for things that don’t need to stop execution. For example, suppose
we want to stop supporting a function that we wish we had never put into a
package but was released for others to use. We can put a warning in the code
and leave it there for a release or two:

```
ch4/test_warnings.py

import warnings
import pytest


def lame_function():
    warnings.warn("Please stop using this", DeprecationWarning)
    # rest of function
```

We can make sure the warning is getting issued correctly with a test:

```
ch4/test_warnings.py

def test_lame_function(recwarn):
    lame_function()
    assert len(recwarn) == 1
    w = recwarn.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'
```


The recwarn value acts like a list of warnings, and each warning in the list has
a category, message, filename, and lineno defined, as shown in the code.

In addition to recwarn, pytest can check for warnings with pytest.warns():

```
ch4/test_warnings.py

def test_lame_function_2():
    with pytest.warns(None) as warning_list:
        lame_function()

    assert len(warning_list) == 1
    w = warning_list.pop()
    assert w.category == DeprecationWarning
    assert str(w.message) == 'Please stop using this'
```

The pytest.warns() context manager provides an elegant way to demark what
portion of the code you’re checking warnings. The recwarn fixture and the
pytest.warns() context manager provide similar functionality, though, so the
decision of which to use is purely a matter of taste.

### Exercises

1. In ch4/cache/test_slower.py, there is an autouse fixture called check_duration(). Copy
it into ch3/tasks_proj/tests/conftest.py.
2. Run the tests in Lab 3.
3. For tests that are really fast, 2x really fast is still really fast. Instead of
2x, change the fixture to check for 0.1 second plus 2x the last duration.
4. Run pytest with the modified fixture. Do the results seem reasonable?

### What’s Next

In this lab, you looked at many of pytest’s builtin fixtures. Next, you’ll
take a closer look at plugins. Small custom plugins are a regular part of the pytest
ecosystem.
