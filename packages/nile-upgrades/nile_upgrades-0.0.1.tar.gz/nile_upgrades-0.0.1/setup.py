# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nile_upgrades']

package_data = \
{'': ['*'], 'nile_upgrades': ['artifacts/*']}

install_requires = \
['click>=8.0.4,<9.0.0']

entry_points = \
{'console_scripts': ['compile = compile_proxy:main'],
 'nile_plugins.nre': ['deploy_proxy = nile_upgrades.deploy_proxy.deploy_proxy',
                      'upgrade_proxy = '
                      'nile_upgrades.upgrade_proxy.upgrade_proxy']}

setup_kwargs = {
    'name': 'nile-upgrades',
    'version': '0.0.1',
    'description': 'Nile plugin to deploy and manage upgradeable smart contracts on StarkNet',
    'long_description': '# OpenZeppelin Nile Upgrades\n\nPlugin for [Nile](https://github.com/OpenZeppelin/nile) to deploy and manage [upgradeable smart contracts](https://docs.openzeppelin.com/contracts-cairo/proxies) on StarkNet.\n\n> ## ⚠️ WARNING! ⚠️\n>\n> **This plugin does not currently validate contracts for upgrade safety.**\n>\n> This repo contains highly experimental code.\n> Expect rapid iteration.\n> **Use at your own risk.**\n\n## Installation\n\n```\npip install nile-upgrades\n```\n\n## Usage\n\nRun the following functions from scripts with the `NileRuntimeEnvironment`.\n\n### `deploy_proxy`\n\nDeploy an upgradeable proxy for an implementation contract.\n\nReturns a Nile Transaction instance representing the proxy deployment.\n\n```\nasync def deploy_proxy(\n    nre,\n    account,\n    contract_name,\n    salt,\n    unique,\n    initializer_args,\n    initializer=\'initializer\',\n    alias=None,\n    max_fee_declare_impl=None,\n    max_fee_declare_proxy=None,\n    max_fee_deploy_proxy=None,\n)\n```\n\n- `nre` - the `NileRuntimeEnvironment` object.\n\n- `account` - the Account to use.\n\n- `contract_name` - the name of the implementation contract.\n\n- `salt` and `unique` - UDC specific arguments for proxy address generation.\n\n- `initializer_args` - array of arguments for the initializer function.\n\n- `initializer` - initializer function name. Defaults to `\'initializer\'`.\n\n- `alias` - Unique identifier for your proxy. Defaults to `None`.\n\n- `max_fee_declare_impl` - Maximum fee for declaring the implementation contract. Defaults to `None`.\n\n- `max_fee_declare_proxy` - Maximum fee for declaring the proxy contract. Defaults to `None`.\n\n- `max_fee_deploy_proxy` - Maximum fee for deploying the proxy contract. Defaults to `None`.\n\nExample usage:\n```\ntx = await nre.deploy_proxy(nre, account, "my_contract_v1", 123, True, ["arg for initializer"])\ntx_status, proxy_address, abi = await tx.execute(watch_mode="track")\n```\n\n### `upgrade_proxy`  \n\nUpgrade a proxy to a different implementation contract.\n\nReturns a Nile Transaction instance representing the upgrade operation.\n\n```\nasync def upgrade_proxy(\n    nre,\n    account,\n    proxy_address_or_alias,\n    contract_name,\n    max_fee_declare_impl=None,\n    max_fee_upgrade_proxy=None,\n)\n```\n\n- `nre` - the `NileRuntimeEnvironment` object.\n\n- `account` - the Account to use.\n\n- `proxy_address_or_alias` - the proxy address or alias.\n\n- `contract_name` - the name of the implementation contract to upgrade to.\n\n- `max_fee_declare_impl` - Maximum fee for declaring the new implementation contract. Defaults to `None`.\n\n- `max_fee_upgrade_proxy` - Maximum fee for upgrading the proxy to the new implementation. Defaults to `None`.\n\nExample usage:\n```\ntx = await nre.upgrade_proxy(nre, account, proxy_address, "my_contract_v2")\ntx_status = await tx.execute(watch_mode="track")\n```\n\n## Contribute\n\n### Setup\n\n#### Using the latest Nile release supported by this plugin\n\n1. Install [Poetry](https://python-poetry.org/docs/#installation)\n2. Clone this project.\n3. From this project\'s root, create a virtualenv, activate it, and install dependencies:\n```\npython3.9 -m venv env\nsource env/bin/activate\npoetry install\npip install -e .\npoetry run compile\n```\n\n**or**\n\n#### Using current Nile source code\n\n1. Install [Poetry](https://python-poetry.org/docs/#installation)\n2. Clone https://github.com/OpenZeppelin/nile\n3. Clone this project.\n4. From this project\'s root, create a virtualenv, activate it, and install dependencies:\n```\npython3.9 -m venv env\nsource env/bin/activate\npoetry install\npip install -e <your_path_to_nile_repo_from_step_2>\npip install -e .\npoetry run compile\n```\n\n### Testing\n\n`poetry run pytest tests`\n',
    'author': 'Eric Lau',
    'author_email': 'ericglau@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenZeppelin/openzeppelin-nile-upgrades',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
