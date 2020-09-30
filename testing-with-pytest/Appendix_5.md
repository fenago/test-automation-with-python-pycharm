<img align="right" src="../logo.png">


**APPENDIX 5**

### xUnit Fixtures

In addition to the fixture model described in Lab 3, pytest Fixtures, pytest also supports xUnit style fixtures, which are similar to jUnit
for Java, cppUnit for C++, and so on.

Generally, xUnit frameworks use a flow of control that looks something
like this:

```
setup()
test_function()
teardown()
```

This is repeated for every test that will run. pytest fixtures can do anything you
need this type of configuration for and more, but if you really want to have setup()
and teardown() functions, pytest allows that, too, with some limitations.

### Syntax of xUnit Fixtures

xUnit fixtures include setup()/teardown() functions for module, function, class,
and method scope:

```
setup_module()/teardown_module()
```

These run at the beginning and end of a module of tests. They run once
each. The module parameter is optional.

```
setup_function()/teardown_function()
```
These run before and after top-level test functions that are not methods
of a test class. They run multiple times, once for every test function. The
function parameter is optional.

```
setup_class()/teardown_class()
```
These run before and after a class of tests. They run only once. The class
parameter is optional.

```
setup_method()/teardown_method()
```
These run before and after test methods that are part of a test class. They
run multiple times, once for every test method. The method parameter is
optional.


Here is an example of all the xUnit fixtures along with a few test functions:

```
appendices/xunit/test_xUnit_fixtures.py
def setup_module(module):
print(f'\nsetup_module() for {module.__name__}')
def teardown_module(module):
print(f'teardown_module() for {module.__name__}')
def setup_function(function):
print(f'setup_function() for {function.__name__}')
def teardown_function(function):
print(f'teardown_function() for {function.__name__}')
def test_1():
print('test_1()')
def test_2():
print('test_2()')
class TestClass:
@classmethod
def setup_class(cls):
print(f'setup_class() for class {cls.__name__}')
@classmethod
def teardown_class(cls):
print(f'teardown_class() for {cls.__name__}')
def setup_method(self, method):
print(f'setup_method() for {method.__name__}')
def teardown_method(self, method):
print(f'teardown_method() for {method.__name__}')
def test_3(self):
print('test_3()')
def test_4(self):
print('test_4()')
```

I used the parameters to the fixture functions to get the name of the module/func-
tion/class/method to pass to the print statement. You don’t have to use the
parameter names module, function, cls, and method, but that’s the convention.


Here’s the test session to help visualize the control flow:


##### Step 1


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/xunit

##### $ pytest -s test_xUnit_fixtures.py

```
============ test session starts =============
plugins: mock-1.6.0, cov-2.5.1
collected 4 items

test_xUnit_fixtures.py
setup_module() for test_xUnit_fixtures
setup_function() for test_1
test_1()
.teardown_function() for test_1
setup_function() for test_2
test_2()
.teardown_function() for test_2
setup_class() for class TestClass
setup_method() for test_3
test_3()
.teardown_method() for test_3
setup_method() for test_4
test_4()
.teardown_method() for test_4
teardown_class() for TestClass
teardown_module() for test_xUnit_fixtures

========== 4 passed in 0.01 seconds ==========
```

### Mixing pytest Fixtures and xUnit Fixtures

You can mix pytest fixtures and xUnit fixtures:

```
appendices/xunit/test_mixed_fixtures.py
import pytest

def setup_module():
print('\nsetup_module() - xUnit')

def teardown_module():
print('teardown_module() - xUnit')

def setup_function():
print('setup_function() - xUnit')

def teardown_function():
print('teardown_function() - xUnit\n')
```


```
@pytest.fixture(scope='module')
def module_fixture():

print('module_fixture() setup - pytest')
yield
print('module_fixture() teardown - pytest')

@pytest.fixture(scope='function')
def function_fixture():
print('function_fixture() setup - pytest')
yield
print('function_fixture() teardown - pytest')

def test_1(module_fixture, function_fixture):
print('test_1()')

def test_2(module_fixture, function_fixture):
print('test_2()')
```

You _can_ do it. But please don’t. It gets confusing. Take a look at this:


##### Step 2


##### $ cd /pytest-labs/testing-with-pytest/code/appendices/xunit

##### $ pytest -s test_mixed_fixtures.py

```
============ test session starts =============
plugins: mock-1.6.0, cov-2.5.1
collected 2 items

test_mixed_fixtures.py
setup_module() - xUnit
setup_function() - xUnit
module_fixture() setup - pytest
function_fixture() setup - pytest
test_1()
.function_fixture() teardown - pytest
teardown_function() - xUnit

setup_function() - xUnit
function_fixture() setup - pytest
test_2()
.function_fixture() teardown - pytest
teardown_function() - xUnit
module_fixture() teardown - pytest
teardown_module() - xUnit

========== 2 passed in 0.01 seconds ==========
```

In this example, I’ve also shown that the module, function, and method parameters
to the xUnit fixture functions are optional. I left them out of the function
definition, and it still runs fine.


### Limitations of xUnit Fixtures

Following are a few of the limitations of xUnit fixtures:

- xUnit fixtures don’t show up in -setup-show and -setup-plan. This might seem
    like a small thing, but when you start writing a bunch of fixtures and
    debugging them, you’ll love these flags.
- There are no session scope xUnit fixtures. The largest scope is module.
- Picking and choosing which fixtures a test needs is more difficult with
    xUnit fixtures. If a test is in a class that has fixtures defined, the test will
    use them, even if it doesn’t need to.
- Nesting is at most three levels: module, class, and method.
- The only way to optimize fixture usage is to create modules and classes
    with common fixture requirements for all the tests in them.
- No parametrization is supported at the fixture level. You can still use
    parametrized tests, but xUnit fixtures cannot be parametrized.

There are enough limitations of xUnit fixtures that I strongly encourage you
to forget you even saw this appendix and stick with normal pytest fixtures.


