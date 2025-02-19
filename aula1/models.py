#Camada Models - Integração com banco da dados

from sqlmodel import SQLModel, Field, create_engine, Relationship #Para transformar classes em tabelas no DB
from enum import Enum
from datetime import date

#classes auxiliares para criação de campos de opções
class Bancos(Enum):
    NUBANK = 'Nubank'
    SANTANDER = 'Santander'
    INTER = 'Inter'
    BRADESCO = 'Bradesco'
    BB = 'Banco Do Brasil'

class Status(Enum):
    ATIVO = 'Ativo'
    INATIVO = 'Inativo'

class Tipos(Enum):
    ENTRADA = 'Entrada'
    SAIDA = 'Saída'

#Tabela de contas (tabelas são criadas como classes)
class Conta(SQLModel, table=True):
    id:int = Field(primary_key=True)
    banco:Bancos = Field(default=Bancos.NUBANK)
    status:Status = Field(default=Status.ATIVO)
    saldo:float = Field(default=0.0)

#Tabela para manter histórico de operações financeiras
class Historico(SQLModel, table=True):
    id:int = Field(primary_key=True)
    conta_id:int = Field(foreign_key='conta.id')
    conta:Conta = Relationship()
    tipo:Tipos = Field(default=Tipos.SAIDA)
    valor:float
    data:date
    descricao:str = Field(nullable=True, default='')

sqlite_file_name = 'database.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'

engine = create_engine(sqlite_url, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_db_and_tables()