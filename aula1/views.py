from models import Conta, engine, Status, Bancos, Historico, Tipos
from sqlmodel import Session, select
from datetime import date
import matplotlib.pyplot as plt

#Cadastrar uma nova conta
def criar_conta(conta:Conta):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.banco==conta.banco)
        results = session.exec(statement).all()
        if results:
            print('Já existe conta cadastrada neste banco.')
            return
        conta.status = Status.ATIVO #para evitar que sejam criadas contas inativas com saldo
        session.add(conta)
        session.commit()
        return conta
    
#Listar contas cadastradas:
def lista_contas():
    with Session(engine) as session:
        statement = select(Conta)
        results = session.exec(statement).all()
    return results

#Tornar uma conta inativa
def desativa_conta(id:int):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==id)
        conta = session.exec(statement).first()
        if not conta:
            print('Nenhuma conta encontrada para o id inserido.')
            return
        if conta.saldo > 0:
            raise ValueError('Não foi possível desativar a conta, pois a mesma possui saldo.')
        conta.status = Status.INATIVO
        session.commit()

def transferir_saldo(id_conta_origem:int, id_conta_destino:int, valor:float):
    with Session(engine) as session:
        #Verificação de conta origem:
        statement = select(Conta).where(Conta.id==id_conta_origem)
        conta_origem = session.exec(statement).first()
        if not conta_origem:
            print ('Conta de origem não encontrada para o ID informado.')
            return
        if conta_origem.saldo < valor:
            raise ValueError('O saldo da conta de origem é insuficiente para a transferência.')
        #Verificação de conta destino:
        statement = select(Conta).where(Conta.id==id_conta_destino)
        conta_destino = session.exec(statement).first()
        if not conta_destino:
            print ('Conta de destino não encontrada para o ID informado.')
            return
        if conta_destino.status==Status.INATIVO:
            print('A conta de destino está inativa. Não foi possível transferir.')
            return
        conta_origem.saldo -= valor
        conta_destino.saldo += valor
        session.commit()

#Lançar uma movimentação financeira
def movimentar_dinheiro(historico:Historico):
    with Session(engine) as session:
        statement = select(Conta).where(Conta.id==historico.conta_id)
        conta = session.exec(statement).first()
        if historico.tipo == Tipos.ENTRADA:
            if conta.status == Status.INATIVO:
                print('A conta de destino está inativa. Selecione outra conta.')
                return
            conta.saldo += historico.valor
        else:
            if conta.saldo < historico.valor:
                raise ValueError('Saldo insulficiente na conta.')
            conta.saldo -= historico.valor
        session.add(historico)
        session.commit()
        return historico

#Visualizar saldo total disponível
def saldo_total():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        total = sum([conta.saldo for conta in contas])
        return total
    
#Visualizar movimentações financeiras entre duas datas
def buscar_historico_entre_datas(data_inicio:date, data_fim:date):
    with Session(engine) as session:
        statement = select(Historico).where(Historico.data>=data_inicio, Historico.data<=data_fim)
        results = session.exec(statement).all()
        return results
    

def criar_grafico_contas():
    with Session(engine) as session:
        statement = select(Conta)
        contas = session.exec(statement).all()
        bancos = [conta.banco.value for conta in contas]
        saldos = [conta.saldo for conta in contas]
        plt.bar(bancos, saldos)
        plt.title('Resumo de Saldo por Banco')
        plt.show()
