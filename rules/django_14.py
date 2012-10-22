def check_operationalerror(line, filename, options):
    errors = []
    if ('mysql' in line or 'MySQL' in line) and 'OperationalError' in line:
        errors.append('MySQLdb.OperationalError is no longer used in Django. Use django.db.utils.DatabaseError instead.')
    return [], errors, []


def check_template_loaders(line, filename, options):
    errors = []
    if 'django.core' in line and 'template_loaders' in line:
        errors.append('django.core.template_loaders alias has been removed; use django.template.loader instead.')
    return [], errors, []


def check_filestorage_mixin(line, filename, options):
    errors = []
    if 'open' in line and 'mixin=' in line:
        errors.append("The 'mixin' argument to Storage.open() has been removed.")
    return [], errors, []


def check_urlconf_imports(line, filename, options):
    warnings = []
    if 'django.conf.urls.defaults' in line:
        warnings.append('django.conf.urls.defaults is deprecated; use django.conf.urls instead.')
    return warnings, [], []


def check_setup_environ(line, filename, options):
    warnings = []
    if 'setup_environ' in line:
        warnings.append('setup_environ() is deprecated; set DJANGO_SETTINGS_MODULE or use settings.configure() instead.')
    return warnings, [], []


def check_filter_attrs(line, filename, options):
    errors = []
    if '.is_safe' in line or '.needs_autoescape' in line:
        errors.append("The 'is_safe' and 'needs_autoescape' attributes of filters are deprecated; use keyword arguments to filter() instead.")
    return [], errors, []


def check_raw_post_data(line, filename, options):
    warnings = []
    if 'raw_post_data' in line:
        warnings.append("The 'raw_post_data' attribute of HttpRequest is deprecated; use the 'body' attribute instead.")
    return warnings, [], []


def check_django_14(line, filename, options):
    warnings = []
    info = []
    errors = []

    for check in (check_operationalerror, check_template_loaders,
                  check_filestorage_mixin, check_urlconf_imports,
                  check_setup_environ, check_filter_attrs,
                  check_raw_post_data):
        warn, err, inf = check(line, filename, options)
        warnings += warn
        info += inf
        errors += err

    return warnings, errors, info


rules = [
    {'long_option': '--django-14',
     'action': 'store_true',
     'dest': 'django_14',
     'help': 'Check for changes and deprecations in Django 1.4.',
     'callback': check_django_14,
     'enabled': lambda options: options.django_14,}
]
