#treino.schemas
from ninja import Schema, ModelSchema
from .models import Alunos
from typing import Optional

class AlunosSchema(ModelSchema):
    class Meta:
        model = Alunos
        exclude = ['id'] #serão utilizados todos os campos do modelo Alunos, menos o campo 'id'

class ProgressoAlunoSchema(Schema):
    email: str
    nome: str
    faixa_atual: str
    total_aulas: int
    aulas_restantes_na_faixa: int

class AulaRealizadaSchema(Schema):
    qtd: Optional[int] = 1
    email_aluno: str