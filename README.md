# Projeto 3 - Catálogo de Itens
### Udacity - Full Stack - Projeto - Catálogo de Itens

Feito por Guilherme Sanches para o Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### Sobre

Este é um projeto de aplicativo Web RESTful que usa a estrutura Flask do Python, acessando um banco de dados PostgreSQL para apresentar um catálogo que pode armazenar informações sobre itens e as categorias às quais eles pertencem. A autenticação e autorização OAuth2 é usada para permitir que os usuários acessem as operações CRUD (criar, ler, atualizar e excluir). Os usuários que fizeram login em uma Conta do Google podem visualizar informações sobre itens e categorias, adicionar novos itens e editar e excluir apenas os itens criados por eles.

### Neste Repositório

O projeto consiste em um módulo principal do Python (projeto.py) que executa o aplicativo da web Flask. Um banco de dados PostgreSQL é criado e preenchido com as tabelas necessárias durante o provisionamento do Vagrant usando bancodedados_setup.py. O aplicativo usa os modelos HTML armazenados na pasta de modelos para gerar as páginas da web visíveis pelo usuário. Arquivos CSS e imagens estáticas são armazenados na pasta estática.

### O que foi usado nesse projeto?

**Pre-requisitos**

* A versão mais recente do [Vagrant] (https://www.vagrantup.com/downloads.html)
para sua plataforma preferida.
* Os arquivos contidos neste repositório

Uma lista detalhada dos módulos do Python instalados durante o provisionamento da nossa máquina virtual Vagrant pode ser encontrada no arquivo `requisitos.txt`.

**Rodando e testando este projeto**

A partir de uma linha de comando, mude para o diretório CatalogoItems onde está este projeto. (Para este exemplo, vamos assumir que está em /home/user/CatalogoItems)

`cd /home/user/CatalogoItems`

A partir deste diretório, vamos executar o nosso Vagrantfile, que irá criar e provisionar as máquinas virtuais necessárias para executar este projeto.

`vagrant up`

Agora que o Vagrantfile e o arquivo de configuração correspondente concluíram o provisionamento de nossa máquina virtual, temos um ambiente Ubuntu configurado para executar o projeto Catálogo de Itens. Todos os pacotes necessários foram instalados e a porta 8000 (a porta usada por este projeto) foi encaminhada corretamente.


A segunda máquina virtual é um servidor PostgreSQL totalmente operacional com um backup SQL carregado. Esse backup é copiado do script `inserecateprod.py`, que carrega o banco de dados com dados de amostra a serem usados pelo aplicativo.

Voltando nossa atenção para um navegador da web, podemos navegar para `http://localhost:8000/` e ver o aplicativo da web funcionando corretamente. Podemos ver categorias e seus itens associados e acessar informações formatadas em JSON também.


**Como configurar o acesso ao Google OAuth 2.0**

Embora um tutorial detalhado para a configuração de credenciais do OAuth esteja fora do escopo deste projeto, informações detalhadas podem ser encontradas em [Guias do Google Identity Platform (https://developers.google.com/identity/protocols/OAuth2?hl=pt-BR) .
Depois de criar um novo projeto por meio do Google Developers Console, podemos adicionar novas credenciais do "OAuth 2.0 client ID". Nosso tipo de aplicativo é um 'aplicativo da Web'. 'Origens de JavaScript autorizadas' são `http://localhost:8000` e 'URIs de redirecionamento autorizados' são `http://localhost:8000/oauth2callback`. Agora podemos baixar um arquivo JSON desta informação, renomeá-lo para `client_secrets.json` e mover este arquivo para a raiz do nosso projeto (`/CatalogoItems/`).

Agora que atualizamos o projeto Catálogo de itens com as credenciais OAuth 2.0 do Google, a funcionalidade completa de adicionar, editar e excluir itens e categorias pode ser usada. Itens podem ser criados por qualquer usuário logado, e os usuários podem editar e excluir quaisquer objetos que tenham criado.
