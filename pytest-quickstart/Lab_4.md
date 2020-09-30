<img align="right" src="../logo.png">


Lab 4. Fixtures
----------------------------


In the previous lab, we learned how to use marks and parametrization
effectively to skip tests, mark them as expected to fail, and
parameterize them, to avoid repetition.

Tests in the real world often need to create resources or data to work
on: a temporary directory to output some files to, a database connection
to test the I/O layer of an application, a web server for integration
testing. Those are all examples of resources that are required in more
complex testing scenarios. More complex resources often need to be
cleaned up at the end of the test session: removing a temporary
directory, cleaning up and disconnecting from a database, shutting down
a web server. Also, these resources should be easily shared across
tests, because during testing we often need to reuse a resource for
different test scenarios. Some resources are costly to create, but
because they are immutable or can be restored to a pristine state, they
should be created only once and shared with all the tests that require
it, only being destroyed when the last test that needs them finishes. 

All of the previous requirements and more are covered by one of the most
important of pytest\'s features: [**fixtures**].

Here\'s what we will cover in this lab:


-   Introducing fixtures
-   Sharing fixtures with `conftest.py` files
-   Scopes
-   Autouse
-   Parametrization
-   Using marks from fixtures
-   An overview of built-in fixtures
-   Tips/discussion


#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `/pytest-labs/pytest-quickstart/code` folder.


Introducing fixtures 
--------------------------------------



Most tests need some kind of data or resource
to operate on:


``` {.programlisting .language-markup}
def test_highest_rated():
    series = [
        ("The Office", 2005, 8.8),
        ("Scrubs", 2001, 8.4),
        ("IT Crowd", 2006, 8.5),
        ("Parks and Recreation", 2009, 8.6),
        ("Seinfeld", 1989, 8.9),
    ]
    assert highest_rated(series) == "Seinfeld"
```


Here, we have a list of (`series name`, `year`,
`rating`) tuples that we use to test the
`highest_rated` function. Inlining data into the test code as
we do here works well for isolated tests, but often you have a dataset
that can be used by multiple tests. One solution would be to copy over
the dataset to each test:


``` {.programlisting .language-markup}
def test_highest_rated():
    series = [
        ("The Office", 2005, 8.8),
        ...,
    ]
    assert highest_rated(series) == "Seinfeld"

def test_oldest():
    series = [
        ("The Office", 2005, 8.8),
        ...,
    ]
    assert oldest(series) == "Seinfeld"
```


But this gets old quickly---plus, copying  and pasting things around
will hurt maintainability in the long run, for example, if the data
layout changes (adding a new item to the tuple or the cast size, for
example).


### Enter fixtures



Pytest\'s solution to this problem is
fixtures. Fixtures are used to provide resources that test the functions
and methods we need to execute.

 

They are created using normal Python functions and the
`@pytest.fixture` decorator:


``` {.programlisting .language-markup}
@pytest.fixture
def comedy_series():
    return [
        ("The Office", 2005, 8.8),
        ("Scrubs", 2001, 8.4),
        ("IT Crowd", 2006, 8.5),
        ("Parks and Recreation", 2009, 8.6),
        ("Seinfeld", 1989, 8.9),
    ]
```


Here, we are creating a fixture named `comedy_series`, which
returns the same list we were using in the previous section.

Tests can access fixtures by declaring the fixture name in their
parameter list. The test function then receives the return value of the
fixture function as a parameter. Here is the
`comedy_series` fixture in action:


``` {.programlisting .language-markup}
def test_highest_rated(comedy_series):
    assert highest_rated(comedy_series) == "Seinfeld"

def test_oldest(comedy_series):
    assert oldest(comedy_series) == "Seinfeld"
```


Here\'s how things work:


-   Pytest looks at the test function parameters before calling it.
    Here, we have one parameter: `comedy_series`.
-   For each parameter, pytest gets the fixture function of same name
    and executes it.
-   The return value of each fixture function becomes a named parameter,
    and the test function is called.


Note that `test_highest_rated` and `test_oldest`
each get their own copy of the comedy series list, so they don\'t risk
interfering with each other if they change the list inside the test.

It is also possible to create fixtures in classes using methods:


``` {.programlisting .language-markup}
class Test:

    @pytest.fixture
    def drama_series(self):
        return [
            ("The Mentalist", 2008, 8.1),
            ("Game of Thrones", 2011, 9.5),
            ("The Newsroom", 2012, 8.6),
            ("Cosmos", 1980, 9.3),
        ]
```


Fixtures defined in test classes are only
accessible by test methods of the class or subclasses:


