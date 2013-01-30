django_compat_lint -- check Django compatibility of your code
===========================================================================

Django's API stability policy is nice, but there are still things that
change from one version to the next. Figuring out all of those things
when it's time to upgrade can be tediious and annoying as you flip
back and forth between the release notes and your code, or start
grepping for things in your code.

So why not automate it?

django_compat_lint, in the grand tradition of lint tools, is a simple
and extensible engine for going through files of code line by line,
applying some rules that look for potential problems, and then report
those problems. As the name suggests, it is geared toward checking a
Django codebase and finding potential issues you'd run into when
upgrading to a more recent Django.


How to use it
-------------

Put simply::

    python django_compat_lint.py [OPTIONS] [FILE1] [FILE2]...

``OPTIONS`` is a set of command-line options. There is one universal
command-line option, implemented as ``-l`` or ``--level``, specifying
the level of messages to report.  See below for a definition of the
message levels and what they mean.

Beyond that, different options (run ``-h`` or ``--help`` to see a
list) can be specified depending on what code-checking rules you have
available.

The output will be a series of messages, on stdout, each specifying
its level, the file it came from, the line of code it came from, and
the problem or suggestion that was noticed.

Two useful shortcuts are available for specifying files to check:

* If no files are specified, all ``.py`` files in the current working
  directory are checked.

* A path to a directory can be specified; all ``.py`` files in that
  directory will be checked.

Recursive checking involving ``os.walk()`` is left as an exercise for
someone to send a pull request for.


How it works
------------

django_compat_lint uses one or more sets of rules to check your
code. A rule is simply a callable; it will be given the line of code
to check, the name of the file that line came from, and an object
representing the command-line options being used. It should return a
3-tuple of ``(warnings, errors, info)``, which are the supported
levels of messages. Which levels are actually displayed is controlled
by a command-line flag; these levels should be used for:

``warning``
    Something that isn't going to immediately break the code, but may
    cause problems later. Deprecated APIs, for example, will issue
    warnings (since the APIs will still be usable for a couple Django
    versions).

``error``
    Something that is going to immediately break your code if you try
    to run under a newer Django version. APIs and modules which have
    been removed are typical examples of this.

``info``
   Something that doesn't and won't break your code, but is an
   outdated idiom or something which can be accomplished in a better
   way using more recent Django.


Registering rules
-----------------

Rules live in the ``rules/`` subdirectory, and a set of rules is simply
a Python module which exports a variable named ``rules``. This should
be a list of dictionaries, one per rule. Each dictionary should have
the following keys. The first five correspond exactly to the
same-named arguments to ``parser.add_option()`` in Python's
``optparse`` module (which implements the parsing of command-line
flags):

``long_option``
    The (long) command-line flag for this rule. To avoid conflicts,
    rules cannot use short flags.

``action``
    What action to take with the flag.

``dest``
   Similarly, where to store the value of the command-line flag.

``help``
    A brief description of the rule and what it checks, for help
    output.

The remaining keys are:

``callback``
    The callback which implements the rule.

``enabled``
    A callable which is passed the command-line options, and returns a
    boolean indicating, from those options, whether this rule is
    enabled.


A simple example
----------------

Suppose that a new version of Django introduces a model field type
called ``SuperAwesomeTextField``, which is just like ``TextField`` but
better. So people who are upgrading may want to change from
``TextField`` to ``SuperAwesomeTextField``. A simple rule for this
might live in a file named ``superawesomefield.py``. First, the
callback for the rule::

    def check_superawesomefield(line, filename, options):
        info = []
        if filename == 'models.py' and 'TextField' in line:
	    info.append('Consider using SuperAwesomeField instead of TextField.')
	return []. [], info

This checks for the filename 'models.py' since a model field change is
probably only applicable to models files. And it checks for use of the
model ``TextField``, by just seeing if that appears in the line of
code. More complex things might use regular expressions or other
tricks to check a line.

Since it's only ever going to give an "info"-level message, the
"warnings" and "errors" lists are just always empty.

Then, at the bottom of the file, the rule gets registered::

    rules = [
        {'option': '-a',
	 'long_option': '--superawesomefield',
	 'action': 'store_true',
	 'dest': 'superawesomefield',
	 'help': 'Check for places where SuperAwesomeField could be used.',
	 'callback': check_superawesomefield,
	 'enabled': lambda options: options.superawesomefield,}
    ]

And that's it -- the engine will pick up that rule, and enable it
whenever the appropriate command-line flag is used.