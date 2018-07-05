# Projeto 5 - Configuração do Servidor Linux
## Udacity - Full Stack Web

Feito por Guilherme Sanches para o Udacity [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004)

### Sobre

Este é um projeto de aplicativo Web RESTful que usa a estrutura Flask do Python, acessando um banco de dados PostgreSQL para apresentar um catálogo que pode armazenar informações sobre itens e as categorias às quais eles pertencem. A autenticação e autorização OAuth2 é usada para permitir que os usuários acessem as operações CRUD (criar, ler, atualizar e excluir). Os usuários que fizeram login em uma Conta do Google podem visualizar informações sobre itens e categorias, adicionar novos itens e editar e excluir apenas os itens criados por eles.

### Recursos
- apache2
- flask
- pip
- sqlalchemy
- PostgreSQL
- mod-wsgi

### Neste Repositório

O projeto consiste em um módulo principal do Python (projeto.py) que executa o aplicativo da web Flask. Um banco de dados PostgreSQL é criado e preenchido com as tabelas necessárias durante o provisionamento do Vagrant usando bancodedados_setup.py. O aplicativo usa os modelos HTML armazenados na pasta de modelos para gerar as páginas da web visíveis pelo usuário. Arquivos CSS e imagens estáticas são armazenados na pasta estática.

### Portas
- 2200
- 80
- 123

### Informações para acessar o projeto

Para conectar no seu terminal (ssh grader@52.90.183.40 -p 2200 -i chave-privada). Vou enviar a chave privada nas nota e a senha a ser utilizada será 190692.
#### Resumo
- Senha (password): 190692
- IP: 52.90.183.40
- Porta SSH: 2200
- URL: http://ec2-52-90-183-40.compute-1.amazonaws.com/

# Alterações de configuração
## Configuração do Firewall (UFW)
Eu decidi começar o projeto pela configuração do ufw. Portanto, se eu fosse bloqueado do servidor, isso aconteceria no começo.

Por padrão, bloqueie todas as conexões de entrada em todas as portas:

`sudo ufw default deny incoming`

Permitir conexão de saída em todas as portas:

`sudo ufw default allow outgoing`

Permitir conexão de entrada para SSH na porta 2200:

`sudo ufw allow 2200/tcp`

