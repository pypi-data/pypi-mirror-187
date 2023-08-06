# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wordcab', 'wordcab.core_objects']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1', 'requests>=2.28.1', 'validators>=0.20.0']

entry_points = \
{'console_scripts': ['wordcab = wordcab.__main__:main']}

setup_kwargs = {
    'name': 'wordcab',
    'version': '0.4.1',
    'description': 'Wordcab Python SDK',
    'long_description': '<h1 align="center">Wordcab Python</h1>\n\n<div align="center">\n\t<a  href="https://pypi.org/project/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/v/wordcab.svg" />\n\t</a>\n\t<a  href="https://pypi.org/project/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/pyversions/wordcab" />\n\t</a>\n\t<a  href="https://github.com/Wordcab/wordcab-python/blob/main/LICENSE" target="_blank">\n\t\t<img src="https://img.shields.io/pypi/l/wordcab" />\n\t</a>\n\t<a  href="https://github.com/Wordcab/wordcab-python/actions?workflow=Tests" target="_blank">\n\t\t<img src="https://github.com/Wordcab/wordcab-python/workflows/Tests/badge.svg" />\n\t</a>\n\t<a  href="https://app.codecov.io/gh/Wordcab/wordcab-python" target="_blank">\n\t\t<img src="https://codecov.io/gh/Wordcab/wordcab-python/branch/main/graph/badge.svg" />\n\t</a>\n</div>\n\n<div align="center">\n\t<a href="https://linkedin.com/company/wordcab" target="_blank">\n\t\t<img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />\n\t</a>\n</div>\n\n### What is Wordcab?\n\n**Summarize any business communications at scale with Wordcab\'s API.**\n\n**Wordcab** is a summarization service that provides a simple API to summarize any `audio`, `text`, or `JSON` file.\n\nIt also includes compatibility with famous transcripts platforms like [AssemblyAI](https://www.assemblyai.com/),\n[Deepgram](https://deepgram.com/), [Rev.ai](https://www.rev.ai/), [Otter.ai](https://otter.ai/), or\n[Sonix.ai](https://sonix.ai/).\n\n### Getting started\n\nYou can learn more about Wordcab services and pricing on [our website](https://wordcab.com/).\n\nIf you want to try out the API, you can [signup](https://wordcab.com/signup/) for a free account and start using the API\nright away.\n\n## Requirements\n\n- Os: Linux, Mac, Windows\n- Python 3.8+\n\n## Installation\n\nYou can install _Wordcab Python_ via [pip] from [PyPI]:\n\n```console\n$ pip install wordcab\n```\n\nStart using the API with any python script right away!\n\n## Usage\n\n### Quick video demo\n\n[<img src="https://cdn.loom.com/sessions/thumbnails/25150a30c593467fa1632145ff2dea6f-with-play.gif" width="50%">](https://www.loom.com/embed/25150a30c593467fa1632145ff2dea6f "Quick Python Package Demo")\n\n### Start Summary full pipeline\n\n```python\nimport time\nfrom wordcab import retrieve_job, retrieve_summary, start_summary\nfrom wordcab.core_objects import AudioSource, GenericSource, InMemorySource\n\n\n# Prepare your input source\n## For a transcript stored as a .txt or .json file\nsource = GenericSource(filepath="path/to/file.txt")  # Or file.json\n## For a transcript stored as an audio file\nsource = AudioSource(filepath="path/to/file.mp3")\n## For a transcript already in memory\ntranscript = {"transcript": ["SPEAKER A: Hello.", "SPEAKER B: Hi."]}\nsource = InMemorySource(obj=transcript)\n\n# Launch the Summarization job\njob = start_summary(\n\tsource_object=source,\n\tdisplay_name="sample_txt",\n\tsummary_type="no_speaker",\n\tsummary_length=3,\n\ttags=["sample", "text"],\n)\n\n# Wait for the job completion\nwhile True:\n\tjob = retrieve_job(job_name=job.job_name)\n\tif job.job_status == "SummaryComplete":\n\t\tbreak\n\telse:\n\t\ttime.sleep(3)\n\n# Get the summary id\nsummary_id = job.summary_details["summary_id"]\n# Retrieve the summary\nsummary = retrieve_summary(summary_id=summary_id)\n\n# Get all information from the retrieved summary\nfor k, v in summary.__dict__.items():\n    print(f"{k}: {v}")\n\n# Get the summary as one block of text\nfor k, v in summary.summary:\n\tprint(f"Summary Length: {k}")\n\tprint(f"Summary: {v[\'structured_summary\'].summary}")\n```\n\n### Documentation\n\nPlease see the [Documentation](https://wordcab-python.readthedocs.io/) for more details.\n\n## Contributing\n\nContributions are very welcome. 🚀\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [Apache 2.0 license][license],\n_Wordcab Python SDK_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]\'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/Wordcab/wordcab-python/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/Wordcab/wordcab-python/blob/main/LICENSE\n[contributor guide]: https://github.com/Wordcab/wordcab-python/blob/main/CONTRIBUTING.md\n[command-line reference]: https://wordcab-python.readthedocs.io/en/latest/usage.html\n',
    'author': 'Wordcab',
    'author_email': 'info@wordcab.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Wordcab/wordcab-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
