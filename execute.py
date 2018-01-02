from PyQt4.QtGui import *
site_pack_path = "C:\\Python34\\Lib\\site-packages"
QApplication.addLibraryPath('{0}\\PyQt4\\plugins'.format(site_pack_path))
from PyQt4.QtSql import *
from PyQt4.QtCore import *
import sys




def createDB():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('sports.db')

    db.open()

    query = QSqlQuery()

    query.exec_("create table sportsmen(id int primary key, "
                "firstname varchar(20), lastname varchar(20))")

    query.exec_("insert into sportsmen values(101, 'Roger2', 'Federer')")
    query.exec_("insert into sportsmen values(102, 'Christiano', 'Ronaldo')")
    query.exec_("insert into sportsmen values(103, 'Ussain', 'Bolt')")
    query.exec_("insert into sportsmen values(104, 'Sachin', 'Tendulkar')")
    query.exec_("insert into sportsmen values(105, 'Saina', 'Nehwal')")

    if query.exec_("SELECT * FROM sportsmen"):
        rec = query.record()
        while query.next():
            for ix in range(rec.count()):
                val = query.value(ix)
                print(rec.fieldName(ix), val)
    else:
        print(query.lastError().text())
    return True






app = QApplication(sys.argv)


createDB()

