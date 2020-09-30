<img align="right" src="../logo.png">

**APPENDIX 1**

### Virtual Environments

Python virtual environments enable you to set up a Python sandbox with its
own set of packages separate from the system site-packages in which to work.
There are many reasons to use virtual environments, such as if you have
multiple services running with the same Python installation, but with different
packages and package version requirements. In addition, you might find it
handy to keep the dependent package requirements separate for every Python
project you work on. Virtual environments let you do that.

As of Python 3.3, the venv virtual environment module is included as part of
the standard library. However, some problems with venv have been reported
on some versions of Linux. If you have any trouble with venv, use virtualenv
instead. Just remember to pip install virtualenv first.

Here’s how to set up a virtual environment in macOS and Linux:


##### Step 1


##### $ python3 -m venv env_name

##### $ source env_name/bin/activate

```
(env_name)$
... do yourwork...
```


##### Step 2
#### (env_name) $ deactivate

In Windows, there’s a change to the activate line:

```
C:/> python3 -m venv env_name
C:/> env_name/Scripts/activate.bat
(env_name) C:/>
... do your work ...
(env_name) C:/> deactivate
```

I usually put the virtual environment directory, env_name, directly in my
project’s top directory. I’ve also seen two additional installation methods that
are interesting and could work for you:

1. Put the virtual environment in the project directory (as was done in the
previous code), but name the env directory something consistent, such
as venv or .venv. The benefit of this is that you can put venv or .venv in your
global .gitignore file. The downside is that the environment name hint in
the command prompt just tells you that you are using a virtual environ-
ment, but not which one.

2. Put all virtual environments into a common directory, such as ~/venvs/.
Now the environment names will be different, letting the command prompt
be more useful. You also don’t need to worry about .gitignore, since it’s not
in your project tree. Finally, this directory is one place to look if you forget
all of the projects you’re working on.

Remember, a virtual environment is a directory with links back to the python.exe
file and the pip.exe file of the site-wide Python version it’s using. But anything
you install is installed in the virtual environment directory, and not in the
global site-packages directory. When you’re done with a virtual environment,
you can just delete the directory and it completely disappears.

I’ve covered the basics and common use case of venv. However, venv is a flexible
tool with many options. Be sure to check out python -m venv --help. It may pre-
emptively answer questions you may have about your specific situation. Also,
the Python docs on venv are worth reading if you still have questions.

1. https://docs.python.org/3/library/venv.html



