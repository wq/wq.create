from wq.core import wq
import click
import os
import shutil
from django.core.management import call_command
from pkg_resources import resource_filename
from wq.core.info import print_versions


template = resource_filename('wq.start', 'django_project')
# resource_filename not returning absolute path after pip install
if os.sep not in template:
    import wq as wq_module
    template = wq_module.__path__[0] + os.sep + template


@wq.command()
@click.argument("project_name", required=True)
@click.argument("destination", required=False)
def start(project_name, destination):
    """
    Start a new project with wq.app and wq.db.  A new Django project will be
    created from a wq-specific template.  After running this command, you may
    want to do the following:

    \b
        sudo chown www-data media/
        cd app
        wq init

    See https://wq.io/docs/setup for more tips on getting started with wq.
    """
    args = [project_name]
    if destination:
        args.append(destination)

    kwargs = dict(
        template=template,
        extensions=["py", "yml", "conf", "html", "sh", "js", "css", "json"],
    )

    call_command('startproject', *args, **kwargs)
    path = destination or project_name
    txt = os.path.join(path, 'requirements.txt')
    print_versions(txt, [
        'wq.app',
        'wq.db',
    ])
    shutil.copytree(
        resource_filename('xlsconv', 'templates'),
        os.path.join(path, 'master_templates'),
        ignore=shutil.ignore_patterns("*.py-tpl"),
    )
