import sys
import os

def getMimeTypes(inputFile):
	mime=dict()
	infile=open(inputFile,'r',errors='ignore')
	lines=infile.readlines()
	counter=0
	for line in lines:
		if 'Content-Type' in line:
			counter+=1
			words=line.split('=')
			if words[1].replace('\n','') not in mime:
				mime[words[1].replace('\n','')]=1
			else:
				mime[words[1].replace('\n','')]+=1
	print('Number of URLs: '+str(counter))
	return mime



def main():
  #Check for proper arguments
  if len(sys.argv) != 2:
    print ('usage: python3 fetch_mime.py inputFile')
    sys.exit(1)
  
  inputFile=sys.argv[1]
  mimeTypes=getMimeTypes(inputFile)
  print(mimeTypes)
  print('********************************distinct types*********************************')
  print(len(mimeTypes))
  

if __name__ == '__main__':
  main()