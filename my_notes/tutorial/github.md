

# Make a new feature with new branch
So do this when we want to make a new feature
### Step 1: Create new Branch on Github
From github repo, click on all branches
<img width="840" height="552" alt="Image" src="https://github.com/user-attachments/assets/cbab5712-c91c-4efb-84de-643e399391c4" />
Then click a 
<img width="1676" height="541" alt="Image" src="https://github.com/user-attachments/assets/bee44258-e284-4df5-babb-306ede117de4" />
Then just type your new branch name on pop up window
<img width="853" height="547" alt="Image" src="https://github.com/user-attachments/assets/006e4188-b356-48f7-8200-9a2a2f465938" />
if successful, you should see something as following
<img width="1563" height="630" alt="Image" src="https://github.com/user-attachments/assets/10f7156e-1b1e-4fab-9458-4288f71d2d28" />
So there are three concepts here:

- Default branch: [This](https://docs.github.com/en/pull-requests/reference/branches#about-the-default-branch) branch is the one shown to the user when they visit our github repo. it is where to pull request. Production-ready product should reside in here
- Your branch: [All](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository/viewing-branches-in-your-repository) the branches that we have *push* access to (exclude the *main*)
- Active branch: show all branches(exclude the main) that is commited in the last three months
- Stale branch: opposite to active branch, show now branch anyone has commited in last three months. Recommended to be used to determine which branch to be deleted
### Step 2: Create new branch at local git
From the VS code Source Control, click on the create 
<img width="925" height="696" alt="Image" src="https://github.com/user-attachments/assets/a997a2eb-ba68-4607-907f-3522e9e01af2" />

Then type your new branch name, it should mactch with the one you created on github branch

<img width="813" height="142" alt="Image" src="https://github.com/user-attachments/assets/db93a427-6314-484f-84f0-b25f23a971af" />

### Step 3: Check your current branch
#### 3.1: Using VS Code
<img width="452" height="977" alt="Image" src="https://github.com/user-attachments/assets/d93a06f4-5727-48bc-abaa-6bcab58fd575" />
Those give you the hints where you are residing

#### 3.2 Using git Command Line

```
git branch --show-current # show the current branch
git branch # show all the branch together with current branch

```
### Step 4 Link to your remote branch
Click on publish to new branch
<img width="537" height="621" alt="Image" src="https://github.com/user-attachments/assets/d26fce65-e0fe-4f33-a579-7b44ac2cd8ec" />
Now you can check with git branch connect to what remote by using

```
git branch -vv
```
**Remote Branch**: the [reference](https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches) to the remote server branches. They can not be manually updated in order to represent the current state on the remote server. Think it as a bookmark where it is only updated automatically by the git when we do something on the internet. they have the format as. origin/\<local_branch\>
**Local Branch**: This is the one we just created  in step 2 and will be the one we manually update in the future
### Step 5: Switch between branch
In the git terminology, swithcing between branch is called *checkout*
#### 5.1: using vs code
From the left bottem corner, click on the branch name
<img width="1437" height="622" alt="Image" src="https://github.com/user-attachments/assets/b8c4b4b8-2815-4b74-852f-3f07d8503cef" />
Depend on which branch want to switch, click on its name in the *Branches* section
<img width="792" height="382" alt="Image" src="https://github.com/user-attachments/assets/29f74302-3ed4-4d93-a121-ae1aace34fef" />

#### 5.2: Using Git cli
Use
```
git switch <branch_name> # newer version with simplified syntax
git checkout <branch_name> # older one
```
### Step 6: Create a pull request
Go to Pull Request section and click on the new Pull Request
<img width="1788" height="817" alt="Image" src="https://github.com/user-attachments/assets/83bef108-9347-4783-b04b-b0b96baddc73" />
In the following, choose **main*** for base and **status_hud** for change
<img width="1562" height="635" alt="Image" src="https://github.com/user-attachments/assets/8b168e8b-f639-493d-bcfb-94e1046c5942" />

- Base: [where](https://docs.github.com/en/pull-requests/how-tos/create-pull-requests/creating-a-pull-request) we want to merge the change to. It is the destination branch 
- Compare: where we want to take the change from. It is the source branch
So we take all the change from **status_hud** and merge it into the base **main**
Then click on the Create New Pull request
<img width="1567" height="665" alt="Image" src="https://github.com/user-attachments/assets/28957814-cecf-4f04-8d8a-7d57853568f0" />
Next Fill in the Title and Description as you want and then click on Create Pull Request
<img width="1627" height="812" alt="Image" src="https://github.com/user-attachments/assets/7cf937aa-42d0-4618-9c5a-f60d86cdeb79" />
Now your pull request should be created. Click Pull Request section again to check it
<img width="1615" height="571" alt="Image" src="https://github.com/user-attachments/assets/43fe5a54-e5ad-4d5c-8101-8c63fb22b9ac" />

### Step 7: Merge the pull request
Since this is just simple pull request without any conflict, It allow us to automatically merge it into main brach. Click on merge pull request
<img width="1275" height="876" alt="Image" src="https://github.com/user-attachments/assets/e72b2c1a-8334-4389-8dbd-573279ae3982" />
then click on Confirm merge

<img width="1085" height="511" alt="Image" src="https://github.com/user-attachments/assets/8e3dde00-f940-40ed-8334-715d8932b50c" />
Now you have just merged a pull request. Now you should switch back to the local main branch and pull from the remote server. So that is pretty much basic of pull request

# Solve the conflict in merging request
### Step 1: Create the pull request
this step is similiar to the step 6
### Step 2: Resolve conflict
What difference from above is that it doesn't show the green words.Instead, it states there is a conflict and shows you which files you need to resolve. Now click on the *Resolve Conflict*
<img width="1147" height="736" alt="Image" src="https://github.com/user-attachments/assets/b3dcd30c-fffe-401f-a13c-1db62fb94b2d" />
After that you will see below
<img width="1896" height="547" alt="Image" src="https://github.com/user-attachments/assets/9de8f37b-c67a-4bf9-bec5-7d4e90c3dd15" />
So currently, there is only one conflict in the file *ProjectileManager.py*. those << and >> are ***conflict markers*** represent where those changes are:

- <<<<: this mark the destination file. The file we want to merge change into

- \>>>>: this mark the source file. The file where we take the change from
Yes I know this is somewhat weird since the base branch has become the source of change. However it has its own reason. Based on [this](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-on-github), when we resolve a conflict, we actually merge entire *base* branch into *head* branch whereas normal *PR* is the opposite. This is done to make the source branch up-to-date with the base branch and ensure smooth merging back to the base branch.
Okay to resolve conflict, we simply remove the conflicts markers and lines we don't want. Only keep the lines from either file you want. You can click **accept...** to make it faster
<img width="657" height="226" alt="Image" src="https://github.com/user-attachments/assets/569b598b-7cb1-47ea-82a7-668b296247ae" />

#### Mark resolved
when done with all conflict, click on mark as resolved for each file
<img width="1892" height="370" alt="Image" src="https://github.com/user-attachments/assets/5ab160a0-faa0-47eb-bc46-4941d9727038" />
After that click on ***Commit merge***
<img width="1894" height="710" alt="Image" src="https://github.com/user-attachments/assets/f877e40c-ff52-42f6-833b-bc6706277185" />

### Step 3: Merge the conflict
After step 2, you source branch has additional commit which is the merge from main to feature branch. Now you feature branch is update to date with the *main* so we can merge the pull request
<img width="1152" height="795" alt="Image" src="https://github.com/user-attachments/assets/79e434ff-daf4-4c1d-b878-c203eb4dfee2" />






# Add a license
As we progress more professional, we should state it clearly that how should our product is treated. One of the best way is to state our software license. Github allow us to dit through license file
### Step 1 Create File
click on **Add file** and **Create new file**
<img width="1512" height="757" alt="Image" src="https://github.com/user-attachments/assets/cb90a27e-c61e-4da2-ab07-553e7448cd11" />

### Step 2 License template
Name the file as "LICENSE" and it should pop up the phrase "Choose a license template". click on it
<img width="1902" height="321" alt="Image" src="https://github.com/user-attachments/assets/dd96c8da-0b41-47f1-b945-6877b57f94ea" />

### Step 3: Choose your suitable license
the top three bold one are popular one:
- ***Apache License:***For large project where it needs some protection
- ***GNU General Public License v3.0:*** If someone use the code in their project, they also need to release the project under the same GPL license. However, they only need to do this if they intented to publish source code on internet. If they use it internally, they are not obligated to do [so](https://vendure.io/blog/busting-the-myth-of-gpl)
- ***MIT License:*** For most personal projects and porfolio. Basically do whatever you want but notice 
Since this project is mainly for porforlio, i was intending to choose the MIT license. HOWEVER, the sort implementation i used had the GPL license. This mean that i have to make it GPL as well. You can quick check if the licnese you chose is compatible in p[here](https://fossa.com/resources/license-compliance-tools/license-compatibility-checker/gpl-3-0-vs-mit/). So we will choose GPL 3.0
Click on "GNU General Public License v3.0" and then click on "Review and submit"
<img width="1481" height="565" alt="Image" src="https://github.com/user-attachments/assets/eae5f8ad-9eff-4183-a176-c1a0f3a58c09" />

### Step 4: Commit the changes
Step 3 only fill up the template but it has not created any file yet. When the information is filled in your LICENSE file and you are happy with it, click on the commit changes
# Remove tracked file
if you accidentally stage change a file, you can not just remove it by using the *.gitignore*. We need to untrack it first
```
git rm --cached <file_name> # Remove track for the file
git rm -r --cached <folder_name> # Remove track for the folder
```




# Unrelated command lines for pip
well this is un related to github overally so I put at last.
### Create requirements txt
```
pip freeze > requirements.txt # Create txt
# the cud121 might need to specify the path
# add this to requirements.txt 
# --extra-index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt # import dependency from txt

```
### Create folder structure
go on [here](https://www.readmecodegen.com/file-tree/github-file-tree-visualizer)
