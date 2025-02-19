from datetime import datetime
from models import *
from views import *


class UI:
    def start(self):
        while True:
            print('''
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
                  ''')
            
            choice = int(input('Escolha uma opção: '))

            if choice == 1:
                self._criar_conta()
            elif choice == 2:
                self._desativar_conta()
            elif choice == 3:
                self._transferir_saldo()
            elif choice == 4:
                self._movimentar_dinheiro()
            elif choice == 5:
                self._total_contas()
            elif choice == 6:
                self._filtrar_movimentacoes()
            elif choice == 7:
                self._criar_grafico()
            else:
                break

    def _criar_conta(self):
        print('Digite o nome de algum dos bancos abaixo:')
        for banco in Bancos:
            print(f'---{banco.value}---')
        
        banco = input().title()
        valor = float(input('Digite o valor atual disponível na conta: '))

        conta = Conta(banco=Bancos(banco), saldo=valor)
        criar_conta(conta)

    def _desativar_conta(self):
        print('Escolha a conta que deseja desativar.')
        for conta in lista_contas():
            if conta.saldo == 0:
                print(f'{conta.id} -> {conta.banco.value} -> R$ {conta.saldo}')

        id_conta = int(input())

        try:
            desativa_conta(id_conta)
            print('Conta desativada com sucesso.')
        except ValueError:
            print('Essa conta ainda possui saldo, faça uma transferência')

    def _transferir_saldo(self):
        print('Escolha a conta de onde retirar o dinheiro.')
        for conta in lista_contas():
            print(f'{conta.id} -> {conta.banco.value} -> R$ {conta.saldo}')

        conta_origem_id = int(input())

        print('Escolha a conta para enviar dinheiro.')
        for conta in lista_contas():
            if conta.id != conta_origem_id:
                print(f'{conta.id} -> {conta.banco.value} -> R$ {conta.saldo}')

        conta_destino_id = int(input())

        valor = float(input('Digite o valor para transferir: '))
        transferir_saldo(conta_origem_id, conta_destino_id, valor)

    def _movimentar_dinheiro(self):
        print('Escolha a conta.')
        for conta in lista_contas():
            print(f'{conta.id} -> {conta.banco.value} -> R$ {conta.saldo}')

        conta_id = int(input())

        valor = float(input('Digite o valor movimentado: '))

        print('Selecione o tipo da movimentação')
        for tipo in Tipos:
            print(f'---{tipo.value}---')
        
        tipo = input().title()
        descricao = input('Digite uma descrição para a movimentação: ')
        historico = Historico(conta_id=conta_id, tipo=Tipos(tipo), valor=valor, data=date.today(), descricao=descricao)
        movimentar_dinheiro(historico)
    
    def _total_contas(self):
        print(f'R$ {saldo_total()}')

    def _filtrar_movimentacoes(self):
        data_inicio = input('Digite a data de início: ')
        data_fim = input('Digite a data final: ')

        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()

        for movimentacao in buscar_historico_entre_datas(data_inicio, data_fim):
            print(f'{movimentacao.data} - {movimentacao.tipo.value} - {movimentacao.valor} - Banco {movimentacao.conta_id} - {movimentacao.descricao}')

    def _criar_grafico(self):
        criar_grafico_contas()

UI().start()