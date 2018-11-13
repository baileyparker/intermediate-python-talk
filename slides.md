## Pythonic Code

As a preview of what's to come, here is how you would check if a number is in
a range in any other language:

```python
if 3 <= num and num < 10:
    pass
```

And here's how you do it in Python:

```python
if 3 <= num < 10:
    pass
```

## Tuples

Tuples are immutable lists. Once they are created, they can't be changed. They
are used *everywhere* in Python.

```python-repl
>>> exam = ('Final Exam', 91)

>>> exam[0]
>>> exam[1]

# Try to change our grade
>>> exam[1] = 100

# A tuple with one element
>>> singleton = ('one element',)
```

Tuples can be returned from functions.

```python
def compute_statistics(nums):
    return average(nums), max(nums), stddev(nums)
```

### Unpacking

Tuples can also be **unpacked** into separate variables.

```python-repl
>>> name, grade = exam
>>> name
>>> grade
```

You can also **unpack** multiple layers of tuples (or any iterable).

```python-repl
>>> player = ('Shaquille', 'O\'Neal', (7, 1))

>>> first_name, last_name, (feet, inches) = player
>>> first_name
>>> last_name
>>> feet
>>> inches
```

### An Aside on Naming

Tuples are often convenient ways of quickly packaging related values together.
However, indexing them by number (ex. `exam[0]`) may be confusing. Instead, we
can name a tuple's elements by using `namedtuple`.

```run:python
from collections import namedtuple

Height = namedtuple('Height', 'feet inches')
Player = namedtuple('Player', 'first_name last_name height')
```

```python-repl
>>> player = Player('Shaquille', 'O\'Neal', Height(7, 1))
>>> player.first_name
>>> player.height.feet

# namedtuples behave like regular tuples (so they can be unpacked)
>>> first_name, last_name, height = player
>>> last_name
>>> height.inches
```

<!---------------------------------------------------------------------------->

## Strings

Python has many commonly used string manipulation functions.

```python-repl
>>> names = 'Foo, Bar, Baz'
>>> names.split(', ')
>>> ' and '.join(names.split(', '))

>>> time_line = 'Time: 23.4'
>>> time_line.startswith('Time: ')

# Combining with unpacking provides a powerful way to parse strings
>>> _, seconds = time_line.split(': ')
>>> seconds = float(seconds)
>>> seconds
```

### Formatting

Python 3.6 introduced f-strings, a convenient way to interpolate variables into
strings.

```python-repl
>>> name = 'Forrest Gump'
>>> birth_year = 1944
>>> skills = ['ping pong', 'running']

>>> f'{name} was born in {birth_year} and is good at: {skills}'
```

<!---------------------------------------------------------------------------->

## Fun with Arguments

Arguments can be given default values.

```run:python
def discount_price(price, discount=0.5):
    return price * discount
```

```python-repl
>>> discount_price(10)
>>> discount_price(10, 0.75)
```

### Default Arguments

Just be careful! Default arguments are only evaluated once (when the function
is defined), *not* at every function call.

```run:python
def record_discount(discount, previous_discounts=[]):
    previous_discounts.append(discount)
    return previous_discounts
```

```python-repl
>>> record_discount(0.5)
>>> record_discount(0.75)
```

The better approach uses `None` instead:

```python
def record_discount(discount, previous_discounts=None):
    if previous_discounts is None:
        previous_discounts = []

    previous_discounts.append(discount)
    return previous_discounts
```

### Naming Arguments

Arguments can and should be passed by name to reduce ambiguity. Compare the
following:

```python
# What do these parameters mean?
search_tweets('@SwiftOnSecurity', 20, True, False)

# Much more clear...
search_tweets('@SwiftOnSecurity', retweets=False, popular=True, limit=20)
```

```python
def search_tweets(query, limit, popular, retweets=True):
    pass
```

Using names makes your code more clear and also doesn't require you to remember
parameter order!

### Requiring Argument Names

You can even require that arguments be passed by name by using `*`.

```run:python
def search_tweets(query, *, limit, popular, retweets=True):
    pass

search_tweets('@SwiftOnSecurity', 20, True, False)
```

### Making a `sum` Function

