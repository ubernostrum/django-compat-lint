import re


DJANGO_UTILS_PATTERN = re.compile(r'(from django\.utils import |import django\.utils\.|from django\.utils\.)(?P<module>\w+)')


SAFE_UTILS_MODULES = [
    'cache',
    'encoding',
    'feedgenerator',
    'http',
    'safestring',
    'translation',
    'tzinfo',
]

DJANGO_14_UTILS = [
    '_os',
    'archive',
    'autoreload',
    'baseconv',
    'cache',
    'checksums',
    'copycompat',
    'crypto',
    'daemonize',
    'datastructures',
    'dateformat',
    'dateparse',
    'dates',
    'datetime_safe',
    'decorators',
    'dictconfig',
    'encoding',
    'feedgenerator',
    'formats',
    'functional',
    'hashcompat',
    'html',
    'html_parser',
    'http',
    'importlib',
    'ipv6',
    'itercompat',
    'jslex',
    'log',
    'module_loading',
    'numberformat',
    'regex_helper',
    'safestring',
    'simplejson',
    'six',
    'synch',
    'termcolors',
    'text',
    'timesince',
    'timezone',
    'translation',
    'tree',
    'tzinfo',
    'unittest',
    'version',
    'xmlutils',
]

UTILS_STDLIB_MAP = {
    'functional': 'functools',
    'simplejson': 'json',
    '_threading_local': 'threading',
    'thread_support': 'threading',
}


def check_utils(line, filename, options):
    warnings = []
    errors = []
    info = []
    module = None
    django_utils = DJANGO_UTILS_PATTERN.search(line)
    if django_utils and 'import' in line:
        module = django_utils.groupdict()['module']
        if module in SAFE_UTILS_MODULES:
            return warnings, errors, info
        if module not in DJANGO_14_UTILS:
            errors.append(
                'django.utils.%s does not exist in Django 1.4.' % module)
        if module in UTILS_STDLIB_MAP:
            info.append(
                'Use %s in stdlib instead of django.utils.%s.' % (
                    UTILS_STDLIB_MAP[module], module))
        if module != 'datastructures' and 'SortedDict' not in line:
            warnings.append(
                'django.utils.%s is not considered stable public API.' % module)
    return warnings, errors, info


rules = [
    {'option': '-u',
     'long_option': '--utils',
     'action': 'store_true',
     'dest': 'utils',
     'help': 'Check for unsafe use of django.utils.',
     'callback': check_utils,
     'enabled': lambda options: options.utils,}
]
