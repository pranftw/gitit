# gitit

<p float=left>
  <img src="logos/gitit_dark_trans.png" alt="logo" width="200" />
  <img src="logos/gitit_light_trans.png" alt="logo" width="200" />
</p>

<a href="https://raw.githubusercontent.com/pranavsastry/gitit/main/gitit.py"><h1>Download</h1></a><br>

# Instructions <br>
**1. Get your GitHub Access Token. Refer to this <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token">link</a>.<br> 2. Download gitit.py <br> 3. Import using `from gitit import GitIt` and use it a Python script. <br>**

# Creating Environment Variables
**We have used environment varaible to store the GitHub Access Token and GitHub Username securely on your local system. To create one on a Mac, follow the steps below.<br><br>1. Create a new dotfile using `mkdir ~/.dotfile_name` and edit it to add `export GITHUB_USERNAME="REPLACE_THIS_WITH_YOUR_GITHUB_USERNAME"` and `export GITHUB_TOKEN="REPLACE_THIS_WITH_YOUR_GITHUB_ACCESS_TOKEN"` <br>2. Source it using `source ~\.dotfile_name` on your terminal and you're all set<br>
<br>
NOTE: <br>
Sourcing using `source ~\.dotfile_name` is only valid as long as the terminal session and gets deleted once the terminal is closed<br>Hence add `source ~\.dotfile_name` to your `.bashrc` and `.bash_profile` for it to be always valid.<br>**
