#!/usr/bin/env python
# coding: utf-8

# In[1]:


#pip install pypiwin32
from win32com import client

def srs_generation():
    excel = client.Dispatch("Excel.Application")
    word = client.Dispatch("Word.Application")
    doc=word.Documents.Open(r"SRS.docx")
    book =excel.Workbooks.Open(r"dataset_output.csv")
    sheet = book.Worksheets(1)
    sheet.Range("C1:D841").Copy()
    wdRange=doc.Content
    wdRange.Collapse(0)
    wdRange.PasteExcelTable(False, True, False)

