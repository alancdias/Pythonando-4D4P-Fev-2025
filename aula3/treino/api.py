#treino.api
"""O conteúdo deste arquivo poderia ser implementado no arquivo views. 
Mas, por boas práticas, colocamos em um arquivo separado tudo que for tratado via APIs de um app."""


from django.shortcuts import get_object_or_404
from ninja import Router
from .schemas import AlunosSchema, ProgressoAlunoSchema, AulaRealizadaSchema
from .models import Alunos, AulasConcluidas
from ninja.errors import HttpError
from .graduacao import *
from datetime import date


treino_router = Router()

#Apenas para teste (fica de easter egg no site)
@treino_router.get('/ola-mundo') #.get: Buscar/exibir dados
def ola_mundo(request):
    return {'Ola_mundo': 'Ola, mundo'}

#Definindo endpoints para os alunos

#Endpoint para criação de aluno
@treino_router.post('/', response={200: AlunosSchema}) #post: criar dados
def cria_aluno(request, aluno_schema:AlunosSchema):
    if Alunos.objects.filter(email=aluno_schema.email).exists():
        raise HttpError(400, 'Já existe um aluno cadastrado com este e-mail')
    #Se não retornar erro:
    aluno = Alunos(**aluno_schema.dict())
    aluno.save()
    return aluno

#Endpoint para listagem de todos os alunos cadastrados    
@treino_router.get('/alunos/', response=list[AlunosSchema]) #.get: Buscar dados
def lista_alunos(request):
    alunos = Alunos.objects.all()
    return alunos


#Definindo endpoints para aulas:
@treino_router.get('/progresso-aluno/', response={200: ProgressoAlunoSchema})
def progresso_aluno(request, email_aluno:str):
    aluno = Alunos.objects.get(email=email_aluno)
    print('Aluno:', aluno)
    total_aulas_concluidas = AulasConcluidas.objects.filter(aluno=aluno).count()
    print('Aulas concluidas', total_aulas_concluidas)
    faixa_atual = aluno.get_faixa_atual_display()
    print('Faixa atual', faixa_atual)
    n = ordem_faixas.get(faixa_atual, 0)
    min_aulas_faixa_atual = calc_min_aulas_por_faixa(n)
    print('aulas necessárias', min_aulas_faixa_atual)
    aulas_concluidas_faixa_atual = AulasConcluidas.objects.filter(aluno=aluno, faixa_atual=aluno.faixa_atual).count()
    print('aulas concluidas', aulas_concluidas_faixa_atual)
    aulas_restantes_faixa_atual = max(min_aulas_faixa_atual - aulas_concluidas_faixa_atual, 0)
    print('aulas restantes', aulas_restantes_faixa_atual)
    return {
        'email': aluno.email,
        'nome': aluno.nome,
        'faixa_atual': faixa_atual,
        'total_aulas': aulas_concluidas_faixa_atual,
        'aulas_restantes_na_faixa': aulas_restantes_faixa_atual
    }

@treino_router.post('/aula-realizada/', response={200:str})
def marca_aula_realizada(request, aula:AulaRealizadaSchema):
    
    if aula.qtd <= 0: #Caso tenha sido marcada menos de uma aula,
        raise HttpError(400,'A quantidade de aulas registrada deve ser maior que 0.')
    aluno = Alunos.objects.get(email=aula.email_aluno)
    aulas = [AulasConcluidas(aluno=aluno, faixa_atual=aluno.faixa_atual) for _ in range(aula.qtd)]
    AulasConcluidas.objects.bulk_create(aulas)
    return 200, f'{aula.qtd} aula(s) registrada(s) com sucesso para {aluno}.'
    



@treino_router.put('/alunos/{aluno_id}', response={200:AlunosSchema})
def atualiza_aluno(request, aluno_id:int, aluno_data:AlunosSchema):
    aluno = Alunos.objects.get(id=aluno_id)
    print('Aluno', aluno)
    idade = (date.today() - aluno.data_nascimento).days // 365
    print('Idade', idade)
    if idade < 18 and aluno_data.dict()['faixa_atual'] in ['A', 'R', 'M', 'P']:
        raise HttpError(400, 'O aluno é menor de idade e não pode receber esta faixa.')
    for attr, value in aluno_data.dict().items():
        if value:
            setattr(aluno, attr, value)
    aluno.save()
    return aluno