<h1 align="center"> 📝Github Notes📝 </h1>

# Table of Contents
<small>

- [1. Make a new feature with a new branch](#1-make-a-new-feature-with-a-new-branch)
  - [1.1 Create a new Branch on GitHub](#step-1-create-a-new-branch-on-github)
  - [1.2 Create a new branch locally in Git](#step-2-create-a-new-branch-locally-in-git)
  - [1.3 Check your current branch](#step-3-check-your-current-branch)
  - [1.4 Link to your remote branch](#step-4-link-to-your-remote-branch)
  - [1.5 Switch between branches](#step-5-switch-between-branches)
  - [1.6 Create a pull request](#step-6-create-a-pull-request)
  - [1.7 Merge the pull request](#step-7-merge-the-pull-request)
- [2. Solve the conflict in the merge request](#2-solve-the-conflict-in-the-merge-request)
  - [2.1 Create the pull request](#step-1-create-the-pull-request)
  - [2.2 Resolve conflict](#step-2-resolve-conflict)
  - [2.3 Merge the conflict](#step-3-merge-the-conflict)
- [3. Add a license](#3-add-a-license)
  - [3.1 Create File](#step-1-create-file)
  - [3.2 License template](#step-2-license-template)
  - [3.3 Choose a suitable license](#step-3-choose-a-suitable-license)
  - [3.4 Commit the changes](#step-4-commit-the-changes)
- [4. Remove tracked file](#4-remove-tracked-file)
- [5. Unrelated command lines for pip](#5-unrelated-command-lines-for-pip)

</small>

# 1 Make a new feature with a new branch
So do this when we want to make a new feature
### Step 1: Create a new Branch on GitHub
From the GitHub repo, click on All branches

<img width="840" height="552" alt="Image" src="https://github.com/user-attachments/assets/cbab5712-c91c-4efb-84de-643e399391c4" />

Then click New branch.

<img width="1676" height="541" alt="Image" src="https://github.com/user-attachments/assets/bee44258-e284-4df5-babb-306ede117de4" />

Then just type your new branch name in the pop-up window.

<img width="853" height="547" alt="Image" src="https://github.com/user-attachments/assets/006e4188-b356-48f7-8200-9a2a2f465938" />

If successful, you should see something as follows

<img width="1563" height="630" alt="Image" src="https://github.com/user-attachments/assets/10f7156e-1b1e-4fab-9458-4288f71d2d28" />

So there are three concepts here:

- **Default branch:** [This](https://docs.github.com/en/pull-requests/reference/branches#about-the-default-branch) branch is the one shown to the user when they visit our GitHub repo. It is where pull requests are. Production-ready product should reside here
- **Your branch:** [All](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository) the branches that we have *push* access to (exclude the *main*)
- **Active branch:** show all branches(exclude the main) that is commited in the last three months
- **Stale branch:** opposite to active branch, show all branches that anyone has committed in the last three months. Recommended to be used to determine which branch to delete


### Step 2: Create a new branch locally in Git
From the VS Code Source Control, click on Create 
<img width="925" height="696" alt="Image" src="https://github.com/user-attachments/assets/a997a2eb-ba68-4607-907f-3522e9e01af2" />

Then type your new branch name. It should match the one you created on GitHub

<img width="813" height="142" alt="Image" src="https://github.com/user-attachments/assets/db93a427-6314-484f-84f0-b25f23a971af" />

### Step 3: Check your current branch
#### 3.1: Using VS Code
<img width="452" height="977" alt="Image" src="https://github.com/user-attachments/assets/d93a06f4-5727-48bc-abaa-6bcab58fd575" />
Those give you the hints where you are residing

#### 3.2 Using git Command Line

```
git branch --show-current # show the current branch
git branch # show all the branches together with the current branch

```
### Step 4 Link to your remote branch
Click on Publish to new branch
<img width="537" height="621" alt="Image" src="https://github.com/user-attachments/assets/d26fce65-e0fe-4f33-a579-7b44ac2cd8ec" />
Now you can check with git branch which remote it connects to by using

```
git branch -vv
```
**Remote Branch**: the [reference](https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches) to the remote server branches. They can not be manually updated in order to represent the current state on the remote server. Think of it as a bookmark where it is only updated automatically by Git when we do something on the internet. They have the format as. origin/\<local_branch\>
**Local Branch**: This is the one we just created  in step 2 and will be the one we manually update in the future
### Step 5: Switch between branches
In git terminology, switching between branches is called *checkout*
#### 5.1: Using VS Code
From the left bottom corner, click on the branch name
<img width="1437" height="622" alt="Image" src="https://github.com/user-attachments/assets/b8c4b4b8-2815-4b74-852f-3f07d8503cef" />
Depending on which branch you want to switch to, click on its name in the *Branches* section
<img width="792" height="382" alt="Image" src="https://github.com/user-attachments/assets/29f74302-3ed4-4d93-a121-ae1aace34fef" />

#### 5.2: Using Git cli
Use
```
git switch <branch_name> # newer version with simplified syntax
git checkout <branch_name> # older one
```
### Step 6: Create a pull request
Go to the Pull Requests section and click on the new Pull Request
<img width="1788" height="817" alt="Image" src="https://github.com/user-attachments/assets/83bef108-9347-4783-b04b-b0b96baddc73" />
In the following, choose **main*** for base and **status_hud** for change
<img width="1562" height="635" alt="Image" src="https://github.com/user-attachments/assets/8b168e8b-f639-493d-bcfb-94e1046c5942" />

- **Base:** [where](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request) we want to merge the change to. It is the destination branch 
- **Compare:** where we want to take the change from. It is the source branch
So we take all the changes from **status_hud** and merge them into the base **main**
Then click on Create New Pull Request
<img width="1567" height="665" alt="Image" src="https://github.com/user-attachments/assets/28957814-cecf-4f04-8d8a-7d57853568f0" />
Next, fill in the Title and Description as you want, and then click on Create Pull Request
<img width="1627" height="812" alt="Image" src="https://github.com/user-attachments/assets/7cf937aa-42d0-4618-9c5a-f60d86cdeb79" />
Now your pull request should be created. Click the Pull Request section again to check it
<img width="1615" height="571" alt="Image" src="https://github.com/user-attachments/assets/43fe5a54-e5ad-4d5c-8101-8c63fb22b9ac" />

### Step 7: Merge the pull request
Since this is just a simple pull request without any conflicts, it allows us to automatically merge it into the main branch. Click on Merge pull request
<img width="1275" height="876" alt="Image" src="https://github.com/user-attachments/assets/e72b2c1a-8334-4389-8dbd-573279ae3982" />
Then click on Confirm merge

<img width="1085" height="511" alt="Image" src="https://github.com/user-attachments/assets/8e3dde00-f940-40ed-8334-715d8932b50c" />
Now you have just merged a pull request. Now you should switch back to the local main branch and pull from the remote server. So that is pretty much the basics of a pull request.

# 2 Solve the conflict in the merge request
### Step 1: Create the pull request
This step is similar to step 6
### Step 2: Resolve conflict
The difference from above is that it doesn't show the green words. Instead, it states there is a conflict and shows you which files you need to resolve. Now click on the *Resolve Conflict*
<img width="1147" height="736" alt="Image" src="https://github.com/user-attachments/assets/b3dcd30c-fffe-401f-a13c-1db62fb94b2d" />
After that, you will see below
<img width="1896" height="547" alt="Image" src="https://github.com/user-attachments/assets/9de8f37b-c67a-4bf9-bec5-7d4e90c3dd15" />
So currently, there is only one conflict in the file *ProjectileManager.py*. those << and >> are ***conflict markers*** represent where those changes are:

- <<<<: this marks the destination file. The file we want to merge changes into

- \>>>>: this marks the source file. The file where we take the change from
Yes, I know this is somewhat weird since the base branch has become the source of change. However, it has its own reason. Based on [this](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-on-github), when we resolve a conflict, we actually merge the entire *base* branch into the *head* branch, whereas a normal *PR* is the opposite. This is done to make the source branch up-to-date with the base branch and ensure smooth merging back to the base branch.
To resolve conflicts, we simply remove the conflict markers and lines we don't want. Only keep the lines from either file you want. You can click **accept...** to make it faster
<img width="657" height="226" alt="Image" src="https://github.com/user-attachments/assets/569b598b-7cb1-47ea-82a7-668b296247ae" />

#### Mark resolved
When done with all conflicts, click on Mark as Resolved for each file
<img width="1892" height="370" alt="Image" src="https://github.com/user-attachments/assets/5ab160a0-faa0-47eb-bc46-4941d9727038" />
After that, click on ***Commit merge***
<img width="1894" height="710" alt="Image" src="https://github.com/user-attachments/assets/f877e40c-ff52-42f6-833b-bc6706277185" />

### Step 3: Merge the conflict
After step 2, your source branch has an additional commit, which is the merge from main to the feature branch. Now your feature branch is up to date with *main*, so we can merge the pull request
<img width="1152" height="795" alt="Image" src="https://github.com/user-attachments/assets/79e434ff-daf4-4c1d-b878-c203eb4dfee2" />

# 3 Add a license
As we progress more professionally, we should state clearly how our product should be treated. One of the best ways is to state our software license. GitHub allows us to edit a license file
### Step 1 Create File
click on **Add file** and **Create new file**
<img width="1512" height="757" alt="Image" src="https://github.com/user-attachments/assets/cb90a27e-c61e-4da2-ab07-553e7448cd11" />

### Step 2: License template
Name the file "LICENSE," and it should pop up the phrase "Choose a license template". click on it
<img width="1902" height="321" alt="Image" src="https://github.com/user-attachments/assets/dd96c8da-0b41-47f1-b945-6877b57f94ea" />

### Step 3: Choose a suitable license
The top three bold ones are popular:
- ***Apache License:*** For large projects where it needs some protection
- ***GNU General Public License v3.0:*** If someone uses the code in their project, they also need to release the project under the same GPL license. However, they only need to do this if they intend to publish source code on the internet. If they use it internally, they are not obligated to do [so](https://vendure.io/blog/busting-the-myth-of-gpl)
- ***MIT License:*** For most personal projects and portfolio. Basically do whatever you want, but notice 
Since this project is mainly for portfolio, I was intending to choose the MIT license. HOWEVER, the sort implementation I used had the GPL license. This means that I have to make it GPL as well. You can quickly check if the license you chose is compatible [here](https://fossa.com/resources/license-compliance-tools/license-compatibility-checker/gpl-3-0-vs-mit/). So we will choose GPL 3.0
Click on "GNU General Public License v3.0" and then click on "Review and submit"
<img width="1481" height="565" alt="Image" src="https://github.com/user-attachments/assets/eae5f8ad-9eff-4183-a176-c1a0f3a58c09" />

### Step 4: Commit the changes
Step 3 only fills out the template, but it has not created any file yet. When the information is filled in your LICENSE file, and you are happy with it, click on Commit Changes
# 4 Remove tracked file
If you accidentally stage a change to a file, you can not just remove it by using the *.gitignore*. We need to untrack it first
```
git rm --cached <file_name> # Remove track for the file
git rm -r --cached <folder_name> # Remove track for the folder
```

# 5 Unrelated command lines for pip
Well, this is unrelated to GitHub overall, so I put it at the end.
### Create requirements.txt
```
pip freeze > requirements.txt # Create txt
# the cud121 might need to specify the path
# add this to requirements.txt 
# --extra-index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt # import dependencies from txt

```
### Create folder structure
Go to [here](https://www.readmecodegen.com/file-tree/github-file-tree-visualizer)
