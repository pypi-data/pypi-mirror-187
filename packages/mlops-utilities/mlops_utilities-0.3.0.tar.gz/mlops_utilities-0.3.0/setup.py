# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlops_utilities']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26,<1.27',
 'omegaconf>=2.2,<2.3',
 'pytest==7.2.0',
 'sagemaker>=2.129,<2.130']

setup_kwargs = {
    'name': 'mlops-utilities',
    'version': '0.3.0',
    'description': '',
    'long_description': '- [Intro](#intro)\n- [Installation](#installation)\n- [User Guide](#user-guide)\n  - [Concepts](#concepts)\n  - [\\[NOT IMPLEMENTED\\] The simplest case](#not-implemented-the-simplest-case)\n    - [You prepared / Project Structure:](#you-prepared--project-structure)\n    - [Library usage:](#library-usage)\n  - [\\[NOT IMPLEMENTED\\] The "simple" layout](#not-implemented-the-simple-layout)\n  - [The "default" layout](#the-default-layout)\n    - [You prepared / Project Structure:](#you-prepared--project-structure-1)\n    - [Structure of Pipeline Definition Script](#structure-of-pipeline-definition-script)\n    - [Component Structure and Environments](#component-structure-and-environments)\n    - [Library usage:](#library-usage-1)\n\n# Intro\nMLOps Utilities provides:\n- Implementation of high level operations most commonly occuring in workflows for production-ready ML models:\n  - Dataset versioning\n  - Building of training pipeline from initial code sources: Jupyter notebooks, python modules, etc.\n  - Training pipeline deployment\n  - Scheduling its execution on timely or event-triggered execution, e.g., new dataset version\n  - Zero-config lineage tracking\n  - Zero-config model versioning and model registry\n  - Model packaging and deployment\n  - Model endpoint management\n  - Data quality monitoring setup\n  - Model quality monitoring setup\n- In AWS cloud.\n\n# Installation\n`pip install mlops-utilities`\n\n# User Guide\n## Concepts\nThis library simplifies MLOps workflow implementation by greatly reducing amount of boilerplate code and configuration required. It does so by relying on specific conventions for project structure  described below.\n\nUse cases are sorted by increasing complexity.\n\n## \\[NOT IMPLEMENTED\\] The simplest case\nYou made a single Jupyter notebook that:\n* takes as input a training dataset location\n* preprocess data using Pandas\n* train model using scikit-learn\n* evaluate model using scikit-learn\n* uses one of the predefined kernels of Sagemaker Studio as an execution environment.\n* You have not changed this environment with `pip install`s. If you did then check the next use case.\n\n### You prepared / Project Structure:\n```\n<PROJECT_ROOT>\n  |-- my_project07.ipynb\n```\n\n### Library usage:\nTo build and deploy pipeline (in SageMaker) use the following CLI command:\n```\nmlops upsert-pipeline TODO header of help description for this command\n```\nor from code:\n```python\nfrom mlops_utilities.actions import upsert_pipeline\n...\nTODO\nupsert_pipeline(TODO args example)\n```\n\nTo execute the previously upserted pipeline:\n```\nmlops run-pipeline TODO\n```\n\nTraining pipeline execution produces new model version in model registry. To deploy it onto real-time endpoint use the following CLI command:\n```\nmlops deploy-model TODO\n```\n\n## \\[NOT IMPLEMENTED\\] The "simple" layout\nTODO - The same as default layout but without writing pipeline definition using SageMaker SDK.\n\n## The "default" layout\nIf you separated code of different pipeline steps and defined training pipeline using SageMaker SDK.\n\n### You prepared / Project Structure:\n```\n<PROJECT_ROOT>\n  |-- components\n          |-- preprocessing\n                  |-- preprocess.py\n                  |__ requirements.txt\n          |-- training\n                  |__ train.py\n          |__ <folders for other steps>\n  |-- pipelines\n          |-- training_pipeline.py\n          |-- training_pipeline.defaults.conf\n          |-- inference_pipeline.py\n          |__ inference_pipeline.defaults.conf\n```\n### Structure of Pipeline Definition Script\nTODO\n\n### Component Structure and Environments\nTODO\n\n### Library usage:\nTo build and deploy pipeline (in SageMaker) use the following CLI command:\n```\nmlops upsert-pipeline TODO header of help description for this command\n```\nor from code:\n```python\nfrom mlops_utilities.actions import upsert_pipeline\n...\nTODO\nupsert_pipeline(TODO args example)\n```\n\nTo execute the previously upserted pipeline:\n```\nmlops run-pipeline TODO\n```\n\nTraining pipeline execution produces new model version in model registry. To deploy it onto real-time endpoint use the following CLI command:\n```\nmlops deploy-model TODO\n```',
    'author': 'Provectus Team',
    'author_email': 'mlops@provectus.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
