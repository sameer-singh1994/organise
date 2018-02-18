from collections import defaultdict
import shutil
import glob
import os, os.path
import heapq
import sys
import operator
import commands

##############top 10 largest files in current directory#######
directory = '/'#os.environ['HOME']
numfiles = int(10)

print "Checking for top 10 files(File Size).............."

filenames = (os.path.join(p, n) for p, _,f in os.walk(directory) for n in f)
filesizes = ((name, os.path.getsize(name)) for name in filenames)

actnames = []
_exhausted = object()

while(1):
	file = next(filenames, _exhausted)
	if file == _exhausted:
		break
	if file.split('/')[-1] == 'SingletonLock' or file.split('/')[-1] == 'lock' or file.split('/')[-1] == 'SingletonCookie' or '/snap/' in file or file.startswith('/run/') or file.startswith('/proc/') or file.startswith('/usr/') or file.startswith('/var/') or file.startswith('/dev/') or 'mozilla' in file or 'chrome' in file or '/mips-ar' in file:
		continue
	actnames.append(file)

bigfiles = heapq.nlargest(numfiles, actnames, key = os.path.getsize)
print "The top 10 largest files in the system(File Size):"
for b in bigfiles:
	temp = b[1:]+"{:"+str(round(os.path.getsize(b)/(1024.0*1024.0), 2))+"MB}"
	print temp

#############retreiving all the files in a given folder#######
a = glob.glob(os.environ['HOME']+"/Desktop/*")
a = list(set(a))
temp = []
for x in a:
	if x.endswith("organise.py"):
		pass
	else:
		temp.append(x)
a = temp

######dict of files with extensions as their key names########
filex = defaultdict(list)
for x in a:
	index = x.rfind('.')
	if(index is not -1):
		key = x[index+1:]
		filex[key].append(x)
	else:
		filex['folder'].append(x)

#print filex
#############for each file type creating a folder#############
for x in filex:
	if x is not 'folder':
		#print x
		if not os.path.exists(os.environ['HOME']+"/Documents/"+x):
			os.makedirs(os.environ['HOME']+"/Documents/"+x)

##adding all the files with same type in the same folder######
for x in filex:
	for y in filex[x]:
		if x is not 'folder':
			shutil.move(y,os.environ['HOME']+"/Documents/"+x+"/")

print ""
print "Your Desktop is clean now !!!!!!!!!!"

#########Delete old files#####################################
print ""
print "Checking for files......."

a = commands.getoutput('find /home/ -type f -print0 | xargs -0 stat --format \'%Y :%y %n\' | sort -nr | cut -d: -f2- | tail -n 10 > output.txt') 
file1 = open("output.txt","r")
k = 1
emptline = []
lines = file1.readlines()

print "Oldest 10 files in the system(Access Time):"
print ""

for line in lines:
	line = str(k) + " ) " + line
	print line
	line1 = line.split()
	line1 = line1[5:]
	sr = str(line1)
	line3 =' '.join(line1)
	emptline.append(line3)
	k += 1

str1 = ""

print ""

while 1:
	print "Enter the corresponding number to remove the file using rm -f (EXIT to exit):"
	str1 = raw_input()
	if str1.upper() == "EXIT":
		commands.getoutput('rm -f output.txt')
		sys.exit(-1)
	print emptline[int(str1) - 1][2:]
	x = "Press Y to confirm delete this file and N to not: " + emptline[int(str1) - 1] + "\n"
	print x,
	temp = raw_input()

	if temp.upper() == "Y":
		if os.path.isdir(emptline[int(str1) - 1][2:]):
			shutil.rmtree(emptline[int(str1) - 1][2:])
		else:
			os.remove(emptline[int(str1) - 1][2:])
	else:
		continue
		
print emptline	




