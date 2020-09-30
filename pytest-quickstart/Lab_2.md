<img align="right" src="../logo.png">


Lab 2. Writing and Running Tests
---------------------------------------------

In the previous lab, we discussed why testing is so important and
looked at a brief overview of the `unittest` module. We also
took a cursory look at pytest\'s features, but barely got a taste of
them.

In this lab, we will start our journey with pytest. We will be
pragmatic, so this means that we will not take an exhaustive look at all
of the things it\'s possible to do with pytest, but instead provide you
with a quick overview of the basics to make you productive quickly. We
will take a look at how to write tests, how to organize them into files
and directories, and how to use pytest\'s command line effectively. 

Here\'s what is covered in this lab:

-   Installing pytest
-   Writing and running tests
-   Organizing files and packages
-   Useful command-line options
-   Configuration: `pytest.ini` file


#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `~/work/pytest-quickstart/code` folder.


### Note

In the lab, there are a lot of examples typed into the command line.
They are marked by the character. To avoid clutter and to focus on the
important parts, the pytest header (which normally displays the pytest
version, the Python version, installed plugins, and so on) will be
suppressed. 


Let\'s jump right into how to install pytest.



Installing pytest 
-----------------------------------



Installing pytest is really simple, but
first, let\'s take a moment to review good practices for Python
development.

 

 

 


### Note

All of the examples are for Python 3. They should be easy to adapt to
Python 2 if necessary.

### pip and virtualenv



