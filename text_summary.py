#!/usr/bin/env python
# coding: utf-8

# In[1]:

from pypdf import PdfReader
from bardapi import Bard

# In[2]:


filename  = 'Attention-Is-All-You-Need.pdf'
# creating a pdf file object
pdfFileObject = open(filename, 'rb')
# creating a pdf reader object
pdfReader = PdfReader(pdfFileObject)
text=[]
summary=' '
#Storing the pages in a list
for i in range(0,len(pdfReader.pages)):
  # creating a page object
  pageObj = pdfReader.pages[i].extract_text()
  pageObj= pageObj.replace('\t\r','')
  pageObj= pageObj.replace('\xa0','')
  # extracting text from page
  text.append(pageObj)


# In[3]:


# Merge multiple page - to reduce API Calls
def join_elements(lst, chars_per_element):
    new_lst = []
    for i in range(0, len(lst), chars_per_element):
        new_lst.append(''.join(lst[i:i+chars_per_element]))
    return new_lst

# Option to keep x elements per list element
new_text = join_elements(text, 3)

print(f"Original Pages = ",len(text))
print(f"Compressed Pages = ",len(new_text))


# In[4]:


def get_completion(prompt):
  response = Bard().get_answer(prompt)['content']
  return response


# In[5]:


for i in range(len(new_text)):
    prompt =f"""
       Your task is to act as a Text Summariser.
        I'll give you text from  pages of a book from beginning to end.
         And your job is to summarise text from these pages in less than 100 words.
         Don't be conversational. I need a plain 100 word answer.
         Text is shared below, delimited with triple backticks:
         ```{text[i]}```
           """
    try:
        response = get_completion(prompt)
    except:
        response = get_completion(prompt)
        print(response)
        summary= summary+' ' +response +'\n\n'
        # result.append(response)
        time.sleep(19)  #You can query the model only 3 times in a minute for free, so we need to put some delay


# In[6]:

with open('bard_summary.txt','w') as out:
    out.write(summary)