``` {.programlisting .language-markup}
class Test:
    ...

    def test_highest_rated(self, drama_series):
        assert highest_rated(drama_series) == "Game of Thrones"

    def test_oldest(self, drama_series):
        assert oldest(drama_series) == "Cosmos"
```


Note that test classes might have other non-test methods, like any other
class.

### Setup/teardown



As we\'ve seen in the introduction, it is very[]{#id325023377
.indexterm} common for resources that are used[]{#id325023385
.indexterm} in testing to require some sort of clean up after a test is
done with them.

In our previous example, we had a very small dataset, so inlining it in
the fixture was fine. Suppose however that we have a much larger dataset
(say, 1,000 entries), so writing it in the code would hurt readability.
Often, the dataset is in an external file, for example, in CSV format,
so porting it into the Python code is a pain.

A solution to that would be to commit the CSV file containing the series
dataset into the repository and read it inside the test, using the
built-in `csv` module; for more details go
to <https://docs.python.org/3/library/csv.html>.

We can change the `comedy_series` fixture to do just that:


``` {.programlisting .language-markup}
@pytest.fixture
def comedy_series():
    file = open("series.csv", "r", newline="")
    return list(csv.reader(file))
```


This works, but we, being diligent developers, want to be able to close
that file properly. How can we do that with fixtures?

Fixture clean up is often referred to as [**teardown**], and it
is easily supported using the `yield` statement:


``` {.programlisting .language-markup}
@pytest.fixture
def some_fixture():
    value = setup_value()
    yield value
    teardown_value(value)
```


By using  `yield` instead of `return`, this is what
happens:


-   The fixture function is called
-   It executes until the yield statement, where it pauses and yields
    the fixture value
-   The test executes, receiving the fixture value as parameter
-   Regardless of whether the test passes or fails, the function is
    resumed so it can perform its teardown actions


