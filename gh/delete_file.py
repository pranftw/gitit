import sys
sys.path.append("/Users/pranavsastry")
from gitit import GitIt

gitit = GitIt()
if(len(sys.argv)==4):
    gitit.delete_file(sys.argv[1],sys.argv[2],sys.argv[3])
elif(len(sys.argv)==3):
    gitit.delete_file(sys.argv[1],sys.argv[2])
else:
    print("Function takes 3 parameters. Repo name, Filename, Filepath in GitHub=None")
