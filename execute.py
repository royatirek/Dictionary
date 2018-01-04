from PyQt4.QtGui import *
site_pack_path = "C:\\Python34\\Lib\\site-packages"
QApplication.addLibraryPath('{0}\\PyQt4\\plugins'.format(site_pack_path))
from PyQt4.QtSql import *
from PyQt4.QtCore import *
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup





def getWordsAndInsert(word, searchShortDefn, mnemonics, defArr, defDict):

    word = str(word)
    searchShortDefn = str(searchShortDefn)
    mnemonics = str(mnemonics)
    defArr = str(defArr)
    defDict = str(defDict)

    query = QSqlQuery()

    #establish placeholders for the data, these placeholders we fill in through bindValue()
    query.prepare("""INSERT INTO dictin (word, searchShortDefn, mnemonics, defArr, defDict)
            VALUES (:word, :searchShortDefn, :mnemonics, :defArr, :defDict)""")

    query.bindValue(":word", word)
    query.bindValue(":searchShortDefn", searchShortDefn)
    query.bindValue(":mnemonics", mnemonics)
    query.bindValue(":defArr", defArr)
    query.bindValue(":defDict", defDict)

    if query.exec_():
        print("Successful")
    else:
        print("Error: ", query.lastError().text())



def scrapPage(pageNo):

    url = "http://www.mnemonicdictionary.com/wordlist/GREwordlist?page="+str(pageNo)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    web_byte = urlopen(req).read()
    webpage = web_byte.decode('utf-8')

    #using soup library
    soup = BeautifulSoup(webpage, "html.parser")

    result = soup.find_all("div", class_="input-append")
    result = result[0]
    result = result.find_parent('form')
    tot = 0
    while True:
        result = result.find_next_sibling('div')
        word = result
        if word['class'] != [u'row-fluid']:
            break
        else:
            search_word = word.find('h2').string
            search_short_defn = word.find('p').text[19:]
            search_def = word.find('div').text

            # mnemonics parser
            mnemonics = ''
            token_sep = '///'
            icons = word.find_all("i", class_='icon-lightbulb')
            size = 4
            mnemonics_len = len(icons)
            if size > mnemonics_len:
                size = mnemonics_len
            for index in range(0, size):
                icon_div = icons[index].find_parent('div')
                mnemonics_str = ''
                try:
                    mnemonics_str = str(icon_div.text).strip()
                except:
                    mnemonics_str = 'NONE'
                mnemonics = mnemonics + mnemonics_str + token_sep

            search_def_arr = str(search_def).split('\n')

            definition_str = ''
            synonym_str = ''
            sentence_str = ''

            search_def_arr = [x.strip() for x in search_def_arr]
            value = 0

            def_arr_in = -1
            def_arr = []
            def_dict = []
            for data in search_def_arr:
                if len(data) > 0 and data != ',':
                    if 'Definition' in data:
                        def_arr_in = def_arr_in + 1
                        test = {'syn': [], 'sent': []}
                        def_dict.append(test)
                        value = 1
                    elif 'Synonyms' in data:
                        value = 2
                    elif 'Example' in data and 'Sentence' in data:
                        value = 3
                    else:
                        if value == 1:
                            def_arr.append(data)
                        elif value == 2:
                            dict = def_dict[def_arr_in]
                            syn_arr = dict['syn']
                            syn_arr.append(data)
                            dict['syn'] = syn_arr
                        elif value == 3:
                            dict = def_dict[def_arr_in]
                            sent_arr = dict['sent']
                            sent_arr.append(data)
                            dict['sent'] = sent_arr

            getWordsAndInsert(search_word,search_short_defn,mnemonics,def_arr,def_dict)
            #print(search_word ,"\n",search_short_defn, "\n",mnemonics, "\n",def_arr, "\n",def_dict)

            tot = tot + 1






def scrapPages():

    print(query.exec_("CREATE TABLE dictin(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                      "word varchar(100), searchShortDefn varchar(300),mnemonics varchar(500), "
                      "defArr varchar(500), defDict varchar(500))"))

    for i in range(1,2):
        scrapPage(i)


    if query.exec_("SELECT * FROM dictin"):
        rec = query.record()
        while query.next():
            for ix in range(rec.count()):
                val = query.value(ix)
                print(rec.fieldName(ix), val)
    else:
        print(query.lastError().text())



app = QApplication(sys.argv)
db = QSqlDatabase.addDatabase('QSQLITE')
db.setDatabaseName('dictionary.db')
if not db.open():
    QMessageBox.critical(None,("Cannot open database"),QMessageBox.Cancel)
query = QSqlQuery()

scrapPages()



