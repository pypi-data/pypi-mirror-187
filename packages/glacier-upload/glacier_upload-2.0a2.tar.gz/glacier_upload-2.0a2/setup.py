# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['glacier_upload', 'glacier_upload.utils']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.47,<2.0.0', 'click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['glacier = glacier_upload.cli:glacier_cli']}

setup_kwargs = {
    'name': 'glacier-upload',
    'version': '2.0a2',
    'description': 'A helper tool to upload and manage archives in AWS Glacier Vaults',
    'long_description': '# glacier-upload\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)\n[![pypi](https://img.shields.io/pypi/v/glacier_upload)](https://pypi.org/project/glacier_upload/)\n[![License-GPLv3](https://img.shields.io/github/license/tbumi/glacier-upload)](https://github.com/tbumi/glacier-upload/blob/main/LICENSE)\n\nA helper tool to upload and manage archives in\n[Amazon S3 Glacier](https://docs.aws.amazon.com/amazonglacier/latest/dev/introduction.html)\nVaults. Amazon S3 Glacier is a cloud storage service that is optimized for long\nterm storage for a relatively cheap price.\n\n## Installation\n\nMinimum required Python version is 3.9. To install, run this in your terminal:\n\n```\n$ pip install glacier_upload\n```\n\n## Usage\n\n### Prerequisites\n\nTo upload an archive to Amazon S3 Glacier vault, ensure you have:\n\n-   Created an AWS account\n-   Created an Amazon S3 Glacier vault from the AWS CLI tool or the Management\n    Console\n\n### Uploading an archive\n\nAn upload can be performed by running `glacier upload` followed by the vault\nname and the file name(s) that you want to upload.\n\n```\nglacier upload VAULT_NAME FILE_NAME [FILE_NAME ...]\n```\n\n`FILE_NAME` can be one or more files or directories.\n\nThe script will:\n\n1. Read the file(s)\n2. Consolidate them into a `.tar.xz` archive if multiple `FILE_NAME`s are\n   specified or `FILE_NAME` is one or more directories\n3. Upload the file in one go if the file is less than 100 MB in size, or\n4. Split the file into chunks\n5. Spawn a number of threads that will upload the chunks in parallel. Note that\n   it will not read the entire file into memory, but only parts of the file as\n   it processes the chunks.\n6. Return the archive ID when complete. Consider saving this archive ID in a\n   safe place for retrieval purposes, because Amazon Glacier does not provide a\n   list of archives in realtime. See the "Requesting an inventory" section below\n   for details.\n\nThere are additional options to customize your upload, such as adding a\ndescription to the archive or configuring the number of threads or the size of\nparts. Run `glacier upload --help` for more information.\n\nIf a multipart upload is interrupted in the middle (because of an exception,\ninterrupted manually, or other reason), the script will show you the upload ID.\nThat upload ID can be used to resume the upload, using the same command but\nadding the `--upload-id` option, like so:\n\n```\nglacier upload --upload-id UPLOAD_ID VAULT_NAME FILE_NAME [FILE_NAME ...]\n```\n\n### Retrieving an archive\n\nRetrieving an archive in glacier requires two steps. First, initiate a\n"retrieval job" using:\n\n```\nglacier archive init-retrieval VAULT_NAME ARCHIVE_ID\n```\n\nTo see a list of archive IDs in a vault, see "Requesting an inventory" below.\n\nThen, the retrieval job will take some time to complete. Run the next step to\nboth check whether the job is complete and retrieve the archive if it has been\ncompleted.\n\n```\nglacier archive get VAULT_NAME JOB_ID FILE_NAME\n```\n\n### Requesting an inventory\n\nVaults do not provide realtime access to a list of their contents. To know what\na vault contains, you need to request an inventory of the archive, in a similar\nmanner to retrieving an archive. To initiate an inventory, run:\n\n```\nglacier inventory init-retrieval VAULT_NAME\n```\n\nThen, the inventory job will take some time to complete. Run the next step to\nboth check whether the job is complete and retrieve the inventory if it has been\ncompleted.\n\n```\nglacier inventory get VAULT_NAME JOB_ID\n```\n\n### Deleting an archive, deleting an upload job, creating/deleting a vault, etc.\n\nAll jobs other than uploading an archive and requesting/downloading an inventory\nor archive can be done using the AWS CLI. Those functionalities are not\nimplemented here to avoid duplication of work, and minimize maintenance efforts\nof this package.\n\n## Contributing\n\nContributions and/or bug fixes are welcome! Just make sure you\'ve read the below\nrequirements, then feel free to fork, make a topic branch, make your changes,\nand submit a PR.\n\n### Development Requirements\n\nBefore committing to this repo, install [poetry](https://python-poetry.org/) on\nyour local machine, then run these commands to setup your environment:\n\n```sh\npoetry install\npre-commit install\n```\n\nAll code is formatted with [black](https://github.com/psf/black). Consider\ninstalling an integration for it in your favourite text editor.\n',
    'author': 'Trapsilo Bumi',
    'author_email': 'tbumi@thpd.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tbumi/glacier-upload',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
