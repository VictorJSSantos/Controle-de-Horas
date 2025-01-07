from pydantic import BaseModel
from typing import List
from datetime import datetime


class TaskSchema(BaseModel):
    name: str
    descricao: str
    horario_de_inicio: Optional[datetime]
    horario_de_finalizacao: Optional[datetime]
    ativo: Optional[bool] = True
    company_id: int


class CompanySchema(BaseModel):
    name: str
    descricao: str
    faixas_salariais: List[int]
    renda_por_faixa: List[int]
