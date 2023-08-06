# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seedspark',
 'seedspark.configs',
 'seedspark.contrib',
 'seedspark.contrib.test',
 'seedspark.dataquality',
 'seedspark.spark',
 'seedspark.spark.dataframe',
 'seedspark.spark.dataframe.compare',
 'seedspark.utils']

package_data = \
{'': ['*']}

install_requires = \
['lognub>=0.1.3,<0.2.0']

setup_kwargs = {
    'name': 'seedspark',
    'version': '0.2.0',
    'description': 'SeedSpark is an Extensible PySpark utility package to create production spark pipelines and dev-test them in dev environments',
    'long_description': '# SeedSpark\n\n**SeedSpark** is an open-source is an Extensible PySpark utility package to create production spark pipelines and dev-test them in dev environments or to perform end to end tests. The goal is to enable rapid development of Spark pipelines via PySpark on Spark clusters\xa0and locally test the pipeline by using various utilities.\n\n## TODO\n\n1. Move logwrap [on top of loguru] extension out as a seperate package.\n1. Add Test containers for [amundsen](https://www.amundsen.io/amundsen/), etc..\n\n## Getting Started\n\n1. Setup [SDKMAN](#setup-sdkman)\n1. Setup [Java](#setup-java)\n1. Setup [Apache Spark](#setup-apache-spark)\n1. Install [Poetry](#poetry)\n1. Install Pre-commit and [follow instruction in here](PreCommit.MD)\n1. Run [tests locally](#running-tests-locally)\n\n### Setup SDKMAN\n\nSDKMAN is a tool for managing parallel Versions of multiple Software Development Kits on any Unix based system. It provides a convenient command line interface for installing, switching, removing and listing Candidates.\nSDKMAN! installs smoothly on Mac OSX, Linux, WSL, Cygwin, etc... Support Bash and ZSH shells.\nSee documentation on the [SDKMAN! website](https://sdkman.io).\n\nOpen your favourite terminal and enter the following:\n\n```shell\n$ curl -s https://get.sdkman.io | bash\nIf the environment needs tweaking for SDKMAN to be installed,\nthe installer will prompt you accordingly and ask you to restart.\n\nNext, open a new terminal or enter:\n\n$ source "$HOME/.sdkman/bin/sdkman-init.sh"\n\nLastly, run the following code snippet to ensure that installation succeeded:\n\n$ sdk version\n```\n\n\n### Setup Java\n\nInstall Java Now open favourite terminal and enter the following:\n\n```shell\nList the AdoptOpenJDK OpenJDK versions\n$ sdk list java\n\nTo install For Java 11\n$ sdk install java 11.0.10.hs-adpt\n\nTo install For Java 11\n$ sdk install java 8.0.292.hs-adpt\n```\n\n### Setup Apache Spark\n\nInstall Java Now open favourite terminal and enter the following:\n\n```bash\nList the Apache Spark versions:\n$ sdk list spark\n\nTo install For Spark 3\n$ sdk install spark 3.0.2\n\nTo install For Spark 3.1\n$ sdk install spark 3.0.2\n```\n\n### Poetry\n\nPoetry [Commands](https://python-poetry.org/docs/cli/#search)\n\n```bash\npoetry install\n\npoetry update\n\n# --tree: List the dependencies as a tree.\n# --latest (-l): Show the latest version.\n# --outdated (-o): Show the latest version but only for packages that are outdated.\npoetry show -o\n```\n\n## Running Tests Locally\n\nTake a look at tests in `tests/dataquality` and `tests/jobs`\n\n```bash\n$ poetry run pytest\nRan 95 tests in 96.95s\n```\n\nNOTE: It\'s just curated stuff in this repo for personal usage.\n',
    'author': 'ChethanUK',
    'author_email': 'chethanuk@outlook.com',
    'maintainer': 'ChethanUK',
    'maintainer_email': 'chethanuk@outlook.com',
    'url': 'https://github.com/ChethanUK/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
