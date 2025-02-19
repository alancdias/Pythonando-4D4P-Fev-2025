import flet as ft
import requests

API_BASE_URL = 'http://localhost:8000/api'

def main(page:ft.Page):
    page.title = "Kobra BJJ - Controle de Alunos"
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    
    
    #Aba de Cadastro de Alunos    
    nome_field = ft.TextField(label='Nome')
    email_field = ft.TextField(label='Email')
    faixa_field = ft.TextField(label='Faixa atual')
    data_nasc_field = ft.TextField(label='Data de Nascimento ("AAAA-MM-DD")')
    
    cadastro_result = ft.Text()

    def cadastrar_aluno_click(evento):
        payload = {
            'nome': nome_field.value,
            'email': email_field.value,
            'faixa_atual': faixa_field.value,
            'data_nascimento': data_nasc_field.value,
        }
        try:
            response = requests.post(API_BASE_URL+'/', json=payload)
            if response.status_code == 200:
                aluno = response.json()
                cadastro_result.value = f'Aluno {aluno} cadastrado com sucesso'
            else:
                cadastro_result.value = f'Erro: {response.text}'
        except Exception as exc:
            cadastro_result.value = f'Exceção: {exc}'
        page.update()


        
    bt_cadastrar = ft.ElevatedButton(text='Cadastrar Aluno', on_click=cadastrar_aluno_click)

    tab_cadastrar_aluno = ft.Column(
        [
            nome_field,
            email_field,
            faixa_field,
            data_nasc_field,
            cadastro_result,
            bt_cadastrar
        ], scroll=True
    )

    
    #Aba Listar Alunos
    tabela_alunos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text('Nome')),
            ft.DataColumn(ft.Text('Email')),
            ft.DataColumn(ft.Text('Faixa atual')),
            ft.DataColumn(ft.Text('Data de nascimento')),
        ],
        rows=[]
    )
    
    lista_result = ft.Text()
    
    def atualiza_lista_click(evento):
        try:
            response = requests.get(API_BASE_URL+'/alunos/')
            if response.status_code == 200:
                alunos = response.json()
                tabela_alunos.rows.clear()
                for aluno in alunos:
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(aluno.get('nome', ''))),
                            ft.DataCell(ft.Text(aluno.get('email', ''))),
                            ft.DataCell(ft.Text(aluno.get('faixa_atual', ''))),
                            ft.DataCell(ft.Text(aluno.get('data_nascimento', ''))),
                        ]
                    )
                    tabela_alunos.rows.append(row)
                lista_result.value = f'{len(alunos)} alunos encontrados.'
            else:
                lista_result.value = f'Erro: {response.text}'
        except Exception as exc:
            lista_result.value = f'Exceção: {exc}'
        page.update()


    bt_atualiza_lista = ft.ElevatedButton(text='Atualizar Lista', on_click=atualiza_lista_click)

    tab_listar_alunos = ft.Column(
        [
            tabela_alunos,
            lista_result,
            bt_atualiza_lista
        ], scroll=True
    )


    #Aba de marcação de aula
    email_field = ft.TextField(label='Email do aluno')
    qtd_field = ft.TextField(label='Quantidade de aulas a serem marcadas como concluídas', value='1')

    marca_aula_result = ft.Text()

    def marca_aula_click(evento):
        try:
            email = email_field.value
            if not email:
                marca_aula_result.value = 'O email do aluno deve ser informado.'
            else:
                payload = {'qtd':int(qtd_field.value), 'email_aluno':email}
                response = requests.post(API_BASE_URL+'/aula-realizada/', json=payload)
                if response.status_code == 200:
                    marca_aula_result.value = f'Sucesso. {response.json()}'
                else:
                    marca_aula_result.value = f'Erro. {response.text}'
        except Exception as exc:
            marca_aula_result.value = f'Exceção: {response.text}'
        page.update()

    bt_marcar_aula = ft.ElevatedButton(text='Marcar aula como Concluída', on_click=marca_aula_click)

    tab_aula_concluida = ft.Column(
        [
            email_field,
            qtd_field,
            marca_aula_result,
            bt_marcar_aula,
        ], scroll=True
    )



    #Aba de acompanhamento do progresso de um aluno
    email_progresso_field = ft.TextField(label='Email do aluno')
    
    progresso_result = ft.Text()

    def ver_progresso_click(evento):
        try:
            email = email_progresso_field.value
            response=requests.get(API_BASE_URL+'/progresso-aluno/', params={'email_aluno':email})
            if response.status_code == 200:
                progresso = response.json()
                progresso_result.value = (
                    f"Nome: {progresso.get('nome', '')}\n"
                    f"Email: {email}\n"
                    f"Faixa Atual: {progresso.get('faixa_atual', '')}\n"
                    f"Aulas completadas nesta faixa: {progresso.get('total_aulas', '')}\n"
                    f"Aulas restantes nesta faixa: {progresso.get('aulas_restantes_na_faixa', '')}\n"
                )
            else:
                progresso_result.value = f'Erro: {response.text}'
        except Exception as exc:
            progresso_result.value = f'Exceção: {response.text}'
        page.update()

    bt_ver_progresso = ft.ElevatedButton(text='Acompanhar progresso do aluno', on_click=ver_progresso_click)

    tab_progresso_aluno = ft.Column(
       [
           email_progresso_field,
            progresso_result,
            bt_ver_progresso
        ], scroll=True
    )




    #Aba de Atualização de Alunos  
    id_aluno_field = ft.TextField(label="ID do Aluno")  
    nome_update_field = ft.TextField(label='Novo nome')
    email_update_field = ft.TextField(label='Novo email')
    faixa_update_field = ft.TextField(label='Nova faixa atual')
    data_nasc_update_field = ft.TextField(label='Nova data de Nascimento ("AAAA-MM-DD")')
    
    atualiza_result = ft.Text()

    def atualizar_aluno_click(evento):
        try:
            aluno_id = id_aluno_field.value
            if not aluno_id:
                atualiza_result.value = 'É necessário inserir o ID do aluno'
            else:
                payload = {}
                if nome_update_field:
                    payload['nome'] = nome_update_field.value
                if nome_update_field:
                    payload['email'] = email_update_field.value
                if nome_update_field:
                    payload['faixa_atual'] = faixa_update_field.value
                if nome_update_field:
                    payload['data_nascimento'] = data_nasc_update_field.value
                response = requests.put(API_BASE_URL+f'/alunos/{aluno_id}', json=payload)
                if response.status_code == 200:
                    aluno = response.json()
                    atualiza_result.value = f'Dados do aluno atualizados com sucesso. {aluno}'
                else:
                    atualiza_result.value = f'Erro: {response.text}'
        except Exception as exc:
            atualiza_result.value = f'Exceção: {exc}'
        page.update()
        
    bt_atualizar = ft.ElevatedButton(text='Atualizar Aluno', on_click=atualizar_aluno_click)

    tab_atualizar_aluno = ft.Column(
        [
            id_aluno_field,
            nome_update_field,
            email_update_field,
            faixa_update_field,
            data_nasc_update_field,
            atualiza_result,
            bt_atualizar
        ], scroll=True
    )


    tabs = ft.Tabs(selected_index=0,
                   tabs=[
                       ft.Tab(text='Cadastrar Aluno', content=tab_cadastrar_aluno),
                       ft.Tab(text='Listar Alunos', content=tab_listar_alunos),
                       ft.Tab(text='Marcar Aula como Concluída', content=tab_aula_concluida),
                       ft.Tab(text='Acompanhar Progresso de Aluno', content=tab_progresso_aluno),
                       ft.Tab(text='Atualizar Aluno', content=tab_atualizar_aluno),
                   ])
    page.add(tabs) 


if __name__ == '__main__':
    ft.app(target=main)