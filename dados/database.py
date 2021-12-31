from PyQt5.QtSql import QSqlDatabase


def connect_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("dados/database.db")
    db.open()
    return db
