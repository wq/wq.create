from wq.core import wq
import click
import os
import shutil
import subprocess
from django.core.management import call_command
from django.core.management.commands import startproject
from pkg_resources import resource_filename
from wq.core.info import print_versions
from .version import VERSION


template = resource_filename('wq.start', 'django_project')
# resource_filename not returning absolute path after pip install
if os.sep not in template:
    import wq as wq_module
    template = wq_module.__path__[0] + os.sep + template


class StartProjectCommand(startproject.Command):
    def add_arguments(self, parser):
        super(StartProjectCommand, self).add_arguments(parser)
        parser.add_argument('--domain', help="Web Domain")
        parser.add_argument('--app-id', help="App Identifier")
        parser.add_argument('--with-gis', help="Enable GeoDjango")
        parser.add_argument('--with-npm', help="Enable NPM")
        parser.add_argument('--wq-start-version', help="wq start version")


@wq.command()
@click.argument("project_name", required=False)
@click.argument("destination", required=False)
@click.option(
    "-d", "--domain", help='Web domain (e.g. example.wq.io)'
)
@click.option(
    "-i", "--app-id", help="Application ID (e.g. io.wq.example)"
)
@click.option(
    "--with-gis/--without-gis", default=None, help="Enable GeoDjango"
)
@click.option(
    "--with-npm/--without-npm", default=None,
    help="Enable NPM (& Create React App)"
)
@click.option(
    "--npm-install/--skip-npm-install",  default=None,
    help="Run NPM install after creating project"
)
def start(project_name, destination, domain=None, app_id=None,
          with_gis=None, with_npm=None, npm_install=None):
    """
    Start a new project with wq.app and wq.db.  A new Django project will be
    created from a wq-specific template.  Any options not specified via
    arguments will be prompted for instead.

    After running this command, you may want to do the following:

    \b
        sudo chown www-data media/
        ./deploy.sh 0.0.0

    See https://wq.io/docs/setup for more tips on getting started with wq.
    """
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

    if app_id is None:
        any_prompts = True
        app_id = click.prompt(
            'Application Bundle ID',
            default='.'.join(reversed(domain.split('.')))
        )

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
        app_id=app_id,
        wq_start_version=VERSION,
        with_gis=with_gis,
        with_npm=with_npm,
    )
    call_command(StartProjectCommand(), *args, **kwargs)

    path = destination or project_name
    print_versions(os.path.join(path, 'requirements.txt'))
    shutil.copytree(
        resource_filename('xlsconv', 'templates'),
        os.path.join(path, 'master_templates'),
        ignore=shutil.ignore_patterns("*.py-tpl"),
    )
    if with_npm:
        shutil.rmtree(os.path.join(path, 'app', 'js'))
        os.remove(os.path.join(path, 'app', 'src', 'README.md'))
    else:
        shutil.rmtree(os.path.join(path, 'app', 'src'))
        os.remove(os.path.join(path, 'app', 'js', 'README.md'))
        os.remove(os.path.join(path, 'app', 'package.json'))
        os.remove(os.path.join(path, 'app', 'public', 'index.html'))
        os.remove(os.path.join(path, 'app', 'pgb', 'pginit.js'))
        public_dir = os.path.join(path, 'app', 'public')
        for filename in os.listdir(public_dir):
            os.rename(
                os.path.join(public_dir, filename),
                os.path.join(path, 'app', filename),
            )
        os.rmdir(public_dir)

    if with_gis:
        if with_npm:
            flag_summary = " with GIS and NPM support"
        else:
            flag_summary = " with GIS support"
    else:
        if with_npm:
            flag_summary = " with NPM support"
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
    if with_npm:
        if npm_install is None:
            npm_install = click.confirm(
                "Run npm install now?"
            )
        if npm_install:
            subprocess.run(
                ['npm', 'install'],
                cwd=os.path.join(path, 'app')
            )
            click.echo()
            click.echo("npm install complete.")

    click.echo("Run ./deploy.sh 0.0.0 to finish initial setup.")
