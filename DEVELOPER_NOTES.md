# Developer notes and GitHub workflow

## Standard workflow to fix one GitHub issue

1. Local: start with the master branch, and make sure there are no uncommitted edits
2. Local: make and test the edits
3. GitHub: create a branch specific to the issue (a 'feature' branch), and select to open the branch in GitHub Desktop
   
   Note: there's an option to do this in the right bar when viewing an issue, but, you can also create a branch from the repo home page at any time
4. Local: make sure the active branch automatically changes to the branch just created on GitHub; if not, you may need to Pull from origin then select the branch by hand
5. Local: commit the edits to that feature branch
6. Local or GitHub: create a pull request to merge the feature branch into master; GitHub Desktop should offer to do this afer completing the previous step
7. GitHub: the pull request web page will tell you whether there are any conflicts to resolve; resolve if any, then, merge the pull request
8. GitHub: from the pull request page, delete the feature branch

## Create and publish new release using bumpver
bumpver works to modify the files locally, but, it doesn't do the commit, commit push, tag, and tag push, probably due to windows path delimiter problems.  So, here's the workflow to create a new release:

1. from github desktop, open a powershell for the repo in question (repository --> open in powershell)
2. bumpver update --minor    (this will increment the middle number and reset the last number to zero, e.g. 3.0.1 --> 3.1.0; use --major for the first number, or --patch for the last number)

NOTE: this will modify four files in the repo where version number is specified, but it will likely fail to do the commit and push that would trigger the github action to make the new tag and the pyinstaller build:

.github/workflows/release.yml
bumpver.toml
radiolog.iss
radiolog.py

It will probably fail with this message:
PS C:\Users\caver\Documents\GitHub\radiolog> bumpver update --minor
INFO    - fetching tags from remote (to turn off use: -n / --no-fetch)
INFO    - Old Version: 3.0.1
INFO    - New Version: 3.1.0
ERROR   - Error running subcommand: ['git', 'add', '--update', '.githubworkflowsrelease.yml']
fatal: pathspec '.githubworkflowsrelease.yml' did not match any files
PS C:\Users\caver\Documents\GitHub\radiolog>

This is probably due to Windows path delimiter issues - see related emails 8/19/2022
Ideally, bumpver would do the following steps too, but you can do them by hand here:

3. in github desktop, commit the modified files and push to master
4. in github desktop, make a tag whose name is the new version name, on the commit from the previous step (History --> right-click on the most recent commit)
5. in github desktop, push the tag to master (up-arrow from History, or, Push Origin from Changes as with any other recent local commit)

This will start the github action.  It will take a few minutes to complete.  While it is running, there will be a brown dot on the repo home page, which you can click to see live progress.  When it finishes, there should be a new release, and you should get an email saying that you can download the assets from the release page.

## Create a new beta release
From the GitHub releases page, select 'Draft a new release'.
Specify what branch (the 'feature' branch) the release should be built from.
Specify a tag name like '3.4.1beta' - use the next version number in order, and the word 'beta' with no space.
Enter any notes that you want.
Create the tag which will start the build process - you will have to look in the Actions page to see the progress.

## Build a test executable on a local clone
Run 'pyinstaller radiolog.spec'.  The executable will be created in the dist/radiolog directory.  Debugging pyinstaller is beyond the scope of this set of notes; it has been running smoothly recently.
