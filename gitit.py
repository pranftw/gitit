# Author: Pranav Sastry [Copyright (c) 2021]
# Created: 8th Feb 2021
# Disclaimer: File contents shouldn't be copied into another repository without prior permission by emailing to pranava.sri@gmail.com,
#             however to fork the repository, you needn't take any

class GitIt:
    '''
        Methods:
            __init__ - Constructor for GitIt class
            search_file - Search for a file recursively in GitHub Repository based on the content in the base_url
            create_repo - Create a new Repository with minimal readme and mit license_template
            delete_repo - Delete a Repository
            delete_file - Delete a file
            search_dir - Search for a directory recursively in GitHub Repository based on the content in the base_url
            delete_dir - Delete a directory and its contents recursively
            update_file - Upload a local file on your computer to GitHub
            update_dir - Update a local directory on your computer to GitHub
    '''

    # Imports TODO: Modify the path in sys.path.append based on your system's python package location
    import sys
    sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")
    import base64 as b64
    import os
    import requests
    import json


    def __init__(self):
        '''
            TODO: Set environment variables on your system that contains
                  your GitHub Username and GitHub Token
            Parameters:
                None
            Returns:
                None
        '''
        self.owner = GitIt.os.getenv('GITHUB_USERNAME')
        self.token = GitIt.os.getenv('GITHUB_TOKEN')
        self.headers = {"Authorization": "token {}".format(self.token),"Accept":"application/vnd.github.v3+json"}


    def search_file(self,base_url,fname):
        '''
            Parameters:
                base_url (string): GitHub API URL in which to search for a file
                fname (string): Name of the file to be searched
            Returns:
                flag (boolean): True if file is found, else False
                path (string): path of file if found, else None
                sha (string): sha of file if found, else None
        '''
        repo_contents = GitIt.requests.get(base_url,headers=self.headers).json()
        flag = False
        path = None
        sha = None
        for content in repo_contents:
            try:
                if(content["type"]=="file"):
                    if(content["name"]==fname):
                        flag = True
                        path = content["path"]
                        sha = content["sha"]
                        break
                else:
                    url = base_url+"/{}".format(content["name"])
                    flag,path,sha = self.search_file(url,fname)
                    if(flag):
                        break
            except:
                pass
        return flag,path,sha


    def create_repo(self,name,license="mit",is_private=None):
        '''
            Parameters:
                name (string): Name of the new repo
                license (string): License Template of the new repo. Default - mit
                is_private (string): false if the new repo is Public, else the new repo is Private Default - None
            Returns:
                None
        '''
        print("Creating Repo...")
        url = "https://api.github.com/user/repos"
        if(is_private=="false"):
            params = {"name":name,"auto_init":True,"license_template":license,"private":False}
        else:
            params = {"name":name,"auto_init":True,"license_template":license,"private":True}
        r = GitIt.requests.post(url,headers=self.headers,data=GitIt.json.dumps(params))
        print(r.text)


    def delete_repo(self,repo):
        '''
            Parameters:
                repo (string): Name of the repo to be deleted
            Returns:
                None
        '''
        print("Deleting Repo...")
        url = "https://api.github.com/repos/{}/{}".format(self.owner,repo) 
        r = GitIt.requests.delete(url,headers=self.headers)
        print(r.text)


    def delete_file(self,repo,fname,filepath_gh=None):
        '''
            Parameters:
                repo (string): Name of the Repository
                fname (string): Name of the file to be deleted
                filepath_gh (string): Path of the file on GitHub. Default - None
            Returns:
                None
        '''
        print("Deleting file...")
        if(filepath_gh is None):
            _,path,sha = self.search_file("https://api.github.com/repos/{}/{}/contents".format(self.owner,repo),fname=fname)
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,path)
        else:
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,filepath_gh)
            file_contents = GitIt.requests.get(url,headers=self.headers).json()
            sha = file_contents["sha"]
        params = {"message":"Deleted {}".format(fname),"sha":sha}
        r = GitIt.requests.delete(url,headers=self.headers,data=GitIt.json.dumps(params))
        print(r.text)


    def search_dir(self,base_url,dir_name):
        '''
            Parameters:
                base_url (string): GitHub API URL in which to search for a directory
                dir_name (string): Name of the Directory to be searched for
            Returns:
                flag (boolean): True if directory is found, else False
                path (string): Path of the directory if found, else None
        '''
        flag = False
        path = None
        repo_contents = GitIt.requests.get(base_url,headers=self.headers).json()
        for content in repo_contents:
            try:
                if(content["type"]=="dir"):
                    if(content["name"]==dir_name):
                        flag = True
                        path = content["path"]
                        break
                    else:
                        url = base_url+"/{}".format(content["name"])
                        flag,path = self.search_dir(url,dir_name)
                        if(flag):
                            break
            except:
                pass
        return flag,path


    def delete_dir(self,repo,dir_name,dir_path=None):
        '''
            Parameters:
                repo (string): Name of the Repository
                dir_name (string): Name of the directory to be deleted
                dir_path (string): Path of the directory to be deleted. Default - None
            Returns:
                None
        '''
        print("Deleting directory...")
        if(dir_path is None):
            _,path = self.search_dir(base_url="https://api.github.com/repos/{}/{}/contents".format(self.owner,repo),dir_name=dir_name)
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,path)
        else:
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,dir_path)
        repo_contents = GitIt.requests.get(url,headers=self.headers).json()
        for content in repo_contents:
            if(content["type"]=="file"):
                self.delete_file(repo,fname=content["name"],filepath_gh=content["path"])
            else:
                self.delete_dir(repo,content["name"],dir_path=content["path"])


    def update_file(self,repo,filepath_local,message="",filepath_gh=None):
        '''
            Parameters:
                repo (string): Name of the Repository
                filepath_local (string): Path of the file on your local computer
                message (string): Commit message. Default - "", if Default, then when file is created,
                                  "Added filename.py" will be default and if updated "Updated filename.py"
                                  will be the default commit messages
                filepath_gh (string): Path of the file on GitHub, default - None
            Returns:
                None
        '''
        file_b64 = GitIt.b64.b64encode(open(filepath_local,"rb").read()).decode("ascii")
        fname = filepath_local.split("/")[-1]
        if(filepath_gh is not None):
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,filepath_gh)
            sha = None
            url_contents = GitIt.requests.get(url,headers=self.headers).json()
            try:
                sha = url_contents["sha"]
                path = url_contents["path"]
            except:
                pass
            if(sha is None):
                print("File not present! Creating file...")
                if(message==""):
                    message = "Added {}".format(fname)
                params = {"message":message,"content":file_b64,"path":filepath_gh}
            else:
                print("File already present! Updating file...")
                if(message==""):
                    message = "Added {}".format(fname)
                params = {"message":message,"content":file_b64,"path":path,"sha":sha}
        else:
            _,path,sha = self.search_file("https://api.github.com/repos/{}/{}/contents".format(self.owner,repo),fname=fname)
            if(sha is None):
                url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,fname)
                print("File not present! Creating file...")
                if(message==""):
                    message = "Added {}".format(fname)
                params = {"message":message,"content":file_b64,"path":fname}
            else:
                url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,path)
                print("File already present! Updating file...")
                if(message==""):
                    message = "Updated {}".format(fname)
                params = {"message":message,"content":file_b64,"path":path,"sha":sha}
        r = GitIt.requests.put(url,headers=self.headers,data=GitIt.json.dumps(params))
        print(r.text)


    def update_dir(self,repo,base_path,dirpath_local,dirpath_gh=None):
        '''
            Parameters:
                repo (string): Name of the Repository
                base_path (string): Path of the directory on your computer
                dirpath_local (string): Path of the directory on your computer
                dirpath_gh (string): Path of the direcory on GitHub to be updated
            Returns:
                None
        '''
        print("Updating directory...")
        print(dirpath_local)
        dir_contents = GitIt.os.listdir(dirpath_local)
        dir_name = dirpath_local.split("/")[-1]
        for content in dir_contents:
            temp_path = "{}/{}".format(dirpath_local,content)
            dir_tree = temp_path.replace("{}/".format(base_path),"")
            if(dirpath_gh is not None):
                dir_tree = "{}/".format(dirpath_gh) + dir_tree
            # print(dir_tree)
            if(GitIt.os.path.isdir(temp_path)):
                self.update_dir(repo,base_path,temp_path,dirpath_gh)
            else:
                self.update_file(repo,temp_path,"",dir_tree)


# Example code
# gitit = GitIt()
# flag,path,sha = gitit.search_file(base_url="https://api.github.com/repos/pranavsastry/neowise/contents",fname="profiles_settings.xml")
# gitit.update_file("stargar","Hello World! This is test!","/Users/pranavsastry/Documents/CP/DivideIt.java","test/DivideIt.java")
# gitit.delete_file("stargar","test")
# gitit.create_repo("hello")
# gitit.delete_repo("hello")
# flag,path = gitit.search_dir(base_url="https://api.github.com/repos/pranavsastry/neowise/contents",dir_name="Visuals")
# print(flag)
# print(path)
# gitit.update_file("stargar","Yahoo! New Commit","/Users/pranavsastry/Documents/CP/KDivisibleSum.java","test/hello/hello_again/KDivisibleSum.java")
# gitit.delete_dir("stargar","test")
# gitit.update_dir("testing","/Users/pranavsastry/Documents/javaFiles","/Users/pranavsastry/Documents/javaFiles")
