<img align="right" src="../logo.png">

Lab 9. Testing Exceptions
----------------------------

Write tests which ensure exceptions are raised when expected.

[![](https://img.youtube.com/vi/eBO2FmoeLKw/0.jpg)](https://www.youtube.com/watch?v=eBO2FmoeLKw)

In the previous step we showed how to debug a problem. Let's show how to
write a test that *recreates* the problem -- *and* ensures our Python
code handles it correctly -- by using `pytest` exception assertions.

We'll then refactor the code to detect that situation and return `None`,
writing tests before doing the refactoring.

Testing Exceptions
==================

We start, as always, with a test.

We're adding a new test `test_no_primary_guardian` in `test_player.py`,
to detect the case when no guardians have been assigned:

```
import pytest
# ....
def test_no_primary_guardian(player_one):
    with pytest.raises(IndexError) as exc:
        player_one.primary_guardian
    assert 'list index out of range' == str(exc.value)
```

As we type the code above, don't forget to use autocomplete to let
PyCharm generate `import pytest` for you.

This test uses a special context manager facility in `pytest`, in which
you run a block of code that you expect to raise an exception, and let
`pytest` handle it. You test will *fail* if the exception is not raised.
The context manager optionally lets you add `as exc` to then do some
asserts after the block, about the nature of the exception value.

Return `None` Instead
=====================

x Perhaps we decide that raising an exception isn't a good pattern.
Instead, we want to detect if `self.guardians` is empty, and if so,
return `None`.

To start, let's...write a test. Or in this case, change that last test:

```
def test_construction(player_one):
    assert 'Tatiana' == player_one.first_name
    assert 'Jones' == player_one.last_name
    assert [] == player_one.guardians

def test_add_guardian(player_one, guardians):
    player_one.add_guardian(guardians[0])
    assert [guardians[0]] == player_one.guardians

def test_add_guardians(player_one, guardians):
    player_one.add_guardian(guardians[0])
    player_one.add_guardians((guardians[1], guardians[2]))
    assert list(guardians) == player_one.guardians

def test_primary_guardian(player_one, guardians):
    player_one.add_guardian(guardians[0])
    player_one.add_guardians((guardians[1], guardians[2]))
    assert guardians[0] == player_one.primary_guardian

def test_no_primary_guardian(player_one):
    assert player_one.primary_guardian is None

```

Good news, the test fails. Remember to remove the now-unused
`import pytest` via PyCharm's `Optimize Imports`.

We now change our implementation in `player.py` to correctly return
`None`. While we're at it, let's put a return type on
`primary_guardian`:

```
from dataclasses import dataclass, field
from typing import List, Iterable, Optional

from laxleague.guardian import Guardian

@dataclass
class Player:
    """ A lacrosse player in the league """

    first_name: str
    last_name: str
    guardians: List[Guardian] = field(default_factory=list)

    def add_guardian(self, guardian: Guardian):
        self.guardians.append(guardian)

    def add_guardians(self, guardians: Iterable[Guardian]):
        self.guardians.extend(guardians)

    @property
    def primary_guardian(self) -> Optional[Guardian]:
        return self.guardians[0] if self.guardians else None

```

Python type hinting uses `Optional` when the value might be `None`.

Our tests now pass which means we did the refactoring safely.
