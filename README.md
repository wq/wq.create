[![wq.start](https://raw.github.com/wq/wq/master/images/256/wq.start.png)](https://wq.io/wq.start)

[wq.start](https://wq.io/wq.start) provides a simple command-line interface (`wq start`) for starting a new project with the [wq framework], with [wq.app] for the front end and [wq.db] as the backend.  wq.start also provides a `wq addform` command that can generate and configure new Django apps from an [XLSForm](http://xlsform.org) definition.

[![Latest PyPI Release](https://img.shields.io/pypi/v/wq.start.svg)](https://pypi.org/project/wq.start)
[![Release Notes](https://img.shields.io/github/release/wq/wq.start.svg)](https://github.com/wq/wq.start/releases)
[![License](https://img.shields.io/pypi/l/wq.start.svg)](https://wq.io/license)
[![GitHub Stars](https://img.shields.io/github/stars/wq/wq.start.svg)](https://github.com/wq/wq.start/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/wq/wq.start.svg)](https://github.com/wq/wq.start/network)
[![GitHub Issues](https://img.shields.io/github/issues/wq/wq.start.svg)](https://github.com/wq/wq.start/issues)

[![Travis Build Status](https://img.shields.io/travis/wq/wq.start/master.svg)](https://travis-ci.org/wq/wq.start)
[![Python Support](https://img.shields.io/pypi/pyversions/wq.start.svg)](https://pypi.org/project/wq.start)
[![Django Support](https://img.shields.io/pypi/djversions/wq.start.svg)](https://pypi.org/project/wq.start)

### Usage

```bash
# Recommended: create virtual environment
# python3 -m venv venv
# . venv/bin/activate
python3 -m pip install wq

wq start <projectname> [directory]
cd <projectname>/db
wq addform ~/my-odk-form.xlsx
```

See the [Getting Started] docs for more information.

### Commands

 * `wq start <projectname> [directory]`: Create a new Django project from the [wq Django template] and (optionally) the [@wq Create React App template][@wq/cra-template]
 * `wq addform ~/my-odk-form.xlsx`: Create a new Django app from the provided XLSForm (uses [xlsform-converter])
 * `wq maketemplates`: Create templates for use with [@wq/jquery-mobile][@wq/jquery-mobile] (deprecated)


[wq framework]: https://wq.io/
[wq.app]: https://wq.io/wq.app
[wq.db]: https://wq.io/wq.db
[wq Django template]: https://github.com/wq/wq-django-template
[@wq/cra-template]: https://github.com/wq/wq.start/tree/packages/cra-template
[@wq/jquery-mobile]: https://github.com/wq/wq.app/tree/packages/jquery-mobile
[xlsform-converter]: https://github.com/wq/xlsform-converter
[Getting Started]: https://wq.io/docs/setup
