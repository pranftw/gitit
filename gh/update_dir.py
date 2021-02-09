import sys
sys.path.append("/Users/pranavsastry")
from gitit import GitIt

gitit = GitIt()
if(len(sys.argv)==5):
    gitit.update_dir(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
elif(len(sys.argv)==4):
    gitit.update_dir(sys.argv[1],sys.argv[2],sys.argv[3])
else:
    print("Function takes 4 parameters. Repo name, base_url, filepath_local, filepath_in_github=None")
