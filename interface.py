from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from database import get_session, Produto, HistoricoPreco

def cadastrar_produto():
    session = get_session()
    
    print("\n--- Cadastro de Produto ---")
    nome = input("Nome do produto: ")
    url = input("URL do produto: ")
    
    # Modificação aqui para aceitar formato brasileiro
    preco_str = input("Preço desejado para alerta (R$): ").strip()
    preco_desejado = float(preco_str.replace('.', '').replace(',', '.'))
    
    frequencia = int(input("Frequência de verificação (horas): "))
    
    novo_produto = Produto(
        nome=nome,
        url=url,
        preco_desejado=preco_desejado,
        frequencia=frequencia,
        ultima_verificacao=None,
        ativo=1
    )
    
    session.add(novo_produto)
    session.commit()
    print("Produto cadastrado com sucesso!")
    session.close()

def listar_produtos():
    session = get_session()
    produtos = session.query(Produto).all()
    
    print("\n--- Produtos Monitorados ---")
    for produto in produtos:
        status = "Ativo" if produto.ativo else "Inativo"
        print(f"ID: {produto.id} | Nome: {produto.nome[:30]}... | Preço Alvo: R${produto.preco_desejado:.2f} | Frequência: {produto.frequencia}minutos | Status: {status}")
    
    session.close()

def ver_historico():
    produto_id = int(input("ID do produto para ver histórico: "))
    
    session = get_session()
    historicos = session.query(HistoricoPreco).filter(HistoricoPreco.produto_id == produto_id).order_by(HistoricoPreco.data_verificacao).all()
    
    if not historicos:
        print("Nenhum histórico encontrado para este produto.")
        return
    
    # Criar DataFrame para exibição
    dados = []
    for hist in historicos:
        dados.append({
            'Data': hist.data_verificacao.strftime('%d/%m/%Y %H:%M'),
            'Preço': f"R${hist.preco_atual:.2f}"
        })
    
    df = pd.DataFrame(dados)
    print("\n--- Histórico de Preços ---")
    print(df.to_string(index=False))
    
    # Plotar gráfico
    datas = [h.data_verificacao for h in historicos]
    precos = [h.preco_atual for h in historicos]
    
    plt.figure(figsize=(10, 5))
    plt.plot(datas, precos, marker='o')
    plt.title(f"Variação de Preço - {session.query(Produto).get(produto_id).nome}")
    plt.xlabel("Data")
    plt.ylabel("Preço (R$)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    session.close()

def menu_principal():
    while True:
        print("\n=== Rastreador de Preços ===")
        print("1. Cadastrar novo produto")
        print("2. Listar produtos monitorados")
        print("3. Ver histórico de preços")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_produto()
        elif opcao == '2':
            listar_produtos()
        elif opcao == '3':
            ver_historico()
        elif opcao == '4':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")