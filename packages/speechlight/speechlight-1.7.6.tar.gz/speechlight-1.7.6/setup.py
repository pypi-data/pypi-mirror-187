# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['speechlight']

package_data = \
{'': ['*'], 'speechlight': ['speech_libs/*']}

extras_require = \
{':sys_platform == "darwin"': ['pyobjc>=8.4,<9.0'],
 ':sys_platform == "win32"': ['pywin32>=303,<400']}

setup_kwargs = {
    'name': 'speechlight',
    'version': '1.7.6',
    'description': 'A lightweight Python library providing a common interface to multiple TTS and screen reader APIs.',
    'long_description': '# Speechlight\n\n[![Current Version on PyPi]][PyPi]\n[![License]][License Page]\n[![Supported Python Versions]][PyPi]\n[![PyPi Downloads in Last 7 Days]][PyPi Download Stats]\n[![PyPi Downloads in Last 30 Days]][PyPi Download Stats]\n[![PyPi Total Downloads]][PyPi Download Stats]\n\nA lightweight [Python][] library providing a common interface to multiple [TTS][] and [screen reader][] APIs. See the [API reference][] for more information.\n\n\n## License And Credits\n\nSpeechlight is licensed under the terms of the [Mozilla Public License, version 2.0.][License Page]\nSpeechlight was originally created by [Nick Stockton.][Nick Stockton GitHub]\nmacOS support by Jacob Schmude.\n\n\n## Installation\n\n```\npip install --user speechlight\n```\n\n\n## Running From Source\n\n### Windows-specific Instructions\n\nExecute the following commands from the root directory of this repository to install the virtual environment and project dependencies.\n```\npy -3 -m venv .venv\n.venv\\Scripts\\activate.bat\npip install --upgrade --require-hashes --requirement requirements-poetry.txt\npoetry install --no-ansi\npre-commit install -t pre-commit\npre-commit install -t pre-push\n```\n\n### Linux-specific Instructions\n\nExecute the following commands from the root directory of this repository to install the virtual environment and project dependencies.\n```\npython3 -m venv .venv\nsource .venv/bin/activate\npip install --upgrade --require-hashes --requirement requirements-poetry.txt\npoetry install --no-ansi\npre-commit install -t pre-commit\npre-commit install -t pre-push\n```\n\n\n## Example Usage\n\n```\nfrom speechlight import speech\n\n# Say something.\nspeech.say("Hello world!")\n\n# Say something else, interrupting the currently speaking text.\nspeech.say("I\'m a rood computer!", interrupt=True)\n\n# Cancel the currently speaking message.\nspeech.silence()\n\n# Braille something.\nspeech.braille("Braille dots go bump in the night.")\n\n# Speak and braille text at the same time.\nspeech.output("Read along with me.")\n\n# And to interrupt speech.\nspeech.output("Rood!", interrupt=True)\n```\n\n\n[Current Version on PyPi]: https://img.shields.io/pypi/v/speechlight.svg\n[License]: https://img.shields.io/github/license/nstockton/speechlight.svg\n[License Page]: https://nstockton.github.io/speechlight/license (License Page)\n[Supported Python Versions]: https://img.shields.io/pypi/pyversions/speechlight.svg\n[PyPi]: https://pypi.org/project/speechlight (Speechlight on PyPi)\n[PyPi Downloads in Last 7 Days]: https://pepy.tech/badge/speechlight/week\n[PyPi Downloads in Last 30 Days]: https://pepy.tech/badge/speechlight/month\n[PyPi Total Downloads]: https://pepy.tech/badge/speechlight\n[PyPi Download Stats]: https://pepy.tech/project/speechlight (Download Statistics)\n[Python]: https://python.org (Python Main Page)\n[TTS]: https://en.wikipedia.org/wiki/Speech_synthesis (Speech Synthesis Wikipedia Page)\n[screen reader]: https://en.wikipedia.org/wiki/Screen_reader (Screen Reader Wikipedia Page)\n[API reference]: https://nstockton.github.io/speechlight/api (Speechlight API reference Page)\n[Nick Stockton GitHub]: https://github.com/nstockton (My Profile On GitHub)\n',
    'author': 'Nick Stockton',
    'author_email': 'nstockton@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nstockton/speechlight',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
