import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Usuario(Base):

    __tablename__ = "usuario"

    id = Column(Integer,primary_key=True)
    nome = Column(String(250),nullable=False)
    email = Column(String(250),nullable=False)
    picture = Column(String(250))


class Categoria(Base):

    __tablename__ = "categoria"

    nome = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))
    usuario = relationship(Usuario)

    '''Essa função infoma quais dados queremos serializar e coloca em um formato
    que o flask consegue trabalhar mais facilmente'''
    @property
    def serialize(self):
        #Retorna os dados do objeto em um formato facilmente serializavel
        return {
            'nome':self.nome,
            'id':self.id,
        }



class Item(Base):

    __tablename__ = "item"

    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    descricao = Column(String(250), nullable=False)
    preco = Column(String(8), nullable=False)
    imagem = Column(String(250))
    categoria = Column(String(100), nullable=False)

    usuario = relationship(Usuario)
    usuario_id = Column(Integer, ForeignKey('usuario.id'))



    '''Essa função infoma quais dados queremos serializar e coloca em um formato
    que o flask consegue trabalhar mais facilmente'''
    @property
    def serialize(self):
        #Retorna os dados do objeto em um formato facilmente serializavel
        return {
            'nome':self.nome,
            'descricao':self.descricao,
            'id':self.id,
            'preco':self.preco,
            'categoria':self.categoria,
            'imagem':self.imagem,
        }

engine = create_engine('sqlite:///catalogodeitems.db')
Base.metadata.create_all(engine)
