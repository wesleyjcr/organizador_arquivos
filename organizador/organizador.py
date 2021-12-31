import os
import pathlib
from PyQt5.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QFileDialog,
    QHeaderView,
)
from PyQt5.QtCore import QDateTime
from PyQt5.QtSql import QSqlQuery
from dados.database import connect_db
from tela.tela_principal import Ui_MainWindow


class Organizador(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.con = connect_db()
        self.btn_pasta_entrada.clicked.connect(self.dialog_pasta_entrada)
        self.btn_add_entrada.clicked.connect(self.add_entrada)
        self.btn_remove_entrada.clicked.connect(self.remove_entrada)
        self.btn_pasta_saida.clicked.connect(self.dialog_pasta_saida)
        self.btn_add_saida.clicked.connect(self.add_saida)
        self.btn_remove_saida.clicked.connect(self.remove_saida)
        self.btn_agendar.clicked.connect(self.agendar)
        self.atualizar_tabela_entrada()
        self.atualizar_tabela_saida()
        self.atualiza_campos_agendamento()


    def atualizar_tabela_entrada(self):
        query = QSqlQuery()
        query.exec_("SELECT * FROM PASTA_ENTRADA")
        row_count = 0
        self.table_entrada.setRowCount(row_count)
        while query.next():
            self.table_entrada.insertRow(row_count)
            self.table_entrada.setItem(row_count, 0, QTableWidgetItem(query.value(1)))
            row_count += 1
        self.table_entrada.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def atualizar_tabela_saida(self):
        query = QSqlQuery()
        query.exec_("SELECT * FROM PASTA_SAIDA")
        row_count = 0
        self.table_saida.setRowCount(row_count)
        while query.next():
            self.table_saida.insertRow(row_count)
            self.table_saida.setItem(row_count, 0, QTableWidgetItem(query.value(1)))
            self.table_saida.setItem(row_count, 1, QTableWidgetItem(query.value(2)))
            row_count += 1
        self.table_saida.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def dialog_pasta_entrada(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Selecione a pasta de entrada")
        if dialog.exec_() == QFileDialog.Accepted:
            self.input_pasta_entrada.setText(dialog.selectedFiles()[0])

    def add_entrada(self):
        query = QSqlQuery()
        query.exec_(
            f"INSERT INTO PASTA_ENTRADA (ENDERECO) VALUES ('{self.input_pasta_entrada.text()}')"
        )
        self.atualizar_tabela_entrada()

    def remove_entrada(self):
        row = self.table_entrada.currentRow()
        if row >= 0:
            text = self.table_entrada.item(row, 0).text()
            query = QSqlQuery()
            query.exec_(f"DELETE FROM PASTA_ENTRADA WHERE ENDERECO = '{text}'")
            self.table_entrada.removeRow(row)
            self.atualizar_tabela_entrada()
        else:
            QMessageBox.warning(self, "Erro", "Nenhum item foi selecionado")

    def dialog_pasta_saida(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.setWindowTitle("Selecione a pasta de destino")
        if dialog.exec_() == QFileDialog.Accepted:
            self.input_pasta_saida.setText(dialog.selectedFiles()[0])

    def add_saida(self):
        if self.input_extensao.text() != "":
            query = QSqlQuery()
            query.exec_(
                f"INSERT INTO PASTA_SAIDA (ENDERECO, EXTENSAO) VALUES ('{self.input_pasta_saida.text()}', '{self.input_extensao.text()}')"
            )
            self.atualizar_tabela_saida()
        else:
            QMessageBox.warning(self, "Erro", "Por favor, preencha o campo de extensão")

    def remove_saida(self):
        row = self.table_saida.currentRow()
        if row >= 0:
            endereco = self.table_saida.item(row, 0).text()
            extensao = self.table_saida.item(row, 1).text()
            query = QSqlQuery()
            query.exec_(
                f"DELETE FROM PASTA_SAIDA WHERE ENDERECO = '{endereco}' AND EXTENSAO = '{extensao}'"
            )
            self.table_saida.removeRow(row)
            self.atualizar_tabela_saida()
        else:
            QMessageBox.warning(self, "Erro", "Nenhum item foi selecionado")

    def atualiza_campos_agendamento(self):
        query = QSqlQuery()
        query.exec_("SELECT * FROM AGENDAMENTO")
        query.next()

        if query.value(0) == "DAILY":
            self.radio_diario.setChecked(True)
        elif query.value(0) == "WEEKLY":
            self.radio_semanal.setChecked(True)
        elif query.value(0) == "MONTHLY":
            self.radio_mensal.setChecked(True)

        now = QDateTime.fromString(query.value(1), "dd/MM/yyyy hh:mm")
        self.date_inicio.setDateTime(now)

    def agendar(self):
        dt = self.date_inicio.dateTime()
        hora = dt.toString("hh:mm")
        date_inicio = dt.toString(self.date_inicio.displayFormat())

        if self.radio_diario.isChecked():
            frequencia = "DAILY"

        elif self.radio_semanal.isChecked():
            frequencia = "WEEKLY"

        elif self.radio_mensal.isChecked():
            frequencia = "MONTHLY"

        query = QSqlQuery()
        query.exec_(
            f"UPDATE AGENDAMENTO SET FREQUENCIA = '{frequencia}', INICIO = '{date_inicio}'"
        )
        
        
        local = pathlib.Path(__file__).parent.resolve()
        os.system(
            f'SchTasks /Create /SC {frequencia} /TN "Organizador de arquivos" /TR "{local}/auto_organizador.exe" /ST {hora} /F'
        )
        QMessageBox.information(self, "Sucesso", "Agendamento realizado com sucesso")
