import sqlite3
import os
from datetime import datetime

def limpar_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def conectar():
    return sqlite3.connect("compras.db")

def criar_tabela():
    with conectar() as con:
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            peso REAL NOT NULL,
            preco REAL NOT NULL,
            total REAL NOT NULL,
            data_compra TEXT NOT NULL
        )''')
        con.commit()

def adicionar_item():
    while True:
        limpar_terminal()
        nome = input("\nProduto: ")
        peso = float(input("Peso (kg): "))
        preco = float(input("Preço por kg: "))
        total = peso * preco
        data_compra = datetime.today().strftime('%d/%m/%Y')
        print(f"Total: R${total:.2f}")

        with conectar() as con:
            cur = con.cursor()
            cur.execute("INSERT INTO compras (nome, peso, preco, total, data_compra) VALUES (?, ?, ?, ?, ?)", (nome, peso, preco, total, data_compra))
            con.commit()
            print("Item adicionado com sucesso!\n")

        opcao = input("Deseja adicionar outra compra? (s/n): ").strip().lower()
        if opcao != 's':
            break

def consultar_lista():
    hoje = datetime.today().strftime('%d/%m/%Y')

    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM compras WHERE data_compra = ?", (hoje,))
        itens = cur.fetchall()
        
        if not itens:
            print("\nNenhuma compra registrada para hoje.\n")
        else:
            print(f"\nLista de Compras ({hoje}):")
            for item in itens:
                print(f"ID: {item[0]} | Nome: {item[1]} | Peso: {item[2]}kg | Preço: R${item[3]:.2f} | Total: R${item[4]:.2f}")
            print()

def minha_lista():
    with conectar() as con:
        cur = con.cursor()
        cur.execute("SELECT DISTINCT data_compra FROM compras ORDER BY data_compra DESC")
        datas = cur.fetchall()
        
        if not datas:
            print("\nNenhuma compra registrada.\n")
            return
        
        print("\nMinhas Compras:")
        for idx, data in enumerate(datas, start=1):
            print(f"{idx}. Compras de {data[0]}")
        
        escolha = input("\nEscolha uma data pelo número (ou pressione Enter para voltar): ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(datas):
            data_selecionada = datas[int(escolha) - 1][0]
            limpar_terminal()
            with conectar() as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM compras WHERE data_compra = ?", (data_selecionada,))
                itens = cur.fetchall()
                print(f"\nCompras de {data_selecionada}:")
                for item in itens:
                    print(f"ID: {item[0]} | Nome: {item[1]} | Peso: {item[2]}kg | Preço: R${item[3]:.2f} | Total: R${item[4]:.2f}")

def excluir_item():
    consultar_lista()
    item_id = input("Digite o ID do item a ser removido: ")
    with conectar() as con:
        cur = con.cursor()
        cur.execute("DELETE FROM compras WHERE id = ?", (item_id,))
        con.commit()
        print("Item removido com sucesso!\n")

def menu():
    criar_tabela()
    while True:
        print("\n1. Adicionar itens")
        print("2. Consultar lista")
        print("3. Minha lista")
        print("4. Excluir item")
        print("5. Fechar")
        opcao = input("\nEscolha uma opção: ")
        
        if opcao == "1":
            adicionar_item()
        elif opcao == "2":
            consultar_lista()
        elif opcao == "3":
            minha_lista()
        elif opcao == "4":
            excluir_item()
        elif opcao == "5":
            limpar_terminal()
            print("Saindo...")
            break
        else:
            print("Opção inválida!\n")

menu()