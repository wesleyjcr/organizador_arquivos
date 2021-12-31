import sqlite3
from shutil import move
from os import listdir, mkdir
from os.path import isfile, isdir, join, splitext


def conecta_banco():
    con = sqlite3.connect("dados/database.db")
    cur = con.cursor()
    return con, cur


def caminho_entrada(cur):
    entrada = []
    for row in cur.execute("SELECT * FROM PASTA_ENTRADA;"):
        entrada.append(row[1])
    return entrada


def caminho_saida(cur):
    saida = []
    for row in cur.execute("SELECT * FROM PASTA_SAIDA;"):
        saida.append({"url": row[1], "extension": row[2]})
    return saida


def mover_arquivos(arquivos, saida):
    for destino in saida:
        for arquivo in arquivos:
            if arquivo["extensao"].lower() in destino["extension"].lower():
                print(arquivo)
                move(arquivo["url"], join(destino["url"], arquivo["arquivo"]))


def verifica_pastas(url):
    arquivos = []
    for arquivo in listdir(url):
        if isfile(join(url, arquivo)):
            caminho = join(url, arquivo)
            extensao = splitext(join(url, arquivo))[1].replace(".", "")
            arquivos.append({"arquivo": arquivo, "url": caminho, "extensao": extensao})
    return arquivos


con, cur = conecta_banco()
entrada = caminho_entrada(cur)
saida = caminho_saida(cur)
con.close()

arquivos = []
for url in entrada:
    arquivos.append(verifica_pastas(url))

for arquivo in arquivos:
    mover_arquivos(arquivo, saida)
