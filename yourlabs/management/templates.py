import shutil
import os
import os.path
from optparse import make_option

from django.template import loader, Context
from django.core.management.commands.makemessages import handle_extensions
from django.core.management.base import BaseCommand, CommandError

import yourlabs
from ..utils.app_inspector import AppInspector

class TemplateCommand(BaseCommand):
    args = '<app_name>'
    help = 'Creates a management command skeleton in the given app'

    option_list = BaseCommand.option_list + (
        make_option('--extension', '-e', dest='extensions',
                    action='append', default=['py'],
                    help='The file extension(s) to render (default: "py"). '
                         'Separate multiple extensions with commas, or use '
                         '-e multiple times.'),
        make_option('--name', '-n', dest='files',
                    action='append', default=[],
                    help='The file name(s) to render. '
                         'Separate multiple extensions with commas, or use '
                         '-n multiple times.'),
        make_option('--dry-run', '-d', dest='dry_run', action='store_true',
                    help='Output instead of writing to the filesystem')
    )

    def handle(self, app_name, template_dir, destination=None, app_path=None,
            extra_context=None, *args, **options):
        self.verbosity = int(options.get('verbosity'))
        self.app_name = app_name

        if app_path is None:
            self.app_path = __import__(app_name).__path__[0]
        else:
            self.app_path = app_path

        if destination is None:
            destination = self.app_path

        extra_context = extra_context or {}

        extensions = tuple(
            handle_extensions(options.get('extensions'), ignored=()))

        extra_files = []
        for f in options.get('files'):
            extra_files.extend(map(lambda x: x.strip(), f.split(',')))

        context = self.build_context(extra_context, *args, **options)

        source = os.path.join(yourlabs.__path__[0], 'templates', 'yourlabs',
                              template_dir)

        for root, dirnames, filenames in os.walk(source):
            relative_root = root.replace(source, '')

            if relative_root != '' and relative_root[0] == '/':
                relative_root = relative_root[1:]

            destination_dirpath = os.path.join(destination,
                                               self.source_rename(relative_root))

            if not options.get('dry_run', False):
                if not os.path.exists(destination_dirpath):
                    os.makedirs(destination_dirpath)

            for source_filename in filenames:
                if source_filename[-4:] == '.pyc':
                    continue

                destination_filepath = os.path.join(destination_dirpath,
                    self.source_rename(source_filename))
                source_filepath = os.path.join(root, source_filename)

                if os.path.exists(destination_filepath):
                    self.stdout.write("Skipping existing %s\n" %
                                    destination_filepath)
                    continue

                if (self.source_rename(source_filename).endswith(extensions) or
                    source_filename in extra_files):
                    template = loader.get_template(
                        os.path.join('yourlabs', template_dir, relative_root,
                                     source_filename))
                    content = template.render(context)
                    content = content.encode('utf-8')
                else:
                    with open(source_filepath, 'rb') as template_file:
                        content = template_file.read()

                if options.get('dry_run', False):
                    print '=' * 40
                    print destination_filepath
                    print '-' * 40
                    print content
                    print '=' * 40
                else:
                    with open(destination_filepath, 'wb') as new_file:
                        new_file.write(content)

                    self.stdout.write("Creating %s\n" % destination_filepath)

                    try:
                        shutil.copymode(source_filepath, destination_filepath)
                    except OSError:
                        self.stderr.write(
                            "Notice: Couldn't set permission bits on %s. You're "
                            "probably using an uncommon filesystem setup. No "
                            "problem." % destination_filepath, self.style.NOTICE)

    def build_context(self, extra_context, *args, **options):
        context = dict(app=AppInspector(path=self.app_path))
        context.update(options)
        context.update(extra_context)

        return Context(context, autoescape=False)

    def source_rename(self, source):
        return source.replace('app_name', self.app_name).replace('.tpl', '')
