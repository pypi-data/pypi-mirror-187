# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sbrunner_pre_commit_hooks']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML']

entry_points = \
{'console_scripts': ['pre-commit-copyright = '
                     'sbrunner_pre_commit_hooks.copyright:main',
                     'pre-commit-run-in-dir = '
                     'sbrunner_pre_commit_hooks.run_in_dir:main',
                     'pre-commit-workflow-timeout = '
                     'sbrunner_pre_commit_hooks.workflow_timeout:main']}

setup_kwargs = {
    'name': 'sbrunner-pre-commit-hooks',
    'version': '0.2.3',
    'description': 'Pre commit hook by sbrunner',
    'long_description': '# Pre commit hooks\n\n[pre-commit](https://pre-commit.com/) hook used to...\n\nCheck if the copyright is up to date (using the Git history).\n\n## Adding to your `.pre-commit-config.yaml`\n\n```yaml\nci:\n  skip:\n    # Skip the copyright check on pre-commit.ci because we don\'t have the Git history\n    - copyright\n    - copyright-required\n    # Poetry didn\'t works with Python 3.11\n    - poetry-lock\n    - poetry-check\n\nrepos:\n  - repo: https://github.com/sbrunner/pre-commit-hooks\n    rev: <version> # Use the ref you want to point at\n    hooks:\n      # Check that the copyright is up to date\n      - id: copyright\n      # Check that the copyright is present and up to date\n      - id: copyright-required\n      # Require a timeout in GitHub workflow files\n      - id: workflows-require-timeout\n      # Check Poetry config\n      - id: poetry-check\n        additional_dependencies:\n          - poetry==<version>\n      # Do Poetry lock\n      - id: poetry-lock\n        additional_dependencies:\n          - poetry==<version>\n      # Do Pipfile lock\n      - id: pipenv-lock\n        additional_dependencies:\n          - pipenv==<version>\n      # Do Helm lock (helm should be installed)\n      - id: helm-lock\n```\n\n## Copyright configuration\n\nThe default values used in the `.github/copyright.yaml` file.\n\nDefault values:\n\n```yaml\none_date_re: \' Copyright \\\\(c\\\\) (?P<year>[0-9]{4})"))\'\ntow_date_re: \' Copyright \\\\(c\\\\) (?P<from>[0-9]{4})-(?P<to>[0-9]{4})")\'\ntow_date_format: \' Copyright (c) {from}-{to}")\'\n```\n',
    'author': 'Stéphane Brunner',
    'author_email': 'stephane.brunner@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sbrunner/pre-commit-hooks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
