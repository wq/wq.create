wq.start: Project template and scaffolding tools
================================

`wq.start` provides a simple command-line interface (`wq start`) for starting a new project with the [wq framework], with [wq.app] for the front end and [wq.db] as the backend component.  `wq.start` also provides commands for generating a default set of offline-capable list, detail, and edit templates.  The templates can be generated for existing Django models (via `wq maketemplates`), or both the models and the templates can be generated from an ODK-style [XLSForm](http://xlsform.org) (via `wq addform`).

### Usage

```sh
pip3 install wq
wq start <projectname> [directory]
cd <projectname>/db
wq addform ~/my-odk-form.xlsx
```

See the [Getting Started] docs for more information.

### Commands

 * `wq start <projectname> [directory]`: Create a new Django project (from the [wq Django template])
 * `wq addform ~/myodk-form.xlsx`: Create a new Django app from the provided XLSForm (uses [xlsform-converter])
 * `wq maketemplates`: Create templates for Django models registered with [wq.db.rest]

[wq framework]: https://wq.io/
[wq.app]: https://wq.io/wq.app
[wq.db]: https://wq.io/wq.db
[wq Django template]: https://github.com/wq/wq-django-template
[xlsform-converter]: https://github.com/wq/xlsform-converter
[Getting Started]: https://wq.io/docs/setup
[wq.db.rest]: https://wq.io/docs/about-rest
