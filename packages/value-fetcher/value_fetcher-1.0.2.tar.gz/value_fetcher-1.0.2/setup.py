# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['value_fetcher']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.27,<2.0.0', 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'value-fetcher',
    'version': '1.0.2',
    'description': 'Fetch a value from various sources, e.g AWS Secrets Manager and SSM Parameter Store',
    'long_description': '# Value fetcher\n## Introduction\nPython module to fetch values from multiple sources with optional defaults, including:\n- Environment variables\n- AWS Systems Manager (SSM) Parameter Store\n- AWS Secrets Manager\n\n## Usage\nInstall the package with the following:\n\n```shell\npip install value-fetcher\n```\n\n### Fetching values directly\nIn this use case, the value fetcher package makes it convenient to fetch values from the supported sources in a consistent and simplified manner.\n```python\nfrom value_fetcher import ValueFetcher\n\n# Instantiate value fetcher class\nfetcher = ValueFetcher()\n\n# Retrieve values from supported AWS sources\nmy_secret = fetcher.get_from_aws_secrets_manager(\'/my/secret/key\')\nmy_param = fetcher.get_from_aws_ssm_parameter_store(\'/my/parameter/key\')\n```\n\n### Configuring source locations dynamically\nIn this use case, environment variables are used to configure the sources for multiple keys.\nThis is useful in more complex applications where lots of values need to be fetched and the source needs to be configured dynamically.\nSee this [contact form handler repository](https://github.com/voquis/aws-lambda-contact-form-handler) for example usage.\n\nEnvironment variables can be appended to the configuration key name, setting the source of the value.\nThese are:\n- `_PARAMETER_STORE_NAME` - for AWS SSM Parameter Store\n- `_SECRETS_MANAGER_NAME` - for AWS Secrets Manager\n\nOne of the available configuration sources for each value must also be set by setting an environment variable ending with `_SOURCE` for the value name:\n- `env` - Environment variables (default)\n- `aws_ssm_parameter_store` - AWS Systems Manager (SSM) Parameter Store\n- `aws_secrets_manager` - AWS Secrets Manager\n\nFor example, to fetch `MY_PARAM` from AWS SSM Parameter Store and `MY_SECRET` from AWS Secrets Manager, consider the following python script (e.g. `app.py`) called subsequently by a shell script:\n\n```python\n# This file is app.py for example\nfrom value_fetcher import ValueFetcher\n\n# Instantiate value fetcher class, with optional defaults if values cannot be found\nfetcher = ValueFetcher({\n    \'MY_PARAM\': \'Default value if none can be found\',\n})\n\n# Retrieve values from supported AWS sources\nmy_secret = fetcher.get(\'MY_SECRET\')\nmy_param = fetcher.get(\'MY_PARAM\')\n\nprint(my_secret)\nprint(my_param)\n```\n\nThe above scripts would be called by the following shell script:\n```shell\n#!/usr/bin/bash\nMY_PARAM_SOURCE="aws_ssm_parameter_store"\nMY_PARAM_PARAMETER_STORE_NAME="/my/parameter/store/key/name"\n\nMY_SECRET_SOURCE="aws_secrets_manager"\nMY_SECRET_SECRETS_MANAGER_NAME="my/secrets/manager/key/name"\n\nexport MY_PARAM_SOURCE MY_PARAM_PARAMETER_STORE_NAME\nexport MY_SECRET_SOURCE MY_SECRET_SECRETS_MANAGER_NAME\n\n# For AWS ensure credentials are available, e.g. with AWS SSO, aws-vault, aws-profile etc.\npython app.py\n```\n\n## Development\nThis project uses Poetry for package management.\nAfter cloning, run:\n```\n./scripts/poetry.sh\n```\nto install dependencies for local development and running tests, etc.\n### Tests\n\nTo run static code analysers and unit tests:\n```\n./scripts/validate.sh\n```\n',
    'author': 'Voquis Limited',
    'author_email': 'opensource@voquis.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/voquis/value-fetcher',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
