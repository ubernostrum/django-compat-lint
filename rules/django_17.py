migration_filenames_seen = []

def check_migrations(line, filename, options):
    info = []
    global migration_filenames_seen
    if ('migrations' in filename) or \
           ('import' in line and 'south' in line):
        if filename not in migration_filenames_seen:
            info.append("Django now includes a migration framework. "
                        "Ensure your pre-existing migration files "
                        "do not conflict with this.")
            migration_filenames_seen.append(filename)
    return [], [], info


def check_allow_syncdb(line, filename, options):
    warnings = []
    if 'allow_syncdb' in line:
        warnings.append("Use of 'allow_syncdb' is deprecated in favor "
                        "of 'allow_migrate.")
    return warnings, [], []


def check_wsgi_handler(line, filename, options):
    errors = []
    if 'django.core.handlers.wsgi.WSGIHandler' in line:
        errors.append("Direct use of 'django.core.handlers.wsgi.WSGIHandler' "
                      "will now raise AppRegistryNotReady. Instead, use "
                      "django.core.wsgi.get_wsgi_application().")
    return [], errors, []


def check_appcommand(line, filename, options):
    errors = []
    if 'handle_app' in line and 'handle_app_config' not in line:
        errors.append("AppCommand subclasses must now implement the method "
                      "'handle_app_config()' instead of 'handle_app()'.")
    return [], errors, []


def check_db_manager(line, filename, options):
    warnings = []
    if 'db_manager' in line and 'using=None' in line:
        warnings.append("'db_manager(using=None)' behavior has changed and now "
                        "retains rather than overrides previous manual DB "
                        "routing choices.")
    return warnings, [], []


def check_remove_clear(line, filename, options):
    warnings = []
    if 'remove(' in line or 'clear(' in line:
        warnings.append("The behavior of the 'remove()' and 'clear()' methods "
                        "of related managers has changed. See the release notes.")
    return warnings, [], []


def check_select_for_update(line, filename, options):
    warnings = []
    if 'select_for_update(' in line:
        warnings.append("The 'select_for_update()' method now requires a "
                        "transaction or will raise an exception.")
    return warnings, [], []


def check_fileuploadhandler(line, filename, options):
    warnings = []
    if 'def' in line and 'new_file(' in line:
        warnings.append("The 'new_file()' method of file upload handlers now "
                        "must accept a 'content_type_extra' parameter.")
    return warnings, [], []


def check_abstract_user(line, filename, options):
    warnings = []
    if 'class' in line and 'AbstractUser' in line:
        warnings.append("AbstractUser no longer defines a 'get_absolute_url' "
                        "method. Define one yourself if it is required.")
    return warnings, [], []


def check_selectdatewidget(line, filename, options):
    errors = []
    if 'SelectDateWidget' in line and 'required' in line:
        errors.append("SelectDateWidget no longer supports a 'required' "
                      "argument. Use 'is_required' on the associated Field "
                      "instead.")
    return [], errors, []


def check_is_hidden(line, filename, options):
    warnings = []
    if 'is_hidden' in line and '=' in line:
        warnings.append("The 'is_hidden' property of widgets is now read-only. "
                        "Use 'input_type = hidden' on a Widget subcless to "
                        "create a hidden widget.")
    return warnings, [], []


def check_init_connection_state(line, filename, options):
    warnings = []
    if 'init_connection_state(' in line:
        warnings.append("The 'init_connection_state()' method of database "
                        "backends now executes in autocommit mode. Ensure "
                        "your backend is compatible with this.")
    return warnings, [], []


def check_auto_primary_key(line, filename, options):
    warnings = []
    if 'allows_primary_key_0' in line:
        warnings.append("The 'allows_primary_key_0' attribute has been renamed "
                        "to 'allows_auto_pk_0'. Check the release notes for "
                        "explanation of what it means.")
    return warnings, [], []


def check_language_supported(line, filename, options):
    errors = []
    if ('get_language_from_path(' in line or
        'get_supported_language_variant(' in line) and \
        'supported=' in line:
        errors.append("The 'get_language_from_path() and "
                      "get_supported_language_variant() functions no longer "
                      "accept the 'supported' argument.")
    return [], errors, []


def check_check(line, filename, options):
    errors = []
    if ('models' in filename or 'managers' in filename or
        'fields' in filename) and \
        'def check(' in line:
        errors.append("The system check framework now reserves the method name "
                      "check() on models, model fields and model managers. You "
                      "will need to rename any existing 'check()' methods.")
    return [], errors, []


