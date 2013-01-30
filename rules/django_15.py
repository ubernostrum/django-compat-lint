def check_password_hasher(line, filename, options):
    warnings = []
    if 'PASSWORD_HASHERS' in line:
        warnings.append('Custom password hashers are now required to accept Unicode strings.')
    return warnings, [], []


def check_simplejson(line, filename, options):
    warnings = []
    if 'simplejson' in line:
        warnings.append("Use of the standard-library 'json' module is strongly recommended instead of simplejson.")
    return warnings, [], []


def check_transactiontestcase(line, filename, options):
    warnings = []
    if 'TransactionTestCase' in line:
        warnings.append("TransactionTestCase behavior has changed; check that tests do not rely on hard-coded primary keys, sequence resets, or on the database being reset before each test run.")
    return warnings, [], []


def check_cleaned_data(line, filename, options):
    warnings = []
    if 'if' in line and 'cleaned_data' in line:
        warnings.append("Checking the existence of cleaned_data to determine validity is no longer supported. Test on is_valid() instead.")
    return warnings, [], []


def check_slugify(line, filename, options):
    warnings = []
    if 'django.template.defaultfilters' in line and 'slugify' in line:
        warnings.append("slugify() is now available as a standalone function in django.utils.text.")
    return warnings, [], []


def check_localflavor(line, filename, options):
    warnings = []
    if 'django.contrib' in line and 'localflavor' in line:
        warnings.append("django.contrib.localflavor is deprecated in favor of the django-localflavor package.")
    return warnings, [], []


def check_depth(line, filename, options):
    warnings = []
    if 'select_related' in line and 'depth' in line:
        warnings.append("The 'depth' parameter to select_related is deprecated. Use field names instead.")
    return warnings, [], []


def check_django_15(line, filename, options):
    warnings = []
    info = []
    errors = []

    for check in (check_password_hasher, check_simplejson,
                  check_transactiontestcase, check_cleaned_data,
                  check_slugify, check_localflavor,
                  check_depth):
        warn, err, inf = check(line, filename, options)
        warnings += warn
        info += inf
        errors += err

    return warnings, errors, info


rules = [
    {'long_option': '--django-15',
     'action': 'store_true',
     'dest': 'django_15',
     'help': 'Check for changes and deprecations in Django 1.5.',
     'callback': check_django_15,
     'enabled': lambda options: options.django_14,}
]
