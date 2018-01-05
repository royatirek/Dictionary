from PyQt4.QtGui import *
site_pack_path = "C:\\Python34\\Lib\\site-packages"
QApplication.addLibraryPath('{0}\\PyQt4\\plugins'.format(site_pack_path))
from PyQt4.QtSql import *
from PyQt4.QtCore import *
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import mainWindow_ui



# This  is how python inherits
class Dictionary(QMainWindow, mainWindow_ui.Ui_MainWindow):

    # class or instance variable

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('dictionary.db')
    if not db.open():
        # print(QMessageBox.critical(self, "critical", ("Cannot open database")))
        print("unable to open")
    query = QSqlQuery()

    # _init is initialiser
    def __init__(self):

        self.scrapPages()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("TimeMac Dictionary")
        self.showWords()
        # when search button is clicked
        self.pushButton.clicked.connect(self.showSearchedWord)

    def showSearchedWord(self):
        self.listWidget.clear()
        search_term = str(self.searchField.text())
        if self.query.exec_("SELECT * FROM dictin"):
            rec = self.query.record()
            while self.query.next():
                # rec.counts() returns no of columns in database
                for ix in range(1):
                    wordSearched=self.query.value(1)
                    if search_term in wordSearched:
                        val = wordSearched +"   ---    "+self.query.value(2)
                        print(rec.fieldName(1), val)
                        self.listWidget.addItem(val)

        else:
            print(self.query.lastError().text())


    def showWords(self):
        if self.query.exec_("SELECT * FROM dictin"):
            rec = self.query.record()
            while self.query.next():
                # rec.counts returns no of columns in database
                for ix in range(1):
                    val = self.query.value(1)+"   ---    "+self.query.value(2)
                    print(rec.fieldName(1), val)
                    self.listWidget.addItem(val)

        else:
            print(self.query.lastError().text())







    def getWordsAndInsert(self,word, searchShortDefn, mnemonics, defArr, defDict):

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



    def scrapPage(self,pageNo):

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

                self.getWordsAndInsert(search_word,search_short_defn,mnemonics,def_arr,def_dict)
                #print(search_word ,"\n",search_short_defn, "\n",mnemonics, "\n",def_arr, "\n",def_dict)

                tot = tot + 1






    def scrapPages(self):

        print(self.query.exec_("CREATE TABLE dictin(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                          "word varchar(100), searchShortDefn varchar(300),mnemonics varchar(500), "
                          "defArr varchar(500), defDict varchar(500))"))

        for i in range(1,2):
            self.scrapPage(i)






app = QApplication(sys.argv)


newDict = Dictionary()
newDict.show()
app.exec_()




