from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from bancodedados_setup import Categoria, Base, Item, Usuario

engine = create_engine('sqlite:///catalogodeitems.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()



# Create dummy user
User1 = Usuario(nome="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


cat1 = Categoria(usuario_id=1, nome="Roupas")
session.add(cat1)
session.commit()

cat2 = Categoria(usuario_id=1, nome="Sapatos")
session.add(cat2)
session.commit()

cat3 = Categoria(usuario_id=1, nome="Chinelos")
session.add(cat3)
session.commit()

cat4 = Categoria(usuario_id=1, nome="Cintos")
session.add(cat4)
session.commit()

cat5 = Categoria(usuario_id=1, nome="Meias")
session.add(cat5)
session.commit()


item1 = Item(usuario_id=1,
             nome="Camiseta Vermelha",
             descricao="Uma maravilhosa camiseta vermelha que vai te fazer ficar lindo!",
             preco="16,99",
             categoria=cat1.nome,
             imagem="")

session.add(item1)
session.commit()

item2 = Item(usuario_id=1,
             nome="Camiseta Preta",
             descricao="Uma maravilhosa camiseta preta que vai te fazer ficar lindo!",
             preco="12,99",
             categoria=cat1.nome,
             imagem="")

session.add(item2)
session.commit()

item3 = Item(usuario_id=1,
             nome="Camiseta Amarela",
             descricao="Uma maravilhosa camiseta amarela que vai te fazer ficar lindo!",
             preco="14,99",
             categoria=cat1.nome,
             imagem="")

session.add(item3)
session.commit()

item4 = Item(usuario_id=1,
             nome="Camiseta Vermelha Estampada",
             descricao="Uma maravilhosa camiseta vermelha estampada que vai te fazer ficar lindo!",
             preco="21,99",
             categoria=cat1.nome,
             imagem="")

session.add(item4)
session.commit()

item5 = Item(usuario_id=1,
             nome="Camiseta Azul",
             descricao="Uma maravilhosa camiseta azul que vai te fazer ficar lindo!",
             preco="19,99",
             categoria=cat1.nome,
             imagem="")

session.add(item5)
session.commit()

item6 = Item(usuario_id=1,
             nome="Camiseta Rosa",
             descricao="Uma maravilhosa camiseta rosa que vai te fazer ficar lindo!",
             preco="17,99",
             categoria=cat1.nome,
             imagem="")

session.add(item6)
session.commit()




item4 = Item(usuario_id=1,
             nome="Sapato Preto",
             descricao="Uma sapato preto brilhoso e estiloso!",
             preco="212,99",
             categoria=cat2.nome,
             imagem="")

session.add(item4)
session.commit()

item5 = Item(usuario_id=1,
             nome="Sapato Azul",
             descricao="Uma maravilhoso sapato azul que vai te fazer ficar lindo!",
             preco="199,99",
             categoria=cat2.nome,
             imagem="")

session.add(item5)
session.commit()

item6 = Item(usuario_id=1,
             nome="Sapatenis Rosa",
             descricao="Uma grande Sapatenis rosa que vai te fazer ficar explendido!",
             preco="175,99",
             categoria=cat2.nome,
             imagem="")

session.add(item6)
session.commit()



item4 = Item(usuario_id=1,
             nome="Havaiana Estampada",
             descricao="Uma Havaiana vermelha estampada que vai te fazer ficar show!",
             preco="21,99",
             categoria=cat3.nome,
             imagem="")

session.add(item4)
session.commit()

item5 = Item(usuario_id=1,
             nome="Havaiana Azul",
             descricao="Uma Havaiana azul que vai te fazer ficar legal!",
             preco="19,99",
             categoria=cat3.nome,
             imagem="")

session.add(item5)
session.commit()

item6 = Item(usuario_id=1,
             nome="Havaiana Rosa",
             descricao="Uma maravilhosa Havaiana rosa que vai te fazer ficar lindo!",
             preco="17,99",
             categoria=cat3.nome,
             imagem="")

session.add(item6)
session.commit()



item5 = Item(usuario_id=1,
             nome="Cinto Azul",
             descricao="Uma Cinto azul para terno!",
             preco="129,99",
             categoria=cat4.nome,
             imagem="")

session.add(item5)
session.commit()

item6 = Item(usuario_id=1,
             nome="Cinto Preto",
             descricao="Um classico cinto preto que combina com tudo!",
             preco="174,99",
             categoria=cat4.nome,
             imagem="")

session.add(item6)
session.commit()



item6 = Item(usuario_id=1,
             nome="Meias Rosa",
             descricao="Uma maravilhosa Meia rosa que vai te fazer ficar lindo!",
             preco="11,99",
             categoria=cat5.nome,
             imagem="")

session.add(item6)
session.commit()

item5 = Item(usuario_id=1,
             nome="Meias Azuis",
             descricao="Uma Meia azul para terno!",
             preco="19,99",
             categoria=cat5.nome,
             imagem="")

session.add(item5)
session.commit()

item6 = Item(usuario_id=1,
             nome="Meias Pretas",
             descricao="Um classico que combina com tudo!",
             preco="14,99",
             categoria=cat5.nome,
             imagem="")

session.add(item6)
session.commit()
