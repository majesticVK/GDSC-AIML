# GDSC-AIML
Projects and resources for GDG AI/ML

<span>
  <img src="https://static.vecteezy.com/system/resources/previews/008/216/725/original/deep-learning-word-concepts-blue-banner-neural-network-machine-learning-infographics-with-icons-on-color-background-isolated-typography-illustration-with-text-vector.jpg" width="50%" height="300" />

  <img src="https://github.com/user-attachments/assets/cd9cd8f8-3749-4b45-a4dc-60dcd7207dc2?raw=true" height="300" />
</span>

## How to submit your projects:
- To begin, fork this repository. This creates a copy of this repository in your github account.
- Clone the forked repository. Go to code section of your repo and copy the HTTPS Link in your clipboard.
- Execute the following command in Command Prompt or Git Bash in desired loaction to load repository files in your local machine:
```
  git clone [HTTPS_Link]
```
- Open your text editor [VS code/ Sublime/ Visual Studio] and open terminal and run the following command:
```
  git branch
```
-> This should display <b>"main"</b>. Never edit files directly in the main branch
- Create a new branch for editing and working upon by executing the following command:
```
  git checkout -b [branch_name]
```
- After working on your project files, save all changes and run the following commands:
```
  git add --all
```
```
  git commit -m [descriptive_message_explaining_your_commited_files]
```
- Run the following command before pushing your files:
```
  git remote -v
```
-> Shows streams of repository while working remotely. You should see the following:
```origin [HTTPS_Link]```
- Run the following commands to add stream to original repository [upstream]:
```
  git remote add upstream https://github.com/lordsid003/GDSC-AIML.git
```
```
  git pull upstream main
```
-> This syncs your current branch with the original repository and ensures, its up to date.
- Finally, push your files using:
```
  git push
```
- Raise your Pull request with proper description and title:
- After your PR has been merged, run the following commands:
```
  git switch main
```
Switches to main branch on your local machine
```
  git merge [branch_name]
```
-> You can then delete your branch and sync your repository with the original repository.
