
from fastapi import FastAPI, HTTPException,Depends,status
from pydantic import BaseModel
from typing import Annotated

import sqlalchemy
from workout_api.yallSchemas import Atleta,Categoria,Centro_Treinamento
from conexaodb import engine,sessionlocal
from sqlalchemy.orm import Session
from workout_api import models
from workout_api.models import AtletaModel, CT_Model , CategoriaModel



app = FastAPI()

models.Basemodel.metadata.create_all(bind=engine)

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()  
        
db_dependency = Annotated[Session,Depends(get_db)]


# Atleta

@app.post('/atleta/',status_code=status.HTTP_201_CREATED)
async def Criar_atleta(Atleta:Atleta,db:db_dependency):
    try:
        db_post = AtletaModel(**Atleta.model_dump())
        db.add(db_post)
        db.commit()
    except sqlalchemy.exc.IntegrityError as ex:
        print('Ja existe um usuario com esse CPF')
        print(ex.orig)
        print(ex.statement)
        db.rollback() 
        raise HTTPException(status_code=303,detail='Ja existe um usuario com esse cpf')
    
    
@app.get('/atleta/{id_atleta}',status_code=status.HTTP_200_OK)
async def Procurar_atleta(id_atleta:int,db:db_dependency):
    atleta = db.query(AtletaModel).filter(AtletaModel.pk_id == id_atleta).first()
    if atleta == None:
        raise HTTPException(status_code=404,detail='Atleta nao encontrado')
    return atleta

@app.get('/atleta/nome/',status_code=status.HTTP_200_OK)
async def Procurar_atleta_nome(nome:str | None,db:db_dependency):
    atletas = db.query(AtletaModel).filter(AtletaModel.nome == nome).all()
    if atletas == None:
        raise HTTPException(status_code=404,detail='Atletas nao encontrado')
    return atletas


@app.get('/atleta/cpf/',status_code=status.HTTP_200_OK)
async def Procurar_atleta_cpf(cpf_atleta:str,db:db_dependency):
    atleta = db.query(AtletaModel).filter(AtletaModel.cpf == cpf_atleta).first()
    if atleta == None:
        raise HTTPException(status_code=404,detail='CPF do atleta nao encontrado')
    return atleta


@app.get('/atleta/',status_code=status.HTTP_200_OK)
async def Listar_Atletas(db:db_dependency):
    query = db.query(AtletaModel).join(CT_Model,CT_Model.pk_id == AtletaModel.centro_treinamento_id, isouter=True).all()

    if query == None:
        raise HTTPException(status_code=404,detail='Não existe nenhum atleta cadastrado')
    return query
        



@app.delete('/atleta/delete/{id_atleta}',status_code=status.HTTP_200_OK)
async def Delete_atleta(id_atleta:int,db:db_dependency):
    atleta = db.query(AtletaModel).filter(AtletaModel.pk_id == id_atleta).first()
    if atleta == None:
        raise HTTPException(status_code=404,detail='Atleta nao encontrado')
    db.delete(atleta)
    db.commit()
    

        

# Categoria

@app.post('/categoria/',status_code=status.HTTP_201_CREATED)
async def Criar_categoria(categoria:Categoria,db:db_dependency):
    db_post = CategoriaModel(**categoria.model_dump())
    db.add(db_post)
    db.commit()

@app.get('/categoria/{id_categoria}',status_code=status.HTTP_200_OK)
async def Procurar_categoria(id_categoria:int,db:db_dependency):
    categoria = db.query(CategoriaModel).filter(CategoriaModel.pk_id == id_categoria).first()
    if categoria == None:
        raise HTTPException(status_code=404,detail='Categoria não encontrada')
    return categoria

@app.delete('/categoria/delete/{id_categoria}',status_code=status.HTTP_200_OK)
async def Delete_categoria(id_categoria:int,db:db_dependency):
    db_delete = db.query(CategoriaModel).filter(CategoriaModel.pk_id == id_categoria).first()
    if db_delete == None:
        raise HTTPException(status_code=404,detail='Categoria não encontrada')
    db.delete(db_delete)
    db.commit()
    
#Centro de treinamento

@app.post('/Centro_treinamento/',status_code=status.HTTP_201_CREATED)
async def Criar_CentroTreinamento(ct:Centro_Treinamento,db:db_dependency):
    db_post = CT_Model(**ct.model_dump())
    db.add(db_post)
    db.commit()
    
    
@app.get('/Centro_treinamento/{id_CT}',status_code=status.HTTP_200_OK)
async def Procurar_CT(id_CT:int,db:db_dependency):
    centro_treinamento = db.query(CT_Model).filter(CT_Model.pk_id == id_CT).first()
    if centro_treinamento == None:
        raise HTTPException(status_code=404,detail='Centro de treinamento não encontrado')
    return centro_treinamento

@app.delete('/Centro_treinamento/delete/{id_CT}',status_code=status.HTTP_200_OK)
async def Delete_Centro_Treinamento(id_CT:int,db:db_dependency):
    centro_treinamento = db.query(CT_Model).filter(CT_Model.pk_id == id_CT).first()
    if centro_treinamento == None:
        raise HTTPException(status_code=404,detail='Centro de treinamento não achado')
    db.delete(centro_treinamento)
    db.commit()
    
    
    
