import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
DIRPATH = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir))

if __name__ == "__main__":
    sys.path.append(DIRPATH)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.test_settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