Let's use our newfound knowledge of arguments to make a function that sums its
arguments.

```python
sum(1, 2, 3)  # 6
sum(0)        # 0
```

```python
def sum(start, *nums):
    total = start

    for num in nums:
        total += num

    return total
```

This new `*` syntax allows us to collect any extra arguments passed to the
function. We can also use it to expand iterables as if they were passed as
individual arguments.

```python
nums = [1, 2, 3]
sum(*nums)
# is the same as...
sum(1, 2, 3)
```

This syntax even works for tuple unpacking!

```python-repl
>>> first, *rest = [1, 2, 3]
>>> first
>>> rest
```

<!---------------------------------------------------------------------------->

## Functional Tools

In fact, Python already has a built-in `sum` function that is much more
powerful.

```python-repl
>>> sum([1, 2, 3])

# The second parameter is the starting value to add values to
>>> sum([[1, 2, 3], [4, 5, 6]], [])
```

Python provides many more functional tools:

```python-repl
>>> min([10, 2, 22, 15])
>>> max([10, 2, 22, 15])
>>> sorted([10, 2, 22, 15])
>>> sorted([10, 2, 22, 15], reverse=True)
```

### On Richer Values

All of these functional tools allow you to specify a `key` which tells the
function what value to compare.

```python-repl
>>> Graded = namedtuple('Graded', 'name grade')
>>> grades = [Graded('Midterm', 80), Graded('Final', 90), Graded('Project', 0)]
>>> min(grades, key=lambda x: x.grade)
>>> max(grades, key=lambda x: x.grade)
>>> sorted(grades, key=lambda x: x.grade, reverse=True)
```

`lambda`s are convenient ways of expressing one line functions. The above one
is equivalent to:

```python
def get_grade(x):
    return x.grade
```

### Iteration

If you were to port iteration over a list from another language to Python, you
may arrive at:

```python
for i in range(len(nums)):
    print(nums[i])
```

But we don't like explicit indices, because they are error prone. Instead, we
can just iterate over the list itself:

```python
for num in nums:
    print(num)
```

If we need the index, we use `enumerate`:

```python
for i, num in enumerate(nums):
    print(i, num)
```

### Iteration of Multiple Lists

What if we want to consider values from two lists at once? You may be inclined
to write:

```python
for i, name in enumerate(students):
    print(f'{name} got a {grades[i]} in the class')
```

Instead, we use `zip` to pair values from iterables together:

```python
for name, grade in zip(students, grades):
    print(f'{name} got a {grade} in the class')
```

<!---------------------------------------------------------------------------->

## Iterables

Python is built around the idea of iterables and provides many standard library
and language features for interacting with and creating them.

We've already seen that `list` is an iterable and `dict` is an iterable, which
also provides other ways of iteration (`.items()` and `.values()`). Most
collections in Python are iterables. Even files are iterables!

We know how to iterate through collections, but let's see how we can build our
own iterables.

### Generators

Generators are a powerful tool for building efficient iterables. Consider
replicating Python's `range()`:

```run:python
def our_range(stop):
    num = 0
    nums = []

    while num < stop:
        print(f'adding {num}')
        nums.append(num)
        num += 1

    return nums
```

What's the problem with this approach?

```run:python
for num in our_range(3):
    print(f'received {num}')
```

#### Deferred Computation

Generators use the `yield` keyword to stop their execution and hand a value
to the iterator's consumer.

```run:python
def our_range(stop):
    num = 0

    while num < stop:
        print(f'yielding {num}')
        yield num
        num += 1
```

Now, the numbers are generated on the fly:

```run:python
for num in our_range(3):
    print(f'received {num}')
```

### Expressions

This syntax can be expanded to create terse expressions of `list`s, `dict`s,
and even generators.

```python-repl
>>> [x * 2 for x in range(4)]
>>> sum(x * 2 for x in range(4))
>>> {x: x * 2 for x in range(4)}
```

<!---------------------------------------------------------------------------->

## OOP

In many ways, object orientation in Python looks exactly like other languages
you may be familiar with like Java. There are a few subtle differences, though.

