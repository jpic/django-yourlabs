import shutil
import os
import os.path
from optparse import make_option

from django.template import loader, Context
from django.core.management.commands.makemessages import handle_extensions
from django.core.management.base import BaseCommand, CommandError

import yourlabs


class Command(BaseCommand):
    args = '<app_name> <command_name>'
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
    )

    def handle(self, app_name, command_name, *args, **options):
        self.verbosity = int(options.get('verbosity'))

        extensions = tuple(
            handle_extensions(options.get('extensions'), ignored=()))

        extra_files = []
        for f in options.get('files'):
            extra_files.extend(map(lambda x: x.strip(), f.split(',')))

        context = Context(dict(options, **{
            'app_name': app_name,
            'command_name': command_name,
        }), autoescape=False)

        source = os.path.join(yourlabs.__path__[0], 'templates', 'yourlabs',
                              'command')
        destination = __import__(app_name).__path__[0]

        for root, dirnames, filenames in os.walk(source):
            relative_root = root.replace(source, '')

            if relative_root != '' and relative_root[0] == '/':
                relative_root = relative_root[1:]

            destination_dirpath = os.path.join(destination, relative_root)

            if not os.path.exists(destination_dirpath):
                os.makedirs(destination_dirpath)

            for source_filename in filenames:
                if source_filename[-4:] == '.pyc':
                    continue

                destination_filepath = os.path.join(destination_dirpath,
                    source_filename.replace('command_name', command_name))
                source_filepath = os.path.join(root, source_filename)

                if os.path.exists(destination_filepath):
                    self.stdout.write("Skipping existing %s\n" %
                                    destination_filepath)
                    continue


                if (source_filename.endswith(extensions)
                        or source_filename in extra_files):
                    template = loader.get_template(
                        os.path.join('yourlabs', 'command', relative_root,
                                     source_filename))
                    content = template.render(context)
                    content = content.encode('utf-8')
                else:
                    with open(source_filepath, 'rb') as template_file:
                        content = template_file.read()

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
