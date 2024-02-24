import pandas as pd 

with open('texto.txt','r') as f:
    list =f.readlines()
list = ''.join(list)
list = list.split('\n')
print(list)