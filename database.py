import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_PATH

Base = declarative_base()

class Produto(Base):
    __tablename__ = 'produtos'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    url = Column(String)
    preco_desejado = Column(Float)
    frequencia = Column(Integer)  # em horas
    ultima_verificacao = Column(DateTime)
    ativo = Column(Integer, default=1)  # 1 para ativo, 0 para inativo

class HistoricoPreco(Base):
    __tablename__ = 'historico_precos'
    
    id = Column(Integer, primary_key=True)
    produto_id = Column(Integer)
    data_verificacao = Column(DateTime)
    preco_atual = Column(Float)

# Inicialização do banco de dados
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()