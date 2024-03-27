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


template = resource_filename("wq.create", "django_project")
# resource_filename not returning absolute path after pip install
if os.sep not in template:
    import wq as wq_module

    template = wq_module.__path__[0] + os.sep + template


if os.name == "nt":
    NPM_COMMAND = "npm.cmd"
    DEPLOY_SCRIPT = "deploy.bat"
else:
    NPM_COMMAND = "npm"
    DEPLOY_SCRIPT = "./deploy.sh"


class StartProjectCommand(startproject.Command):
    def add_arguments(self, parser):
        super(StartProjectCommand, self).add_arguments(parser)
        parser.add_argument("--domain", help="Web Domain")
        parser.add_argument("--title", help="Site Title")
        parser.add_argument("--with-gis", help="Enable GeoDjango")
        parser.add_argument("--with-npm", help="Enable NPM)")
        parser.add_argument("--with-gunicorn", help="Enable Gunicorn")
        parser.add_argument("--wq-create-version", help="wq create version")


@wq.command()
@click.argument("project_name", required=False)
@click.argument("destination", required=False)
@click.option("-d", "--domain", help="Web domain (e.g. example.wq.io)")
@click.option("-t", "--title", help="Site title + App label")
@click.option(
    "--with-gis/--without-gis", default=None, help="Enable GeoDjango"
)
@click.option(
    "--with-npm/--without-npm",
    default=None,
    help="Enable NPM (Vite with @wq/rollup-plugin)",
)
@click.option(
    "--with-gunicorn/--with-apache",
    default=None,
    help="Use Gunicorn + Whitenoise instead of Apache WSGI",
)
def create(
    project_name,
    destination,
    domain=None,
    title=None,
    with_gis=None,
    with_npm=None,
    with_gunicorn=None,
):
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
    do_create(
        project_name,
        destination,
        domain,
        title,
        with_gis,
        with_npm,
        with_gunicorn,
    )


def do_create(
    project_name,
    destination,
    domain,
    title,
    with_gis,
    with_npm,
    with_gunicorn,
):
    any_prompts = False

    if project_name is None:
        any_prompts = True
        project_name = click.prompt(
            "Project codename",
        )

    if destination is None:
        any_prompts = True
        destination = click.prompt(
            "Directory",
            default="./{}/".format(project_name),
        )

    if domain is None:
        any_prompts = True
        domain = click.prompt(
            "Web domain", default="{}.example.org".format(project_name)
        )

    if title is None:
        any_prompts = True
        title = click.prompt(
            "Site title + App label", default="{} Project".format(project_name)
        )
    elif title == "__old__":
        title = "{} Project".format(project_name)

    if with_gis is None:
        any_prompts = True
        with_gis = click.confirm(
            "Enable GIS? (Requires PostGIS or SpatialLite)",
            default=False,
        )

    if with_npm is None:
        any_prompts = True
        with_npm = click.confirm(
            "Enable NPM / Vite + @wq/rollup-plugin? (Requires Node.js)",
            default=False,
        )

    if with_gunicorn is None:
        any_prompts = True
        with_gunicorn = click.confirm(
            "Enable Gunicorn + Whitenoise instead of Apache WSGI?",
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
        with_gunicorn=with_gunicorn,
    )
    call_command(StartProjectCommand(), *args, **kwargs)

    path = destination or project_name
    if freeze:
        with open(os.path.join(path, "requirements.txt"), "w") as f:
            for dep in freeze.freeze():
                print(dep, file=f)

    os.remove(os.path.join(path, "app", "README.md"))
    if with_npm:
        project_static_dir = os.path.join(path, "db", project_name, "static")
        os.makedirs(project_static_dir, exist_ok=True)
        shutil.move(os.path.join(path, "app"), project_static_dir)
        subprocess.check_call(
            [NPM_COMMAND, "init", "@wq", project_name], cwd=path
        )
        os.rename(
            os.path.join(path, project_name),
            os.path.join(path, "app"),
        )
        for filename in ("index.html", "vite.config.js"):
            filepath = os.path.join(path, "app", filename)
            with open(filepath) as f:
                content = f.read()

            content = content.replace("Example Project", title)
            content = content.replace("project", project_name)

            with open(filepath, "w") as f:
                f.write(content)
        subprocess.check_call(
            [NPM_COMMAND, "install"], cwd=os.path.join(path, "app")
        )

    if with_gunicorn:
        os.remove(os.path.join(path, "conf", f"{project_name}.conf"))

    flags = []
    if with_gis:
        flags.append("GIS")
    if with_npm:
        flags.append("NPM")
    if with_gunicorn:
        flags.append("Gunicorn")

    if len(flags) > 2:
        flag_summary = " with {first}, and {last} support".format(
            first=", ".join(flags[:-1]), last=flags[-1]
        )
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
