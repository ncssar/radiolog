# Developer notes and GitHub workflow

## Standard workflow to fix one GitHub issue

1. Local: start with the master branch, and make sure there are no uncommitted edits
2. Local: make and test the edits
3. GitHub: create a branch specific to the issue (a 'feature' branch), and select to open the branch in GitHub Desktop
   
   Note: there's an option to do this in the right bar when viewing an issue, but, you can also create a branch from the repo home page at any time
   
   ![image](https://user-images.githubusercontent.com/18752102/207062951-865acd22-64df-40f6-8e6a-3ea3a699e4b1.png)

4. Local: make sure the active branch automatically changes to the branch just created on GitHub; if not, you may need to Pull from origin then select the branch by hand.  Make sure to bring the current changes to the feature branch.

![image](https://user-images.githubusercontent.com/18752102/207063441-fc24652c-932e-46a8-8257-cbcb8a175fca.png)


6. Local: commit the edits to that feature branch
7. Local or GitHub: create a pull request to merge the feature branch into master; GitHub Desktop should offer to do this afer completing the previous step
8. GitHub: the pull request web page will tell you whether there are any conflicts to resolve; resolve if any, then, merge the pull request
9. GitHub: from the pull request page, delete the feature branch

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

## Create a new beta release from a feature branch
1. From the GitHub releases page, select 'Draft a new release'.
2. Under 'Choose a tag', type in a new tag name like '3.4.1beta' - use the next version number in order, and the word 'beta' with no space.
3. Under 'Target', specify what branch (the 'feature' branch) the release should be built from.
4. Set the release title to the same as the tag name, or to anything else you want.
5. Enter any description you want.
6. Check 'Set as a pre-release' which should automatically uncheck 'Set as the latest release'.

![image](https://user-images.githubusercontent.com/18752102/207063846-b0fb915c-b4b5-4871-af8b-b760563ac9ee.png)

7. Click 'Publish release' which will start the build process.  You will have to look in the Actions page to see the progress.

## Build a test executable on a local clone
Run 'pyinstaller radiolog.spec'.  The executable will be created in the dist/radiolog directory.  Debugging pyinstaller is beyond the scope of this set of notes; it has been running smoothly recently.

## Build a test installer (e.g. to test edits to radiolog.iss before committing)
Run '\<Inno Setup install dir\>\ISCC.exe radiolog.iss' - this will build dist\radiolog-\<version\>-setup.exe.

## Run in a virtual environment (e.g. to test specific dependency versions)
On the development machine, a venv exists in Documents/GitHub/.radiolog.venv.
1. From Documents/GitHub, run ./.radiolog.venv/Scripts/activate.
2. Copy the latest GitHub/radiolog directory into the .radiolog.venv directory.
3. Install whatever module versions you want to test, probably by modifying requirements.txt then running 'pip -install requirements.txt'.
4. Running python or pyinstaller or ISSC from that virtual env will use whatever module versions you have installed into that virtual env.  The resulting builds will be placed in the non-virtual-env directory (Documents/GitHub/radiolog rather than Documents/GitHub/.radiolog.venv/radiolog).
