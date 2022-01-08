#!/opt/local/bin/python
#
# python script to process the british library digitised manuscripts csv file
#
# to run type: 
#   data_analysis.py file.cvs 
#   the program will ask for strings to search for (it will do these in order)
#   and ask for strings to exclude use 'none' if you wish no exclude string
#
# or for a quick search with only on include and one exclude string type
#   data_analysis.py file.cvs search_string exclude_string
#   use 'none' if you wish no exclude string
#    
# 
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#
# setup files to read
dir=os.getcwd()
data_file=str(sys.argv[1])
out_file1='clean'
out_file2='out'   
search_string=[]
exclude_string=[]

# get info
if len(sys.argv) <= 3:
  S=input('type terms to search, (no strange characters) ')
  print(S)
  search_string=S.rstrip().split()
  s='number of terms is '
  print('{0:}{1:}'.format(s,len(search_string)))
  if len(search_string) == 0:
    print('will perform only a clean')
    search_string.append('clean')
#
  S=input('type terms to exclude, (no strange characters) ')
  print(S)
  exclude_string=S.rstrip().split()
  s='number of terms is '
  print('{0:}{1:}'.format(s,len(exclude_string)))
  if len(exclude_string) == 0:
    print('no exclude tems')
    exclude_string.append('none')
else:
  data_file=str(sys.argv[1])
  search_string.append(str(sys.argv[2]))
  exclude_string.append(str(sys.argv[3]))
  s='input file is '
  print('{0:}{1:}'.format(s,data_file))
  s='search string is '
  print('{0:}{1:}'.format(s,search_string))
  s='exclude string is '
  print('{0:}{1:}'.format(s,exclude_string))
#
# read file
df0=pd.read_csv(data_file)
#
# strip any carrage returns
df=df0.replace(r'\n',' ', regex=True) 

# strip empty columns and rows
df=df.dropna(axis='columns',how='all')
df=df.dropna(axis='rows',how='all')

# check for any null values
nul=df.isnull().values.any()
if nul == True :
  print('there is missing data!')

# print check info and cleaned file
#s='taking a peak: '
#print('{0:}'.format(s))
#print(df)
#df.to_csv(out_file1+'.csv',index=False)
#df.info()
s='starting dimensions (rows, columns)='
print('{0:}{1:}'.format(s,df.shape))
if search_string[0] == 'clean':
  print('{0:}{1:}'.format(s,out_file2+'.csv'))
  df.to_csv(out_file2+'.csv',index=False)
  df.head(10)
  sys.exit()

# separate columns
ms=df['Shelfmark']
content=df['Contents']
#print(content)
link=df['Link to Digitised Manuscripts']

# now extract data according to search strings
# read column contents true if string occurs, case insensitive save row to new data

i=0
while i < len(search_string):
  df=df[df['Contents'].str.contains(search_string[i],case=False)]
  s='including '
  print('{0:}{1:}'.format(s,search_string[i]))
  i=i+1

s='after search (rows, columns)='
print('{0:}{1:}'.format(s,df.shape))
#
# now extract data that has the exclude string
#
if exclude_string[0] != 'none':
  i=0
  while i < len(exclude_string):
    df=df[~df['Contents'].str.contains(exclude_string[i],case=False)]
    s='excluding '
    print('{0:}{1:}'.format(s,exclude_string[i]))
    i=i+1

  s='after exclusions (rows, columns)='
  print('{0:}{1:}'.format(s,df.shape))
#
# print suff
# save new .cvs file (without an index added by pandas)
s='new file is called '
print('{0:}{1:}'.format(s,out_file2+'.csv'))
df.to_csv(out_file2+'.csv',index=False)
df.head(10)
#
# exit
sys.exit()






