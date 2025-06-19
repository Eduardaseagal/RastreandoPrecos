import schedule
import time
from threading import Thread
from alert import verificar_alertas
from interface import menu_principal
from database import get_session, Produto

def agendar_verificacoes():
    session = get_session()
    produtos = session.query(Produto).filter(Produto.ativo == 1).all()
    session.close()
    
    for produto in produtos:
        # Alterado para .minutes ao invés de .hours
        schedule.every(produto.frequencia).minutes.do(verificar_alertas)
    
    print(f"Agendamentos configurados. Verificações a cada {produto.frequencia} minutos.")
    
    while True:
        schedule.run_pending()
        time.sleep(1)  # Verifica a cada segundo se há tarefas pendentes

def iniciar_sistema():
    # Iniciar thread para verificações agendadas
    thread_agendamentos = Thread(target=agendar_verificacoes)
    thread_agendamentos.daemon = True
    thread_agendamentos.start()
    
    # Iniciar interface do usuário
    menu_principal()

if __name__ == "__main__":
    iniciar_sistema()