```run:python
class Course:
    def __init__(self, number, name, instructor):
        self.number = number
        self.name = name
        self.instructor = instructor
        self._student_grades = {}

    def add_student_grade(self, student, grade):
        self._student_grades[student] = grade

    def curve(self, amount):
        for student, grade in self._student_grades.items():
            self.add_student_grade(student, grade + amount)
```

Notably, Python uses a lot of `__x__` methods (we call them dunder methods).
Above, we see that the constructor is called `__init__`. Additionally, all
methods take an explicit `self` parameter, which is similar to `this` in C++ or
Java.

Python has no visibility controls and instead prefers the convention of
prefixing private/protected properties with an `_`.

### Usage

```python-repl
>>> csf = Course('601.229', 'CSF', 'Peter')
>>> csf.number
>>> csf.add_student_grade('Johnny Hopkins', 85)
```

### Inheritance

Python supports traditional Java-like inheritance (as well as multiple
inheritance, which we won't delve into).

```python
class PassFailCourse(Course):
    def add_student_grade(self, student, *, passed):
        super().add_student_grade(student, 100 if passed else 0)
```

We use `super()` to access methods from ancestor classes. Other methods (in
this example, `__init__` and `curve`) are inherited as we would expect.

### Static Methods

In Python methods on a class are called **class methods**, and we denote them
by using a decorator.

```python
class Course:
    # ...

    @classmethod
    def retrieve_from_db(cls, number):
        # Lookup in your database ...

        return cls(number, name, instructor)


csf = Course.retrieve_from_db('601.229')
```

### An Aside on Decorators

Decorators are a powerful Python feature that allow you to augment function
behavior. They are functions that are passed another function and return a new
function with modified behavior.

```run:python
def cache(func):
    func._cache = {}

    def wrapped(url):
        if url not in func._cache:
            func._cache[url] = func(url)

        return func._cache[url]

    return wrapped
```

We then can use `cache` as a decorator:

```run:python
@cache
def slow_web_request(url):
    print('requesting page')

    # ...

    return f'page: {url}'
```

This is equivalent to:

```python
slow_web_request = cache(slow_web_request)
```

### Decorators Demo

```python-repl
>>> slow_web_request('http://www.google.com')

>>> slow_web_request('http://www.apple.com')

>>> slow_web_request('http://www.apple.com')
```

### An Aside on Decorators (The Full Story)

```python
from functools import wraps

def cache(func):
    func._cache = {}

    @wraps(func)
    def wrapped(*args, **kwargs):
        frozen_args = (args, tuple(sorted(kwargs.items())))

        if frozen_args not in func._cache:
            func._cache[frozen_args] = func(*args, **kwargs)

        return func._cache[frozen_args]

    return wrapped
```

### More Dunder Methods

There are
[a ton of dunder methods](https://docs.python.org/3/reference/datamodel.html#special-method-names)
you can define on your classes.

```python
class Person:
    def __init__(self, first_name, last_name, age):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age

    def __hash__(self):
        return self.first_name, self.last_name

    def __eq__(self, other):
        if not isinstance(other, Person):
            return False

        return self.first_name == other.first_name \
            and self.last_name == other.last_name \
            and self.age == other.age

    def __lt__(self, other):
        return self.age < other.age

    def __str__(self):
        return f'{self.last_name}, {self.first_name} is {self.age} years old'
```

### Cutting out the Boilerplate

Defining all of these dunder methods can be tedious, so Python 3.7 introduced
**dataclasses**, which give a much more terse way to express classes.

```python
from dataclasses import dataclass, field

@dataclass
class Person:
    first_name: str = field(compare=False)
    last_name: str = field(compare=False)
    age: int = field(hash=False)
```

<!---------------------------------------------------------------------------->

## `Enum`s

Enums allow you to replace magic constants with efficient, named placeholders.

```run:python
from enum import Enum, auto

class Color(Enum):
    RED = auto()
    BLUE = auto()
    PURPLE = auto()
```

```python-repl
>>> Color.RED
>>> Color.RED.name
>>> Color.RED == Color.BLUE
>>> list(Color)
```

<!---------------------------------------------------------------------------->

## Exceptions

Python prefers a "do first, ask for forgiveness later" approach to exceptional
cases at runtime. This has the benefit of being safe from data races.

`IndexError` and `KeyError` are common when indexing into a sequence or
accessing a key in a `dict`-like data structure.

```python-repl
>>> cities = ['Boston', 'New York City', 'Los Angeles']
>>> cities[4]

>>> capitals = {'Maryland': 'Annapolis', 'Connecticut': 'Hartford'}
>>> capitals['Hawaii']
```

### Handling Exceptions

We handle exceptions in Python using a `try`/`except` (and maybe an
`else`/`finally`).

`ValueError` is commonly used when an argument is in an unexpected format.

```python
def get_birth_year():
    while True:
        try:
            birth_year = int(input('Enter birth year: '))
        except ValueError:
            pass
        else:
            if 1900 <= birth_year <= 2018:
                return birth_year
```

<!---------------------------------------------------------------------------->

## More Data Structures

The Python standard library has a plethora of useful data structures.

Many common tasks in Python can be written as one-liners by combining these
data structures in clever ways.

### `set`s

```python-repl
>>> unique_nums = set([5, 8, 4, 5, 8])
>>> unique_nums

>>> unique_nums.add(6)
>>> 6 in unique_nums

>>> len(unique_nums)

>>> unique_nums - set([5, 4])

>>> unique_nums | set([8, 4])
```

Sets (like most other data structures) can even be created by providing an
iterable (like a generator):

```python-repl
>>> set(x * 2 for x in range(8))
```

### `defaultdict`

Behaves like a `dict`, but returns a default value when a key is not found.

```run:python
from collections import defaultdict

names = ['Michael', 'Dwight', 'Jim', 'Pam', 'Meredith']
names_by_first_letter = defaultdict(list)

for name in names:
    names_by_first_letter[name[0]].append(name)

print(names_by_first_letter)
```

Without it, we'd have to write something like:

```python
names_by_first_letter = {}

for name in names:
    try:
        letter_names = names_by_first_letter[name[0]]
    except KeyError:
        letter_names = names_by_first_letter[name[0]] = []
    finally:
        letter_names.append(name)
```

#### Another `defaultdict` example

When implementing Dijkstra's algorithm, a `defaultdict` is a convenient way to
store the distances from the source node.


```python
import sys

distance_from_source = defaultdict(lambda: sys.maxsize)
distance_from_source[source] = 0
```

#### When to not use `defaultdict`

If we just want to return a default value (and not also store that default
value), we can use a regular `dict`:

```python-repl
>>> nicknames = {'Robert': 'Bob', 'Kate': 'Katherine'}

>>> nicknames.get('Brenda', 'Brenda')
>>> nicknames
```

### `Counter`

To keep track of counts of just about anything (including other iterables) use
`Counter`.

```python-repl
>>> from collections import Counter

>>> spellings = Counter(['color', 'colour', 'color', 'color', 'colour'])
>>> spellings.most_common()

>>> spellings.update(['color', 'color'])
>>> spellings.most_common(1)
```

### `deque`

`list` has constant-time append and pop (from the end). If you need constant
time operations at both ends (a queue, instead of a stack), use a `deque`.

```python-repl
>>> from collections import deque

>>> checkout = deque(['oranges', 'blueberries'])

>>> checkout.append('strawberries')
>>> checkout

>>> checkout.appendleft('eggs')
>>> checkout

>>> checkout.popleft()
```

<!---------------------------------------------------------------------------->

## File I/O

File handling (and resource management) in Python is a breeze thanks to
**context managers**. These provide automatic cleanup of resources by using a
`with` statement.

```python
# By default, files are opened for reading
with open('essay.txt') as f:
    essay = f.read()
```

This is almost equivalent to the following, but with one important distinction:
**exception handling!**

```python
f = open('essay.txt')

essay = f.read()
# What if an exception happens here?

f.close()
```

### Examples

```python
# By default, files are opened for reading
with open('essay.txt') as f:
    essay = f.read()

translated = translate(essay, from_language='english',
                       to_language='french')

# 'w' truncates the file, then opens it for writing
with open('essay_translated.txt', 'w') as f:
    print(translated, file=f)
```

Reading a file line-by-line is also straightforward.

```python
# Each line in urls.txt contains a url
with open('urls.txt') as f:
    for url in f:
        download_file(url)
```

### CSV

Python makes reading CSVs super simple.

```python
import csv

with open('games.csv') as f:
    for home_team, away_team, score in csv.reader(f):
        print(f'{away_team} @ {home_team}: {score}')
```

### Gzip

And handling compressed data is just requires a slight modification.

```python
import csv
import gzip

with gzip.open('games.csv.gz') as f:
    for home_team, away_team, score in csv.reader(f):
        print(f'{away_team} @ {home_team}: {score}')
```

### Pickle Serialization

Python provides a serialization method that works out of the box for every
standard library class and almost every class you'll create:

```python
import pickle

with open('dump.pkl', 'wb') as f:
    pickle.dump(f, my_object)

# Then later...
with open('dump.pkl', 'rb') as f:
    my_object = pickle.load(f)
```

### JSON Serialization

JSON serialization can be done in an almost identical way.

```python
import json

with open('dump.json', 'w') as f:
    json.dump(f, my_dict)

# Then later...
with open('dump.json', 'r') as f:
    my_dict = json.load(f)
```

JSON can be dumped/loaded to a string with `json.dumps()` and `json.loads()`.

<!---------------------------------------------------------------------------->

## Paths

Python 3.4 added a new API for handling file system paths in a cross-platform
manner.

```python
from pathlib import Path

# Finds all files of the form logs/*.log
log_files = (Path.cwd() / 'logs').glob('*.log')
# If files have form 20181112.log, builds a list of the timestamps
log_timestamps = [p.stem for p in log_files]

data_dir = Path.cwd() / 'dir'

# We can even open files given a path
train_file = (data_dir / 'train').open()
dev_dev = (data_dir / 'dev').open()
test_test = (data_dir / 'test').open()
```

<!---------------------------------------------------------------------------->

## Multiprocessing

If you have some computationally expensive process run on an iterable, Python's
standard library makes it easy to distribute it across your computer's cores.

```python
for x in inputs:
    print(long_computation(x))
```

For an effortless speedup:

```python
from multiprocessing import Pool

with Pool() as pool:
    for x in pool.map(long_computation, inputs):
        print(x)
```

<!---------------------------------------------------------------------------->

## Command Line Arguments

Python is often used for building command line utilities, so parsing arguments
is a common task. Fortunately, the standard library provides an incredibly
comprehensive library for doing most of the heavy lifting.

```python
from argparse import ArgumentParser, FileType

parser = ArgumentParser(description='processes some input files')

parser.add_argument('files', type=FileType('r'), nargs='+', help='input files')
parser.add_argument('--mode', choices=list(Mode), default=Mode.CONCAT)
parser.add_argument('--limit', type=int, default=10,
                    help='limit the number of lines')
parser.add_argument('-v', dest='verbose', action='store_true')

# Parses arguments like:
#   foo.txt bar.txt -v --limit 100
#
args = parser.parse_args()

# A list of already opened files passed as CLI args
args.files

# The mode enum
args.mode

# The limit passed (or the default)
args.limit
```

Learning how to use `argparse` is a key Python skill.

<!---------------------------------------------------------------------------->

## Unit Testing

Python's standard library also makes it really simple to test your code. You
have no excuse not to!

```python
from my_package import Calculator
from unittest import main, TestCase


class TestCalculator(TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_add(self):
        self.assertEqual(4, self.calculator.add(2, 2))

    def test_divide_by_zero(self):
        with self.assertRaises(DivisionByZeroError):
            self.calculator.divide(2, 0)


if __name__ == '__main__':
    main()
```

<!---------------------------------------------------------------------------->

## Web Scraping

We'll combine everything that we've learned to build a tool that uses
`requests` and `bs4` to check if a person is still alive (according to
Wikipedia).

```shell
$ python3 -m pip install pipenv
$ pipenv install requests bs4
```

<!---------------------------------------------------------------------------->

## Final Thoughts

  - As with any skill, the only way to improve is to practice!
  - Find small tasks that need automating or menial things and try to write a
    script to help you
  - Try out Python libraries like Django, Flask, and PyTorch for more domain
    specific experience
  - Watch talks by Raymond Hettinger (he's a Python core developer and a
    fantastic speaker)
