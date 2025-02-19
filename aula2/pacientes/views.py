from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Pacientes, Tarefas, Consultas, Visualizacoes
from django.contrib import messages
from django.contrib.messages import constants




# Create your views here.
def pacientes(request):
    queixas = Pacientes.queixa_choices
    pacientes = Pacientes.objects.all()
    if request.method == 'GET':
        return render(request, 'pacientes.html', context={'queixas':queixas, 'pacientes':pacientes})
    elif request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        queixa = request.POST.get('queixa')
        foto = request.FILES.get('foto')

        if len(nome.strip()) == 0 or not foto:
            messages.add_message(request, constants.ERROR, 'Os campos "Nome"  e "Foto" são obrigatórios.')
            return redirect('pacientes')
        paciente = Pacientes(
            nome= nome,
            email = email,
            telefone = telefone,
            queixa = queixa,
            foto = foto)
        paciente.save()
        messages.add_message(request, constants.SUCCESS, f'Paciente {nome} cadastrado com sucesso.')
        return redirect('pacientes')


def paciente_view(request, id):
    paciente = Pacientes.objects.get(id=id)
    tarefas = Tarefas.objects.all()
    consultas = Consultas.objects.filter(paciente=paciente)
    if request.method == 'GET':
        tuple_grafico = ([str(c.data) for c in consultas], [str(c.humor) for c in consultas])
        return render(request, 'paciente.html', {'paciente': paciente, 'tarefas':tarefas, 'consultas':consultas, 'tuple_grafico':tuple_grafico})
    elif request.method == 'POST':
        humor = request.POST.get('humor')
        registro_geral = request.POST.get('registro_geral')
        video = request.FILES.get('video')
        tarefas = request.POST.getlist('tarefas')
        consultas = Consultas(
            humor = int(humor),
            registro_geral = registro_geral,
            video = video,
            paciente = paciente
        )
        consultas.save() #para carregar as tarefas da consulta
        for t in tarefas:
            tarefa = Tarefas.objects.get(id=t)
            consultas.tarefas.add(tarefa)
        consultas.save() #para salvar as alterações feitas na consulta
        messages.add_message(request, constants.SUCCESS, 'Consulta registrada com sucesso.')
        return redirect(f'/pacientes/{id}')
    
def atualizar_paciente(request, id):
    paciente = Pacientes.objects.get(id=id)
    inadimplente = request.POST.get('inadimplente')
    status = False if inadimplente == 'ativo' else True
    paciente.inadimplente = status
    paciente.save()
    return redirect(f'/pacientes/{id}')

def excluir_consulta(request, id):
    consulta = Consultas.objects.get(id=id)
    consulta.delete()
    return redirect(f'/pacientes/{consulta.paciente.id}')


def consulta_publica(request, id):
    consulta = Consultas.objects.get(id=id)
    view = Visualizacoes(
        consulta=consulta,
        ip=request.META['REMOTE_ADDR']
    )
    view.save()
    if consulta.paciente.inadimplente:
        raise Http404()
    return render(request, 'consulta_publica.html', {'consulta':consulta})