from wq.build import wq
import click
import os
import shutil
import subprocess
from django.core.management import call_command
from django.core.management.commands import startproject
from pkg_resources import resource_filename
from .version import VERSION
try:
    from pip._internal.operations import freeze
except ImportError:
    pass


template = resource_filename('wq.create', 'django_project')
# resource_filename not returning absolute path after pip install
if os.sep not in template:
    import wq as wq_module
    template = wq_module.__path__[0] + os.sep + template


if os.name == 'nt':
    NPX_COMMAND = 'npx.cmd'
    DEPLOY_SCRIPT = 'deploy.bat'
else:
    NPX_COMMAND = 'npx'
    DEPLOY_SCRIPT = './deploy.sh'


class StartProjectCommand(startproject.Command):
    def add_arguments(self, parser):
        super(StartProjectCommand, self).add_arguments(parser)
        parser.add_argument('--domain', help="Web Domain")
        parser.add_argument('--title', help="Site Title")
        parser.add_argument('--with-gis', help="Enable GeoDjango")
        parser.add_argument('--with-npm', help="Enable NPM")
        parser.add_argument('--wq-create-version', help="wq create version")


@wq.command()
@click.argument("project_name", required=False)
@click.argument("destination", required=False)
@click.option(
    "-d", "--domain", help='Web domain (e.g. example.wq.io)'
)
@click.option(
    "-t", "--title", help="Site title + App label"
)
@click.option(
    "--with-gis/--without-gis", default=None, help="Enable GeoDjango"
)
@click.option(
    "--with-npm/--without-npm", default=None,
    help="Enable NPM (& Create React App)"
)
def create(project_name, destination, domain=None, title=None,
           with_gis=None, with_npm=None):
    """
    Start a new project with wq.app and wq.db.  A new Django project will be
    created from a wq-specific template.  Any options not specified via
    arguments will be prompted for instead.

    After running this command, you may want to do the following:

    \b
        sudo chown www-data media/
        ./deploy.sh 0.0.0

    See https://wq.io/overview/setup for more tips on getting started with wq.
    """
    do_create(project_name, destination, domain, title, with_gis, with_npm)


def do_create(project_name, destination, domain, title, with_gis, with_npm):
    any_prompts = False

    if project_name is None:
        any_prompts = True
        project_name = click.prompt(
            'Project codename',
        )

    if destination is None:
        any_prompts = True
        destination = click.prompt(
            'Directory',
            default='./{}/'.format(project_name),
        )

    if domain is None:
        any_prompts = True
        domain = click.prompt(
            'Web domain',
            default='{}.example.org'.format(project_name)
        )

    if title is None:
        any_prompts = True
        title = click.prompt(
            'Site title + App label',
            default='{} Project'.format(project_name)
        )
    elif title == '__old__':
        title = '{} Project'.format(project_name)

    if with_gis is None:
        any_prompts = True
        with_gis = click.confirm(
            'Enable GIS? (Requires PostGIS or SpatialLite)',
            default=False,
        )

    if with_npm is None:
        any_prompts = True
        with_npm = click.confirm(
            'Enable NPM / Create React App? (Requires Node.js)',
            default=False,
        )

    os.makedirs(
        os.path.abspath(os.path.expanduser(destination)),
        exist_ok=True,
    )
    args = [project_name, destination]
    kwargs = dict(
        template=template,
        extensions="py,yml,conf,html,sh,js,css,json,xml,gitignore".split(","),
        domain=domain,
        title=title,
        wq_create_version=VERSION,
        with_gis=with_gis,
        with_npm=with_npm,
    )
    call_command(StartProjectCommand(), *args, **kwargs)

    path = destination or project_name
    if freeze:
        with open(os.path.join(path, 'requirements.txt'), 'w') as f:
            for dep in freeze.freeze():
                print(dep, file=f)

    if with_npm:
        shutil.rmtree(os.path.join(path, 'app'))
        subprocess.check_call([
            NPX_COMMAND,
            'create-react-app',
            project_name,
            '--template', '@wq',
            '--scripts-version', '4.0.3'
        ], cwd=path)
        os.rename(
            os.path.join(path, project_name),
            os.path.join(path, 'app'),
        )
        for filename in ('index.html', 'manifest.json'):
            filepath = os.path.join(path, 'app', 'public', filename)
            with open(filepath) as f:
                content = f.read()

            content = content.replace('{{ title }}', title)
            content = content.replace('{{ project_name }}', project_name)

            with open(filepath, 'w') as f:
                f.write(content)
    else:
        os.remove(os.path.join(path, 'app', 'README.md'))

    flags = []
    if with_gis:
        flags.append('GIS')
    if with_npm:
        flags.append('NPM')

    if len(flags) == 3:
        flag_summary = " with {0}, {1}, and {2} support".format(*flags)
    elif len(flags) == 2:
        flag_summary = " with {0} and {1} support".format(*flags)
    elif len(flags) == 1:
        flag_summary = " with {} support".format(*flags)
    else:
        flag_summary = ""

    if any_prompts:
        click.echo()

    click.echo(
        'Project "{project_name}" created successfully in {destination}'
        "{flag_summary}.".format(
            project_name=project_name,
            destination=destination,
            flag_summary=flag_summary,
        )
    )

    click.echo(f"Run {DEPLOY_SCRIPT} 0.0.0 to finish initial setup.")
