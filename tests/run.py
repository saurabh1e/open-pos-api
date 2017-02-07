import sys
import unittest

from coverage import coverage


def run():
    cov = coverage(source=['flask_testing'])
    cov.start()

    from tests import suite
    result = unittest.TextTestRunner(verbosity=2).run(suite())
    if not result.wasSuccessful():
        sys.exit(1)
    cov.stop()
    print("\nCode Coverage")
    cov.report()
    cov.html_report(directory='cover')

if __name__ == '__main__':
    run()