def check_get_cache(line, filename, options):
    warnings = []
    if 'django.core.cache' in line and 'get_cache' in line:
        warnings.append("django.core.cache.get_cache() is deprecated. Use "
                        "django.core.cache.caches instead.")
    return warnings, [], []


def check_dictconfig_importlib(line, filename, options):
    warnings = []
    if 'django.utils' in line and \
       ('dictconfig' in line or 'importlib' in line):
        warnings.append("django.utils.dictconfig and django.utils.importlib "
                        "are deprecated. Use logging.config or importlib from "
                        "the Python standard library instead.")
    return warnings, [], []


def check_import_by_path(line, filename, options):
    warnings = []
    if ('django.utils.module_loading' in line and
       'import_by_path' in line) or \
       'import_by_path(' in line:
        warnings.append("django.utils.module_loading.import_by_path is "
                        "deprecated. Use import_string() from the same module "
                        "instead.")
    return warnings, [], []


def check_tzinfo(line, filename, options):
    warnings = []
    if 'LocalTimezone' in line or 'FixedOffset' in line:
        warnings.append("django.utils.tzinfo.LocalTimezone and "
                        "django.utils.tzinfo.FixedOffset are deprecated. Use "
                        "django.utils.timezone.get_default_timezone() or "
                        "django.utils.timezone.get_fixed_timezone() instead.")
    return warnings, [], []


def check_unittest(line, filename, options):
    warnings = []
    if 'django.utils' in line and 'unittest' in line:
        warnings.append("django.utils.unittest is deprecated. Use the unittest "
                        "module in the Python standard library instead.")
    return warnings, [], []


def check_sorteddict(line, filename, options):
    warnings = []
    if 'SortedDict' in line:
        warnings.append("django.utils.datastructures.SortedDict is deprecated. "
                        "Use collections.OrderedDict from the Python standard "
                        "library instead.")
    return warnings, [], []


def check_sites(line, filename, options):
    warnings = []
    if 'RequestSite' in line or 'get_current_site(' in line:
        warnings.append("django.contrib.sites.RequestSite and "
                        "django.contrib.sites.get_current_site() have been moved. "
                        "Use django.contrib.sites.requests.RequestSite or "
                        "django.contrib.sites.shortcuts.get_current_site() instead.")
    return warnings, [], []


def check_declared_fieldsets(line, filename, options):
    warnings = []
    if 'declared_fieldsets' in line:
        warnings.append("ModelAdmin.declared_fieldsets is deprecated. Implement the "
                        "get_fieldsets() method instead.")
    return warnings, [], []


def check_contenttypes(line, filename, options):
    warnings = []
    moves = [('GenericForeignKey', 'fields'),
             ('GenericRelation', 'fields'),
             ('BaseGenericInlineFormSet', 'forms'),
             ('generic_inlineformset_factory', 'forms'),
             ('GenericInlineModelAdmin', 'admin'),
             ('GenericStackedInline', 'admin'),
             ('GenericTabularInline', 'admin')]
    for cls, new_location in moves:
        if cls in line:
            warnings.append("django.contrib.contenttypes.generic.%s is now located in "
                            "django.contrib.contenttypes.%s" % (cls, new_location))
    return warnings, [], []


def check_utils_modules(line, filename, options):
    warnings = []
    module_locations = ('django.contrib.admin', 'django.contrib.gis.db.backends',
                        'django.db.backends', 'django.forms')
    for mod in module_locations:
        if mod in line and 'util' in line and 'utils' not in line:
            warnings.append("%s.util has been renamed to %s.utils" % (mod, mod))
    return warnings, [], []


def check_get_formsets(line, filename, options):
    warnings = []
    if 'admin' in filename and 'get_formsets' in line:
        warnings.append("ModelAdmin.get_formsets() has been renamed to "
                        "ModelAdmin.get_formsets_with_inlines().")
    return warnings, [], []


def check_ipaddressfields(line, filename, options):
    warnings = []
    if ('IPAddressField' in line and
        'GenericIPAddressField' not in line):
        warnings.append("IPAddressField is deprecated in favor of "
                        "GenericIPAddressField.")
    return warnings, [], []


def check_get_memcached_timeout(line, filename, options):
    warnings = []
    if '_get_memcache_timeout(' in line:
        warnings.append("_get_memcache_timeout is deprecated in favor of "
                        "get_backend_timeout().")
    return warnings, [], []


def check_request_request(line, filename, options):
    warnings = []
    if 'request.REQUEST' in line:
        warnings.append("request.REQUEST is deprecated. Use request.GET or "
                        "request.POST as appropriate.")
    return warnings, [], []


