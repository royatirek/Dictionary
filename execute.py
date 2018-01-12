from PyQt4.QtGui import *
from PyQt4.QtCore import *
import traceback
site_pack_path = "C:\\Python34\\Lib\\site-packages"
QApplication.addLibraryPath('{0}\\PyQt4\\plugins'.format(site_pack_path))
from PyQt4.QtSql import *
import sys
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import mainWindow_ui
from PerWordWindow import PerWordDisplay


# This  is how python inherits
class Dictionary(QMainWindow, mainWindow_ui.Ui_MainWindow, PerWordDisplay):
    """ This is the main class and provides the basis of creation of the main Window"""
    # class or instance variable

    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('dictionary.db')
    if not db.open():
        # print(QMessageBox.critical(self, "critical", ("Cannot open database")))
        print("unable to open")
    query = QSqlQuery()

    # _init is initialiser
    def __init__(self):

        self.createTable()

        # Comment the below line if database is already created
        self.scrapPages()
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("TimeMac Dictionary")
        self.showWords()
        # when search button is clicked
        self.pushButton.clicked.connect(self.showSearchedWord)
        self.listWidget.doubleClicked.connect(self.getPerWordDisplay)
        self.listWidget.itemClicked.connect(self.showMessage)


    def showMessage(self):
         self.statusbar.showMessage("[Double click to expand]")


    def getPerWordDisplay(self, item):
        """This calls the PerWordWindow Dialog box and show each word in detail"""
        # type of the item  is QModelIndex
        currentRow = item.data()
        endOfWord = currentRow.index(" ")
        # wordClicked returns the word that is being clicked
        wordClicked = currentRow[:endOfWord]
        self.query.prepare("""SELECT * FROM dictin WHERE word=:word""")

        self.query.bindValue(":word", wordClicked)

        if self.query.exec_():
            print("Successful")
        else:
            print("Error: ", self.query.lastError().text())

        rec = self.query.record()
        self.query.next()

        perWordObject = PerWordDisplay(self.query.value(1), self.query.value(2), self.query.value(3),
                                       self.query.value(4), self.query.value(5), self.query.value(6))
        perWordObject.exec_()

    def showSearchedWord(self):
        """  This method shows the searched word """

        self.listWidget.clear()
        search_term = str(self.searchField.text())
        if self.query.exec_("SELECT * FROM dictin"):
            rec = self.query.record()
            while self.query.next():
                # rec.counts() returns no of columns in database
                for ix in range(1):
                    wordSearched = self.query.value(1)
                    if search_term in wordSearched:
                        val = wordSearched + "   ---    " + self.query.value(2)
                        print(rec.fieldName(1), val)
                        self.listWidget.addItem(val)

        else:
            print(self.query.lastError().text())

    def showWords(self):
        """This shows all the words present in the database"""
        if self.query.exec_("SELECT * FROM dictin"):
            rec = self.query.record()
            while self.query.next():
                # rec.count returns no of columns in database
                for ix in range(1):
                    val = self.query.value(1).strip() + "   ---    " + self.query.value(6).strip()
                    #print(rec.fieldName(1), val)
                    self.listWidget.addItem(val)

        else:
            print(self.query.lastError().text())

    def getHindiTrans(self, word):
        """ This scarps the hindi translation of word from the internet and returns its value"""
        url = "http://dict.hinkhoj.com/"+word+"-meaning-in-hindi.words"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')
        # print(webpage)
        # using soup library
        soup = BeautifulSoup(webpage, "html.parser")
        try:
            result = soup.find("span", {"itemprop" : "itemListElement"})
            result = "".join(result.strings)
        except(Exception):
            result = "NONE"

        print(result)
        return result

    def getWordsAndInsert(self, word, searchShortDefn, mnemonics, defArr, defDict):
        """ This inserts the scrapped word and its contents in the database"""
        word = str(word)
        searchShortDefn = str(searchShortDefn)
        mnemonics = str(mnemonics)
        synListDB = []
        defString = "<u>Short Meaning</u><br>"+searchShortDefn+"<br><br>"
        for i in range(len(defArr)):
            defString = defString + "<u>Defination</u><br>"
            defString += defArr[i] + "<br><br>"
            print(defArr[i], i)

            synList = defDict[i]['syn']

            noOfSynonymes = len(synList)
            if (noOfSynonymes > 0):
                synListDB.extend(synList)
                defString += "<u>Synonymes</u><br>"
            if (noOfSynonymes > 0):
                for j in range(noOfSynonymes):
                    defString += synList[j] + "<br>"

            sentenceList = defDict[i]['sent']
            noOfSentences = len(sentenceList)
            if (noOfSentences > 0):
                defString += "<u>Example Sentences</u><br>"
            if (noOfSentences > 0):
                for j in range(noOfSentences):
                    defString += sentenceList[j] + "<br>"

            defString += "<br><hr><br>"

        # .index throws value error therefore try except block
        try:
            indexOfSeperater=mnemonics.index('///')
        except(Exception):
            indexOfSeperater=0

        if indexOfSeperater > 0:
            noOfMnemonics = 2
        elif len(mnemonics)>0:
            noOfMnemonics=1
        else:
            noOfMnemonics=0

        if noOfMnemonics>0:
            defString += "<u>Mnemonics</u><br><br>"



        # Formatting mnemonic in defString
        start = -3

        for i in range(noOfMnemonics):
            # .index throws value error therefore try except block
            try:
                stop = mnemonics.index('///', start + 3)
            except:
                stop=len(mnemonics)

            defString += mnemonics[start + 3:stop] + "<br>"
            start = stop
            defString += "<br>"

        hindi = self.getHindiTrans(word)
        print(hindi)
        query = QSqlQuery()

        # establish placeholders for the data, these placeholders we fill in through bindValue()
        query.prepare("INSERT INTO dictin (word, searchShortDefn, mnemonics, defArr, syn, hindi)"
                      "VALUES (:word, :searchShortDefn, :mnemonics, :defArr, :syn, :hindi)")

        query.bindValue(":word", word.strip())
        query.bindValue(":searchShortDefn", searchShortDefn.strip())
        query.bindValue(":mnemonics", mnemonics.strip())
        # defString is created using arguments defArr and defDict
        query.bindValue(":defArr", defString)
        # synListDB is the list of all the synonymes
        query.bindValue(":syn", str(synListDB))
        query.bindValue(":hindi", hindi.strip())

        if query.exec_():
            print("Successful")
        else:
            print("Error1: ", query.lastError().text())

    def scrapPage(self, pageNo):
        """ It scraps all the words and its related contents and send it to the getWordandInsert method"""
        url = "http://www.mnemonicdictionary.com/wordlist/GREwordlist?page=" + str(pageNo)
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web_byte = urlopen(req).read()
        webpage = web_byte.decode('utf-8')

        # using soup library
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

                self.getWordsAndInsert(search_word, search_short_defn, mnemonics, def_arr, def_dict)

                print(search_word, "\n", search_short_defn, "\n", mnemonics, "\n", def_arr, "\n", def_dict)

                tot = tot + 1


    def createTable(self):
        print(self.query.exec_("PRAGMA encoding='UTF-8'"))

        print(self.query.exec_("CREATE TABLE dictin(ID INTEGER PRIMARY KEY AUTOINCREMENT, "
                               "word varchar(100), searchShortDefn varchar(300),mnemonics varchar(500), "
                               "defArr varchar(2000), syn varchar(500), hindi nvarchar(200))"))

    def scrapPages(self):
        """ This creates the database and scraps all the pages of the target website"""

        # startAgain needs to be changed be scarping fails
        startAgain = 1
        lastStableID=self.getNoOfRows()

        for i in range(startAgain, 788):
            try:
                self.scrapPage(i)
            except TypeError:
                # When  word['class'] != [u'row-fluid']: in scrapPage method raises the error
                print("TypeError caught")
                pass
            except Exception as exception:
                print(type(exception).__name__)
                print(str(exception))
                print(traceback.format_exc())
                print("Error occured while processing page ",i,
                " : Rollback to last state\n")
                currentID = self.getNoOfRows()
                self.rollback(lastStableID+1,currentID+1)
                print("Pages till ",i," are fully committed to database")
                print("No of words -> ",lastStableID)
                exit(0)

            lastStableID=self.getNoOfRows()







    def rollback(self,start,stop):
        """ Rollbacks into previous full committed page"""
        for i in range(start,stop):
            deleteQuery = "DELETE FROM dictin WHERE id ="+str(i)
            if self.query.exec_(deleteQuery):
                print("DElETE Successfull")
            else:
                print(self.query.lastError)


    def getNoOfRows(self):
        if self.query.exec_("SELECT * FROM dictin"):
            i = 0
            while self.query.next():
                i = i + 1

        return i


    def forTesting(self):

        if self.query.exec_("SELECT * FROM dictin"):
            rec = self.query.record()


            i=0
            while self.query.next():
                i=i+1

            print(i)





app = QApplication(sys.argv)

"""# Create and display the splash screen
splash_pix = QPixmap('splash.jpg')
splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
# adding progress bar
progressBar = QProgressBar(splash)
splash.setMask(splash_pix.mask())
splash.show()
 """



newDict = Dictionary()
newDict.show()
#splash.finish(newDict)
app.exec_()
