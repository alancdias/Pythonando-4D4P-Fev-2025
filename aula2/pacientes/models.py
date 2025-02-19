from django.db import models
from django.urls import reverse

# Create your models here.
class Pacientes(models.Model):
    queixa_choices = (
        ('TD', 'TDAH'),
        ('DE', 'Depressão'),
        ('AN', 'Ansiedade'),
        ('AG', 'Transtorno de Ansiedade Generalizada'),
    )
    nome = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    queixa = models.CharField(max_length=2, choices=queixa_choices, default="TD")
    foto = models.ImageField(upload_to='fotos')
    inadimplente = models.BooleanField(default=False)

    def __str__(self):
        return self.nome
    


class Tarefas(models.Model):
    frequencia_choices = (
        ('D', 'Diário'),
        ('1S', '1 vez por semana'),
        ('2S', '2 vezes por semana'),
        ('3S', '3 vezes por semana'),
        ('N', 'Ao necessitar'),
    )
    tarefa = models.CharField(max_length=255)
    instrucoes = models.TextField(null=True, blank=True)
    frequencia = models.CharField(max_length=2, choices=frequencia_choices, default='N')

    def __str__(self):
        return self.tarefa


class Consultas(models.Model):
    humor = models.PositiveIntegerField()
    registro_geral = models.TextField()
    video = models.FileField(upload_to='videos')
    tarefas = models.ManyToManyField(Tarefas)
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)

    @property
    def link_publico(self):
        return f"http://127.0.0.1:8000{reverse('consulta_publica', kwargs={'id': self.id})}"


    def __str__(self):
        return self.paciente.nome


class Visualizacoes(models.Model):
    consulta = models.ForeignKey(Consultas, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    
    @property
    def views(self):
        views = Visualizacoes.objects.filter(consulta=self)
        totais = views.count()
        unicas = views.values('ip').distinct().count()
        return f'{totais} - {unicas}'