For those familiar with it, this is very
similar to a [**context manager**]
(<https://docs.python.org/3/library/contextlib.html#contextlib.contextmanager>),
except that you don\'t need to surround the yield statement with a
try/except clause to ensure the block after yield is executed, even if
an exception occurs.

Let\'s return to our example; we can now use  `yield` instead
of `return` and close the file:


``` {.programlisting .language-markup}
@pytest.fixture
def comedy_series():
    file = open("series.csv", "r", newline="")
    yield list(csv.reader(file))
    file.close()
```


This is good, but notice that because `yield` works well with
the `with` statement of the file object, we can write this
instead:


``` {.programlisting .language-markup}
@pytest.fixture
def comedy_series():
    with open("series.csv", "r", newline="") as file:
        return list(csv.reader(file))
```


The file will be closed automatically by the `with` statement
after the test completes, which is shorter and considered more
Pythonic. 

Awesome.

### Composability



Suppose we receive a new series.csv file that now[]{#id325023522
.indexterm} contains a much larger number of TV series, including the
comedy series we had before and many other genres as well. We want to
use this new data for some other tests, but we would like to keep
existing tests working as they did previously.

Fixtures in pytest can easily depend on other fixtures just by declaring
them as parameters. Using this property, we are able to create a new
series fixture that reads all the data from `series.csv`
(which now contains more genres), and change our
`comedy_series` fixture to filter out only comedy series:


``` {.programlisting .language-markup}
@pytest.fixture
def series():
    with open("series.csv", "r", newline="") as file:
        return list(csv.reader(file))

@pytest.fixture
def comedy_series(series):
    return [x for x in series if x[GENRE] == "comedy"]
```


The tests which use `comedy_series` are unchanged:


``` {.programlisting .language-markup}
def test_highest_rated(comedy_series):
    assert highest_rated(comedy_series) == "Seinfeld"

def test_oldest(comedy_series):
    assert oldest(comedy_series) == "Seinfeld"
```


Note that, because of those characteristics, fixtures are a prime
example of dependency injection, which is a technique where a function
or an object declares its dependencies, but otherwise doesn\'t know or
care how those dependencies will be created, or by who. This makes them
extremely modular and reusable.



Sharing fixtures with conftest.py files 
---------------------------------------------------------



Suppose we need to use our
`comedy_series` fixture from the previous[]{#id324673427
.indexterm} section in other test modules. In pytest, sharing fixtures
is easily done by just moving the fixture code to a
`conftest.py` file.

A `conftest.py` file is a normal Python module, except that it
is loaded automatically by pytest, and any fixtures defined in it are
available to test modules in the same directory and below automatically.
Consider this test module hierarchy:


``` {.programlisting .language-markup}
tests/
    ratings/
        series.csv
        test_ranking.py
    io/
        conftest.py
        test_formats.py 
    conftest.py
```


The `tests/conftest.py` file is at the root of the hierarchy,
so any fixtures defined on it are automatically available to all other
test modules in this project. Fixtures in
`tests/io/conftest.py` will be available only to modules at
and below `tests/io`, so only to `test_formats.py`
for now.

This might not look like a big deal, but it makes sharing fixtures a
breeze: it is very liberating to be able to start small with just a few
fixtures when writing a test module, knowing that if those fixtures are
useful to other tests in the future, it will be just a small matter of
moving the fixtures to a `conftest.py` to reuse them. This
avoids the temptation to copy and paste test data around, or to spend
too much time thinking about how to organize test-supporting code from
the start, to avoid  having to do a lot of refactoring later.



Scopes 
------------------------



Fixtures are always created when a test
function requests them, by declaring them on the parameter list, as
we\'ve seen already. By default, each fixture is destroyed when each
test finishes.

As mentioned at the beginning of this lab, some fixtures can be
costly to create or set up, and it would be helpful to be able to create
as few instances of it as possible, to save time. Here are some
examples:


-   Initializing database tables
-   Reading cached data from a disk, for example, large CSV data
-   Starting up external services


To help solve this issue, fixtures in pytest can have different
[**scopes**]. The scope of a fixture defines when the fixture
should be cleaned up. While the fixture is not cleaned up, tests
requesting the fixture will receive the same fixture value.

The scope parameter of the \@pytest.fixture decorator is used to set the
fixture\'s scope:


``` {.programlisting .language-markup}
@pytest.fixture(scope="session")
def db_connection():
    ...
```


The following scopes are available:


-   `scope="session"`: fixture is teardown when all
    tests finish.
-   `scope="module"`: fixture is teardown when the last test
    function of a module finishes.
-   `scope="class"`: fixture is teardown when the last test
    method of a class finishes.
-   `scope="function"`: fixture is teardown when the test
    function requesting it finishes. This is the default.


It is important to emphasize that, regardless of scope, each fixture
will be created only when a test function requires it. For example,
session-scoped fixtures are not necessarily created at the start of the
session, but only when the first test that requests it is about to be
called. This makes sense when you consider that not all tests might need
a session-scoped fixture, and there are various forms to run only a
subset of tests, as we have seen in previous labs.


### Scopes in action



To show scopes in action, let\'s take a look
at a common pattern that\'s used when your tests involve some form of
database. In the upcoming example, don\'t focus on the database API
(which is made up anyway), but on the concepts and design of the
fixtures involved.

Usually, the connection to a database and table creation are slow. If
the database supports transactions, which is the ability to perform a
set of changes that can be applied or discarded atomically, then the
following pattern can be used.

For starters, we can use a session-scoped fixture to connect and
initialize the database with the tables we need:


``` {.programlisting .language-markup}
@pytest.fixture(scope="session")
def db():
    db = connect_to_db("localhost", "test") 
    db.create_table(Series)
    db.create_table(Actors)
    yield db
    db.prune()
    db.disconnect()
```


Note that we prune the test database and disconnect from it at the end
of the fixture, which will happen at the end of the session. 

With the `db` fixture, we can share the same database across
all our tests. This is great, because it saves time. But it also has the
downside that now tests can change the database and affect other tests.
To solve that problem, we create a transaction fixture that starts a new
transaction before a test starts and rolls the transaction back when the
test finishes, ensuring the database returns to its previous state:


``` {.programlisting .language-markup}
@pytest.fixture(scope="function")
def transaction(db):
    transaction = db.start_transaction()
    yield transaction
    transaction.rollback()
```


Note that our transaction fixture depends on `db`. Tests now
can use the transaction fixture to read and write to the database at
will, without worrying about cleaning it up for other tests:


``` {.programlisting .language-markup}
def test_insert(transaction):
    transaction.add(Series("The Office", 2005, 8.8))
    assert transaction.find(name="The Office") is not None
```


With just these two fixtures, we have a very solid foundation to write
our database tests with: the first test that requires the transaction
fixture will automatically initialize the database through the
`db` fixture, and each test from now on that needs to perform
transactions will do so from a pristine database.

This composability between fixtures of
different scopes is very powerful and enables all sorts of clever
designs in real-world test suites.



Autouse 
-------------------------



It is possible to apply a fixture to all of
the tests in a hierarchy, even if the tests don\'t explicitly request a
fixture, by passing `autouse=True` to the
`@pytest.fixture` decorator. This is useful when we need to
apply a side-effect before and/or after each test unconditionally.


``` {.programlisting .language-markup}
@pytest.fixture(autouse=True)
def setup_dev_environment():
    previous = os.environ.get('APP_ENV', '')
    os.environ['APP_ENV'] = 'TESTING'
    yield
    os.environ['APP_ENV'] = previous
```


 

An autouse fixture is applied to all tests which the fixture is
available for use with:


-   Same module as the fixture
-   Same class as the fixture, in the case of a fixture defined by a
    method
-   Tests in the same directory or below, if the fixture is defined in a
    `conftest.py` file


In other words, if a test can access an autouse fixture by declaring it
in the parameter list, the autouse fixture will be automatically used by
that test. Note that it is possible for a test function to add the
autouse fixture to its parameter list if it is interested in the return
value of the fixture, as normal.


### \@pytest.mark.usefixtures



The `@pytest.mark.usefixtures` mark can be used[]{#id325023326
.indexterm} to apply one or more fixtures to
tests, as if they have the fixture name declared in their parameter
list. This can be an alternative in situations where you want all tests
in a group to always use a fixture that is not `autouse`.

For example, the code below will ensure all tests methods in
the `TestVirtualEnv` class execute in a brand new virtual
environment:


``` {.programlisting .language-markup}
@pytest.fixture
def venv_dir():
    import venv

    with tempfile.TemporaryDirectory() as d:
        venv.create(d)
        pwd = os.getcwd()
        os.chdir(d)
        yield d
        os.chdir(pwd)

@pytest.mark.usefixtures('venv_dir')
class TestVirtualEnv:
    ...
```


As the name indicates, you can pass multiple fixtures names to the
decorator: 


``` {.programlisting .language-markup}
@pytest.mark.usefixtures("venv_dir", "config_python_debug")
class Test:
    ...
```




Parametrizing fixtures 
----------------------------------------



Fixtures can also be parametrized directly.
When a fixture is parametrized, all tests that use the fixture will now
run multiple times, once for each parameter. This is an excellent tool
to use when we have variants of a fixture and each test that uses the
fixture should also run with all variants.

In the previous lab, we saw an example of parametrization using
multiple implementations of a serializer:


``` {.programlisting .language-markup}
@pytest.mark.parametrize(
    "serializer_class",
    [JSONSerializer, XMLSerializer, YAMLSerializer],
)
class Test:

    def test_quantity(self, serializer_class):
        serializer = serializer_class()
        quantity = Quantity(10, "m")
        data = serializer.serialize_quantity(quantity)
        new_quantity = serializer.deserialize_quantity(data)
        assert new_quantity == quantity

    def test_pipe(self, serializer_class):
        serializer = serializer_class()
        pipe = Pipe(
            length=Quantity(1000, "m"), diameter=Quantity(35, "cm")
        )
       data = serializer.serialize_pipe(pipe)
       new_pipe = serializer.deserialize_pipe(data)
       assert new_pipe == pipe
```


We can update the example to parametrize on a fixture instead:


``` {.programlisting .language-markup}
class Test:

    @pytest.fixture(params=[JSONSerializer, XMLSerializer,
                            YAMLSerializer])
    def serializer(self, request):
        return request.param()

    def test_quantity(self, serializer):
        quantity = Quantity(10, "m")
        data = serializer.serialize_quantity(quantity)
        new_quantity = serializer.deserialize_quantity(data)
        assert new_quantity == quantity

    def test_pipe(self, serializer):
        pipe = Pipe(
            length=Quantity(1000, "m"), diameter=Quantity(35, "cm")
        )
        data = serializer.serialize_pipe(pipe)
        new_pipe = serializer.deserialize_pipe(data)
        assert new_pipe == pipe
```


Note the following:


-   We pass a `params` parameter to the fixture definition.
-   We access the parameter inside the fixture, using the
    `param` attribute of the special `request`
    object. This built-in fixture provides access to the requesting test
    function and the parameter when the fixture is parametrized. We will
    see more about the `request` fixture later in this
    lab.
-   In this case, we instantiate the serializer inside the fixture,
    instead of explicitly in each test.


As can be seen, parametrizing a fixture is very similar to parametrizing
a test, but there is one key difference: by parametrizing a fixture we
make all tests that use that fixture run against all the parametrized
instances, making them an excellent solution for fixtures shared in
`conftest.py` files. 

It is very rewarding to see a lot of new
tests being automatically executed when you add a new parameter to an
existing fixture.



Using marks from fixtures 
-------------------------------------------



We can use the `request` fixture to access []{#id324673418
.indexterm}marks that are applied to test
functions.

Suppose we have an `autouse` fixture that always initializes
the current locale to English:


``` {.programlisting .language-markup}
@pytest.fixture(autouse=True)
def setup_locale():
    locale.setlocale(locale.LC_ALL, "en_US")
    yield
    locale.setlocale(locale.LC_ALL, None)

def test_currency_us():
    assert locale.currency(10.5) == "$10.50"
```


But what if we want to use a different locale for just a few tests?

 

One way to do that is to use a custom mark, and access the
`mark` object from within our fixture:


``` {.programlisting .language-markup}
@pytest.fixture(autouse=True)
def setup_locale(request):
mark = request.node.get_closest_marker("change_locale")
    loc = mark.args[0] if mark is not None else "en_US"
    locale.setlocale(locale.LC_ALL, loc)
    yield
    locale.setlocale(locale.LC_ALL, None)

@pytest.mark.change_locale("pt_BR")
def test_currency_br():
    assert locale.currency(10.5) == "R$ 10,50"
```


Marks can be used that way to pass information to fixtures. Because it
is somewhat implicit though, I recommend using it sparingly, because it
might lead to hard-to-understand code.



An overview of built-in fixtures 
--------------------------------------------------



Let\'s take a look at some built-in pytest
fixtures.


### tmpdir



The `tmpdir` fixture provides an empty[]{#id325023226
.indexterm} directory that is removed automatically[]{#id325023235
.indexterm} at the end of each test:


``` {.programlisting .language-markup}
def test_empty(tmpdir):
    assert os.path.isdir(tmpdir)
    assert os.listdir(tmpdir) == []
```


Being a `function`-scoped fixture, each test gets its own
directory so they don\'t have to worry about clean up or generating
unique directories.

The fixture provides a `py.local` object
(<http://py.readthedocs.io/en/latest/path.html>), from
the `py` library
([http://py.readthedocs.io](http://py.readthedocs.io/)), which
provides convenient methods to deal with file paths, such as joining,
reading, writing, getting the extension, and so on; it is similar in
philosophy to the `pathlib.Path` object
(<https://docs.python.org/3/library/pathlib.html>) from the standard
library:


``` {.programlisting .language-markup}
def test_save_curves(tmpdir):
    data = dict(status_code=200, values=[225, 300])
fn = tmpdir.join('somefile.json')
    write_json(fn, data)
    assert fn.read() == '{"status_code": 200, "values": [225, 300]}'
```



### Note

Why pytest use `py.local` instead of `pathlib.Path`?
Pytest had been around for years before `pathlib.Path` came
along and was incorporated into the standard library, and
the `py` library  was one the best solutions for path-like
objects at the time. Core pytest developers are looking into how to
adapt pytest to the now-standard `pathlib.Path` API.


### tmpdir\_factory



The `tmpdir` fixture is very handy,
but it is only `function`[*-*]scoped: this has the
downside that it can only be used by
other `function`-scoped fixtures.

The `tmpdir_factory` fixture is
a [*session-scoped*] fixture that allows creating empty and
unique directories at any scope. This can be useful when we need to
store data on to a disk in fixtures of other scopes, for example a
`session`-scoped cache or a database file.

To show it in action, the `images_dir` fixture shown next
uses `tmpdir_factory` to create a unique directory for the
entire test session containing a series of sample image files:


``` {.programlisting .language-markup}
@pytest.fixture(scope='session')
def images_dir(tmpdir_factory):
    directory = tmpdir_factory.mktemp('images')
    download_images('https://example.com/samples.zip', directory)
    extract_images(directory / 'samples.zip')
    return directory
```


Because this will be executed only once per session, it will save us
considerable time when running the tests.

Tests can then use the `images_dir` fixture tests to easily
access the sample image files:


``` {.programlisting .language-markup}
def test_blur_filter(images_dir):
    output_image = apply_blur_filter(images_dir / 'rock1.png')
    ...
```


Keep in mind however that a directory created by this fixture is shared
and will only be deleted at the end of the test session. This means that
tests should not modify the contents of the directory; otherwise, they
risk affecting other tests.

### monkeypatch



In some situations, tests need features that
are complex or hard to set up in a testing
environment, for example:


-   Clients to an external resource (for example GitHub\'s API), where
    access during testing might be impractical or too expensive
-   Forcing a piece of code to behave as if on another platform, such as
    error handling
-   Complex conditions or environments that are hard to reproduce
    locally or in the CI


The `monkeypatch` fixture allows you to cleanly overwrite
functions, objects, and dictionary entries of the system being tested
with other objects and functions, undoing all changes during test
teardown. For example: 


``` {.programlisting .language-markup}
import getpass

def user_login(name):
    password = getpass.getpass()
    check_credentials(name, password)
    ...
```


In this code, `user_login` uses
the `getpass.getpass()` function
(<https://docs.python.org/3/library/getpass.html>) from the standard
library to prompt for the user\'s password in the most secure manner
available in the system. It is hard to simulate the actual entering of
the password during testing because `getpass` tries to read
directly from the terminal (as opposed to from `sys.stdin`)
when possible. 

We can use the `monkeypatch` fixture to bypass the call to
`getpass` in the tests, transparently and without changing the
application code:


``` {.programlisting .language-markup}
def test_login_success(monkeypatch):
monkeypatch.setattr(getpass, "getpass", lambda: "valid-pass")
    assert user_login("test-user")

def test_login_wrong_password(monkeypatch):
monkeypatch.setattr(getpass, "getpass", lambda: "wrong-pass")
    with pytest.raises(AuthenticationError, match="wrong password"):
        user_login("test-user")
```


In the tests, we use `monkeypatch.setattr` to replace the
real `getpass()` function of the `getpass` module
with a dummy `lambda`, which returns a hard-coded password.
In `test_login_success`, we return a known, good password to
ensure the user can authenticate successfully, while
in `test_login_wrong_password`, we use a bad password to
ensure the authentication error is handled correctly. As mentioned
before, the original `getpass()` function is restored
automatically at the end of the test, ensuring we don\'t leak that
change to other tests in the system.


#### How and where to patch



The `monkeypatch` fixture works by
replacing an attribute of an object[]{#id325022845
.indexterm} by another object (often called a [*mock*]),
restoring the original object at the end of the test. A common problem
when using this fixture is patching the wrong object, which causes the
original function/object to be called instead of the mock one.

To understand the problem, we need to understand
how `import` and `import from` work in Python.

Consider a module called `services.py`:


``` {.programlisting .language-markup}
import subprocess

def start_service(service_name):
subprocess.run(f"docker run {service_name}")
```


In this code, we are importing the `subprocess` module and
bringing the `subprocess` module object into
the `services.py` namespace. That\'s why we
call `subprocess.run`: we are accessing
the `run` function of the `subprocess` object in
the `services.py` namespace.

Now consider the previous code written slightly differently:


``` {.programlisting .language-markup}
from subprocess import run

def start_service(service_name):
run(f"docker run {service_name}")
```


Here, we are importing the `subprocess` module but bringing
the `run` function object into
the `service.py` namespace. That\'s why `run` can be
called directly in `start_service`, and
the `subprocess` name is not even available (if you try to
call `subprocess.run`, you will get a `NameError`
exception).

We need to be aware of this difference, to
properly `monkeypatch` the usage
of `subprocess.run` in `services.py`.

In the first case, we need to replace the `run` function of
the `subprocess` module, because that\'s
how `start_service` uses it: 


``` {.programlisting .language-markup}
import subprocess
import services

def test_start_service(monkeypatch):
    commands = []
    monkeypatch.setattr(subprocess, "run", commands.append)
    services.start_service("web")
    assert commands == ["docker run web"]
```


In this code,
both `services.py` and `test_services.py` have the
reference to the same `subprocess` module object.

In the second case, however, `services.py` has a reference to
the original `run` function in its own namespace. For this
reason, the correct approach for the second case is to replace
the `run` function in `services.py` \'s namespace:


``` {.programlisting .language-markup}
import services

def test_start_service(monkeypatch):
    commands = []
    monkeypatch.setattr(services, "run", commands.append)
    services.start_service("web")
    assert commands == ["docker run web"]
```


How the code being tested imports code that needs to be
monkeypatched is the reason why people are
tripped by this so often, so make sure you take a look at the code
first.


### capsys/capfd



The `capsys` fixture captures all
text written to `sys.stdout` and `sys.stderr` and
makes it available during[]{#id325091911
.indexterm} testing.

Suppose we have a small command-line script
and want to check the usage instructions are correct when the script is
invoked without arguments:


``` {.programlisting .language-markup}
from textwrap import dedent

def script_main(args):
    if not args:
        show_usage()
        return 0
    ...

def show_usage():
    print("Create/update webhooks.")
    print(" Usage: hooks REPO URL")
```


During testing, we can access the captured output, using the
`capsys` fixture. This fixture has a
`capsys.readouterr()` method that returns
a `namedtuple` (<https://docs.python.org/3/library/collections.html#collections.namedtuple>) with `out` and `err` attributes,
containing the captured text
from `sys.stdout` and `sys.stderr` respectively:


``` {.programlisting .language-markup}
def test_usage(capsys):
    script_main([])
    captured = capsys.readouterr()
    assert captured.out == dedent("""\
        Create/update webhooks.
          Usage: hooks REPO URL
    """)
```


There\'s also the `capfd` fixture that works similarly
to `capsys`, except that it also captures the output of file
descriptors `1` and `2`. This makes it possible to
capture the standard output and standard errors, even for extension
modules.


#### Binary mode



`capsysbinary` and `capfdbinary` are
fixtures identical
to `capsys` and `capfd`, except that they
capture output in binary mode, and their
`readouterr()` methods return raw bytes instead of text. It
might be useful in specialized situations, for example, when running an
external process that produces binary output, such as `tar`.


### request



The `request` fixture is an internal[]{#id325092051
.indexterm} pytest fixture that provides useful information about the
requesting test. It can be declared in test functions and fixtures, and
provides attributes such as the following:


-   `function`: the Python `test` function object,
    available for `function`-scoped fixtures.
-   `cls`/`instance`: the Python class/instance of a
    `test` method object, available for function- and
    `class`-scoped fixtures. It can be `None` if the
    fixture is being requested from a `test` function, as
    opposed to a test method.
-   `module`: the Python module object of the requesting test
    method, available for `module`-, `function`-,
    and `class`-scoped fixtures.



-   `session`: pytest\'s internal `Session` object,
    which is a singleton for the test session and represents the root of
    the collection tree. It is available to fixtures of all scopes.
-   `node`: the pytest collection node, which wraps one of the
    Python objects discussed that matches the fixture scope. 
-   `addfinalizer(func)`: adds a `new finalizer`
    function that will be called at the end of the test. The finalizer
    function is called without arguments. `addfinalizer` was
    the original way to execute teardown in fixtures, but has since then
    been superseded by the `yield` statement, remaining in use
    mostly for backward compatibility.


Fixtures can use those attributes to customize their own behavior based
on the test being executed. For example, we can create a fixture that
provides a temporary directory using the current test name as the prefix
of the temporary directory, somewhat similar to the built-in
`tmpdir` fixture:


``` {.programlisting .language-markup}
@pytest.fixture
def tmp_path(request) -> Path:
    with TemporaryDirectory(prefix=request.node.name) as d:
        yield Path(d)

def test_tmp_path(tmp_path):
    assert list(tmp_path.iterdir()) == []
```


This code created the following directory when executed on my system:


``` {.programlisting .language-markup}
C:\Users\Bruno\AppData\Local\Temp\test_tmp_patht5w0cvd0
```


The `request` fixture can be used whenever[]{#id325092194
.indexterm} you want to customize a fixture based on the attributes of
the test being executed, or to access the marks applied to the test
function, as we have seen in the previous sections.



Tips/discussion 
---------------------------------



The following are some short topics and tips
that did not fit into the previous sections, but that I think are worth
mentioning. 


### When to use fixtures, as opposed to simple functions



Sometimes, all you need is to construct a
simple object for your tests, and arguably this can be done in a plain
function, not necessarily needing to be implemented as a fixture.
Suppose we have a `WindowManager` class, that does not receive
any parameters:


``` {.programlisting .language-markup}
class WindowManager:
    ...
```


One way to use it in our tests would be to write a fixture:


``` {.programlisting .language-markup}
@pytest.fixture
def manager():
    return WindowManager()

def test_windows_creation(manager):
    window = manager.new_help_window("pipes_help.rst")
    assert window.title() == "Pipe Setup Help"
```


Alternatively, you could argue that a fixture for such simple usage is
overkill, and use a plain function instead:


``` {.programlisting .language-markup}
def create_window_manager():
    return WindowManager()

def test_windows_creation():
    manager = create_window_manager()
    window = manager.new_help_window("pipes_help.rst")
    assert window.title() == "Pipe Setup Help"
```


Or you could even create the manager explicitly on each test:


``` {.programlisting .language-markup}
def test_windows_creation():
    manager = WindowManager()
    window = manager.new_help_window("pipes_help.rst")
    assert window.title() == "Pipe Setup Help"
```


This is perfectly fine, especially if this is used in a few tests in a
single module.

Keep in mind, however, that fixtures [**abstract away details about the
construction and teardown process of objects**]. This is
crucial to remember when deciding to forego fixtures in favor of normal
functions.

Suppose that our `WindowManager` now needs to be closed
explicitly, or that it needs a local directory for logging purposes:


``` {.programlisting .language-markup}
class WindowManager:

    def __init__(self, logging_directory):
        ...

    def close(self):
        """
        Close the WindowManager and all associated resources. 
        """
        ...
```


If we have been using a fixture such as the one given in the first
example, we just update the fixture function and [**no tests need to
change at all**]:


``` {.programlisting .language-markup}
@pytest.fixture
def manager(tmpdir):
    wm = WindowManager(str(tmpdir))
    yield wm
    wm.close()
```


But if we opted to use a plain function, now we [**have to update all
places that call our function**]: we need to pass a logging
directory and guarantee that `.close()` is called at the end
of the test:


``` {.programlisting .language-markup}
def create_window_manager(tmpdir, request):
    wm = WindowManager(str(tmpdir))
    request.addfinalizer(wm.close)
    return wm

def test_windows_creation(tmpdir, request):
manager = create_window_manager(tmpdir, request)
    window = manager.new_help_window("pipes_help.rst")
    assert window.title() == "Pipe Setup Help"
```


Depending on how many times this function has
been used in our tests, this can be quite a refactoring.

The message is: it is fine to use plain functions when the underlying
object is simple and unlikely to change, but keep in mind that fixtures
abstract the details of the creation/destruction of objects, and they
might need to change in the future. On the other hand, using fixtures
creates another level of indirection, which slightly increases code
complexity. In the end, it is a balance that should be weighted by you.

 

### Renaming fixtures



The `@pytest.fixture` decorator accepts[]{#id325534030
.indexterm} a `name` parameter that can be used to specify a
name for the fixture, different from the fixture function:


``` {.programlisting .language-markup}
@pytest.fixture(name="venv_dir")
def _venv_dir():
    ...
```


This is useful, because there are some annoyances that might affect
users when using fixtures declared in the same module as the test
functions that use them:


-   If users forget to declare the fixture in the parameter list of a
    test function, they will get a `NameError` instead of the
    fixture function object (because they are in the same module).
-   Some linters complain that the test function parameter is shadowing
    the fixture function.


You might adopt this as a good practice in your team if the previous
annoyances are frequent. Keep in mind that these problems only happen
with fixtures defined in test modules, not in `conftest.py`
files.

### Prefer local imports in conftest files



`conftest.py` files are imported during[]{#id325538657
.indexterm} collection, so they directly affect your
experience when running tests from the
command line. For this reason, I suggest using local imports in
`conftest.py` files as often as possible, to keep import times
low.

So, don\'t use this:


``` {.programlisting .language-markup}
import pytest
import tempfile
from myapp import setup

@pytest.fixture
def setup_app():
    ...
```


 

 

Prefer local imports:


``` {.programlisting .language-markup}
import pytest

@pytest.fixture
def setup_app():
    import tempfile
    from myapp import setup
    ...
```


This practice has a noticeable impact on test startup in large test
suites.

### Fixtures as test-supporting code



You should think of fixtures not only as a
means of providing resources, but also of providing supporting code for
your tests. By supporting code, I mean classes that provide high-level
functionality for testing.

For example, a bot framework might provide a fixture that can be used to
test your bot as a black box:


``` {.programlisting .language-markup}
def test_hello(bot):
    reply = bot.say("hello")
    assert reply.text == "Hey, how can I help you?"

def test_store_deploy_token(bot):
    assert bot.store["TEST"]["token"] is None
    reply = bot.say("my token is ASLKM8KJAN")
    assert reply.text == "OK, your token was saved"
    assert bot.store["TEST"]["token"] == "ASLKM8KJAN"
```


The `bot` fixture allows the developer to talk to the bot,
verify responses, and check the contents of the internal store that is
handled by the framework, among other things. It provides a high-level
interface that makes tests easier to write and understand, even for
those who do not understand the internals of the framework.

This technique is useful for applications, because it will make it easy
and enjoyable for developers to add new tests. It is also useful for
libraries, because they will provide high-level testing support for
users of your library.





Summary 
-------------------------



In this lab, we delved into one of pytest\'s most famous features:
fixtures. We have seen how they can be used to provide resources and
test functionality, and how to concisely express setup/teardown code. We
learned how to share fixtures, using `conftest.py` files; to
use fixture scopes, to avoid creating expensive resources for every
test; and to autouse fixtures that are executed for all tests in the
same module or hierarchy. Then, we learned how to parametrize
fixtures and use marks from them. We took an overview of various
built-in fixtures, and closed the lab with some short discussions
about fixtures in general. I hope you enjoyed the ride!

In the next lab, we will explore a little of the vast pytest plugin
ecosystem that is at your disposal.
