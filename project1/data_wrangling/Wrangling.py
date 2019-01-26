
# coding: utf-8

# <img src="../../img/data-access-wrangling1_0.png" alt="Drawing" style="width: 200px;"/>
# <b>I will one day update this to be a giant binary snake</b> <small>prbly not</small>

# Wrangling is the first part/step in this pipeline.
# The importance of this is simple. Data exists, it is a wild and dangerous creature that sometimes comes is a wrapped up csv or in this case as a compiled pdf. We must take the bull or in this case pdf by the horns and do as the cowboys once did and break this beast!

# First comes the lasso

# In[ ]:


get_ipython().system('pip install PyPDF2 #we will use this to scrape text out of the pdf ')


# Now in my opinion the most important part. Finding the bull.

# In[ ]:


#This works in most linux enviroments
#!rm *.pdf
#!wget https://github.com/c2-d2/pr_mort_official/raw/master/data/RD-Mortality-Report_2015-18-180531.pdf
#!mv RD-Mortality-Report_2015-18-180531.pdf Mortality.pdf

#The above works fine but you need wget so id rather it all be in plain python
import requests
pdf = r"https://github.com/c2-d2/pr_mort_official/raw/master/data/RD-Mortality-Report_2015-18-180531.pdf"
open("Mortality.pdf" , 'wb').write(requests.get(pdf).content)


# In[ ]:


from IPython.display import HTML
HTML('<iframe src=Mortality.pdf width=700 height=350></iframe>')


# In[ ]:


#Necesary imports
import PyPDF2
from pandas import DataFrame as df
import matplotlib.pyplot as plt


# In[ ]:


pdfFileObj = open('Mortality.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pageObj = pdfReader.getPage(0)
pageObj.extractText()


# G R 8. I havent the foggiest idea what that is.
# Lets fix that right now.

# In[ ]:


mToNum = {
    "SEP":"09",
    "OCT":"10",
    "NOV":"11",
    "DEC":"12",
    "JAN":"01",
    "FEB":"02",
    "MAR":"03",
    "APR":"04",
    "MAY":"05",
    "JUN":"06",
    "JUL":"07",
    "AGO":"08"}
#This is usefull


# In[ ]:


def general_scrape(data):
    data = data[1].split()
    labels = data[0:4]
    indexes = []
    stop = data.index('Total')
    #for i , val in enumerate(data):
    #    if not (i-4) % 5 and i < 160:
    #        print(F"{val}:{i}")
    out = []
    for i in range(4 , stop , 5):
        indexes.append(data[i])
        out.append([])
        out[-1].append(int(data[i+1]))
        out[-1].append(int(data[i+2]))
        out[-1].append(int(data[i+3]))
        out[-1].append(int(data[i+4]))
    return df(data=out , index=indexes , columns=labels)


# In[ ]:


def feb_scrape(data):
    data = data[1].split()
    labels = data[0:4]
    indexes = []
    stop = data.index('Total')
    #for i , val in enumerate(data):
    #    if not (i-4) % 5 and i < 160:
    #        print(F"{val}:{i}")
    out = []
    for i in range(4 , stop , 5):
        indexes.append(data[i])
        out.append([])
        if i != 144:
            out[-1].append(int(data[i+1]))
            out[-1].append(int(data[i+2]))
            out[-1].append(int(data[i+3]))
            out[-1].append(int(data[i+4]))
        else:
            break
    out[-1].append(0)
    out[-1].append(int(data[i+1]))
    out[-1].append(0)
    out[-1].append(0)
    indexes.append(data[i+2])
    out.append([])
    out[-1].append(int(data[i+3]))
    out[-1].append(int(data[i+4]))
    out[-1].append(int(data[i+5]))
    out[-1].append(int(data[i+6]))
    
    #return df(data=out , index=indexes , columns=labels)
    return fmt


# In[ ]:


def scrape_data(data , month):
    data = data[1].split()
    labels = data[0:4]
    indexes = []
    stop = data.index('Total')
    out = []
    for i in range(4 , stop , 5):
        indexes.append(data[i])
        day = data[i]
        if not len(day)-1:
            day = "0"+day
        if (i != 144 or month!="FEB"):
            
            out.append([F"{labels[0]}-{mToNum[month]}-{day}",int(data[i+1])])
            out.append([F"{labels[1]}-{mToNum[month]}-{day}",int(data[i+2])])
            out.append([F"{labels[2]}-{mToNum[month]}-{day}",int(data[i+3])])            
            out.append([F"{labels[3]}-{mToNum[month]}-{day}",int(data[i+4])])
        else:
            #print("Breaking")
            out.append([F"{labels[1]}-{mToNum[month]}-{day}",int(data[i+1])])
            break
    
    return out


# In[ ]:




        
def scrape(txt):
    data = []
    months = ["SEP", "OCT", "NOV", "DEC" , "JAN", "FEB", "MAR", "APR", "MAY" , "JUN" , "JUL", "AGO"]
    for month in months:
        if month in txt:
            """if "FEB"==month:
                return feb_scrape(txt.split(month))
            else:
                return general_scrape(txt.split(month))"""
            return scrape_data(txt.split(month) , month)

    
        
    #print(out)
scrape(pageObj.extractText())


# That looks presentable :). Now for the rest.

# In[ ]:


data = []
for pages in range(pdfReader.getNumPages()):
    data += scrape(pdfReader.getPage(pages).extractText())
data.sort()
for frame in data:
    print(frame)

