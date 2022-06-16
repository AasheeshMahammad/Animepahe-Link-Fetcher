import os, fnmatch
import time
import webbrowser as web
import sys,wmi


def add_links(files,links,arr):
    path=''
    for i in arr:
        d_file=open(path+str(files[i]),'r')
        for line in d_file:
            hi = line.strip().split("-")[-1].strip()
            if "https" in hi:
                links.append(hi)
        d_file.close()

n = len(sys.argv)-1
start=time.time()
path="./"
listOfFiles = os.listdir(path)
pattern = "*.txt"
files=[]
i=1
file_name=""
choice=-1;sel=[]
for y in sys.argv:
    if "name=" in y and ".txt" in y:
        file_name=y.split("=")[-1::][0]
        break
#os.system("cls")
for entry in listOfFiles:
    if fnmatch.fnmatch(entry, pattern):
           files.append(entry)
           if file_name=="":
                print(str(i)+"."+str(entry))
           if str(file_name)==str(entry):
                choice=i
                break
           i=i+1
if choice==-1:
    sel=input("Enter :")
    try:
        sel=sel.split(",")
        temp=[]
        for i in range(len(sel)):
            if(sel[i].isdigit):
                sel[i]=int(sel[i])-1
    except :
           quit()
else:
    sel.append(choice-1)
start=time.time()

for i in sel:
    if(0 <= i < len(files)):
        pass
    else:
        quit()
links=[]
add_links(files,links,sel)
len_l=0
if len(links) < 25:
    links.reverse()
else:
    len_l=1
input("Open Chrome and Enter")
chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'  #chrome path
if len_l==0:
    for i in range(0,len(links)):
        web.get(chrome_path).open_new_tab(links[i])
else:
    temp_num=len(links)
    len_l=0
    first_hold=True
    for _ in range(0,len(links),25):
        temp=[]
        try:
            for x in range(0,25):
                temp.append(links[len_l+x])
        except:
            pass
        temp.reverse()
        try:
            for y in range(0,25):
                web.get(chrome_path).open_new(temp[y])
                len_l=len_l+1
            input("Enter...")
        except:
            pass