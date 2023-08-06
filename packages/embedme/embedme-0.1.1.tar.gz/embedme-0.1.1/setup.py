# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embedme']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0', 'openai>=0.26.1,<0.27.0']

setup_kwargs = {
    'name': 'embedme',
    'version': '0.1.1',
    'description': "Easily create and search text embeddings using OpenAI's API using json for local storage. Just add dicts of info and search! Built for rapid prototyping.",
    'long_description': '# Embedme\n\nEmbedme is a python module that allows you to easily use embeddings from text fields with OpenAI\'s Embedding API and store them in a local folder.\n\nIt\'s like a lazy version of pinecone - Numpy is actually pretty fast for embeddings stuff at smaller scale, why overthink stuff? We store the data and vectors as json and build the numpy array before you search (and store it until you add more)\n\n## Installation\n\nTo install Embedme, you can use pip:\n\n```sh\npip install embedme\n```\n\n## Setup\n\nThe only thing you _must_ do before you use `embedme` is setup auth with OpenAI. We use it to embed your items and search queries, so it is required. I don\'t want to touch **any** of that code - just sign in how they tell you to, either in the script via a file for the key, or an environment variable for your key.\n\n[OpenAI Python Module (With Auth Instructions)](https://github.com/openai/openai-python)\n\n## Usage\n\nEmbedme provides a simple interface to use embeddings from text fields with OpenAI\'s Embedding API and store them in a local folder.\n\nCheck out the example notebook for a better example, but useage is something like:\n\n```py\nimport openai\nimport nltk\nfrom more_itertools import chunked\nfrom embedme import Embedme\nfrom tqdm import tqdm\n\n# Downloading the NLTK corpus\nnltk.download(\'gutenberg\')\n\n# Creating an instance of the Embedme class\nembedme = Embedme(data_folder=\'.embedme\', model="text-embedding-ada-002")\n\n# Getting the text\ntext = nltk.corpus.gutenberg.raw(\'melville-moby_dick.txt\')\n\n# Splitting the text into sentences\nsentences = nltk.sent_tokenize(text)\n\ninput("Hey this call will cost you money and take a minute. Like, a few cents probably, but wanted to warn you.")\n\nfor i, chunk in enumerate(tqdm(chunked(sentences, 20))):\n    data = {\'name\': f\'moby_dick_chunk_{i}\', \'text\': \' \'.join(chunk)}\n    embedme.add(data, save=False)\n\nembedme.save()\n```\n\nAnd to search:\n\n```py\nembedme.search("lessons")\n```\n\nYou can do anything you would want to with `.vectors` after you call `.prepare_search()` (or... search something, it\'s automatic mostly), like plot clusters, etc.\n\n## Follow Us\n\nSome friends and I are writing about large language model stuff at [SensibleDefaults.io](https://sensibledefaults.io), honest to god free. Follow us (or star this repo!) if this helps you!\n\n## Note\n\nEmbedme uses OpenAI\'s Embedding API to get embeddings for text fields, so an API key is required to use it. You can get one from https://beta.openai.com/signup/\n\nThe token limit today is about 8k, so... you\'re probably fine\n',
    'author': 'John Partee',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/morganpartee/embedme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
