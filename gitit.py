class GitIt:
    import sys
    sys.path.append("/opt/anaconda3/lib/python3.7/site-packages/")
    import base64 as b64
    import os
    import requests
    import json
    def __init__(self):
        self.owner = "pranavsastry"
        self.token = GitIt.os.getenv('GITHUB_TOKEN')
        self.headers = {"Authorization": "token {}".format(self.token),"Accept":"application/vnd.github.v3+json"}
    def search_file(self,base_url,fname):
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
    def create_repo(self,name,is_private=None):
        print("Creating Repo...")
        url = "https://api.github.com/user/repos" #POST
        if(is_private=="false"):
            params = {"name":name,"auto_init":True,"license_template":"mit","private":False}
        else:
            params = {"name":name,"auto_init":True,"license_template":"mit","private":True}
        r = GitIt.requests.post(url,headers=self.headers,data=GitIt.json.dumps(params))
        print(r.text)
    def delete_repo(self,repo):
        print("Deleting Repo...")
        url = "https://api.github.com/repos/{}/{}".format(self.owner,repo) #DELETE
        r = GitIt.requests.delete(url,headers=self.headers)
        print(r.text)
    def delete_file(self,repo,fname,filepath_gh=None):
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
    def update_file(self,repo,message,filepath_local,filepath_gh=None):
        file_b64 = GitIt.b64.b64encode(open(filepath_local,"rb").read()).decode("ascii")
        if(filepath_gh is not None):
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,filepath_gh)
            print("File not present! Creating file...")
            params = {"message":message,"content":file_b64,"path":filepath_gh}
        else:
            print("File already present! Updating file...")
            fname = filepath_local.split("/")[-1]
            _,path,sha = self.search_file("https://api.github.com/repos/{}/{}/contents".format(self.owner,repo),fname=fname)
            url = "https://api.github.com/repos/{}/{}/contents/{}".format(self.owner,repo,path)
            params = {"message":message,"content":file_b64,"path":path,"sha":sha}
        r = GitIt.requests.put(url,headers=self.headers,data=GitIt.json.dumps(params))
        print(r.text)

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
