import sys
import os
import re

seggregatedURLs=dict()
urlList=list()
statusList=list()
metaDataList=list()
urlDict=dict()


def isPrintMetadata(str):
  if re.search('[a-zA-Z]', str):
    if ('content-type=' not in str.lower() and 'Status:' not in str):
      return True
  return False
  
def printFile(status,value):
  status=status.replace("(","").replace(")","")
  outfile=open(status,'w')
  for tempDict in value:
    if isPrintMetadata(tempDict['metadata'])==True:
      outfile.write('Unfetched URL: '+ tempDict['url']+'\n')
      outfile.write('Reason: '+ tempDict['metadata']+'\n')
    #if status=='db_unfetched':
      #if re.search('[a-zA-Z]', tempDict['metadata']):
        #if ('content-type=' not in tempDict['metadata'].lower() and 'Status:' not in tempDict['metadata']):
          #print(tempDict['metadata'])
  outfile.close()

def storeURL(line):
  global urlList
  if '://' in line:
    if len(line.split())==3:
      if line.split()[1]=='Version:':
        urlList.append(line.split()[0])
        
def isURL(line):
  if '://' in line:
    if len(line.split())==3:
      if line.split()[1]=='Version:':
        return True
  return False        
  
def isStatus(line):
  if '(db_' in line:
    return True
  return False
    
def storeStatus(line):
  global statusList
  if '(db_' in line:
    statusList.append(line.split()[2])

def isMetadata(line):
  if 'Metadata' in line:
    return True
  return False
    
def storeMetadata(line):
  global metaDataList
  metaDataList.append(line)    

def sortURLs():
  global urlList
  global statusList
  global metaDataList
  for i in range(0,len(urlList)):
    curStatus=statusList[i]
    curURL=urlList[i]
    curMetadata=metaDataList[i]
    if curStatus not in seggregatedURLs:
      seggregatedURLs[curStatus]=list()
      tempDict=dict()
      tempDict['url']=curURL
      tempDict['metadata']=curMetadata
      seggregatedURLs[curStatus].append(tempDict)
    else:
      tempList=seggregatedURLs[curStatus]
      tempDict=dict()
      tempDict['url']=curURL
      tempDict['metadata']=curMetadata
      tempList.append(tempDict)
      seggregatedURLs[curStatus]=tempList

  
def parseURLs(logFile):
  #read keywords from input file, remove end of line character and return keyword list.
  infile=open(logFile,'r',errors='ignore')
  lines=infile.readlines()
  global urlList
  global statusList
  global metaDataList
  global seggregatedURLs
  #print('inside parse logfile')
  for i in range(0,len(lines)):
    line=lines[i]
    if isURL(line)==True:
      storeURL(line)
    elif isStatus(line)==True:
      storeStatus(line)
    elif isMetadata(line)==True:
      storeMetadata(lines[i+1])

  #print('len(urlList) : '+ str(len(urlList)))
  #print('len(statusList) : '+ str(len(statusList)))
  #print('len(metaDataList) : '+ str(len(metaDataList)))
  
  #print(urlList)
  #print(statusList)
  #print(metaDataList)
  sortURLs()
  #print(seggregatedURLs)
  for status,value in seggregatedURLs.items():
    printFile(status,value)
  
def parseInputFiles(inputFile):
  infile=open(inputFile,'r',errors='ignore')
  lines=infile.readlines()

  for i in range(0,len(lines)):
    line=lines[i]
    if ('Content:' in line and 'Content::' not in line):
      #print(line)
      filename=str(i)+'_file.txt'
      outfile=open(filename,'w',errors='ignore')
      urlLine=lines[i-4]
      metadataLine=lines[i-1]
      outfile.write(urlLine)
      outfile.write(metadataLine)
      while ('CrawlDatum::' not in line and 'ParseText::' not in line):
        outfile.write(line)
        i+=1
        line=lines[i]
      outfile.close()

    
def main():
  #Check for proper arguments
  if len(sys.argv) != 2:
    print ('usage: python3 parseContent.py inputFile')
    sys.exit(1)
  inputFile = sys.argv[1]
  parseInputFiles(inputFile)

if __name__ == '__main__':
  main()