from wq.build import wq
import click
import os
from xlsconv import parse_xls, xls2django
import subprocess
import json
from difflib import unified_diff
from pyxform.question_type_dictionary import QUESTION_TYPE_DICT as QTYPES
import pathlib


@wq.command()
@click.argument(
    "xlsform",
    required=True,
    type=click.Path(exists=True),
)
@click.option(
    "--django-dir",
    default=".",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="Root of Django project",
)
@click.option(
    "--form-name",
    help="Name to use for Django app package directory",
)
@click.option(
    "--with-admin/--no-admin",
    default=False,
    help="Generate admin.py",
)
@click.option(
    "--with-wizard/--no-wizard",
    default=False,
    help="Generate wizard.py",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Answer yes to all prompts",
)
def addform(
    xlsform,
    django_dir,
    form_name,
    with_admin,
    with_wizard,
    force,
):
    """
    Convert an XLSForm into a Django app for wq.  Generates Python and mustache
    files including:

    \b
        db/[form_name]/models.py
        db/[form_name]/rest.py
        db/[form_name]/serializers.py (if applicable)
        db/[form_name]/admin.py (if requested)
        db/[form_name]/wizard.py (if requested)
    """

    manage_py = django_dir / "manage.py"

    if django_dir == pathlib.Path("."):
        if not manage_py.exists():
            if (django_dir / "db" / "manage.py").exists():
                django_dir = django_dir / "db"
                manage_py = django_dir / "manage.py"
            else:
                raise click.ClickException(
                    "Could not find manage.py in current directory.  Try specifying --django-dir"
                )

    xls_json = parse_xls(xlsform)
    if not form_name:
        form_name = xls_json["name"]

    form_dir = django_dir / form_name
    form_dir.mkdir(exist_ok=True)
    (form_dir / "migrations").mkdir(exist_ok=True)

    create_file(
        form_dir / "__init__.py",
        "",
        overwrite=force,
    )

    create_file(
        form_dir / "migrations" / "__init__.py",
        "",
        overwrite=force,
    )

    create_file(
        form_dir / "models.py",
        xls2django(xlsform, "models"),
        overwrite=force,
    )

    has_nested = False
    for field in xls_json["children"]:
        if field.get("wq:nested", False):
            has_nested = True
    if has_nested:
        create_file(
            form_dir / "serializers.py",
            xls2django(xlsform, "serializers"),
            overwrite=force,
        )

    create_file(
        form_dir / "rest.py",
        xls2django(xlsform, "rest"),
        overwrite=force,
    )
    if with_admin:
        create_file(
            form_dir / "admin.py",
            xls2django(xlsform, "admin"),
            overwrite=force,
        )
    if with_wizard:
        create_file(
            form_dir / "wizard.py",
            xls2django(xlsform, "wizard"),
            overwrite=force,
        )

    settings_paths = sorted(django_dir.glob("**/settings.py"))
    if not settings_paths:
        settings_paths = sorted(django_dir.glob("**/settings/base.py"))

    if not settings_paths:
        click.echo("Warning: No settings found in Django directory.")
        return

    settings_path = settings_paths[0]

    new_settings = []
    app_section = False
    has_app = False
    for row in settings_path.read_text().split(os.linesep):
        if "INSTALLED_APPS" in row:
            app_section = True
        elif app_section:
            if ")" in row or "]" in row:
                app_section = False
                if not has_app:
                    new_settings.append(f'    "{form_name}",')
            else:
                if f'"{form_name}"' in row or f"'{form_name}'" in row:
                    has_app = True
        new_settings.append(row)
    create_file(
        settings_path,
        os.linesep.join(new_settings),
        overwrite=force,
        show_diff=True,
    )
    if not manage_py.exists():
        click.echo("Warning: No manage.py found in Django directory.")
        return

    result = (
        subprocess.check_output(
            [manage_py.absolute(), "makemigrations", "--no-input"]
        )
        .decode("utf-8")
        .strip()
    )
    click.echo(result)
    if "No changes" in result:
        return
    migrate = force or click.confirm("Update database schema?", default=True)
    if not migrate:
        return
    subprocess.call([manage_py.absolute(), "migrate"])


def create_file(
    path, contents, overwrite=False, show_diff=False, previous_diff=False
):
    has_diff = previous_diff
    path_label = f"{path.parent.name}/{path.name}"

    if path.exists() and not overwrite:
        existing_content = path.read_text()
        if existing_content.strip() == contents.strip():
            return False

        def print_diff():
            diff = unified_diff(
                existing_content.split("\n"),
                contents.split("\n"),
                fromfile=f"{path_label} (current)",
                tofile=f"{path_label} (new)",
            )
            for row in diff:
                click.echo(row)

        if show_diff:
            print_diff()
            message = f"Update {path_label}? [Y/n/d/?]"
            default_choice = "y"
        else:
            if not previous_diff:
                choice = click.prompt(
                    f"{path.parent.name} package already exists; update modules? [y/n]"
                )
                if choice.lower() != "y":
                    click.echo("Skipping module updates.")
                    return "skipall"

            message = f"{path_label} already exists; overwrite? [y/n/d/?]"
            default_choice = None

        has_diff = True
        choice = ""
        while choice.lower() not in ("y", "n"):
            choice = click.prompt(
                message,
                default=default_choice,
                show_default=False,
            )
            if choice == "" and show_diff:
                choice = "y"
            if choice.lower() == "n":
                return has_diff
            elif choice.lower() == "?":
                click.echo(
                    "  y - overwrite\n"
                    "  n - skip\n"
                    "  d - show diff\n"
                    "  ? - show help"
                )
            elif choice.lower() == "d":
                print_diff()
    path.write_text(contents)
    return has_diff
