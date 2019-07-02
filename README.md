## How to run
Only works for python3.x!

`$ python3 script.py`

Before running the script, make sure there is an active SQL server.
Hint: Easiest solution is to download XAMPP https://www.apachefriends.org/download.html. Open the XAMPP application and start the MySQL server.

The following packages need to be installed  with `$ pip3 install package_name`

In order install wordfreq, Visual Studio is required. Download it from http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe

### Package names
mysql-connector<br/>
google<br/>
requests<br/>
pdfminer.six<br/>
pandas<br/>
xlrd<br/>
lxml<br/>
sklearn<br/>
beautifulsoup4<br/>
tabulate<br/>
nltk<br/>
validators<br/>
validator_collection<br/>
numpy<br/>
wordfreq<br/>

### Special installation
word_forms package
github link: https://github.com/gutfeeling/word_forms

How to install:
- First clone:
`$ git clone https://github.com/gutfeeling/word_forms.git`
- Then install:
`$ pip3 install -e word_forms`

 How to fix "Resource 'tokenizers/punkt/english.pickle' not found."
 - Enter python command prompt:
 `$ python`
 - Import nltk library:
 `>>> import nltk`
 - Enter nltk download screen:
 `>>> nltk.download()`
 - Download modules:
 Select the 'all' option and click on download


