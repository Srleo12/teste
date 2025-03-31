import sqlite3


conexao = sqlite3.connect("bancoDB.bd")
cursor = conexao.cursor()

def inserir_compra(nome, peso, preco):
    total = peso * preco  
    cursor.execute("INSERT INTO compras (nome, peso, preco, total) VALUES (?, ?, ?, ?)", 
                   (nome, peso, preco, total))
    conexao.commit()
    print(f"Compra de {nome} salva com sucesso!")

def listar_compras():
    cursor.execute("SELECT * FROM compras")
    compras = cursor.fetchall()
    print("\nLista de Compras:")
    for compra in compras:
        print(f"ID: {compra[0]} | Nome: {compra[1]} | Peso: {compra[2]} kg | Preço: R$ {compra[3]:.2f} | Total: R$ {compra[4]:.2f}")

while True:
    nome = input("Digite o nome do produto: ")
    peso = float(input("Digite o peso (kg): "))
    preco = float(input("Digite o preço por kg: R$ "))

    inserir_compra(nome, peso, preco)

    opcao = input("Deseja adicionar outra compra? (s/n): ").strip().lower()
    if opcao != "s":
        break

listar_compras()

conexao.close()
