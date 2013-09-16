import os
import os.path
import imp
import inspect

from django.views import generic


class AppInspector(object):
    def __init__(self, name=None, path=None):
        if path is None and name:
            self.path = __import__(name).__path__[0]
            self.name = name
        elif name is None and path:
            self.name = path.split('/')[-1]
            self.path = path
        else:
            raise Exception('Need either a name or path')

        self.dir = self.inspect_dir()

        if 'views' in self.dir.keys():
            self.views = self.inspect_views()
        else:
            self.views = {}

    def inspect_dir(self):
        def inspect_dir(path):
            dirs = {}

            for child in os.listdir(path):
                child_path = os.path.join(path, child)

                if os.path.isfile(child_path):
                    if os.path.splitext(child)[1] in ('.swp', '.pyc'):
                        continue

                    dirs[os.path.splitext(child)[0]] = dict(name=child)

                elif os.path.isdir(child_path):
                    dirs[child] = dict(dir=inspect_dir(child_path))

            return dirs

        return inspect_dir(self.path)

    def inspect_views(self):
        result = dict(functions=[], classes=[])
        views_py = os.path.join(self.path, 'views.py')
        views_pyc = os.path.join(self.path, 'views.pyc')

        mod = imp.load_source('%s.views' % self.name, views_py)

        for k, v in mod.__dict__.items():
            if k[:2] == '__' or k[-4:] == '.pyc':
                continue

            if inspect.getfile(v) not in (views_py, views_pyc):
                continue

            if inspect.isfunction(v):
                if inspect.getargspec(v).args[0] != 'request':
                    continue

                result['functions'].append({'name': v.__name__})

            elif inspect.isclass(v):
                if not issubclass(v, generic.View):
                    continue

                result['classes'].append({'name': v.__name__})

        return result