def check_mergedict(line, filename, options):
    warnings = []
    if 'MergeDict' in line:
        warnings.append("django.utils.datastructures.MergeDict is deprecated. "
                        "Use standard dict.update() calls instead.")
    return warnings, [], []


def check_memoize(line, filename, options):
    warnings = []
    if 'django.utils.functional' in line and 'memoize' in line:
        warnings.append("django.utils.functional.memoize is deprecated. On "
                        "Python 2, use django.utils.lru_cache.lru_cache. On "
                        "Python 3, use functools.lru_cache.")
    return warnings, [], []


def check_admin_for(line, filename, options):
    warnings = []
    if 'ADMIN_FOR' in line:
        warnings.append("The ADMIN_FOR setting is no longer used.")
    return warnings, [], []


def check_splitdatetimewidget(line, filename, options):
    warnings = []
    if 'SplitDateTimeWidget' in line:
        warnings.append("Use of SplitDateTimeWidget with DateTimeField "
                        "is deprecated. Use it with SplitDateTimeField "
                        "instead.")
    return warnings, [], []


def check_requires_model_validation(line, filename, options):
    errors = []
    if 'requires_model_validation' in line:
        errors.append("The 'requires_model_validation' option of "
                      "management commands is deprecated. Use "
                      "requires_system_checks instead. Use of "
                      "both is an error.")
    return [], errors, []


def check_validate_field(line, filename, options):
    warnings = []
    if 'def' in line and 'validate_field(' in line:
        warnings.append("DatabaseValidation.validate_field() is deprecated. "
                        "Implement check_field() instead.")
    return warnings, [], []


def check_future_tags(line, filename, options):
    warnings = []
    if 'from future %}' in line:
        warnings.append("{% load ssi from future %} and "
                        "{% load url from future %} are "
                        "deprecated and no longer necessary; simply "
                        "remove the 'from future'.")
    return warnings, [], []


def check_javascript_quote(line, filename, options):
    errors = []
    if 'javascript_quote' in line:
        errors.append("django.utils.text.javascript_quote() should "
                      "not be used; use the escapejs template tag "
                      "or django.utils.html.escapejs() instead.")
    return [], errors, []


def check_fix_ampersands(line, filename, options):
    warnings = []
    if 'fix_ampersands' in line:
        warnings.append("The fix_ampersands template filter and "
                        "django.utils.html.fix_ampersands() are "
                        "deprecated; Django's template escaping "
                        "performs this automatically.")
    return warnings, [], []


def check_itercompat_product(line, filename, options):
    errors = []
    if 'itercompat' in line and 'product' in line:
        errors.append("django.utils.itercompat.product() has been "
                      "removed.")
    return [], errors, []


def check_simplejson(line, filename, options):
    errors = []
    if 'django.utils' in line and 'simplejson' in line:
        errors.append("django.utils.simplejson has been removed.")
    return [], errors, []


def check_mimetype(line, filename, options):
    errors = []
    if 'mimetype' in line:
        errors.append("The 'mimetype' option for HTTP response classes "
                      "and rendering shortcuts has been removed. Use "
                      "'content_type' instead.")
    return [], errors, []


def check_old_profile_methods(line, filename, options):
    errors = []
    if 'AUTH_PROFILE_MODULE' in line or \
       'get_profile(' in line:
        errors.append("The AUTH_PROFILE_MODULE setting and the "
                      " User.get_profile() method have been removed.")
    return [], errors, []


def check_select_related_depth(line, filename, options):
    errors = []
    if 'select_related' in line and 'depth' in line:
        errors.append("The 'depth' argument to select_related() has "
                      "been removed.")
    return [], errors, []


def check_test_cookie(line, filename, options):
    errors = []
    if 'check_for_test_cookie' in line:
        errors.append("The check_for_test_cookie() method of "
                      "AuthenticationForm has been removed.")
    return [], errors, []


def check_strandunicode(line, filename, options):
    errors = []
    if 'StrAndUnicode' in line:
        errors.append("django.utils.encoding.StrAndUnicode has been "
                      "removed.")
    return [], errors, []


def do_check_django_17(line, filename, options):
    warnings = []
    info = []
    errors = []

    for check in [globals()[f] for f in globals().keys() if
                  callable(globals()[f]) and f.startswith('check_')]:
        warn, err, inf = check(line, filename, options)
        warnings += warn
        info += inf
        errors += err

    return warnings, errors, info


rules = [
    {'long_option': '--django-17',
     'action': 'store_true',
     'dest': 'django_17',
     'help': 'Check for changes and deprecations in Django 1.7.',
     'callback': do_check_django_17,
     'enabled': lambda options: options.django_17,}
]
