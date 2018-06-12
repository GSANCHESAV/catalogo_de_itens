from flask import Flask, render_template, request, redirect, url_for, flash
from flask import make_response, jsonify
from flask import session as login_session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bancodedados_setup import Base, Categoria, Item, Usuario

import random
import httplib2
import json
import requests
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError


app = Flask(__name__)

# Declara o Client ID fazendo referencia ao arquivo client_secrets.json
CLIENT_ID = json.loads(open(
                            'client_secrets.json', 'r'
                            ).read())['web']['client_id']
# Nome do Aplicativo registrado no Google Dev
APPLICATION_NAME = "Catalogo Itens App"


engine = create_engine('sqlite:///catalogodeitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# #### Login Google #### #

# Create anti-forgery state token
@app.route('/login/')
def exibirLogin():
    # Cria uma mistura randomica de digitos e letras usada para
    # identificar a sessão gerada
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Parametro STATE invalido'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    print(code)

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
                                 'Falha na atuali. do código de autorização.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Tokens client ID does not match apps.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
                                 'Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    usuario_id = getUsuarioID(login_session['email'])
    if not usuario_id:
        usuario_id = criarUsuario(login_session)
    login_session['user_id'] = usuario_id

    output = ''
    output += '<h1>Bem-vindo, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ''' " style = "width: 300px; height: 300px;border-radius: 150px;
                -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    flash("Você está Logado como %s" % login_session['username'])
    print("done!")
    return output


@app.route('/gdisconnect')
def gdisconnect():
    # Limpa o cache
    login_session.clear()
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Usuario nao conectado.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == 200:
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Desconectado com Sucesso.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps(
                                'Failed to revoke token for given user.',
                                400))
        response.headers['Content-Type'] = 'application/json'
        return response


# #### Funções de Auxilio #### #

