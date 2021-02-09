import sys
sys.path.append("/Users/pranavsastry")
from gitit import GitIt

gitit = GitIt()
if(len(sys.argv)==2):
    gitit.delete_repo(sys.argv[1])
else:
    print("Function takes 1 parameter. Repo name")
