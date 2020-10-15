# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 19:54:47 2020

@author: chris
"""
import docx2txt
import itertools
import pandas as pd
import re
from rapidfuzz import fuzz
from nltk.tokenize import PunktSentenceTokenizer
from termcolor import colored
import tkinter
from tkinter import filedialog

print( "\n")  
print("Welcome to SentSim!")
print( "\n")  
print("Please select your file")

root = tkinter.Tk()
root.wm_withdraw() # this completely hides the root window

file1 = filedialog.askopenfilename()
file2 = filedialog.askopenfilename()

print( "\n")
print("""Processing.. 
      
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)   """)
    
    
print( "\n")   
print( "\n")  
print( "\n")  
print( "\n")   

text1 = docx2txt.process(file1)
text2 = docx2txt.process(file2)

sent_tokenizer1 = PunktSentenceTokenizer(text1)
sent_tokenizer2 = PunktSentenceTokenizer(text2)

sents1 = sent_tokenizer1.tokenize(text1)
sents2 = sent_tokenizer2.tokenize(text2)

sents1 = set(sents1)
sents2 = set(sents2)

x_list = []
y_list = []
score = []

for x,y in zip(sents1, sents2):
    fuzz.ratio(x, y)
    score.append(fuzz.ratio(x, y))
    x_list.append(x)
    y_list.append(y)
    
# remove consecutive blank lines

x_list1 = []  
for x in x_list:

    xn = re.sub(r'\n\s*\n', '\n\n', x)
    x_list1.append(xn)
    
y_list1 = []  
for y in y_list:

    yn = re.sub(r'\n\s*\n', '\n\n', y)
    y_list1.append(yn)
    
data_tuples = list(zip(x_list1,y_list1,score))

results = pd.DataFrame(data_tuples, columns=['X','Y', 'Score'])  

results = results.sort_values(by=['Score'], ascending=False)
results = results[results['Score'] > 60]

x_list3 = list(results['X'])
y_list3 = list(results['Y'])
        
    
# uncommon words

diffs = []


def find(X, Y):
    count = {}
    for word in X.split():
        count[word] = count.get(word, 0) + 1

    for word in Y.split():
        count[word] = count.get(word, 0) + 1
    return [word for word in count if count[word] == 1]



for X,Y in zip(x_list3, y_list3):
    diffs.append((find(X, Y)))
    
diffsList = [' '.join(x) for x in diffs]
results['Diffs'] = diffsList
results = results[['Score', 'X', 'Y', 'Diffs']]


resultsXlist = results['X'].tolist()
resultsYlist = results['Y'].tolist()
resultDIFFSYlist = results['Diffs'].tolist()
resultSCORElist  = results['Score'].tolist()




n = 0
while n <= len(resultsXlist) - 1:

    text1 = resultsXlist[n]  
    text2 = resultsYlist[n] 
    l1 = resultDIFFSYlist[n].split()

    
    
    formattedText1 = []
    for t in text1.split():
        if t in l1:
            formattedText1.append(colored(t,'red', attrs=['bold']))
        else: 
            formattedText1.append(t)

    
    formattedText2 = []
    for t in text2.split():
        if t in l1:
            formattedText2.append(colored(t,'red', attrs=['bold']))
        else: 
            formattedText2.append(t)
 
    print( "\n")
    print(colored(resultSCORElist[n], 'green'))
    print(colored(l1, 'blue'))
    print( "\n")
    print(" ".join(formattedText1))
    print( "\n")
    print(" ".join(formattedText2))
    print( "\n")
    print( "\n")
    
    n = n+1