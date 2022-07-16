This document will lay out the manual steps needed to create a new release of 
radiolog.

## Prequisites:
1. Ensure you have installed the requirements-dev.txt 
`pip install -r requirements-dev.txt`
2. This project uses [semantic](https://semver.org) versioning, 
take a look at the details to understand that. 

## Manual Steps
1. AFTER all changes have been merged into main/master use
[bumpver](https://pypi.org/project/bumpver/) in the main/master 
branch to bump the version number, tag it, and push the tag and commit 
to the repository. More details can be found in the bumpver documentation. 
Quickly `bumpver update --major` or `--minor` or `--patch`. If this is 
your first time doing this add the `--dry` flag to the command and bumpver 
will show you the steps it intends to take without taking them.
