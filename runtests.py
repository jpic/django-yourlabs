import os, sys
from django.conf import settings

settings.configure(
    DEBUG=True,
    DATABASES={
         'default': {
             'ENGINE': 'django.db.backends.sqlite3',
         }
    },
    INSTALLED_APPS=(
        'yourlabs',
    )
)

from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['yourlabs', ])
if failures:
    sys.exit(failures)
