import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from database import get_session, Produto, HistoricoPreco
from config import EMAIL_CONFIG

def enviar_alerta(produto, preco_atual):
    subject = f"Alerta de Preço: {produto.nome} atingiu R${preco_atual:.2f}"
    body = f"""
    O produto que você está monitorando atingiu o preço desejado!
    
    Detalhes:
    - Produto: {produto.nome}
    - Preço Atual: R${preco_atual:.2f}
    - Preço Desejado: R${produto.preco_desejado:.2f}
    - URL: {produto.url}
    
    Aproveite a oportunidade!
    """
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_CONFIG['sender']
    msg['To'] = EMAIL_CONFIG['sender']  # Enviando para si mesmo, pode modificar
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender'], EMAIL_CONFIG['password'])
        server.send_message(msg)
        server.quit()
        print(f"Alerta enviado para {produto.nome}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")

def verificar_alertas():
    session = get_session()
    produtos = session.query(Produto).filter(Produto.ativo == 1).all()
    
    for produto in produtos:
        preco_atual = obter_preco_atual(produto.url)
        if preco_atual and preco_atual <= produto.preco_desejado:
            enviar_alerta(produto, preco_atual)
            
        # Registrar no histórico independente de alerta
        novo_historico = HistoricoPreco(
            produto_id=produto.id,
            data_verificacao=datetime.now(),
            preco_atual=preco_atual
        )
        session.add(novo_historico)
        produto.ultima_verificacao = datetime.now()
    
    session.commit()
    session.close()



"""
# Código que força o alerta chegar no email, sem precisar esperar o site abaixar o preço. 

if __name__ == "__main__":
    from database import Produto
    session = get_session()
    
    # Cria um produto de teste
    produto_teste = Produto(
        nome="PRODUTO TESTE",
        url="https://www.amazon.com.br/dummy-product",
        preco_desejado=100.00,
        frequencia=1,
        ultima_verificacao=None
    )
    session.add(produto_teste)
    session.commit()
    
    # Força um alerta (preço abaixo do desejado)
    enviar_alerta(produto_teste, 95.99)  # Preço mockado abaixo do desejado
    session.close()

"""