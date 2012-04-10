from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.template.loader import find_template_loader
from django.utils.importlib import import_module
from pkg_resources import resource_filename
import cssutils
import os
import subprocess
import sys

fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir.decode(fs_encoding))


def grep(filename, arg):
    process = subprocess.Popen(['grep', '-r', arg, filename], stdout=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return stdout, stderr


class Command(BaseCommand):
    help = 'Check CSS usage'
    args = "<static_css static_css ...>"

    option_list = BaseCommand.option_list

    def handle(self, *args, **options):

        template_dirs = list(settings.TEMPLATE_DIRS)
        template_dirs += app_template_dirs

        pkg_name = 'templates/'
        for app in settings.INSTALLED_APPS:
            try:
                path = resource_filename(app, pkg_name).decode(settings.FILE_CHARSET)
                if os.path.exists(path):
                    template_dirs.append(path)
            except:
                pass

        for static_css in args:
            absolute_path = finders.find(static_css)
            sheet = cssutils.parseFile(absolute_path)
            for rule in sheet.cssRules:
                if hasattr(rule, "selectorList"):
                    for selector in rule.selectorList:
                        for seq in selector.seq:
                            if seq.type == "class":
                                # grep for that class
                                cls = seq.value.replace(".", "")
                                res = ""
                                for folder in template_dirs:
                                    stdout, stderr = grep(folder, cls)
                                    res += stdout
                                if res == "":
                                    print ".%s\n\t(...%s:%i)" % (cls, sheet.href[-16:], seq.line)
