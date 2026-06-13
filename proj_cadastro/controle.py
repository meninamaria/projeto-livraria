from pathlib import Path
import mysql.connector
from PyQt5 import uic, QtWidgets

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Vieira_maria22",
    database="livraria"
)


def funcao_principal():
    nome = formulario.txt_nome.text()
    autor = formulario.txt_autor.text()
    preco = formulario.txt_preco.text()
    categoria = ""

    if formulario.bt_categ_romance.isChecked():
        categoria = "Romance"
    elif formulario.bt_categ_terror.isChecked():
        categoria = "Terror"
    elif formulario.bt_categ_misterio.isChecked():
        categoria = "Mistério"
    elif formulario.bt_categ_infantil.isChecked():
        categoria = "Infantil"
    elif formulario.bt_categ_fantasia.isChecked():
        categoria = "Fantasia"
    else:
        categoria = "Biografia"

    # Inserir os dados no BD
    cursor = banco.cursor()
    comando_SQL = "INSERT INTO livros (nome, autor, preco, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(nome), str(autor), str(preco), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit()

    # Limpar os campos
    formulario.txt_nome.setText("")
    formulario.txt_autor.setText("")
    formulario.txt_preco.setText("")

    # Desmarcar os botões
    formulario.bt_categ_romance.setCheckable(False)
    formulario.bt_categ_terror.setCheckable(False)
    formulario.bt_categ_misterio.setCheckable(False)
    formulario.bt_categ_infantil.setCheckable(False)
    formulario.bt_categ_fantasia.setCheckable(False)
    formulario.bt_categ_biografia.setCheckable(False)


def listar_livros():
    formulario.close()
    acervo.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * from livros"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    acervo.tabela_livros.setRowCount(len(dados_lidos))
    acervo.tabela_livros.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            acervo.tabela_livros.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    acervo.bt_voltar.clicked.connect(lambda: [acervo.close(), formulario.show()])

def deletar_livros():
    formulario.close()
    deletar_livro.show()

    deletar_livro.bt_voltar.clicked.connect(lambda: [acervo.close(), formulario.show()])

    busca = deletar_livro.txt_busca.text()
    deletar_livro.bt_buscar.clicked.connect(lambda: buscar(busca))
        
def buscar(busca):
    cursor = banco.cursor()
    comando_SQL = "SELECT * from livros WHERE codigo = %s OR nome = %s"
    dado = (busca, str(busca))
    cursor.execute(comando_SQL, dado)
    dados_lidos = cursor.fetchall()

    deletar_livro.tabela_livro_excluir.setRowCount(len(dados_lidos))
    deletar_livro.tabela_livro_excluir.setColumnCount(5)

    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            deletar_livro.tabela_livro_excluir.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


# executar o sistema
app = QtWidgets.QApplication([])

ui_path1 = Path(__file__).with_name("formulario.ui")
formulario = uic.loadUi(str(ui_path1))
formulario.bt_cadastrar.clicked.connect(funcao_principal)

ui_path2 = Path(__file__).with_name("acervo.ui")
acervo = uic.loadUi(str(ui_path2))
formulario.bt_listarLivros.clicked.connect(listar_livros)

ui_path3 = Path(__file__).with_name("deletar_livro.ui")
deletar_livro = uic.loadUi(str(ui_path3))
acervo.bt_excluir.clicked.connect(deletar_livros)

formulario.show()
app.exec()