The recommended practice for installing
dependencies is to create a
`virtualenv`. A `virtualenv`
(<https://packaging.python.org/guides/installing-using-pip-and-virtualenv/>)
acts like a complete separate Python
installation from the one that comes with your operating system, making
it safe to install the packages required by your application without
risk of breaking your system Python or tools.

Now we will learn how to create a virtual environment and install pytest
using pip. If you are already familiar with `virtualenv` and
pip, you can skip this section:


1.  Type this in your Command Prompt to create a `virtualenv`:



``` {.programlisting .language-markup}
python -m venv .env
```



2.  This command will create a `.env` folder in the current
    directory, containing a full-blown Python installation. Before
    proceeding, you should `activate` the
    `virtualenv`:



``` {.programlisting .language-markup}
source .env/bin/activate
```


Or on Windows:


``` {.programlisting .language-markup}
.env\Scripts\activate
```


This will put the `virtualenv` Python in front of the
`$PATH` environment variable, so Python, pip, and other tools
will be executed from the `virtualenv`, not from your system.


3.  Finally, to install pytest, type:



``` {.programlisting .language-markup}
pip install pytest
```


You can verify that everything went well by typing:


``` {.programlisting .language-markup}
pytest --version
This is pytest version 3.5.1, imported from x:\fibo\.env36\lib\site-packages\pytest.py
```


 

 

 

 

Now, we are all set up and can begin!



Writing and running tests 
-------------------------------------------



Using pytest, all you need to do to start
writing tests is to create a new file named `test_*.py` and
write test functions that start with
`test`:


``` {.programlisting .language-markup}
    # contents of test_player_mechanics.py
    def test_player_hit():
        player = create_player()
        assert player.health == 100
        undead = create_undead()
        undead.hit(player)
        assert player.health == 80
```


To execute this test, simply execute `pytest`, passing the
name of the file:


``` {.programlisting .language-markup}
pytest test_player_mechanics.py
```


If you don\'t pass anything, pytest will look for all of the test files
from the current directory recursively and execute them automatically.


### Note

You might encounter examples on the internet that use
`py.test` in the command line instead of `pytest`.
The reason for that is historical: pytest used to be part of the
`py` package, which provided several general purpose
utilities, including tools that followed the convention of starting with
`py.<TAB>` for tab completion, but since then, it has been
moved into its own project. The old `py.test` command is still
available and is an alias to `pytest`, but the latter is the
recommended modern usage.


Note that there\'s no need to create classes; just simple functions and
plain `assert` statements are enough, but if you want to use
classes to group tests you can do so:


``` {.programlisting .language-markup}
    class TestMechanics:

        def test_player_hit(self):
            ...

        def test_player_health_flask(self):
            ...
```


 

 

 

 

 

 

Grouping tests can be useful when you want to put a number of tests
under the same scope: you can execute tests based on the class they are
in, apply markers to all of the tests in a class ([Lab
3](https://subscription.packtpub.com/book/web_development/9781789347562/3){.link},
[*Markers and Parametrization*]), and create fixtures bound
to a class ([Lab
4](https://subscription.packtpub.com/book/web_development/9781789347562/4){.link},
[*Fixtures*]).


### Running tests



Pytest can run your tests in a number of
ways. Let\'s quickly get into the basics now and, later on in the
lab, we will move on to more advanced options.

You can start by just simply executing the `pytest` command:


``` {.programlisting .language-markup}
pytest
```


This will find all of the `test_*.py` and
`*_test.py` modules in the current directory and below
recursively, and will run all of the tests found in those files:


-   You can reduce the search to specific directories:



``` {.programlisting .language-markup}
      pytest tests/core tests/contrib
```



-   You can also mix any number of files and directories:



``` {.programlisting .language-markup}
      pytest tests/core tests/contrib/test_text_plugin.py
```



-   You can execute specific tests by using the
    syntax `<test-file>::<test-function-name>`:



``` {.programlisting .language-markup}
      pytest tests/core/test_core.py::test_regex_matching
```



-   You can execute all of the `test` methods of a
    `test` class:



``` {.programlisting .language-markup}
      pytest tests/contrib/test_text_plugin.py::TestPluginHooks
```



-   You can execute a specific `test` method of a
    `test` class using the
    syntax `<test-file>::<test-class>::<test-method-name>`:



``` {.programlisting .language-markup}
      pytest tests/contrib/
      test_text_plugin.py::TestPluginHooks::test_registration
```


The syntax used above is created internally by pytest, is unique to each
test collected, and is called
a `node id` or `item id`[*. *]It
basically consists of the filename of the testing module, class, and
functions joined together by the `::` characters.

 

Pytest will show a more verbose output, which includes node IDs, with
the `-v` flag:


``` {.programlisting .language-markup}
 pytest tests/core -v
======================== test session starts ========================
...
collected 6 items

tests\core\test_core.py::test_regex_matching PASSED            [ 16%]
tests\core\test_core.py::test_check_options FAILED             [ 33%]
tests\core\test_core.py::test_type_checking FAILED             [ 50%]
tests\core\test_parser.py::test_parse_expr PASSED              [ 66%]
tests\core\test_parser.py::test_parse_num PASSED               [ 83%]
tests\core\test_parser.py::test_parse_add PASSED               [100%]
```


To see which tests there are without running them, use
the `--collect-only`  flag:


``` {.programlisting .language-markup}
pytest tests/core --collect-only
======================== test session starts ========================
...
collected 6 items
<Module 'tests/core/test_core.py'>
  <Function 'test_regex_matching'>
  <Function 'test_check_options'>
  <Function 'test_type_checking'>
<Module 'tests/core/test_parser.py'>
  <Function 'test_parse_expr'>
  <Function 'test_parse_num'>
  <Function 'test_parse_add'>

=================== no tests ran in 0.01 seconds ====================
```


`--collect-only` is especially useful if you want to execute a
specific test but can\'t remember its exact name.

### Powerful asserts



As you\'ve probably already noticed, pytest makes use of the built-in
`assert` statement to check assumptions during testing.
Contrary to other frameworks, you don\'t need
to remember various `self.assert*` or `self.expect*`
functions. While this may not seem like a big deal at first, after
spending some time using plain asserts, you will realize how much that
makes writing tests more enjoyable and natural.

 

Again, here\'s an example of a failure:


``` {.programlisting .language-markup}
________________________ test_default_health ________________________

    def test_default_health():
        health = get_default_health('warrior')
>       assert health == 95
E       assert 80 == 95

tests\test_assert_demo.py:25: AssertionError
```


Pytest shows the line of the failure, as well as the variables and
expressions involved in the failure. By itself, this would be pretty
cool already, but pytest goes a step further and provides specialized
explanations of failures involving other data types.


#### Text differences



When showing the explanation for short
strings, pytest uses a simple difference method:


``` {.programlisting .language-markup}
_____________________ test_default_player_class _____________________

    def test_default_player_class():
        x = get_default_player_class()
>       assert x == 'sorcerer'
E       AssertionError: assert 'warrior' == 'sorcerer'
E         - warrior
E         + sorcerer
```


Longer strings show a smarter delta, using `difflib.ndiff` to
quickly spot the differences:


``` {.programlisting .language-markup}
__________________ test_warrior_short_description ___________________

    def test_warrior_short_description():
        desc = get_short_class_description('warrior')
>       assert desc == 'A battle-hardened veteran, can equip heavy armor and weapons.'
E       AssertionError: assert 'A battle-har... and weapons.' == 'A battle-hard... and weapons.'
E         - A battle-hardened veteran, favors heavy armor and weapons.
E         ?                            ^ ^^^^
E         + A battle-hardened veteran, can equip heavy armor and weapons.
E         ?                            ^ ^^^^^^^
```


Multiline strings are also treated specially:


``` {.programlisting .language-markup}
    def test_warrior_long_description():
        desc = get_long_class_description('warrior')
>       assert desc == textwrap.dedent('''\
            A seasoned veteran of many battles. Strength and Dexterity
            allow to yield heavy armor and weapons, as well as carry
            more equipment. Weak in magic.
            ''')
E       AssertionError: assert 'A seasoned v... \n' == 'A seasoned ve... \n'
E         - A seasoned veteran of many battles. High Strength and Dexterity
E         ?                                     -----
E         + A seasoned veteran of many battles. Strength and Dexterity
E           allow to yield heavy armor and weapons, as well as carry
E         - more equipment while keeping a light roll. Weak in magic.
E         ?               ---------------------------
E         + more equipment. Weak in magic. 
```


#### Lists



Assertion failures for lists also show only
differing items by default:


``` {.programlisting .language-markup}
____________________ test_get_starting_equiment _____________________

    def test_get_starting_equiment():
        expected = ['long sword', 'shield']
>       assert get_starting_equipment('warrior') == expected
E       AssertionError: assert ['long sword'...et', 'shield'] == ['long sword', 'shield']
E         At index 1 diff: 'warrior set' != 'shield'
E         Left contains more items, first extra item: 'shield'
E         Use -v to get the full diff

tests\test_assert_demo.py:71: AssertionError
```


Note that pytest shows which index differs, and also that the
`-v` flag can be used to show the complete difference between
the lists:


``` {.programlisting .language-markup}
____________________ test_get_starting_equiment _____________________

    def test_get_starting_equiment():
        expected = ['long sword', 'shield']
>       assert get_starting_equipment('warrior') == expected
E       AssertionError: assert ['long sword'...et', 'shield'] == ['long sword', 'shield']
E         At index 1 diff: 'warrior set' != 'shield'
E         Left contains more items, first extra item: 'shield'
E         Full diff:
E         - ['long sword', 'warrior set', 'shield']
E         ?               ---------------
E         + ['long sword', 'shield']

tests\test_assert_demo.py:71: AssertionError
```


If the difference is too big, pytest is smart enough to show only a
portion to avoid showing too much output, displaying a message like the
following:


``` {.programlisting .language-markup}
E         ...Full output truncated (100 lines hidden), use '-vv' to show
```


#### Dictionaries and sets



Dictionaries are probably one of the most
used data structures in Python, so, unsurprisingly, pytest has
specialized representation for them:


``` {.programlisting .language-markup}
_______________________ test_starting_health ________________________

    def test_starting_health():
        expected = {'warrior': 85, 'sorcerer': 50}
>       assert get_classes_starting_health() == expected
E       AssertionError: assert {'knight': 95...'warrior': 85} == {'sorcerer': 50, 'warrior': 85}
E         Omitting 1 identical items, use -vv to show
E         Differing items:
E         {'sorcerer': 55} != {'sorcerer': 50}
E         Left contains more items:
E         {'knight': 95}
E         Use -v to get the full diff
```


Sets also have similar output:


``` {.programlisting .language-markup}
________________________ test_player_classes ________________________

    def test_player_classes():
>       assert get_player_classes() == {'warrior', 'sorcerer'}
E       AssertionError: assert {'knight', 's...r', 'warrior'} == {'sorcerer', 'warrior'}
E         Extra items in the left set:
E         'knight'
E         Use -v to get the full diff
```


As with lists, there are also `-v` and `-vv` options
for displaying more detailed output.

 

#### How does pytest do it?



By default, Python\'s assert statement does
not provide any details when it fails, but as we just saw, pytest shows
a lot of information about the variables and expressions involved in a
failed assertion. So how does pytest do it?

Pytest is able to provide useful exceptions because it implements a
mechanism called [*assertion rewriting*].

Assertion rewriting works by installing a custom import hook that
intercepts the standard Python import mechanism. When pytest detects
that a test file (or plugin) is about to be imported, instead of loading
the module, it first compiles the source code into an [**abstract syntax
tree**] ([**AST**]) using the built-in `ast`
module. Then, it searches for any `assert` statements and
[*rewrites*] them so that the variables used[]{#id325536776
.indexterm} in the expression are kept so that they can be used to show
more helpful messages if the assertion fails. Finally, it saves the
rewritten `pyc` file to disk for caching.

This all might seem very magical, but the process is actually simple,
deterministic, and, best of all, completely transparent.


### Note

If you want more details, refer
to <http://pybites.blogspot.com.br/2011/07/behind-scenes-of-pytests-new-assertion.html>,
written by the original developer of this feature, Benjamin
Peterson. The `pytest-ast-back-to-python` plugin shows exactly
what the AST of your test files looks like after the rewriting process.
Refer to: <https://github.com/tomviner/pytest-ast-back-to-python>.



### Checking exceptions: pytest.raises



A good API documentation will clearly explain
what the purpose of each function is, its parameters, and return values.
Great API documentation also clearly explains which exceptions are
raised and when.

For that reason, testing that exceptions are raised in the appropriate
circumstances is just as important as testing the main functionality of
APIs. It is also important to make sure that exceptions contain an
appropriate and clear message to help users understand the issue.

Suppose we are writing an API for a game. This API allows programmers to
write `mods`, which are a plugin of sorts that can change
several aspects of a game, from new textures to complete new story lines
and types of characters.

 

 

This API has a function that allows mod writers to create a new
character, and it can raise exceptions in some situations:


``` {.programlisting .language-markup}
def create_character(name: str, class_name: str) -> Character:
    """
    Creates a new character and inserts it into the database.

    :raise InvalidCharacterNameError:
        if the character name is empty.

    :raise InvalidClassNameError:
        if the class name is invalid.

    :return: the newly created Character.
    """
    ...
```


Pytest makes it easy to check that your code is raising the proper
exceptions with the `raises` statement:


``` {.programlisting .language-markup}
def test_empty_name():
    with pytest.raises(InvalidCharacterNameError):
        create_character(name='', class_name='warrior')


def test_invalid_class_name():
    with pytest.raises(InvalidClassNameError):
        create_character(name='Solaire', class_name='mage')
```


`pytest.raises` is a with-statement that ensures the exception
class passed to it will be [**raised**] inside its
execution [**block**]. For more details
(<https://docs.python.org/3/reference/compound_stmts.html#the-with-statement>).
Let\'s see how `create_character` implements those checks:


``` {.programlisting .language-markup}
def create_character(name: str, class_name: str) -> Character:
    """
    Creates a new character and inserts it into the database.
    ...
    """
    if not name:
        raise InvalidCharacterNameError('character name empty')

    if class_name not in VALID_CLASSES:
        msg = f'invalid class name: "{class_name}"'
        raise InvalidCharacterNameError(msg)
    ...
```


 

 

 

 

If you are paying close attention, you probably noticed that the
copy-paste error in the preceding code should
actually raise an  `InvalidClassNameError` for the class name
check.

Executing this file:


``` {.programlisting .language-markup}
======================== test session starts ========================
...
collected 2 items

tests\test_checks.py .F                                        [100%]

============================= FAILURES ==============================
______________________ test_invalid_class_name ______________________

    def test_invalid_class_name():
        with pytest.raises(InvalidCharacterNameError):
>           create_character(name='Solaire', class_name='mage')

tests\test_checks.py:51:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'Solaire', class_name = 'mage'

    def create_character(name: str, class_name: str) -> Character:
        """
        Creates a new character and inserts it into the database.

        :param name: the character name.

        :param class_name: the character class name.

        :raise InvalidCharacterNameError:
            if the character name is empty.

        :raise InvalidClassNameError:
            if the class name is invalid.

        :return: the newly created Character.
        """
        if not name:
            raise InvalidCharacterNameError('character name empty')

        if class_name not in VALID_CLASSES:
            msg = f'invalid class name: "{class_name}"'
>           raise InvalidClassNameError(msg)
E           test_checks.InvalidClassNameError: invalid class name: "mage"

tests\test_checks.py:40: InvalidClassNameError
================ 1 failed,  1 passed in 0.05 seconds =================
```


`test_empty_name` passed as expected.
`test_invalid_class_name` raised
`InvalidClassNameError`, so the exception was not captured
by `pytest.raises`, which failed the test (as any other
exception would).


#### Checking exception messages



As stated at the start of this section, APIs should[]{#id325537115
.indexterm} provide clear messages in the exceptions they raise. In the
previous examples, we only verified that the code was raising the
appropriate exception type, but not the actual message.

`pytest.raises` can receive an optional `match`
argument, which is a regular expression string that will be matched
against the exception message, as well as checking the exception type.
For more details, go to: <https://docs.python.org/3/howto/regex.html>.
We can use that to improve our tests even further:


``` {.programlisting .language-markup}
def test_empty_name():
    with pytest.raises(InvalidCharacterNameError,
match='character name empty'):
        create_character(name='', class_name='warrior')


def test_invalid_class_name():
    with pytest.raises(InvalidClassNameError,
match='invalid class name: "mage"'):
        create_character(name='Solaire', class_name='mage')
```


Simple!


### Checking warnings: pytest.warns



APIs also evolve. New and better alternatives
to old functions are provided, arguments are removed, old ways of using
a certain functionality evolve into better ways, and so on.

 

API writers have to strike a balance between keeping old code working to
avoid breaking clients and providing better ways of doing things, while
all the while keeping their own API code maintainable. For this reason,
a solution often adopted is to start to issue `warnings` when
API clients use the old behavior, in the hope that they update their
code to the new constructs. Warning messages are shown in situations
where the current usage is not wrong to warrant an exception, it just
happens that there are new and better ways of doing it. Often, warning
messages are shown during a grace period for this update to take place,
and afterward the old way is no longer supported.

Python provides the standard warnings module exactly for this purpose,
making it easy to warn developers about forthcoming changes in APIs. For
more details, go to: <https://docs.python.org/3/library/warnings.html>.
It lets you choose from a number of warning classes, for example:


-   `UserWarning`: user warnings (`user` here means
    developers, not software users)
-   `DeprecationWarning`: features that will be removed in the
    future
-   `ResourcesWarning`: related to resource usage


(This list is not exhaustive. Consult the warnings documentation for the
full listing. For more details, go
to: <https://docs.python.org/3/library/warnings.html>[).](https://docs.python.org/3/library/warnings.html)

Warning classes help users control which warnings should be shown and
which ones should be suppressed.

For example, suppose an API for a computer game provides this handy
function to obtain the starting hit points of player characters given
their class name:


``` {.programlisting .language-markup}
def get_initial_hit_points(player_class: str) -> int:
    ...
```


Time moves forward and the developers decide to use an `enum`
instead of class names in the next release. For more details, go to:
<https://docs.python.org/3/library/enum.html>, which is more adequate to
represent a limited set of values:


``` {.programlisting .language-markup}
class PlayerClass(Enum):
    WARRIOR = 1
    KNIGHT = 2
    SORCERER = 3
    CLERIC = 4
```


 

 

 

 

 

 

 

 

 

 

 

 

 

 

But changing this suddenly would break all clients, so they wisely
decide to support both forms for the next release: `str` and
the `PlayerClass``enum`. They don\'t want to keep
supporting this forever, so they start showing a warning whenever a
class is passed as a `str`:


``` {.programlisting .language-markup}
def get_initial_hit_points(player_class: Union[PlayerClass, str]) -> int:
    if isinstance(player_class, str):
        msg = 'Using player_class as str has been deprecated' \
              'and will be removed in the future'
warnings.warn(DeprecationWarning(msg))
        player_class = get_player_enum_from_string(player_class)
    ...
```


In the same vein as `pytest.raises` from the previous section,
the `pytest.warns` function lets you test whether your API
code is producing the warnings you expect:


``` {.programlisting .language-markup}
def test_get_initial_hit_points_warning():
    with pytest.warns(DeprecationWarning):
        get_initial_hit_points('warrior')
```


As with `pytest.raises`, `pytest.warns` can receive
an optional `match` argument, which is a regular expression
string. For more details, go
to:<https://docs.python.org/3/howto/regex.html>, which will be matched
against the exception message:


``` {.programlisting .language-markup}
def test_get_initial_hit_points_warning():
    with pytest.warns(DeprecationWarning,
match='.*str has been deprecated.*'):
        get_initial_hit_points('warrior')
```


### Comparing floating point numbers: pytest.approx



Comparing floating point numbers can be tricky. For more details, go to:
<https://docs.python.org/3/tutorial/floatingpoint.html>. Numbers that we
consider equal in the real world are not so
when represented by computer hardware:


``` {.programlisting .language-markup}
>>> 0.1 + 0.2 == 0.3
False
```


When writing tests, it is very common to compare the results produced by
our code against what we expect as floating point values. As shown
above, a simple `==` comparison often won\'t be sufficient. A
common approach is to use a known tolerance instead and use
`abs` to correctly deal with negative numbers:


``` {.programlisting .language-markup}
def test_simple_math():
    assert abs(0.1 + 0.2) - 0.3 < 0.0001
```


But besides being ugly and hard to understand, it is sometimes difficult
to come up with a tolerance that works in most situations. The chosen
tolerance of `0.0001` might work for the numbers above, but
not for very large numbers or very small ones. Depending on the
computation performed, you would need to find a suitable tolerance for
every set of input numbers, which is tedious and error-prone.

`pytest.approx` solves this problem by automatically choosing
a tolerance appropriate for the values involved in the expression,
providing a very nice syntax to boot:


``` {.programlisting .language-markup}
def test_approx_simple():
    assert 0.1 + 0.2 == approx(0.3)
```


You can read the above as
`assert that 0.1 + 0.2 equals approximately to 0.3`.

But the  `approx` function does not stop there; it can be used
to compare:


-   Sequences of numbers:



``` {.programlisting .language-markup}
      def test_approx_list():
          assert [0.1 + 1.2, 0.2 + 0.8] == approx([1.3, 1.0])
```



-   Dictionary `values` (not keys):



``` {.programlisting .language-markup}
      def test_approx_dict():
          values = {'v1': 0.1 + 1.2, 'v2': 0.2 + 0.8}
          assert values == approx(dict(v1=1.3, v2=1.0))
```



-   `numpy` arrays:



``` {.programlisting .language-markup}
      def test_approx_numpy():
          import numpy as np
          values = np.array([0.1, 0.2]) + np.array([1.2, 0.8])
          assert values == approx(np.array([1.3, 1.0]))
```


When a test fails, `approx` provides a nice error message
displaying the values that failed and the tolerance used:


``` {.programlisting .language-markup}
    def test_approx_simple_fail():
>       assert 0.1 + 0.2 == approx(0.35)
E       assert (0.1 + 0.2) == 0.35 ± 3.5e-07
E        + where 0.35 ± 3.5e-07 = approx(0.35)
```




Organizing files and packages 
-----------------------------------------------



Pytest needs to import your code and test
modules, and it is up to you how to organize them. Pytest supports two
common test layouts, which we will discuss
next.


### Tests that accompany your code



You can place your test modules together with
the code they are testing by creating a `tests` folder next to
the modules themselves:


``` {.programlisting .language-markup}
setup.py
mylib/
    tests/
         __init__.py
         test_core.py
         test_utils.py    
    __init__.py
    core.py
    utils.py
```


By putting the tests near the code they test, you gain the following
advantages:


-   It is easier to add new tests and test modules in this hierarchy and
    keep them in sync
-   Your tests are now part of your package, so they can be deployed and
    run in other environments


The main disadvantage with this approach is that some folks don\'t like
the added package size of the extra modules, which are now packaged
together with the rest of the code, but this is usually minimal and of
little concern.

As an additional benefit, you can use the `--pyargs` option to
specify tests using their module import path. For example:


``` {.programlisting .language-markup}
pytest --pyargs mylib.tests
```


This will execute all test modules found under `mylib.tests`.

 

 

 

 


### Note

You might consider using `_tests` for the test module names
instead of `_test`. This makes the directory easier to find
because the leading underscore usually makes them appear at the top of
the folder hierarchy. Of course, feel free to use `tests` or
any other name that you prefer; pytest doesn\'t care as long as the test
modules themselves are named `test_*.py` or
`*_test.py`.


### Tests separate from your code



An alternative to the method above is to
organize your tests in a separate directory from the main package:


``` {.programlisting .language-markup}
setup.py
mylib/  
    __init__.py
    core.py
    utils.py
tests/
    __init__.py
    test_core.py
    test_utils.py 
```


Some people prefer this layout because:


-   It keeps library code and testing code separate
-   The testing code is not included in the source package


One disadvantage of the above method is that, once you have a more
complex hierarchy, you will probably want to keep the same hierarchy
inside your tests directory, and that\'s a little harder to maintain and
keep in sync:


``` {.programlisting .language-markup}
mylib/  
    __init__.py
    core/
        __init__.py
        foundation.py
    contrib/
        __init__.py
        text_plugin.py
tests/
    __init__.py
    core/
        __init__.py
        test_foundation.py
    contrib/
        __init__.py
        test_text_plugin.py
```



### Note

So, which layout is the best? Both layouts have advantages and
disadvantages. Pytest itself works perfectly well with either of them,
so feel free to choose a layout that you are more comfortable with.




Useful command-line options 
---------------------------------------------



Now we will take a look at command-line
options that will make you more productive in your daily work. As stated
at the beginning of the lab, this is not a complete list of all of
the command-line features; just the ones that you will use (and love)
the most.


### Keyword expressions: -k



Often, you don\'t exactly remember the full
path or name of a test that you want to execute. At other times, many
tests in your suite follow a similar pattern and you want to execute all
of them because you just refactored a sensitive area of the code.

By using the `-k <EXPRESSION>` flag (from [*keyword
expression*]), you can run tests whose
`item id` loosely matches the given expression:


``` {.programlisting .language-markup}
pytest -k "test_parse"
```


This will execute all tests that contain the string `parse` in
their item IDs. You can also write simple Python expressions using
Boolean operators:


``` {.programlisting .language-markup}
pytest -k "parse and not num"
```


This will execute all tests that contain `parse` but not
`num` in their item IDs.

### Stop soon: -x, \--maxfail



When doing large-scale refactorings, you might not know beforehand how
or which tests are going to be affected. In those situations, you might
try to guess which modules will be affected
and start running tests for those. But, often, you end up breaking more
tests than you initially estimated and quickly try to stop the test
session by hitting `CTRL+C` when everything starts to fail
unexpectedly. 

 

In those situations, you might try using the `--maxfail=N`
command-line flag, which stops the test session automatically after
`N` failures or errors, or the shortcut `-x`, which
equals `--maxfail=1`.


``` {.programlisting .language-markup}
pytest tests/core -x
```


This allows you to quickly see the first failing test and deal with the
failure. After fixing the reason for the failure, you can continue
running with `-x` to deal with the next problem.

If you find this brilliant, you don\'t want to skip the next section!

### Last failed,  failed first: \--lf, \--ff



Pytest always remembers tests that failed in
previous sessions, and can reuse that information to skip right to the
tests that have failed previously. This is excellent news if you are
incrementally fixing a test suite after a large refactoring, as
mentioned in the previous section.

You can run the tests that failed before by passing the `--lf`
flag (meaning last failed[*):*]


``` {.programlisting .language-markup}
pytest --lf tests/core
...
collected 6 items / 4 deselected
run-last-failure: rerun previous 2 failures
```


When used together with `-x` (`--maxfail=1`) these
two flags are refactoring heaven:


``` {.programlisting .language-markup}
pytest -x --lf
```


This lets you start executing the full suite and then pytest stops at
the first test that fails. You fix the code, and execute the same
command line again. Pytest starts right at the failed test, and goes on
if it passes (or stops again if you haven\'t yet managed to fix the code
yet). It will then stop at the next failure. Rinse and repeat until all
tests pass again.

Keep in mind that it doesn\'t matter if you execute another subset of
tests in the middle of your refactoring; pytest always remembers which
tests failed,  regardless of the command-line executed.

If you have ever done a large refactoring and had to keep track of which
tests were failing so that you didn\'t waste your time running the test
suite over and over again, you will definitely appreciate this boost in
your productivity.

 

Finally, the `--ff` flag is similar to `--lf`, but
it will reorder your tests so the previous failures are run
[**first**], followed by the tests that passed or that were not
run yet:


``` {.programlisting .language-markup}
pytest -x --lf
======================== test session starts ========================
...
collected 6 items
run-last-failure: rerun previous 2 failures first
```


### Output capturing: -s and \--capture



Sometimes, developers leave `print` statements laying around
by mistake, or even on purpose, to be used later for debugging. Some
applications also may write to `stdout`  or `stderr`
as part of their normal operation or logging.

All that output would make understanding the test suite display much
harder. For this reason, by default, pytest captures all output written
to `stdout` and `stderr` automatically. 

Consider this function to compute a hash of some text given to it that
has some debugging code left on it:


``` {.programlisting .language-markup}
import hashlib

def commit_hash(contents):
    size = len(contents)
    print('content size', size)
    hash_contents = str(size) + '\0' + contents
    result = hashlib.sha1(hash_contents.encode('UTF-8')).hexdigest()
    print(result)
    return result[:8]
```


We have a very simple test for it:


``` {.programlisting .language-markup}
def test_commit_hash():
    contents = 'some text contents for commit'
    assert commit_hash(contents) == '0cf85793'
```


When executing this test, by default, you won\'t see the output of the
`print` calls:


``` {.programlisting .language-markup}
pytest tests\test_digest.py

======================== test session starts ========================
...

tests\test_digest.py .                                         [100%]

===================== 1 passed in 0.03 seconds ======================
```


 

 

 

 

That\'s nice and clean.

But those print statements are there to help you understand and debug
the code, which is why pytest will show the captured output if the
test [**fails**].

Let\'s change the contents of the hashed text but not the hash itself.
Now, pytest will show the captured output in a separate section after
the error traceback:


``` {.programlisting .language-markup}
pytest tests\test_digest.py

======================== test session starts ========================
...

tests\test_digest.py F                                         [100%]

============================= FAILURES ==============================
_________________________ test_commit_hash __________________________

    def test_commit_hash():
        contents = 'a new text emerges!'
>       assert commit_hash(contents) == '0cf85793'
E       AssertionError: assert '383aa486' == '0cf85793'
E         - 383aa486
E         + 0cf85793

tests\test_digest.py:15: AssertionError
----------------------- Captured stdout call ------------------------
content size 19
383aa48666ab84296a573d1f798fff3b0b176ae8
===================== 1 failed in 0.05 seconds ======================
```


Showing the captured output on failing tests is very handy when running
tests locally, and even more so when running tests on CI.


#### Disabling capturing with -s



While running your tests locally, you might
want to disable output capturing to see what messages are being printed
in real-time, or whether the capturing is interfering with other
capturing your code might be doing.

In those cases, just pass `-s` to pytest to completely disable
capturing:


``` {.programlisting .language-markup}
pytest tests\test_digest.py -s
======================== test session starts ========================
...

tests\test_digest.py content size 29
0cf857938e0b4a1b3fdd41d424ae97d0caeab166
.

===================== 1 passed in 0.02 seconds ======================
```


#### Capture methods with \--capture



Pytest has two methods to capture output.
Which method is used can be chosen with the `--capture`
command-line flag:


-   `--capture=fd`: captures output
    at the [**file-descriptor level**], which means that all
    output written to the file descriptors, 1 (stdout) and 2 (stderr),
    is captured. This will capture output even from C extensions and is
    the default.
-   `--capture=sys`: captures output written directly to
    `sys.stdout` and `sys.stderr` at the Python
    level, without trying to capture system-level file descriptors.


Usually, you don\'t need to change this, but in a few corner cases,
depending on what your code is doing, changing the capture method might
be useful.

For completeness, there\'s also `--capture=no`, which is the
same as `-s`.


### Traceback modes and locals: \--tb, \--showlocals



Pytest will show a complete traceback of a
failing test, as expected from a testing framework. However, by default,
it doesn\'t show the standard traceback that most Python programmers are
used to; it shows a different traceback:


``` {.programlisting .language-markup}
============================= FAILURES ==============================
_______________________ test_read_properties ________________________

 def test_read_properties():
 lines = DATA.strip().splitlines()
> grids = list(iter_grids_from_csv(lines))

tests\test_read_properties.py:32:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests\test_read_properties.py:27: in iter_grids_from_csv
 yield parse_grid_data(fields)
tests\test_read_properties.py:21: in parse_grid_data
 active_cells=convert_size(fields[2]),
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

s = 'NULL'

 def convert_size(s):
> return int(s)
E ValueError: invalid literal for int() with base 10: 'NULL'

tests\test_read_properties.py:14: ValueError
===================== 1 failed in 0.05 seconds ======================
```


This traceback shows only a single line of code and file location for
all frames in the traceback stack, except for the first and last one,
where a portion of the code is shown as well (in bold).

While some might find it strange at first, once you get used to it you
realize that it makes spotting the cause of the error much simpler. By
looking at the surrounding code of the start and end of the traceback,
you can usually understand the error better. I suggest that you try to
get used to the default traceback provided by pytest for a few weeks;
I\'m sure you will love it and never look back.

If you don\'t like pytest\'s default traceback, however, there are other
traceback modes, which are controlled by the `--tb` flag. The
default is `--tb=auto` and was shown previously. Let\'s have a
look at an overview of the other modes in the next sections.


#### --tb=long



This mode will show a [**portion of the code
for**][**all**][**frames**] of failure
tracebacks, making it quite verbose: 


``` {.programlisting .language-markup}
============================= FAILURES ==============================
_______________________ t________

    def test_read_properties():
        lines = DATA.strip().splitlines()
>       grids = list(iter_grids_from_csv(lines))

tests\test_read_properties.py:32:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

lines = ['Main Grid,48,44', '2nd Grid,24,21', '3rd Grid,24,null']

    def iter_grids_from_csv(lines):
        for fields in csv.reader(lines):
>       yield parse_grid_data(fields)

tests\test_read_properties.py:27:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fields = ['3rd Grid', '24', 'null']

    def parse_grid_data(fields):
        return GridData(
            name=str(fields[0]),
            total_cells=convert_size(fields[1]),
>       active_cells=convert_size(fields[2]),
        )

tests\test_read_properties.py:21:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

s = 'null'

    def convert_size(s):
>       return int(s)
E       ValueError: invalid literal for int() with base 10: 'null'

tests\test_read_properties.py:14: ValueError
===================== 1 failed in 0.05 seconds ======================
```


#### --tb=short



This mode will show a single line of code
from all the frames of the failure traceback, providing short and
concise output:


``` {.programlisting .language-markup}
============================= FAILURES ==============================
_______________________ test_read_properties ________________________
tests\test_read_properties.py:32: in test_read_properties
    grids = list(iter_grids_from_csv(lines))
tests\test_read_properties.py:27: in iter_grids_from_csv
    yield parse_grid_data(fields)
tests\test_read_properties.py:21: in parse_grid_data
    active_cells=convert_size(fields[2]),
tests\test_read_properties.py:14: in convert_size
    return int(s)
E   ValueError: invalid literal for int() with base 10: 'null'
===================== 1 failed in 0.04 seconds ======================
```


 

#### --tb=native



This mode will output the exact same
traceback normally used by Python to report exceptions and is loved by
purists:


``` {.programlisting .language-markup}
_______________________ test_read_properties ________________________
Traceback (most recent call last):
  File "X:\CH2\tests\test_read_properties.py", line 32, in test_read_properties
    grids = list(iter_grids_from_csv(lines))
  File "X:\CH2\tests\test_read_properties.py", line 27, in iter_grids_from_csv
    yield parse_grid_data(fields)
  File "X:\CH2\tests\test_read_properties.py", line 21, in parse_grid_data
    active_cells=convert_size(fields[2]),
  File "X:\CH2\tests\test_read_properties.py", line 14, in convert_size
    return int(s)
ValueError: invalid literal for int() with base 10: 'null'
===================== 1 failed in 0.03 seconds ======================
```


#### --tb=line



This mode will output a single line per
failing test, showing only the exception message and the file location
of the error:


``` {.programlisting .language-markup}
============================= FAILURES ==============================
X:\CH2\tests\test_read_properties.py:14: ValueError: invalid literal for int() with base 10: 'null'
```


This mode might be useful if you are doing a
massive refactoring and except a ton of failures anyway, planning to
enter [**refactoring-heaven mode**] with
the `--lf -x` flags afterwards.

#### --tb=no 



This does not show any traceback or failure
message at all, making it also useful to run the suite first to get a
glimpse of how many failures there are, so that you can start using
`--lf -x` flags to fix tests step-wise:


``` {.programlisting .language-markup}
tests\test_read_properties.py F                                [100%]

===================== 1 failed in 0.04 seconds ======================
```


 

 

 

 

#### --showlocals (-l)



Finally, while this is not a traceback mode
flag specifically, `--showlocals` (or `-l` as
shortcut) augments the traceback modes by showing a list of the [**local
variables and their values**] when using `--tb=auto`,
`--tb=long`, and `--tb=short` modes.

For example, here\'s the output of `--tb=auto` and
`--showlocals`:


``` {.programlisting .language-markup}
_______________________ test_read_properties ________________________

    def test_read_properties():
        lines = DATA.strip().splitlines()
>       grids = list(iter_grids_from_csv(lines))

lines      = ['Main Grid,48,44', '2nd Grid,24,21', '3rd Grid,24,null']

tests\test_read_properties.py:32:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests\test_read_properties.py:27: in iter_grids_from_csv
    yield parse_grid_data(fields)
tests\test_read_properties.py:21: in parse_grid_data
    active_cells=convert_size(fields[2]),
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

s = 'null'

    def convert_size(s):
>       return int(s)
E       ValueError: invalid literal for int() with base 10: 'null'

s          = 'null'

tests\test_read_properties.py:14: ValueError
===================== 1 failed in 0.05 seconds ======================
```


Notice how this makes it much easier to see where the bad data is coming
from: the `'3rd Grid,24,null'` string that is being read from
a file at the start of the test.

`--showlocals` is extremely useful both when running your
tests locally and in CI, being a firm favorite. Be careful, though, as
this might be a security risk: local variables might expose passwords
and other sensitive information, so make sure to transfer tracebacks
using secure connections and be careful to make them public.
 

### Slow tests with --durations


At the start of a project,  your test suite
is usually blazingly fast, running in a few seconds, and life is good.
But as projects grow in size, so do their test suites, both in the
number of tests and the time it takes for them to run.

Having a slow test suite affects productivity, especially if you follow
TDD and run tests all the time. For this reason, it is healthy to
periodically take a look at your longest running tests and perhaps
analyze whether they can be made faster: perhaps you are using a large
dataset in a place where a much smaller (and faster) dataset would do,
or you might be executing redundant steps that are not important for the
actual test being done. 

When that happens, you will love the `--durations=N` flag.
This flag provides a summary of the `N` longest running tests,
or uses zero to see a summary of all tests:


``` {.programlisting .language-markup}
pytest --durations=5

...
===================== slowest 5 test durations ======================
3.40s call CH2/tests/test_slow.py::test_corner_case
2.00s call CH2/tests/test_slow.py::test_parse_large_file
0.00s call CH2/tests/core/test_core.py::test_type_checking
0.00s teardown CH2/tests/core/test_parser.py::test_parse_expr
0.00s call CH2/tests/test_digest.py::test_commit_hash
================ 3 failed,  7 passed in 5.51 seconds =================
```


This output provides invaluable information when you start hunting for
tests to speed up.

Although this flag is not something that you will use daily, because it
seems that many people don\'t know about it, it is worth mentioning.

### Extra test summary: -ra



Pytest shows rich traceback information on
failing tests. The extra information is great, but the actual footer is
not very helpful in identifying which tests have actually failed:


``` {.programlisting .language-markup}
...
________________________ test_type_checking _________________________

    def test_type_checking():
>       assert 0
E       assert 0

tests\core\test_core.py:12: AssertionError
=============== 14 failed,  17 passed in 5.68 seconds ================
```


 

 

 

 

The `-ra` flag can be passed to produce a nice summary with
the full name of all failing tests at the end of the session:


``` {.programlisting .language-markup}
...
________________________ test_type_checking _________________________

    def test_type_checking():
>       assert 0
E       assert 0

tests\core\test_core.py:12: AssertionError
====================== short test summary info ======================
FAIL tests\test_assert_demo.py::test_approx_simple_fail
FAIL tests\test_assert_demo.py::test_approx_list_fail
FAIL tests\test_assert_demo.py::test_default_health
FAIL tests\test_assert_demo.py::test_default_player_class
FAIL tests\test_assert_demo.py::test_warrior_short_description
FAIL tests\test_assert_demo.py::test_warrior_long_description
FAIL tests\test_assert_demo.py::test_get_starting_equiment
FAIL tests\test_assert_demo.py::test_long_list
FAIL tests\test_assert_demo.py::test_starting_health
FAIL tests\test_assert_demo.py::test_player_classes
FAIL tests\test_checks.py::test_invalid_class_name
FAIL tests\test_read_properties.py::test_read_properties
FAIL tests\core\test_core.py::test_check_options
FAIL tests\core\test_core.py::test_type_checking
=============== 14 failed,  17 passed in 5.68 seconds ================
```


This flag is particularly useful when running the suite from the command
line directly, because scrolling the terminal to find out which tests
failed can be annoying.

The flag is actually `-r`, which accepts a number of
single-character arguments:


-   `f` (failed): `assert` failed
-   `e` (error): raised an unexpected exception
-   `s` (skipped): skipped (we will get to this in the next
    lab)
-   `x` (xfailed): expected to fail, did fail (we will get to
    this in the next lab)
-   `X` (xpassed): expected to fail, but passed (!) (we will
    get to this in the next lab)
-   `p` (passed): test passed
-   `P` (passed with output): displays captured output even
    for passing tests (careful -- this usually produces a lot of output)
-   `a`: shows all the above, except for `P`; this
    is the [**default**] and is usually the most useful.


 

The flag can receive any combination of the above. So, for example, if
you are interested in failures and errors only, you can pass
`-rfe` to pytest.

In general, I recommend sticking with `-ra`, without thinking
too much about it and you will obtain the most benefits.

Configuration: pytest.ini 
--------------------------

Users can customize some pytest behavior using[]{#id325536777
.indexterm} a configuration file called `pytest.ini`. This
file is usually placed at the root of the repository and contains a
number of configuration values that are applied to all test runs for
that project. It is meant to be kept under version control and committed
with the rest of the code.

The format follows a simple ini-style format with all pytest-related
options under a `[pytest]` section. For more details, go
to:<https://docs.python.org/3/library/configparser.html>.


``` {.programlisting .language-markup}
[pytest]
```


The location of this file also defines what pytest calls the [**root
directory**] (`rootdir`): if present, the directory
that contains the configuration file is considered the root directory.

The root directory is used for the following:


-   To create the tests node IDs
-   As a stable location to store information about the project (by
    pytest plugins and features)


Without the configuration file, the root directory will depend on which
directory you execute pytest from and which arguments are passed (the
description of the algorithm can be found
here: <https://docs.pytest.org/en/latest/customize.html#finding-the-rootdir>).
For this reason, it is always recommended to have a
`pytest.ini` file in all but the simplest projects, even if
empty.


### Note

Always define a `pytest.ini` file, even if empty.


If you are using `tox`, you can put a `[pytest]`
section in the traditional `tox.ini` file and it will work
just as well. For more details, go
to:<https://tox.readthedocs.io/en/latest/>:


``` {.programlisting .language-markup}
[tox]
envlist = py27,py36
...

[pytest]
# pytest options
```


This is useful to avoid cluttering your repository root with too many
files, but it is really a matter of preference.

Now, we will take a look at more common configuration options. More
options will be introduced in the coming labs as we cover new
features.


### Additional command-line: addopts



We learned some very useful command-line
options. Some of them might become personal favorites, but having to
type them all the time would be annoying.

The `addopts` configuration option can be used instead to
always add a set of options to the command line:


``` {.programlisting .language-markup}
[pytest]
addopts=--tb=native --maxfail=10 -v
```


With that configuration, typing the following:


``` {.programlisting .language-markup}
pytest tests/test_core.py
```


Is the same as typing:


``` {.programlisting .language-markup}
pytest --tb=native --max-fail=10 -v tests/test_core.py
```


Note that, despite its name, `addopts` actually inserts the
options [**before**] other options typed in the command line.
This makes it possible to override most options in `addopts`
when passing them in explicitly. 

For example, the following code will now
display [**auto **]tracebacks, instead of native ones, as
configured in `pytest.ini`:


``` {.programlisting .language-markup}
pytest --tb=auto tests/test_core.py
```


 

 

### Customizing a collection



By default, pytest collects tests using this
heuristic:


-   Files that match `test_*.py` and `*_test.py`
-   Inside test modules, functions that match `test*` and
    classes that match `Test*`
-   Inside test classes, methods that match `test*`


This convention is simple to understand and works for most projects, but
they can be overwritten by these configuration options:


-   `python_files`: a list of patterns to use to collect test
    modules
-   `python_functions`: a list of patterns to use to collect
    test functions and test methods
-   `python_classes`: a list of patterns to use to collect
    test classes


Here\'s an example of a configuration file changing the defaults:


``` {.programlisting .language-markup}
[pytest]
python_files = unittests_*.py
python_functions = check_*
python_classes = *TestSuite
```



### Note

The recommendation is to only use these configuration options for legacy
projects that follow a different convention, and stick with the defaults
for new projects. Using the defaults is less work and avoids confusing
other collaborators.


### Cache directory: cache\_dir



The `--lf` and `--ff` options shown[]{#id325541444
.indexterm} previously are provided by an internal plugin named
`cacheprovider`, which saves data on a directory on disk so it
can be accessed in future sessions. This directory by default is located
in the [**root directory**] under the name
`.pytest_cache`. This directory should never be committed to
version control.

If you would like to change the location of that directory, you can use
the `cache_dir` option. This option also expands environment
variables automatically:


``` {.programlisting .language-markup}
[pytest]
cache_dir=$TMP/pytest-cache
```


### Avoid recursing into directories: norecursedirs



pytest by default will recurse over all
subdirectories of the arguments given on the command line. This might
make test collection take more time than desired when recursing into
directories that never contain any tests, for example:


-   virtualenvs
-   Build artifacts
-   Documentation
-   Version control directories


pytest by default tries to be smart and will not recurse inside folders
with the patterns `.*`, `build`, `dist`,
`CVS`, `_darcs`, `{arch}`,
`*.egg`, `venv`. It also tries to detect virtualenvs
automatically by looking at known locations for activation scripts.

The `norecursedirs` option can be used to override the default
list of pattern names that pytest should never recurse into:


``` {.programlisting .language-markup}
[pytest]
norecursedirs = artifacts _build docs
```


You can also use the `--collect-in-virtualenv` flag to skip
the `virtualenv` detection.

In general, users have little need to override the defaults, but if you
find yourself adding the same directory over and over again in your
projects, consider opening an issue. For more details
(<https://github.com/pytest-dev/pytest/issues/new>).

### Pick the right place by default: testpaths



As discussed previously, a common directory structure is [*out-of-source
layout*], with tests separated from[]{#id325023584
.indexterm} the application/library code in a `tests` or
similarly named directory. In that layout it is useful to use the
`testpaths` configuration option:


``` {.programlisting .language-markup}
[pytest]
testpaths = tests
```


This will tell pytest where to look for tests when no files,
directories, or node ids are given in the command line, which might
speed up test collection. Note that you can configure more than one
directory, separated by spaces.

 

 

### Override options with -o/\--override



Finally, a little known feature is that you
can override any configuration option directly in the command-line using
the `-o` /`--override` flags. This flag can be
passed multiple times to override more than one option:


``` {.programlisting .language-markup}
pytest -o python_classes=Suite -o cache_dir=$TMP/pytest-cache
```



Summary 
-------------------------


In this lab, we covered how to use `virtualenv` and
`pip` to install pytest. After that, we jumped into how to
write tests, and the different ways to run them so that we can execute
just the tests we are interested in. We had an overview of how pytest
can provide rich output information for failing tests for different
built-in data types. We learned how to use `pytest.raises` and
`pytest.warns` to check exceptions and warnings, and
`pytest.approx` to avoid common pitfalls when comparing
floating point numbers. Then, we briefly discussed how to organize test
files and modules in your projects. We also took a look at some of the
more useful command-line options so that we can get productive right
away. Finally, we covered how `pytest.ini` files are used for
persistent command-line options and other configuration.

In the next lab, we will learn how to use marks to help us skip
tests on certain platforms, how to let our test suite know when a bug is
fixed in our code or in external libraries, and how to group sets of
tests so that we can execute them selectively in the command line. After
that, we will learn how to apply the same checks to different sets of
data to avoid copying and pasting testing code.
