test_filenames_seen = []

def check_transaction_use(line, filename, options):
    warnings = []
    if 'transaction' in line:
        warnings.append('Transaction handling behavior has changed in 1.6; please review use of transactions.')
    return warnings, [], []


def check_tests_init(line, filename, options):
    errors = []
    global test_filenames_seen
    if '__init__' in filename and 'tests' in filename:
        if filename not in test_filenames_seen:
            errors.append("Django's test runner no longer finds tests in __init__.py files.")
            test_filenames_seen.append(filename)
    return [], errors, []


def check_user_override_in_tests(line, filename, options):
    warnings = []
    if 'override_settings' in line and 'AUTH_USER_MODEL' in line:
        warnings.append('You must now import your custom user model in test files which will swamp it in.')
    return warnings, [], []


def check_dates(line, filename, options):
    warnings = []
    if '.dates(' in line:
        warnings.append("Behavior of dates() has changed; please see release notes and investigate use of datetimes() instead.")
    return warnings, [], []


def check_date_hierarchy(line, filename, options):
    info = []
    if 'date_hierarchy' in line:
        info.append("date_hierarchy now uses datetimes() and requires USE_TZ and time zone definitions.")
    return [], [], info


def check_booleanfield_default(line, filename, options):
    warnings = []
    if 'BooleanField' in line and 'default' not in line:
        warnings.append('BooleanField no longer has an implicit default; set an explicit default if one is needed.')
    return warnings, [], []


def check_empty_qs(line, filename, options):
    errors = []
    if 'EmptyQuerySet(' in line:
        errors.append("EmptyQuerySet can't be directly instantiated; use a none() method of a manager instead.")
    return [], errors, []


def check_cycle_firstof(line, filename, options):
    info = []
    if '{% cycle' in line or '{% firstof' in line:
        info.append("The behavior of the 'cycle' and 'firstof' template tags will change by Django 1.8.")
    return [], [], info


def check_module_name(line, filename, options):
    warnings = []
    if '.module_name' in line:
        warnings.append("The meta 'module_name' attribute is deprecated; use 'model_name' instead.")
    return warnings, [], []


def check_get_query_set(line, filename, options):
    warnings = []
    if 'get_query_set(' in line or '.queryset(' in line:
        warnings.append("Methods which return querysets have all been standardized to 'get_queryset()'.")
    return warnings, [], []


def check_django_16(line, filename, options):
    warnings = []
    info = []
    errors = []

    for check in (check_transaction_use, check_tests_init,
                  check_user_override_in_tests, check_dates,
                  check_date_hierarchy, check_booleanfield_default,
                  check_empty_qs, check_cycle_firstof,
                  check_module_name, check_get_query_set):
        warn, err, inf = check(line, filename, options)
        warnings += warn
        info += inf
        errors += err

    return warnings, errors, info


rules = [
    {'long_option': '--django-16',
     'action': 'store_true',
     'dest': 'django_16',
     'help': 'Check for changes and deprecations in Django 1.6.',
     'callback': check_django_16,
     'enabled': lambda options: options.django_16,}
]
