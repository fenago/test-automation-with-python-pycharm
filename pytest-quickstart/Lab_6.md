
<img align="right" src="../logo.png">


Lab 6. Converting unittest suites to pytest
--------------------------------------------------------



In the previous lab, we have seen how the flexible pytest
architecture has created a rich plugin ecosystem, with hundreds of
plugins available. We learned how easy it is to find and install
plugins, and had an overview of a number of interesting plugins.

Now that you are proficient with pytest, you might be in a situation
where you have one or more `unittest`-based test suites and
want to start using pytest with them. In this lab, we will discuss
the best approaches to start doing just that, ranging from simple test
suites that might require little to no modification, to large
in-house-grown test suites that contain all kinds of customizations
grown organically over the years. Most of the tips and advice in this
lab come from my own experience when migrating our[]{#id324673405
.indexterm} massive `unittest`-style test suite at ESSS
([https://wwww.esss.co](https://www.esss.co/)), where I work.

Here is what we will cover in this lab:


-   Using pytest as a test runner
-   Converting asserts with `unittest2pytest`
-   Handling setup and teardown
-   Managing test hierarchies
-   Refactoring test utilities
-   Migration strategy



#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `/pytest-labs/pytest-quickstart/code` folder.


Using pytest as a test runner 
-----------------------------------------------



One thing that surprisingly many people don\'t know[]{#id324673415
.indexterm} is that pytest can run `unittest` suites out of
the box, without any modifications.

For example:


``` {.programlisting .language-markup}
class Test(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.filepath = cls.temp_dir / "data.csv"
        cls.filepath.write_text(DATA.strip())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        self.grids = list(iter_grids_from_csv(self.filepath))

    def test_read_properties(self):
        self.assertEqual(self.grids[0], GridData("Main Grid", 48, 44))
        self.assertEqual(self.grids[1], GridData("2nd Grid", 24, 21))
        self.assertEqual(self.grids[2], GridData("3rd Grid", 24, 48))

    def test_invalid_path(self):
        with self.assertRaises(IOError):
            list(iter_grids_from_csv(Path("invalid file")))

    @unittest.expectedFailure
    def test_write_properties(self):
        self.fail("not implemented yet")
```


We can run this using the `unittest` runner:


``` {.programlisting .language-markup}
..x
----------------------------------------------------------------------
Ran 3 tests in 0.005s

OK (expected failures=1)
```


But the cool thing is that pytest also runs this test without any
modifications:


``` {.programlisting .language-markup}
pytest test_simple.py

======================== test session starts ========================
...
collected 3 items

test_simple.py ..x                                             [100%]

================ 2 passed, 1 xfailed in 0.11 seconds ================
```


This makes it really easy to just start using pytest as a test runner,
which brings several benefits:


-   You can use plugins---for example, `pytest-xdist`, to
    speed up the test suite.
-   You have several command-line options at your
    disposal: `-k` for selecting tests, `--pdb` to
    jump into the debugger on errors, `--lf` to run last
    failed tests only, and so on.
-   You can stop writing `self.assert*` methods and go with
    plain `assert`s. pytest will happily provide rich failure
    information, even for `unittest`-based subclasses.


For completeness, here are the `unittest` idioms and features
supported out of the box:


-   `setUp` and `tearDown` for function-level
    `setup`/`teardown`
-   `setUpClass` and `tearDownClass` for class-level
    `setup`/`teardown`
-   `setUpModule` and `tearDownModule` for
    module-level `setup`/`teardown`
-   `skip`, `skipIf`, `skipUnless`,
    and `expectedFailure` decorators, for functions and
    classes
-   `TestCase.skipTest` to imperatively skip inside tests


The following idioms are currently not supported:


-   `load_tests protocol`: This protocol allows users to
    completely customize which tests are loaded from a module
    (<https://docs.python.org/3/library/unittest.html#load-tests-protocol>).
    The collection concept used by pytest is not compatible with how
    `load_tests` protocol works, so no work is planned by the
    pytest core team to support this feature (see
    the `#992` (<https://github.com/pytest-dev/pytest/issues/992>)
    issue if you are interested in the details).
-   `subtests`: Tests using this feature can report multiple
    failures inside the same test method
    (<https://docs.python.org/3/library/unittest.html#distinguishing-test-iterations-using-subtests>).
    This feature is similar to pytest\'s own parametrization support,
    with the difference that the test results can be determined at
    runtime instead of collection time. In theory, this can be supported
    by pytest, and the feature is currently
    being tracked by issue
    `#1367` (<https://github.com/pytest-dev/pytest/issues/1367>).



### Note

[**Surprises with**]`pytest-xdist` If you decide to
use `pytest-xdist` in your test suite, be aware that it runs
tests in an arbitrary order: each worker will run tests as they finish
other tests, so the order the in which the tests are executed is not
predictable. Because the default `unittest` runner runs tests
sequentially and always in the same order, often this will bring to
light concurrency problems to your test suite---for example, tests
trying to create a temporary directory with the same name. You should
see this as an opportunity to fix the underlying concurrency problems,
as they should not be part of the test suite anyway.

### Pytest features in unittest subclasses



Although not designed to support all its
features when running `unittest`-based tests, a few of the
pytest idioms are supported:


-   [**Plain asserts**]: pytest assertion introspect works just
    as well when subclassing `unittest.TestCase`
-   [**Marks**]: marks can be applied normally to
    `unittest` test methods and classes. Plugins that deal
    with marks should work normally in most cases (for
    example, `pytest-timeout` marks)
-   [**Autouse**] fixtures: autouse fixtures defined in modules
    or `conftest.py` files will be created/destroyed when
    executing `unittest` test methods normally,
    including  `unittest` subclasses in the case of
    class-scoped autouse fixtures
-   [**Test selection**]: `-k` and `-m` in
    the command line should work as normal


Other pytest features do not work with `unittest`, especially:


-   [**Fixtures**]: `unittest` test methods cannot
    request fixtures. Pytest uses `unittest`\'s own result
    collector to execute the tests, which doesn\'t support passing
    arguments to test functions
-   [**Parametrization**]: this is not supported, for similar
    reasons as for fixtures: we need to pass the parametrized values,
    and this is not currently possible


Plugins that don\'t rely on fixtures may work normally, for
example `pytest-timeout`or `pytest-randomly`.



Converting asserts with unitest2pytest 
--------------------------------------------------------



Once you have changed the test runner to
pytest, you can take advantage of writing
plain assert statements instead of `self.assert*` methods.

Converting all the method calls is boring and error-prone, that\'s why
the
[`unittest2pytest`](https://github.com/pytest-dev/unittest2pytest) tool
exists. It converts all `self.assert*` method calls to plain
asserts, and also converts `self.assertRaises` calls to the
appropriate pytest idiom.

Install it using `pip`:


``` {.programlisting .language-markup}
pip install unittest2pytest
```


Once installed, you can now execute it on the files you want:


``` {.programlisting .language-markup}
unittest2pytest test_simple2.py
RefactoringTool: Refactored test_simple2.py
--- test_simple2.py (original)
+++ test_simple2.py (refactored)
@@ -5,6 +5,7 @@
 import unittest
 from collections import namedtuple
 from pathlib import Path
+import pytest

 DATA = """
 Main Grid,48,44
@@ -49,12 +50,12 @@
         self.grids = list(iter_grids_from_csv(self.filepath))

     def test_read_properties(self):
-        self.assertEqual(self.grids[0], GridData("Main Grid", 48, 44))
-        self.assertEqual(self.grids[1], GridData("2nd Grid", 24, 21))
-        self.assertEqual(self.grids[2], GridData("3rd Grid", 24, 48))
+        assert self.grids[0] == GridData("Main Grid", 48, 44)
+        assert self.grids[1] == GridData("2nd Grid", 24, 21)
+        assert self.grids[2] == GridData("3rd Grid", 24, 48)

     def test_invalid_path(self):
-        with self.assertRaises(IOError):
+        with pytest.raises(IOError):
             list(iter_grids_from_csv(Path("invalid file")))

     @unittest.expectedFailure
RefactoringTool: Files that need to be modified:
RefactoringTool: test_simple2.py
```


By default, it won\'t touch the files and will only show the difference
in the changes it could apply. To actually apply the changes, pass
`-wn` (`--write` and `--nobackups`).

Note that in the previous example, it correctly replaced the
`self.assert*` calls, `self.assertRaises`, and added
the `pytest` import. It did not change the subclass of our
test class, as this could have other consequences, depending on the
actual subclass you are using, so `unittest2pytest` leaves
that alone.

The updated file runs just as before:


``` {.programlisting .language-markup}
pytest test_simple2.py

======================== test session starts ========================
...
collected 3 items

test_simple2.py ..x                                            [100%]

================ 2 passed, 1 xfailed in 0.10 seconds ================
```


Adopting pytest as a runner and being able to use plain assert
statements is a great win that is often underestimated: it is liberating
to not have to type `self.assert...` all the time any more. 


### Note

At the time of writing, `unittest2pytest` doesn\'t handle the
`self.fail("not implemented yet")` statement of the last test
yet. So, we need to replace it manually with
`assert 0, "not implemented yet"`. Perhaps you would like
to submit a PR to improve the project?
(<https://github.com/pytest-dev/unittest2pytest>).



Handling setup/teardown 
-----------------------------------------



To fully convert a `TestCase` subclass to pytest style, we
need to replace `unittest` with pytest\'s idioms. We have
already seen how to do that with `self.assert*` methods in the
previous section, by using `unittest2pytest`. But what can we
do do about `setUp` and `tearDown` methods?

As we learned previously, autouse fixtures
work just fine in `TestCase`
subclasses, so they are a natural way to replace `setUp` and
`tearDown` methods. Let\'s use the example from the previous
section.

 

After converting the `assert` statements, the first thing to
do is to remove the `unittest.TestCase` subclassing:


``` {.programlisting .language-markup}
class Test(unittest.TestCase):
    ...
```


This becomes the following:


``` {.programlisting .language-markup}
class Test:
    ...
```


Next, we need to transform the `setup`/`teardown`
methods into fixture equivalents:


``` {.programlisting .language-markup}
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.filepath = cls.temp_dir / "data.csv"
        cls.filepath.write_text(DATA.strip())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
```


So, the class-scoped `setUpClass` and
`tearDownClass` methods will become a single class-scoped
fixture:


``` {.programlisting .language-markup}
    @classmethod
@pytest.fixture(scope='class', autouse=True)
    def _setup_class(cls):
        temp_dir = Path(tempfile.mkdtemp())
        cls.filepath = temp_dir / "data.csv"
        cls.filepath.write_text(DATA.strip())
yield
        shutil.rmtree(temp_dir)
```


Thanks to the `yield` statement, we can easily write the
teardown code in the fixture itself, as we\'ve already learned.

Here are some observations:


-   Pytest doesn\'t care what we call our fixture, so we could just as
    well keep the old `setUpClass` name. We chose to change it
    to `setup_class` instead, with two objectives: avoid
    confusing readers of this code, because it might seem that it is
    still a `TestCase` subclass, and using a
    `_` prefix denotes that this fixture should not be used as
    a normal pytest fixture.



-   We change `temp_dir` to a local variable because we don\'t
    need to keep it around in `cls` any more. Previously, we
    had to do that because we needed to access `cls.temp_dir`
    during `tearDownClass`, but now we can keep it as a local
    variable instead and access it after the `yield`
    statement. That\'s one of the beautiful things about using
    `yield` to separate setup and teardown code: you don\'t
    need to keep context variables around; they are kept naturally as
    the local variables of the function.


We follow the same approach with the `setUp` method:


``` {.programlisting .language-markup}
    def setUp(self):
        self.grids = list(iter_grids_from_csv(self.filepath))
```


This becomes the following:


``` {.programlisting .language-markup}
@pytest.fixture(autouse=True)
    def _setup(self):
        self.grids = list(iter_grids_from_csv(self.filepath))
```


This technique is very useful because you can get a pure pytest class
from a minimal set of changes. Also, using a naming
convention for fixtures, as we
did previously, helps to convey to readers
that the fixtures are converting the old
`setup`/`teardown` idioms.

Now that this class is a proper pytest class, you are free to use
fixtures and parametrization.



Managing test hierarchies 
-------------------------------------------



As we have seen, it is commonto need to share
functionality in large test suites. Because `unittest` is
based on subclassing `TestCase`, it is common to put extra
functionality in your `TestCase` subclass itself. For example,
if we need to test application logic that requires a database, we might
initially add functionality to the start and connect to a database in
our `TestCase` subclass directly:


``` {.programlisting .language-markup}
class Test(unittest.TestCase):

    def setUp(self):
        self.db_file = self.create_temporary_db()
        self.session = self.connect_db(self.db_file)

    def tearDown(self):
        self.session.close()
        os.remove(self.db_file)

    def create_temporary_db(self):
        ...

    def connect_db(self, db_file):
        ...

    def create_table(self, table_name, **fields):
        ...

    def check_row(self, table_name, **query):
        ...

    def test1(self):
        self.create_table("weapons", name=str, type=str, dmg=int)
        ...
```


This works well for a single test module, but often it is the case that
we need this functionality in another test module sometime later. The
`unittest` module does not contain built-in provisions to
share common `setup`/`teardown` code, so what comes
naturally for most people is to extract the required functionality in a
superclass, and then a subclass from that, where needed:


``` {.programlisting .language-markup}
# content of testing.py
class DataBaseTesting(unittest.TestCase):

    def setUp(self):
        self.db_file = self.create_temporary_db()
        self.session = self.connect_db(self.db_file)

    def tearDown(self):
        self.session.close()
        os.remove(self.db_file)

    def create_temporary_db(self):
        ...

    def connect_db(self, db_file):
        ...

    def create_table(self, table_name, **fields):
        ...

    def check_row(self, table_name, **query):
        ...

# content of test_database2.py
from . import testing

class Test(testing.DataBaseTesting):

    def test1(self):
        self.create_table("weapons", name=str, type=str, dmg=int)
        ...
```


The superclass usually not only contains
`setup`/`teardown` code, but it often also includes
utility functions that call `self.assert*` to perform common
checks (such as `check_row` in the previous example).

Continuing with our example: some time later, we need completely
different functionality in another test module, for example, to test a
GUI application. We are now wiser and suspect we will need GUI-related
functionality in several other test modules, so we start by creating a
superclass with the functionality we need directly:


``` {.programlisting .language-markup}
class GUITesting(unittest.TestCase):

    def setUp(self):
        self.app = self.create_app()

    def tearDown(self):
        self.app.close_all_windows()

    def mouse_click(self, window, button):
        ...

    def enter_text(self, window, text):
        ...
```


The approach of moving `setup`/`teardown` and test
functionality to superclasses works `OK` and is easy to
understand.

The problem comes when we get to the point where we need two unrelated
functionalities in the same test module. In that case, we have no other
choice than to resort to multiple inheritance. Suppose we need to test a
dialog that connects to the database; we will need to write code such as
this:


``` {.programlisting .language-markup}
from . import testing

class Test(testing.DataBaseTesting, testing.GUITesting):

    def setUp(self):
        testing.DataBaseTesting.setUp(self)
        testing.GUITesting.setUp(self)

    def tearDown(self):
        testing.GUITesting.setUp(self)
        testing.DataBaseTesting.setUp(self)
```


Multiple inheritance in general tends to make
the code less readable and harder to follow. Here, it also has the
additional aggravation that we need to call `setUp` and
`tearDown` in the correct order, explicitly. 

Another point to be aware of is that `setUp` and
`tearDown` are optional in the `unittest` framework,
so it is common for a certain class to not declare a
`tearDown` method at all if it doesn\'t need any teardown
code. If this class contains functionality that is later moved to a
superclass, many subclasses probably will not declare a
`tearDown` method as well. The problem comes when, later on in
a multiple inheritance scenario, you improve the super class and need to
add a `tearDown` method, because you will now have to go over
all subclasses and ensure that they call the `tearDown` method
of the super class.

So, let\'s say we find ourselves in the previous situation and we want
to start to use pytest functionality that is incompatible with
`TestCase` tests. How can we refactor our utility classes so
we can use them naturally from pytest and also keep existing
`unittest`-based tests working?


### Reusing test code with fixtures



The first thing we should do is to extract
the desired functionality into well-defined
fixtures and put them into a `conftest.py` file. Continuing
with our example, we can create `db_testing` and
`gui_testing` fixtures:


``` {.programlisting .language-markup}
class DataBaseFixture:

    def __init__(self):
        self.db_file = self.create_temporary_db()
        self.session = self.connect_db(self.db_file)

    def teardown(self):
        self.session.close()
        os.remove(self.db_file)

    def create_temporary_db(self):
        ...

    def connect_db(self, db_file):
        ...

    ...

@pytest.fixture
def db_testing():
    fixture = DataBaseFixture()
    yield fixture
    fixture.teardown()


class GUIFixture:

    def __init__(self):
        self.app = self.create_app()

    def teardown(self):
        self.app.close_all_windows()

    def mouse_click(self, window, button):
        ...

    def enter_text(self, window, text):
        ...


@pytest.fixture
def gui_testing():
    fixture = GUIFixture()
    yield fixture
    fixture.teardown()
```


Now, you can start to write new tests using plain pytest style and use
the `db_testing` and `gui_testing` fixtures, which
is great because it opens the door to use pytest features in new tests.
But the cool thing here is that we can now change
`DataBaseTesting` and `GUITesting` to reuse the
functionality provided by the fixtures, in a way that we don\'t break
existing code:


``` {.programlisting .language-markup}
class DataBaseTesting(unittest.TestCase):

@pytest.fixture(autouse=True)
def _setup(self, db_testing):
        self._db_testing = db_testing

    def create_temporary_db(self):
        return self._db_testing.create_temporary_db()

    def connect_db(self, db_file):
        return self._db_testing.connect_db(db_file)

    ...


class GUITesting(unittest.TestCase):

@pytest.fixture(autouse=True)
    def _setup(self, gui_testing):
        self._gui_testing = gui_testing

    def mouse_click(self, window, button):
        return self._gui_testing.mouse_click(window, button)

    ...
```


Our `DatabaseTesting` and `GUITesting` classes
obtain the fixture values by declaring an autouse `_setup`
fixture, a trick we have learned early in
this lab. We can get rid of the
`tearDown` method because the fixture will take care of
cleaning up after itself after each test, and the utility methods become
simple proxies for the methods implemented in the fixture.

As bonus points, `GUIFixture` and `DataBaseFixture`
can also use other pytest fixtures. For example, we can probably remove
`DataBaseTesting.create_temporary_db()` and use the built-in
`tmpdir` fixture to create the temporary database file for us:


``` {.programlisting .language-markup}
class DataBaseFixture:

    def __init__(self, tmpdir):
        self.db_file = str(tmpdir / "file.db")
        self.session = self.connect_db(self.db_file)

    def teardown(self):
        self.session.close()

    ...

@pytest.fixture
def db_testing(tmpdir):
    fixture = DataBaseFixture(tmpdir)
    yield fixture
    fixture.teardown()
```


Using other fixtures can then greatly simplify the existing testing
utilities code.

It is worth emphasizing that this refactoring will require zero
changes to the existing tests. Here, again, one of the benefits of
fixtures becomes evident: changes in requirements of a fixture do not
affect tests that use the fixture.



Refactoring test utilities 
--------------------------------------------



In the previous section, we saw how test
suites might make use of subclasses to share test functionality and how
to refactor them into fixtures while keeping existing tests working.

An alternative to sharing test functionality through superclasses in
`unittest` suites is to write separate utility classes and use
them inside the tests. Getting back to our example, where we need to
have database-related facilities, here is a way to implement that in a
`unittest`-friendly way, without using superclasses:


``` {.programlisting .language-markup}
# content of testing.py
class DataBaseTesting:

    def __init__(self, test_case):        
        self.db_file = self.create_temporary_db()
        self.session = self.connect_db(self.db_file)
self.test_case = test_case
test_case.addCleanup(self.teardown)

    def teardown(self):
        self.session.close()
        os.remove(self.db_file)

    ...

    def check_row(self, table_name, **query):
        row = self.session.find(table_name, **query)
self.test_case.assertIsNotNone(row)
        ...

# content of test_1.py
from testing import DataBaseTesting

class Test(unittest.TestCase):

    def test_1(self):
        db_testing = DataBaseTesting(self)
        db_testing.create_table("weapons", name=str, type=str, dmg=int)
        db_testing.check_row("weapons", name="zweihander")
        ...
```


In this approach, we separate our testing functionality in a class that
receives the current `TestCase` instance as its first
argument, followed by any other arguments, as required.

The `TestCase` instance serves two purposes: to provide the
class access to the various `self.assert*` functions, and as a
way to register clean-up functions with
`TestCase.addCleanup` (<https://docs.python.org/3/library/unittest.html#unittest.TestCase.addCleanup>).
`TestCase.addCleanup` registers functions that will be called
after each test is done, regardless of whether they have been
successful. I consider them a superior alternative to the
`setUp`/`tearDown` functions because they allow
resources to be created and immediately registered for cleaning up.
Creating all resources during `setUp` and releasing them
during `tearDown` has the disadvantage that if any exception
is raised during the `setUp` method, then `tearDown`
will not be called at all, leaking resources and state, which might
affect the tests that follow.

If your `unittest` suite uses this approach for testing
facilities, then the good news is that you are in for an easy ride to
convert/reuse this functionality for pytest.

Because this approach is very similar to how fixtures work, it is simple
to change the classes slightly to work as fixtures:


``` {.programlisting .language-markup}
# content of testing.py
class DataBaseFixture:

    def __init__(self):
        self.db_file = self.create_temporary_db()
        self.session = self.connect_db(self.db_file)

    ...

    def check_row(self, table_name, **query):
        row = self.session.find(table_name, **query)
assert row is not None

# content of conftest.py
@pytest.fixture
def db_testing():
    from .testing import DataBaseFixture
    result = DataBaseFixture()
    yield result
    result.teardown()
```


We get rid of the dependency to the `TestCase` instance
because our fixture now takes care of calling `teardown()`,
and we are free to use plain asserts instead of `Test.assert*`
methods.

To keep the existing suite working, we just need to make a thin subclass
to handle cleanup when it is used with `TestCase` subclasses:


``` {.programlisting .language-markup}
# content of testing.py
class DataBaseTesting(DataBaseFixture):

    def __init__(self, test_case):
        super().__init__()
test_case.addCleanup(self.teardown)
```


With this small refactoring, we can now use native pytest fixtures in
new tests, while keeping the existing tests working exactly as before.

While this approach works well, one problem
is that unfortunately, we cannot use other pytest fixtures (such
as `tmpdir`) in our `DataBaseFixture` class without
breaking compatibility with `DataBaseTesting` usage in
`TestCase` subclasses.



Migration strategy 
------------------------------------



Being able to run `unittest`-based tests out[]{#id325091700
.indexterm} of the box is definitely a very powerful feature, because it
allows you to start using pytest right away as a runner.

Eventually, you need to decide what to do with the existing
`unittest`-based tests. There are a few approaches you can
choose:


-   [**Convert everything**]: if your test suite is relatively
    small, you might decide to convert all tests at once. This has the
    advantage that you don\'t have to make compromises to keep existing
    `unittest` suites working, and being simpler to be
    reviewed by others because your pull request will have a single
    theme.
-   [**Convert as you go**]: you might decide to convert tests
    and functionality as needed. When you need to add new tests or
    change existing tests, you take the opportunity to convert tests
    and/or refactor functionality to fixtures using the techniques from
    the previous sections. This is a good approach if you don\'t want to
    spend time upfront converting everything, while slowly but surely
    paving the way to have a pytest-only test suite.
-   [**New tests only**]: you might decide to never touch the
    existing `unittest` suite, only writing new tests in
    pytest-style. This approach is reasonable if you have thousands of
    tests that might never need to undergo maintenance, but you will
    have to keep the hybrid approaches shown in the previous sections
    working indefinitely.



### Note

Choose which migration strategy to use based on the time budget you have
and the test suite\'s size. 



Summary 
-------------------------



We have discussed a few strategies and tips on how to use pytest in
`unittest`-based suites of various sizes. We started with a
discussion about using pytest as a test runner, and which features work
with `TestCase` tests. We looked at how to use
the `unittest2pytest` tool to convert `self.assert*`
methods to plain assert statements and take full advantage of pytest
introspection features. Then, we learned a few techniques on how to
migrate `unittest`-based
`setUp`/`tearDown` code to pytest-style in test
classes, manage functionality spread in test hierarchies, and general
utilities. Finally, we wrapped up the lab with an overview of the
possible migration strategies that you can take for test suites of
various sizes.

In the next lab, we will see a quick summary of what we have learned
in this course, and discuss what else might be in store for us.
