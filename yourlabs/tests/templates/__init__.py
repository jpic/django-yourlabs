import subprocess
import shutil
import optparse
import tempfile
import os.path
import imp
import os
import unittest
import warnings

warnings.simplefilter('ignore', RuntimeWarning)


def clear_pyc(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename[-4:] == '.pyc':
                os.unlink(os.path.join(root, filename))


class TemplatesTestCase(unittest.TestCase):
    def assertGenerateExpected(self, test_name):
        fixture = os.path.realpath(os.path.join(os.path.dirname(__file__),
            test_name, 'fixture'))
        expected = os.path.realpath(os.path.join(os.path.dirname(__file__),
            test_name, 'expected'))

        tempdir = tempfile.mkdtemp('test_%s' % test_name)
        app_path = os.path.join(tempdir, 'fixture')
        shutil.copytree(fixture, app_path)
        self.paths_to_remove.append(tempdir)

        if not os.path.exists(expected):
            self.skipTest('No %s' % expected)

        command = __import__('yourlabs.management.commands.%s' % test_name,
                             globals(), locals(), ['Command']).Command()
        command.stdout = open(os.devnull, 'w')

        kwargs_path = os.path.join( fixture, 'kwargs.py')
        if os.path.exists(kwargs_path):
            kwargs = imp.load_source('%s.kwargs' % test_name,
                    kwargs_path).kwargs
        else:
            kwargs = {}

        defaults = {}
        for opt in command.option_list:
            if opt.default is optparse.NO_DEFAULT:
                defaults[opt.dest] = None
            else:
                defaults[opt.dest] = opt.default

        kwargs.update(defaults)
        kwargs.update({'verbosity': -1, 'app_path': fixture,
                       'destination': app_path})

        command.handle('fixture', command.template_dir, **kwargs)


        try:
            clear_pyc(app_path)
            clear_pyc(expected)
            subprocess.check_output(['diff', '-ur', app_path, expected])
        except subprocess.CalledProcessError as e:
            self.fail("\n" + e.output)

    def setUp(self):
        self.paths_to_remove = []

    def tearDown(self):
        if os.environ.get('YL_DEBUG', False):
            print self.paths_to_remove
        else:
            for path in self.paths_to_remove:
                shutil.rmtree(path)

def test_generator(test_name):
    def test(self):
        self.assertGenerateExpected(test_name)
    return test


for dirname in os.listdir(os.path.dirname(__file__)):
    if not os.path.isdir(os.path.join(os.path.dirname(__file__), dirname)):
        continue

    setattr(TemplatesTestCase, 'test_%s' % dirname, test_generator(dirname))
