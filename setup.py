import os
from setuptools import setup

LONG_DESCRIPTION = """
Project scaffolding tools for creating a new crowdsourcing or citizen science application with the wq framework.
"""


def readme():
    try:
        readme = open('README.md')
    except IOError:
        return LONG_DESCRIPTION
    return readme.read()


def create_wq_namespace():
    """
    Generate the wq namespace package
    (not checked in, as it technically is the parent of this folder)
    """
    if os.path.isdir("wq"):
        return
    os.makedirs("wq")
    init = open(os.path.join("wq", "__init__.py"), 'w')
    init.write("__import__('pkg_resources').declare_namespace(__name__)")


def list_package_data(root):
    """
    Include project template as package data
    """
    paths = []

    for base, dirs, files in os.walk(root, topdown=True):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        paths.extend([
            os.path.join(base, name) for name in files
            if name not in ('.git', 'package-lock.json')
        ])
    return paths

create_wq_namespace()

# Project template data
TEMPLATES = [
    'django_project',
]
TEMPLATE_DATA = []
for folder in TEMPLATES:
    TEMPLATE_DATA.extend(list_package_data(folder))

setup(
    name='wq.start',
    use_scm_version=True,
    author='S. Andrew Sheppard',
    author_email='andrew@wq.io',
    url='https://wq.io/wq.start',
    license='MIT',
    description=LONG_DESCRIPTION.strip(),
    long_description=readme(),
    long_description_content_type='text/markdown',
    entry_points={'wq': 'wq.start=wq.start'},
    packages=['wq.start'],
    package_dir={'wq.start': '.'},
    namespace_packages=['wq'],
    package_data={'wq.start': TEMPLATE_DATA},
    install_requires=[
        'wq.core',
        'psycopg2-binary',
        'xlsconv>=1.1.0',
    ],
    setup_requires=[
        'setuptools_scm',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: JavaScript',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Pre-processors',
    ]
)
