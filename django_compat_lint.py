from optparse import OptionParser
import os

try:
    from importlib import import_module
except ImportError:
    try:
        from django.utils.importlib import import_module
    except ImportError:
        raise


RULES = []

usage = 'usage: %prog OPTIONS file1 file2 ...'

MESSAGE_TEMPLATE = '%s:%s:%s:%s'


def register_rules(rules_file):
    global RULES
    module = import_module('rules.%s' % rules_file)
    RULES += module.rules


def setup():
    self_dir = os.path.abspath(os.path.dirname(__file__))
    rules_dir = os.path.join(self_dir, 'rules')
    for f in os.listdir(rules_dir):
        if f != '__init__.py' and '.pyc' not in f:
            register_rules(f.replace('.py', ''))


def format_messages(messages, line, filename, level):
    return [MESSAGE_TEMPLATE % (level, filename, line, message) for \
            message in messages]


def check_file(filename, enabled_rules, options):
    messages = []
    lines = open(os.path.abspath(filename)).readlines()
    for i, line in enumerate(lines):
        for rule in enabled_rules:
            warnings, errors, info = rule(line, filename, options)
            if options.level in ('warnings', 'all'):
                messages += format_messages(warnings, i + 1, filename, 'WARNING')
            if options.level in ('errors', 'all'):
                messages += format_messages(errors, i + 1, filename, 'ERROR')
            if options.level in ('info', 'all'):
                messages += format_messages(info, i + 1, filename, 'INFO')
    return messages


if __name__ == '__main__':
    setup()

    parser = OptionParser(usage)
    parser.add_option('-l', '--level', dest='level',
                      action='store',
                      type='string',
                      default='errors',
                      help="Level of messages to display. 'errors', 'warnings', 'info' or 'all'. Default 'errors'.")

    for rule in RULES:
        parser.add_option(rule['long_option'],
                          dest=rule['dest'], action=rule['action'],
                          help=rule['help'])

    options, args = parser.parse_args()

    enabled_rules = []
    for rule in RULES:
        if rule['enabled'](options):
            enabled_rules.append(rule['callback'])

    files = []
    if not args:
        files += [path for path in os.listdir(os.getcwd()) if \
                  (os.path.isfile(path) and '.pyc' not in path)]
    else:
        for path in args:
            if os.path.isdir(os.path.abspath(path)):
                subdir = os.path.abspath(path)
                files += [os.path.join(subdir, f) for f in os.listdir(subdir) if \
                          (os.path.isfile(os.path.join(subdir, f)) and '.pyc' not in f)]
            else:
                files.append(path)
    
    messages = []
    for filename in files:
        messages += check_file(filename, enabled_rules, options)
        
    for message in messages:
        print message
