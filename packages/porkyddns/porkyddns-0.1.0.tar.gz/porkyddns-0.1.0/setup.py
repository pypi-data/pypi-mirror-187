# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['porkyddns']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'toml>=0.10.2,<0.11.0', 'urllib3>=1.26.14,<2.0.0']

entry_points = \
{'console_scripts': ['porkyddns = porkyddns.main:run']}

setup_kwargs = {
    'name': 'porkyddns',
    'version': '0.1.0',
    'description': 'Simple Porkbun DDNS Client',
    'long_description': '# PorkyDDNS\nSimple Porkbun DDNS Client\n\n## 💡 Features\n\n- Support for multiple subdomains on multiple domains\n- Easily and quickly configurable, with cron-able error reporting\n\n\n## 💾 Installation\n\n**Install PorkyDDNS using `pip`**\n```bash\n  $ pip install porkyddns\n  $ porkyddns\n```\n\n## 🔨 Usage\n\n- Edit the values in `porkyddns.toml.example` as required\n- Copy `porkyddns.toml.example` to `/etc/porkyddns.toml`\n- Run the `porkyddns` script on a cron job or systemd timer however often you want!\n\n\n## 📜 License\n\n[GPLv3-only](https://choosealicense.com/licenses/gpl-3.0/)\n\n',
    'author': 'Michal S.',
    'author_email': 'mchal_@tuta.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
