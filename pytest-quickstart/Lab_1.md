<img align="right" src="../logo.png">


Lab 1. Introducing pytest
--------------------------------------



Automated testing is considered to be an indispensable tool and
methodology for producing high-quality software. Testing should be a
part of every professional software developer\'s toolbox, yet at the
same time, it is considered by many to be a boring and repetitive part
of the job. But that does not have to be the case when you use pytest as
your testing framework.

This course will introduce you to various key features and will teach how
to use pytest effectively in your day-to-day coding tasks right from the
first lab, focusing on making you productive as quickly as possible.
Writing tests should then become a joy, rather than a boring part of the
job.

We will start by taking a look at the reasons why automated testing is
important. I will also try to convince you that it is not something that
you should have simply because it is the right thing to do. Automated
testing is something that you will want to have because it will make
your job much [**easier and more enjoyable**]. We will take a
glimpse at Python\'s standard `unittest` module, and introduce
pytest and why it carries so much more punch while also being dead
simple to get started with. Then, we will cover how to write tests, how
to organize them into classes and directories, and how to use pytest\'s
command line effectively. From there, we will take a look at how to use
marks to control skipping tests or expecting test failures, how to use
custom marks to your advantage, and how to test multiple inputs using
the same testing code parameterization to avoid copy/pasting code. This
will help us to learn how to manage and reuse testing resources and
environments using one of pytest\'s most loved features: fixtures. After
that, we will take a tour of some of the more popular and useful plugins
from the vast plugin ecosystem that pytest has to offer. Finally, we
will approach the somewhat more advanced topic of how to gradually
convert `unittest` based test suites into the pytest style in
order to take advantage of its many benefits in existing code bases.

 

In this lab, we will take a quick look at why we should be testing,
the built-in `unittest` module, and an overview of pytest.
Here is what will be covered:


-   Why spend time writing tests?
-   A quick look at the `unittest` module
-   Why pytest?


Let\'s get started by taking a step back and thinking about why writing
tests is considered to be so important.



Why spend time writing tests?  
------------------------------------------------


Testing programs manually is natural; writing automated tests is not.

