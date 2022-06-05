# Desafio Técnico Geofusion - Engenheiro de Machine Learning
## Como rodar a aplicação:
É possivel rodar o app diretamente pelo arquivo main.py ou usando Docker

### Rodando localmente:
(É necessario ter o Python/Pip na sua maquina!)\
Primeiro, é necessario baixar as dependências. Vá ao diretorio do projeto e execute o comando:
```
pip install -r requirements.txt
```
Após baixar as dependências, vá ao diretorio do projeto e rode o arquivo main.py:
```
python app/main.py
```
Ao rodar o comando, poderá ver os logs da aplicação e o app já esta ativo na porta 80 da sua máquina.\
É possivel acessar nesse link: http://localhost:8000

### Rodando com Docker:
(É necessario ter o Docker na sua maquina, e alterar imports de dependências locais (checar #1))\
Primeiro, é necessario criar a imagem Docker. Vá até o diretorio do projeto e execute o comando:
```
docker build --tag geofusion .
```
Agora a imagem já está salva na maquina local e você pode roda-la com o comando:
```
docker run --publish 80:80  geofusion
```
Ao rodar o comando, poderá ver os logs da aplicação e o app já esta ativo na porta 80 da sua máquina.\
É possivel acessar nesse link: http://localhost

#1 - Colocar um ponto na frente dos imports locais no arquivo main.py, como apresentado abaixo:
![image](https://user-images.githubusercontent.com/38021205/172028229-bde4166f-e508-49c2-8d6e-b3babd201b5f.png)


## Na aplicação:
É possivel acessar a documentação da API no path /docs (http://localhost:8000/docs) e testar diretamente as funções.

## Rodar testes:
Vá ao diretório do projeto e execute o comando:
```
python -m unittest discover ./app
```

## Decições técnicas
Decidi fazer a API em FastAPI por ser levemente mais simples e, principalmente, por gerar documentação automaticamente com base nas docstrings.\
Quanto a organização do diretório do projeto, a aplicação inteira está dentro da pasta app devido ao Docker utilizado exigir que seja colocado em uma pasta app.\
As pastas dentro de /app estão organizados quanto a suas funções:
- core: Pasta utilizada para colocar informações importantes da aplicação (como configuração de ambiente)
- middleware: Pasta utilizada para funções "secundarias" que normalmente fazem verificações/formatações nos Controllers
- services: Pasta utilizada para funções "principais" no Controller, tentando abstrair funcionalidades dos Controllers e colocando nos services. Tambem é utilizada para consultar APIs externas
- requirements: Pasta responsavel por armazenar arquivos necessarios para aplicação