def criarUsuario(login_session):
    novoUsuario = Usuario(nome=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(novoUsuario)
    session.commit()
    usuario = session.query(Usuario).filter_by(
                                               email=login_session['email']
                                              ).one()
    return usuario.id


def getUsuarioInfo(usuario_id):
    print(usuario_id)
    usuario = session.query(Usuario).filter_by(id=usuario_id).one()
    print(usuario)
    return usuario


def getUsuarioID(email):
    try:
        usuario = session.query(Usuario).filter_by(email=email).one()
        return usuario.id
    except:
        return None

# #### Paginas Pricipais #### #


@app.route('/')
@app.route('/catalogo/')
def exibirCatalogo():
    categorias = session.query(Categoria)
    itens = session.query(Item)

    if 'username' not in login_session:
        return render_template('home_publico.html',
                               categorias=categorias,
                               itens=itens)
    else:
        return render_template('home.html',
                               categorias=categorias,
                               itens=itens)


@app.route('/meucatalogo/')
def exibirCatalogoUsuario():
    categorias = session.query(Categoria)
    itens = session.query(Item).filter_by(usuario_id=login_session['user_id'])

    if 'username' not in login_session:
        return render_template('home_publico.html',
                               categorias=categorias,
                               itens=itens)
    else:
        return render_template('home_usuario.html',
                               categorias=categorias,
                               itens=itens)


@app.route('/catalogo/<categoria_nome>/itens/')
def exibirCategoria(categoria_nome):

    categorias = session.query(Categoria)
    categoria = session.query(Categoria).filter_by(nome=categoria_nome).one()
    itens = session.query(Item).filter_by(categoria=categoria.nome)

    if 'username' not in login_session:
        return render_template('categoria_publico.html',
                               categorias=categorias,
                               categoria=categoria,
                               itens=itens)
    else:
        return render_template('categoria.html',
                               categorias=categorias,
                               categoria=categoria,
                               itens=itens)


@app.route('/meucatalogo/<categoria_nome>/itens/')
def exibirCategoriaUsuario(categoria_nome):

    categorias = session.query(Categoria)
    categoria = session.query(Categoria).filter_by(nome=categoria_nome).one()
    itens = session.query(Item).filter_by(
                                          categoria=categoria.nome).filter_by(
                                          usuario_id=login_session['user_id'])

    if 'username' not in login_session:
        return render_template('categoria_publico.html',
                               categorias=categorias,
                               categoria=categoria,
                               itens=itens)
    else:
        return render_template('categoria_usuario.html',
                               categorias=categorias,
                               categoria=categoria,
                               itens=itens)

# #### Adiciona/Edita/Deleta #### #


@app.route('/catalogo/<categoria_nome>/itens/<int:item_id>/')
def exibirItem(categoria_nome, item_id):

    categoria = session.query(Categoria).filter_by(nome=categoria_nome).one()
    item = session.query(Item).filter_by(id=item_id).one()
    print(item)
    criador = getUsuarioInfo(item.usuario_id)

    if 'username' not in login_session or criador.id != login_session['user_id']:
        return render_template('item_publico.html',
                               categoria=categoria,
                               item=item,
                               criador=criador)
    else:
        return render_template('item.html',
                               categoria=categoria,
                               item=item,
                               criador=criador)


@app.route('/catalogo/<categoria_nome>/novo/', methods=['GET', 'POST'])
def novoItem(categoria_nome):
    if 'username' not in login_session:
        return redirect('/login')

    categorias = session.query(Categoria)
    categoria = session.query(Categoria).filter_by(nome=categoria_nome).one()

    if request.method == 'POST':
        novoItem = Item(nome=request.form['nome'],
                        descricao=request.form['descricao'],
                        categoria=request.form['categoria'],
                        preco=request.form['preco'],
                        usuario_id=login_session['user_id'],
                        )

        session.add(novoItem)
        session.commit()

        # Envia uma mensagem informando que o pruduto foi editado com sucesso
        flash("%s Adicionado com Sucesso!" % novoItem.nome)

        return redirect(url_for('exibirCategoriaUsuario',
                                categoria_nome=novoItem.categoria))
    else:
        return render_template('novoitem.html',
                               categoria_nome=categoria_nome,
                               categorias=categorias)


@app.route('/catalogo/<categoria_nome>/<int:item_id>/editar/',
           methods=['GET', 'POST'])
def editarItem(categoria_nome, item_id):
    categorias = session.query(Categoria)
    itemEditado = session.query(Item).filter_by(id=item_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if itemEditado.usuario_id != login_session['user_id']:
        return("""<script>function naoEditar(){alert('Você não está autorizado
               a Editar esse Item. Só é possivel editar itens criados pelo seu
               usuario'); window.location='http://localhost:8000/catalogo/'}
               </script><body onload=naoEditar()>""")

    if request.method == 'POST':
        # Coloca o valor digitado/selecionado no input dentro de uma variavel
        nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        preco = request.form['preco']

        if nome and categoria and descricao and preco:
            # Se todos os itens tiverem valor dentro ele faz a alteração
            itemEditado.nome = nome
            itemEditado.categoria = categoria
            itemEditado.descricao = descricao
            itemEditado.preco = preco

        # Envia uma mensagem informando que o pruduto foi editado com sucesso
        flash("%s Editado com Sucesso!" % itemEditado.nome)

        session.add(itemEditado)
        session.commit()

        return redirect(url_for('exibirCategoriaUsuario',
                                categoria_nome=itemEditado.categoria))
    else:
        return render_template('editaritem.html',
                               categorias=categorias,
                               categoria_nome=categoria_nome,
                               item_id=item_id,
                               item=itemEditado,
                               )


@app.route('/catalogo/<categoria_nome>/<int:item_id>/deletar/',
           methods=['GET', 'POST'])
def deletarItem(categoria_nome, item_id):
    categoria = session.query(Categoria).filter_by(nome=categoria_nome).one()
    itemDeletado = session.query(Item).filter_by(id=item_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    if itemDeletado.usuario_id != login_session['user_id']:
        return("""<script>function naoDeletar(){alert('Você não está autorizado
               a deletar esse Item. Só é possivel deletar itens criados pelo
               seu usuario'); window.location='http://localhost:8000/catalogo/'
               }</script><body onload=naoDeletar()>""")

    if request.method == 'POST':
        session.delete(itemDeletado)
        session.commit()

        # Envia uma mensagem informando que o pruduto foi excluido com sucesso
        flash("Produto Excluido com Sucesso!")

        return redirect(url_for('exibirCatalogoUsuario',
                                categoria_nome=categoria.nome))
    else:
        return render_template('deletaritem.html',
                               categoria_nome=categoria_nome,
                               item_id=item_id,
                               item=itemDeletado
                               )

# #### API's - end points #### #


@app.route('/catalogo/<categoria_nome>/itens/JSON/')
def itensCategoriaJSON(categoria_nome):

    itensCategoria = session.query(Item).filter_by(
                                                   categoria=categoria_nome
                                                  ).all()

    return jsonify(ItensCategoria=[i.serialize for i in itensCategoria])


# Criando um endpoint da API (solicitação GET)
@app.route('/catalogo/<categoria_nome>/itens/<int:item_id>/JSON/')
def itemMenuJSON(categoria_nome, item_id):

    # Verificar os Id's de entrada porque senão dá erro
    item = session.query(Item).filter_by(
                                         categoria=categoria_nome).filter_by(
                                         id=item_id).one()

    return jsonify(ItemMenu=item.serialize)


if __name__ == '__main__':
    # chave secreta que o flask usará para criar as sessões dos usuários.
    # Sem ele as mensagens utilizando 'flash'não funcionam
    app.secret_key = 'super_secret_key'
    # modo de dubug ativado, atualiza sempre que for salvo cód. editado
    app.debug = True
    # Roda o app no localhost vago e na porta indicada.
    app.run(host='0.0.0.0', port=8000)
