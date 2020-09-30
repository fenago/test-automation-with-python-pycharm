
<img align="right" src="../logo.png">


Lab 7. Wrapping Up
--------------------


In the previous lab, we learned a number of techniques that can be
used to convert `unittest`-based suites to pytest, ranging
from simply starting using it as a runner, all the way to porting
complex existing functionality to a more pytest-friendly style.

This is the final lab in this quick-start guide, and we will discuss
the following topics:


-   An overview of what we have learned
-   The pytest community
-   Next steps 
-   Final summary



#### Pre-reqs:
- Google Chrome (Recommended)

#### Lab Environment
Al labs are ready to run. All packages have been installed. There is no requirement for any setup.

All exercises are present in `~/work/pytest-quickstart/code` folder.


Overview of what we have learned 
-----------------------------------

The following sections will summarize what we have learned in this course.


### Introduction


-   You should consider writing tests as your safety net. It will make
    you more confident in your work, allow you to refactor with
    confidence, and be certain that you are not breaking other parts of
    the system.
-   A test suite is a must-have if you are [**porting a Python 2 code
    base to Python 3**], as any guide will tell you,
    (<https://docs.python.org/3/howto/pyporting.html#have-good-test-coverage>).
-   It is a good idea to write tests for the [**external
    APIs**] you depend on, if they don\'t have automated tests.
-   One of the reasons pytest is a great choice for beginners is because
    it is easy to get started; write your tests using simple functions
    and `assert` statements. 


### Writing and running tests




-   Always use a [**virtual
    environment**] to manage your packages[]{#id325091930
    .indexterm} and dependencies. This advice goes for any Python
    project.
-   pytest [**introspection features**] make it easy to express
    your checks concisely; it is easy to compare dictionaries, text, and
    lists directly.
-   Check exceptions with `pytest.raises` and warnings with
    `pytest.warns`.
-   Compare floating-point numbers and arrays with
    `pytest.approx`.
-   Test organization; you can [**inline your tests**] with
    your application code or keep them in a separate directory.
-   Select tests with the `-k` flag:
    `-k test_something`.
-   Stop at the [**first failure**] with `-x`.
-   Remember the awesome [**refactoring duo**]:
    `--lf -x`.
-   Disable [**output capturing**] with `-s`.
-   Show the [**complete summary**] of test failures, xfails,
    and skips with `-ra`.
-   Use `pytest.ini` for [**per-repository
    configuration**].


### Marks and parametrization




-   [**Create marks**] in test functions[]{#id325092040
    .indexterm} and classes with the
    `@pytest.mark` decorator. To apply to
    [**modules**], use the `pytestmark` special
    variable.
-   Use `@pytest.mark.skipif`,
    `@pytest.mark.skip` and
    `pytest.importorskip("module")` to skip tests that are not
    applicable to the [**current environment**].
-   Use `@pytest.mark.xfail(strict=True)` or
    `pytest.xfail("reason")` to mark tests that are
    [**expected to fail**]. 
-   Use `@pytest.mark.xfail(strict=False)` to mark [**flaky
    tests**].
-   Use `@pytest.mark.parametrize` to quickly test code for
    [**multiple inputs**] and to test [**different
    implementations**] of the same interface.


 

 

### Fixtures




-   [**Fixtures**] are one of the main[]{#id325092179
    .indexterm} pytest features, used to [**share resources**]
    and provide easy-to-use [**test helpers**].
-   Use `conftest.py` files to [**share fixtures**]
    across test modules. Remember to prefer local imports to speed up
    test collection.
-   Use [**autouse**] fixtures to ensure every test in a
    hierarchy uses a certain fixture to perform a required setup or
    teardown action.
-   Fixtures can assume [**multiple
    scopes**]:`function`,`class`,`module`,
    and`session`. Use them wisely to reduce the total time of
    the test suite, keeping in mind that high-level fixture instances
    are shared between tests.
-   Fixtures can be [**parametrized**] using the
    `params` parameter of the `@pytest.fixture`
    decorator. All tests that use a parametrized fixture will be
    parametrized automatically, making this a very powerful tool.
-   Use `tmpdir` and `tmpdir_factory` to create
    empty directories.
-   Use `monkeypatch` to temporarily change attributes of
    objects, dictionaries, and environment variables. 
-   Use `capsys` and `capfd` to capture and verify
    output sent to standard out and standard error.
-   One important feature of fixtures is that they [**abstract way
    dependencies**], and there\'s a balance between
    using [**simple functions versus fixtures**]. 


### Plugins




-   Use`plugincompat` (<http://plugincompat.herokuapp.com/>)
    and PyPI (<https://pypi.org/>[) to
    search](https://pypi.org/) for
    new plugins.
-   Plugins are [**simple to install**]: install with
    `pip` and they are activated automatically.
-   There are a huge number of plugins available, for all needs.


### Converting unittest suites to pytest




-   You can start by switching to [**pytest
    as a runner**]. Usually, this can be done[]{#id325022589
    .indexterm} with [**zero changes**] in existing code.
-   Use `unittest2pytest` to convert `self.assert*`
    methods to plain `assert`.
-   Existing [**set-up**] and [**teardown**] code can
    be reused with a small refactoring using [**autouse**]
    fixtures.
-   Complex test utility [**hierarchies**] can be refactored
    into more [**modular fixtures**] while keeping the existing
    tests working.
-   There are a number of ways to approach migration: convert
    [**everything**] at once, convert tests as you
    [**change**] existing tests, or only use pytest for
    [**new**] tests. It depends on your test-suite size and
    time budget.



The pytest community 
--------------------------------------



Our community lives in the
`pytest-dev` organizations on GitHub
(<https://github.com/pytest-dev>) and BitBucket
(<https://bitbucket.org/pytest-dev>). The pytest repository
(<https://github.com/pytest-dev/pytest>) itself is hosted on GitHub,
while both GitHub and Bitbucket host a number of plugins. Members strive
to make the community as welcome and friendly to new contributors as
possible, for people from all backgrounds. We also have a mailing list
on `pytest-dev@python.org`, which everyone is welcome to join
(<https://mail.python.org/mailman/listinfo/pytest-dev>).

Most pytest-dev members reside in Western Europe, but we have members
from all around the globe, including UAE, Russia, India, and Brazil
(which is where I live).


### Getting involved



Because all pytest maintenance is completely
voluntary, we are always looking for people who would like to join the
community and help out, working in good faith with others[]{#id325091841
.indexterm} towards improving pytest and its plugins. There are a number
of ways to get involved:


-   Submit feature requests; we love to hear from users about new
    features they would like to see in pytest or plugins. Make sure to
    report them as issues to start a discussion
    (<https://github.com/pytest-dev/pytest/issues>). 
-   Report bugs: if you encounter a bug, please report it. We do our
    best to fix bugs in a timely manner.
-   Update documentation; we have many open issues related to
    documentation
    (<https://github.com/pytest-dev/pytest/issues?utf8=%E2%9C%93&q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3A%22status%3A+easy%22+label%3A%22type%3A+docs%22+>).
    If you like to help others and write good documents, this is an
    excellent opportunity to help out.
-   Implement new features; although the code base might appear daunting
    for newcomers, there are a number of features or improvements marked
    with an easy label
    (<https://github.com/pytest-dev/pytest/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3A%22status%3A+easy%22>),
    which is friendly to new contributors. Also, if you are unsure, feel
    free to ask!
-   Fix bugs; although pytest has more than 2,000 tests against itself,
    it has known bugs as any software. We are always glad to review pull
    requests for known bugs
    (<https://github.com/pytest-dev/pytest/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc+label%3A%22type%3A+bug%22>).
-   Spread your love on twitter by using the `#pytest` hash
    tag or mentioning `@pytestdotorg`. We also love to read
    blog posts about your experiences with pytest.
-   At many conferences, there are members of the community organizing
    workshops, sprints, or giving talks. Be sure to say hi!


It is easy to become a contributor; you need only to contribute a pull
request about a relevant code change, documentation, or bug-fix, and you
can become a member of the `pytest-dev` organization if you
wish. As a member, you can help answer, label, and close issues, and
review and merge pull requests. 

Another way to contribute is to submit new plugins to
`pytest-dev`, either on GitHub or BitBucket. We love when new
plugins are added to the organization, as this provides more visibility
and helps share maintenance with other members.

You can read our full contribution guide on the pytest website
(<https://docs.pytest.org/en/latest/contributing.html>).

### 2016 Sprint



In June 2016, the core group held a big
sprint in Freiburg, Germany. Over 20 participants attended, over six
days; the event was themed around implementing new features and fixing
issues. We had a ton of group discussions and lightning talks, taking a
one-day break to go hiking in the beautiful Black Forest.

The team managed to raise a successful Indiegogo campaign
(<https://www.indiegogo.com/projects/python-testing-sprint-mid-2016#/>),
aiming for US \$11,000 to reimburse travel costs, sprint venue, and
catering for the participants. In the end, we managed to raise over US
\$12,000, which shows the appreciation of users and companies that use
pytest.

It was great fun! We are sure to repeat it in the future, hopefully with
even more attendees.

 


Next steps 
----------------------------



After all we learned, you might be anxious to get started with pytest or
be eager to use it more frequently.

Here are a few ideas of the next steps you can take:


-   Use it at work; if you already use Python in your day job and have
    plenty of tests, that\'s the best way to start. You can start slowly
    by using pytest as a test runner, and use more pytest features at a
    pace you feel comfortable with.
-   Use it in your own open source projects: if you are a member or an
    owner of an open source project, this is a great way to get some
    pytest experience. It is better if you already have a test suite,
    but if you don\'t, certainly starting with pytest will be an
    excellent choice.
-   Contribute to open source projects; you might choose an open source
    project that has `unittest` style tests and decide to
    offer to change it to use pytest. In April 2015, the pytest
    community organized what was called Adopt pytest month
    (<https://docs.pytest.org/en/latest/adopt.html>), where open
    source projects paired up with community
    members to convert their test suites to pytest. The event was
    successful and most of those involved had a blast. This is a great
    way to get involved in another open source project and learn pytest
    at the same time.
-   Contribute to pytest itself; as mentioned in the previous section,
    the pytest community is very welcoming to new contributors. We would
    love to have you!



### Note

Some topics were deliberately left out of this course, as they are
considered a little advanced for a quick start, or because we couldn\'t
fit them into the book due to space constraints. 



-   tox (<https://tox.readthedocs.io/en/latest/>) is a generic virtual
    environment manager and command-line tool
    that can be used to test projects with multiple Python versions and
    dependencies. It is a godsend if you maintain projects that support
    multiple Python versions and environments. pytest and
    `tox` are brother projects and work extremely well
    together, albeit independent and useful for their own purposes.
-   Plugins: this course does not cover how to extend pytest with plugins,
    so if you are interested, be sure to check the plugins section
    (<https://docs.pytest.org/en/latest/fixture.html>) of the pytest
    documentation and look around for other plugins that can serve as an
    example. Also, be sure to checkout the examples section
    (<https://docs.pytest.org/en/latest/example/simple.html>) for
    snippets of advanced pytest customization.
-   Logging and warnings are two Python features that pytest has
    built-in support for and were not covered in detail in this course,
    but they certainly deserve a good look if you use those features
    extensively.



Final summary 
-------------------------------



So, we have come to the end of our quick start guide. In this course, we
had a complete overview, from using pytest on the command-line all the
way to tips and tricks to convert existing test suites to make use of
the powerful pytest features. You should now be comfortable using pytest
daily and be able to help others as needed.

You have made it this far, so congratulations! I hope you have learned
something and had fun along the way!
