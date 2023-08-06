# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ontopic', 'ontopic.models']

package_data = \
{'': ['*'], 'ontopic.models': ['pretrained/*']}

install_requires = \
['numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'torch>=1.13.1,<2.0.0',
 'transformers>=4.25.1,<5.0.0']

extras_require = \
{':python_version >= "3.9" and python_version < "3.12"': ['scipy>=1.10.0,<2.0.0']}

setup_kwargs = {
    'name': 'ontopic',
    'version': '0.1.0',
    'description': '',
    'long_description': '# Example workflow\n\n\n## Load ontology\nvia github link or local directory\n\n```python\nimport ontopics as ot\nonthology = ot.load_onthology("https://github.com/OpenCS-ontology/OpenCS")\n\n# or \n\nonthology = ot.load_onthology("onthologies/OpenCS", objects = "", descriptions = "")\n```\n\n## Prepare topics for classification\n\n```python\n# topics is a \ntopics = onthology.prepare_topics()\n\n```\n\n## Classify text to ontologies\n\n```python\nfrom ontopic.models import TopicalClassifier\n\ntext = "In this paper we introduce novel NLP NER machine learning model"\nmodel = TopicalClassifier()\n\n# to get top 10 topics, 5 is by default\ntopics = model.predict(text, top=10)\n\n# to get topics which are above given threshold of \'probability\'\ntopics = model.predict(text, threshold=0.2)\n\n# to get topics and also probabilities\ntopics, proba = model.predict(text, proba=True)\n```\n',
    'author': 'GiveMeMoreData',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/GiveMeMoreData/ontopic',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
