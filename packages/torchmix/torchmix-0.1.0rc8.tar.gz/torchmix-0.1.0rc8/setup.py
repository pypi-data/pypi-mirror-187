# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['torchmix',
 'torchmix.components',
 'torchmix.components.attention',
 'torchmix.components.container',
 'torchmix.components.feedforward',
 'torchmix.core',
 'torchmix.nn',
 'torchmix.third_party']

package_data = \
{'': ['*']}

install_requires = \
['einops>=0.6.0', 'hydra-core>=1.0.0', 'hydra-zen>=0.8.0', 'jaxtyping>=0.2.0']

setup_kwargs = {
    'name': 'torchmix',
    'version': '0.1.0rc8',
    'description': 'Flexible components for transformers 🧩',
    'long_description': '<h1 align="center">torchmix</h1>\n\n<h3 align="center">The missing component library for PyTorch</h3>\n\n<br />\n\n`torchmix` is a collection of pre-made PyTorch components designed to simplify model development process, primarily for **transformers**. Our goal is to enable easy adoption of cutting-edge components with minimal code and maximum scalability.\n\n**Note: `torchmix` is a prototype that is currently in development and has not been tested for production use. The API may change at any time.**\n\n## Install\n\nTo use `torchmix`, you will need to have `torch` already installed on your environment.\n\n```sh\npip install torchmix\n```\n\n## Documentation\n\nTo learn more, check out our [documentation](https://torchmix.vercel.app).\n\n## Contributing\n\nIf you have ideas for new components or ways to enhance the library, feel free to open an issue or start a discussion. We welcome all forms of feedback, including criticism and suggestions for significant design changes.\n\n## License\n\n`torchmix` is licensed under the MIT License.\n',
    'author': 'junhsss',
    'author_email': 'junhsssr@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
