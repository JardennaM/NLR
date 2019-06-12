import os
import pandas as pd 
from tika import parser
from scraper import Scraper

os.system('clear')

# scraper = Scraper('terms.xls', 10, True, True)


raw = parser.from_file('CSD-Counter-Drone-Systems-Report.pdf')

import PyPDF2
pdfFileObj = open('CSD-Counter-Drone-Systems-Report.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

pageObj = pdfReader.getPage(0)
print(pageObj.extractText())
