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

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO livros (nome, autor, preco, categoria) VALUES (%s, %s, %s, %s)"
    dados = (str(nome), str(autor), float(preco), categoria)
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



# executar o sistema
app = QtWidgets.QApplication([])
ui_path = Path(__file__).with_name("formulario.ui")
formulario = uic.loadUi(str(ui_path))
formulario.bt_cadastrar.clicked.connect(funcao_principal)

formulario.show()
app.exec()