Permitir conexões de entrada para SSH na porta 22 (bloquear as conexões na porta 22 após a porta ter sido alterada no arquivo sshd_config (próximo passo):
`sudo ufw allow 22`

Permitir conexões de entrada para HTTP na porta 80:

`sudo ufw allow www`

Permitir conexão de entrada para NTP na porta 123:

`sudo ufw allow ntp`

Para verificar as regras que foram adicionadas antes de ativar o uso do firewall:

`sudo ufw show added`

Para habilitar o firewall, use:

`sudo ufw enable`

Para verificar o status do firewall, use:

`sudo ufw status`

## Alterar porta SSH de 22 para 2200
Edite o arquivo `/ etc / ssh / sshd_config` e mude a linha` Port 22` para:

`Port 2200`

## Bloqueando a conexão para a porta 22
[Começando com o UFW] (https://www.howtoforge.com/tutorial/ufw-uncomplicated-firewall-on-ubuntu-15-04/)

`ufw deny 22`

Para verificar se as regras foram alteradas:

`sudo ufw show added`

Em seguida, reinicie o serviço SSH:

`sudo service ssh restart`
Agora, quando a porta 22 está fechada, eu sempre preciso do SSH para minha instância como um usuário remoto.

## Atualiza todos os pacotes atualmente instalados

`apt-get update` - para atualizar os package indexes

`apt-get upgrade` - tpara realmente atualizar os packages instalados

Se no login a mensagem `*** System restart required ***` for exibida, execute o seguinte comando 
para reinicializar a máquina:

`reboot`


## Adicionando o usuário grader
Adicione o `grader` com o comando: `useradd -m -s grader`

## Adicionando o privilegio ao usuario grader
Para adicionar os privilegios do sudo ao usuario grader:
```
usermod -aG sudo grader
```
Edite o arquivo sudoers:
Procure a linha
`root ALL=(ALL:ALL) ALL`
e adicione 
`grader LL=(ALL:ALL) ALL`

## Configurar as chaves SSH para o usuário
Como usuário root:
```
mkdir /home/grader/.ssh
chown grader:grader /home/grader/.ssh
chmod 700 /home/grader/.ssh
cp /root/.ssh/authorized_keys /home/grader/.ssh/
chown grader:grader /home/grader/.ssh/authorized_keys
chmod 644 /home/grader/.ssh/authorized_keys
```

Agora pode logar como o usuário `grader` usando o comando:
`ssh -i ~/.ssh/graderUdacity grader@35.157.67.119 -p 2200`

## Disabilitando o login root
Altere a seguinte linha no arquivo `/etc/ssh/sshd_config`:

De `PermitRootLogin without-password` para `PermitRootLogin no`.

Além disso, descomente a seguinte linha para ler:
```
PasswordAuthentication no
```

Faça `service ssh restart` para que as mudanças entrem em vigor.

Agora fará todos os comandos usando o usuário `grader`, usando` sudo` quando necessário.

## Alterar o fuso horário para UTC
Verifique o fuso horário com o comando `date`. Isso exibirá o fuso horário atual após o horário.
Se não é UTC, mude assim:

`sudo timedatectl set-timezone UTC`

## Instale o Apache para servir um aplicativo mod_wsgi em Python
Instale o Apache:

`sudo apt-get install apache2`

Instale o pacote `libapache2-mod-wsgi`:

`sudo apt-get install libapache2-mod-wsgi`

## Instlando e configurando o PostgreSQL
Instale PostgreSQL com:

`sudo apt-get install postgresql postgresql-contrib`

Para garantir que conexões remotas com o PostgreSQL não sejam permitidas, verifique se o arquivo de configuração `/etc/postgresql/9.5cd/main/pg_hba.conf` somente permitia conexões dos endereços de host locais` 127.0.0.1` para IPv4 e `:: 1` para IPv6.

Crie um usuário do PostgreSQL chamado `catalogo` com:

`sudo -u postgres createuser -P catalogo`

Você é solicitado a fornecer uma senha. Isso cria um usuário normal que não pode criar
bancos de dados, funções (usuários).

Crie um banco de dados vazio chamado `catalogo` com:

`sudo -u postgres createdb -O catalogo catalogo`

## Instalando os pacotes: Flask e SQLAlchemy
Emita os seguintes comandos:

```
sudo apt-get install python-psycopg2 python-flask
sudo apt-get install python-sqlalchemy python-pip
sudo pip install --upgrade pip
sudo pip install oauth2client
sudo pip install requests
sudo pip install httplib2 

```

## Instalando o Git
`sudo apt-get install git`

## Configurar e ativar o Apache2 para servir seu aplicativo
Para servir o aplicativo de catálogo usando o servidor da web Apache2, você precisa criar um arquivo de configuração do host virtual.

`sudo nano /etc/apache2/sites-available/catalogo.conf`

Estes são os conteúdos:

```
<VirtualHost *:80>
        # The ServerName directive sets the request scheme, hostname and port that
        # the server uses to identify itself. This is used when creating
        # redirection URLs. In the context of virtual hosts, the ServerName
        # specifies what hostname must appear in the request's Host: header to
        # match this virtual host. For the default virtual host (this file) this
        # value is not decisive as it is used as a last resort host regardless.
        # However, you must set it for any further virtual host explicitly.
        ServerName www.example.com
        WSGIScriptAlias / /var/www/Catalogo/app.wsgi
        WSGIDaemonProcess projeto.py
        <Directory /var/www/Catalogo>
                WSGIProcessGroup projeto.py
                WSGIApplicationGroup %{GLOBAL}
                        Order deny,allow
                        Allow from all
        </Directory>

        # ServerAdmin webmaster@localhost
        # DocumentRoot /var/www/Catalogo/

        # Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
        # error, crit, alert, emerg.
        # It is also possible to configure the loglevel for particular
        # modules, e.g.
        #LogLevel info ssl:warn

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined

        # For most configuration files from conf-available/, which are
        # enabled or disabled at a global level, it is possible to
        # include a line for only one particular virtual host. For example the
        # following line enables the CGI configuration for this host only
        # after it has been globally disabled with "a2disconf".
        #Include conf-available/serve-cgi-bin.conf
</VirtualHost>
```

#### Reinicie o Apache
`sudo service apache2 restart`

## Referências
- [Ask Ubuntu](https://askubuntu.com/)
- [Docs do PosgreSQL](https://www.postgresql.org/docs/)
- [Apache Docs](https://httpd.apache.org/docs/2.4/)
- [Como instalar e usar o PostgreSQL no Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04)
- O Stackoverflow e o Readme de outros alunos FSND no Github também foram úteis em momentos de necessidade.