Programmers use various techniques when
learning to code or when dabbling in new
technologies and libraries. It is common to write short snippets, follow
a tutorial, play in the REPL, or even use Jupyter
(<http://jupyter.org/>). Often, this involves manually verifying the
results of what is being studied by using print statements or plotting
graphics. This is easy, natural, and a perfectly valid way of learning
new things.

This pattern, however, should not be carried over to professional
software development. Professional software is not simple; on the
contrary, it is usually very complex. Depending on how well designed a
system is, parts can be intertwined in strange ways, with the addition
of new functionality potentially breaking another, apparently unrelated,
part of the system. Fixing a bug might cause another bug to spring up
somewhere else.

How can you make sure that a new functionality is working or that a bug
has been squashed for good? Just as important, how can you ensure that,
by fixing or introducing a new feature, another part of the system will
not be broken?

The answer is by having a healthy and embracing suite of automated
tests, also called a test suite.

A test suite is, simply put, code that tests your code. Usually, they
create one or more necessary resources and call the application code
under test. They then assert that the results are as expected. Besides
being executed on the developer\'s machine, in most modern setups, they
are run continuously for example, every hour or every commit by an
automated system such as Jenkins. Because of this, adding tests for a
piece of code means that, from now on, it will be tested again and again
as features are added and bugs are fixed.

 

Having automated tests means that you can make changes to a program and
immediately see if those changes have broken part of the system, acting
as a safety net for developers. Having a good test suite is very
liberating: you no longer fear improving a piece of code that was
written 8 years ago, and if you make any mistakes, the test suite will
tell you. You can add a new feature and be confident that it will not
break any other parts of the system that you did not expect. It is
absolutely essential to be able to convert a large library from Python 2
to 3 with confidence, or make large-scale refactorings. By adding one or
more automated tests that reproduce a bug, and prove that you fixed it,
you ensure the bug won\'t be reintroduced by refactoring or another
coding error later down the road.

Once you get used to enjoying the benefits of having a test suite as a
safety net, you might even decide to write tests for APIs that you
depend on but know that developers don\'t have tests for: it is a rare
moment of professional pride to be able to produce failing tests to the
original developers to prove that their new release is to blame for a
bug and not your code.

Having a well written and in-depth test suite will allow you to make
changes, big or small, with confidence, and help you sleep better at
night.



#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `~/work/pytest-quickstart/code` folder.


A quick look at the unittest module 
-----------------------------------------------------



Python comes with the built-in `unittest` module, which is a
framework to write automated tests based on
JUnit, a unit testing framework for Java. You create tests by
subclassing from `unittest.TestCase` and defining methods that
begin with `test`. Here\'s an example of a typical minimal
test case using `unittest`:


``` {.programlisting .language-markup}
    import unittest
    from fibo import fibonacci

    class Test(unittest.TestCase):

        def test_fibo(self):
            result = fibonacci(4)
            self.assertEqual(result, 3)

    if __name__ == '__main__':
        unittest.main()
```


The focus of this example is on showcasing the test itself, not the code
being tested, so we will be using a simple `fibonacci`
function. The Fibonacci sequence is an infinite sequence of positive
integers where the next number in the sequence is found by summing up
the two previous numbers. Here are the first 11 numbers:


``` {.programlisting .language-markup}
1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...
```


 

 

 

 

Our `fibonacci` function receives an `index` of the
fibonacci sequence, computes the value on the fly, and returns it.

To ensure the function is working as expected, we call it with a value
that we know the correct answer for (the fourth element of the Fibonacci
series is 3), then the `self.assertEqual(a, b)` method is
called to check that `a` and `b` are equal. If the
function has a bug and does not return the expected result, the
framework will tell us when we execute it:


``` {.programlisting .language-markup}
    python3 -m venv .env
  source .env/bin/activate
    F
    ======================================================================
    FAIL: test_fibo (__main__.Test)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "test_fibo.py", line 8, in test_fibo
        self.assertEqual(result, 3)
    AssertionError: 5 != 3

    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    FAILED (failures=1)
```


It seems there\'s a bug in our `fibonacci` function and
whoever wrote it forgot that for `n=0` it should return
`0`. Fixing the function and running the test again shows that
the function is now correct:


``` {.programlisting .language-markup}
    python test_fibo.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s

    OK
```


This is great and is certainly a step in the right direction. But notice
that, in order to code this very simple check, we had to do a number of
things not really related to the check itself:


1.  Import `unittest`
2.  Create a class subclassing from `unittest.TestCase`


 


3.  Use `self.assertEqual()` to do the checking; there are a
    lot of `self.assert*` methods that should be used for all
    situations like `self.assertGreaterEqual` (for ≥
    comparisons), `self.assertLess` (for \< comparisons),
    `self.assertAlmostEqual` (for floating point comparisons),
    `self.assertMultiLineEqual()` (for multi-line string
    comparisons), and so on


The above feels like unnecessary boilerplate, and while it is certainly
not the end of the world, some people feel that the code is
non-Pythonic; code is written just to placate the framework into doing
what you need it to.

Also, the `unittest` framework doesn\'t provide much in
terms of batteries included to help you write
your tests for the real world. Need a temporary directory? You need to
create it yourself and clean up afterwards. Need to connect to a
PostgreSQL database to test a Flask application? You will need to write
the supporting code to connect to the database, create the required
tables, and clean up when the tests end. Need to share utility test
functions and resources between tests? You will need to create base
classes and reuse them through subclassing, which in large code bases
might evolve into multiple inheritance. Some frameworks provide their
own `unittest` support code (for example, Django,
<https://www.djangoproject.com/>), but those frameworks are rare.



Why pytest? 
-----------------------------



Pytest is a mature and full-featured testing
framework, from small tests to large scale functional tests for
applications and libraries alike.

Pytest is simple to get started with. To write tests, you don\'t need
classes; you can write simple functions that start with `test`
and use Python\'s built-in `assert` statement:


``` {.programlisting .language-markup}
    from fibo import fibonacci

    def test_fibo():
        assert fibonacci(4) == 3
```


That\'s it. You import your code, write a function, and use plain assert
calls to ensure they are working as you expect: no need to make a
subclass and use various `self.assert*` methods to do your
testing. And the beautiful thing is that it also provides helpful output
when an assertion fails:


``` {.programlisting .language-markup}
    pytest test_fibo2.py -q
    F                                                              [100%]
    ============================= FAILURES ==============================
    _____________________________ test_fibo _____________________________

        def test_fibo():
    >       assert fibonacci(4) == 3
    E       assert 5 == 3
    E        + where 5 = fibonacci(4)

    test_fibo2.py:4: AssertionError
    1 failed in 0.03 seconds
```


Notice that the values involved in the expression and the code around it
are displayed to make it easier to understand the error.

Pytest not only makes it [**simple to write tests**], it has
many [**command-line options that increase productivity**],
such as running just the last failing tests, or running a specific group
of tests by name or because they\'re specially marked.

Creating and managing testing resources is an important aspect that is
often overlooked in tutorials or overviews of testing frameworks. Tests
for real-world applications usually need complex setups, such as
starting a background worker, filling up a database, or initializing a
GUI. Using pytest, those complex test resources can be managed by a
powerful mechanism called
[**fixtures**]. Fixtures are simple to use but very powerful at
the same time, and many people refer to them as [*pytest\'s killer
feature.*] They will be shown in detail in Lab 4 *Fixtures*

Customization is important, and pytest goes a step further by defining a
very powerful [**plugin**] system. Plugins can change several
aspects of the test run, from how tests are executed to providing new
fixtures and capabilities to make it easy to test many types of
applications and frameworks. There are plugins that execute tests in a
random order each time to ensure tests are not changing global state
that might affect other tests, plugins that repeat failing tests a
number of times to weed out flaky behavior, plugins that show failures
as they appear instead of only at the end of the run, and plugins that
execute tests across many CPUs to speed up the suite. There are also
plugins that are useful when testing Django, Flask, Twisted, and Qt
applications, further plugins for the acceptance testing of web
applications using Selenium. The number of external[]{#id325533913
.indexterm} plugins is really staggering: at the time of writing, there
are over 500 pytest plugins available to be installed and used right
away (<http://plugincompat.herokuapp.com/>).

To summarize pytest:


-   You use plain `assert` statements to write your checks,
    with detailed reporting
-   pytest has automatic test discovery
-   It has fixtures to manage test resources
-   It has many, many plugins to expand its built-in capabilities and
    help test a huge number of frameworks and applications
-   It runs `unittest` based test suites out of the box and
    without any modifications, so you can gradually migrate existing
    test suites


For these reasons, many consider pytest to be a Pythonic approach to
writing tests in Python. It makes it easy to write simple tests and is
powerful enough to write very complex functional tests. Perhaps more
importantly, though, pytest makes testing fun.

Writing automated tests, and enjoying their many benefits, will become
natural with pytest.



Summary 
-------------------------



In this lab, we covered why writing tests is important in order to
produce high-quality software and to give you the confidence to
introduce changes without fear. After that, we took a look at the
built-in `unittest` module and how it can be used to write
tests. Finally, we had a quick introduction to pytest, discovered how
simple it is to write tests with it, looked at its key features, and
also looked at the vast quantity of third-party plugins that cover a
wide range of use cases and frameworks.

In the next lab, we will learn how to install pytest, how to write
simple tests, how to better organize them into files and directories
within your project, and how to use the command line effectively.
