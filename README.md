[![wq.create](https://raw.github.com/wq/wq/master/images/256/wq.create.png)](https://wq.io/wq.create)

[wq.create](https://wq.io/wq.create) (formerly wq.start) provides a simple command-line interface (`wq create`) for starting a new project with the [wq framework], with [wq.app] for the front end and [wq.db] as the backend.  wq.create also provides a `wq addform` command that can generate and configure new Django apps from an [XLSForm](http://xlsform.org) definition.

[![Latest PyPI Release](https://img.shields.io/pypi/v/wq.create.svg)](https://pypi.org/project/wq.create)
[![Release Notes](https://img.shields.io/github/release/wq/wq.create.svg)](https://github.com/wq/wq.create/releases)
[![License](https://img.shields.io/pypi/l/wq.create.svg)](https://wq.io/license)
[![GitHub Stars](https://img.shields.io/github/stars/wq/wq.create.svg)](https://github.com/wq/wq.create/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/wq.create.svg)](https://github.com/wq/wq.create/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/wq.create.svg)](https://github.com/wq/wq.create/issues)

[![Travis Build Status](https://img.shields.io/travis/wq/wq.create/master.svg)](https://travis-ci.org/wq/wq.create)
[![Python Support](https://img.shields.io/pypi/pyversions/wq.create.svg)](https://pypi.org/project/wq.create)
[![Django Support](https://img.shields.io/pypi/djversions/wq.create.svg)](https://pypi.org/project/wq.create)

### Usage

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate
python3 -m pip install wq

wq create <projectname> [directory]
cd <projectname>/db
wq addform ~/my-odk-form.xlsx
```

See the [Getting Started] docs for more information.

### Commands

 * `wq create <projectname> [directory]`: Create a new Django project from the [wq Django template] and (optionally) the [@wq Create React App template][@wq/cra-template]
 * `wq addform ~/my-odk-form.xlsx`: Create a new Django app from the provided XLSForm (uses [xlsform-converter])
 * `wq maketemplates`: Create templates for use with [@wq/jquery-mobile][@wq/jquery-mobile] (deprecated)


[wq framework]: https://wq.io/
[wq.app]: https://wq.io/wq.app
[wq.db]: https://wq.io/wq.db
[wq Django template]: https://github.com/wq/wq-django-template
[@wq/cra-template]: https://github.com/wq/wq.create/tree/master/packages/cra-template
[@wq/jquery-mobile]: https://github.com/wq/wq.app/tree/master/packages/jquery-mobile
[xlsform-converter]: https://github.com/wq/xlsform-converter
[Getting Started]: https://wq.io/docs/setup
