import sys
sys.path.append("/Users/pranavsastry")
from gitit import GitIt

gitit = GitIt()
if(len(sys.argv)==3):
    gitit.create_repo(sys.argv[1],sys.argv[2])
elif(len(sys.argv)==2):
    gitit.create_repo(sys.argv[1])
else:
    print("Function takes 2 parameters. name, is_private=True")
