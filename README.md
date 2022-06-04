# Desafio Técnico Geofusion - Engenheiro de Machine Learning
## Como rodar a aplicação:
É possivel rodar o app diretamente pelo arquivo main.py ou usando Docker
### Rodando com Docker:
(É necessario ter o Docker na sua maquina!)
Primeiro, é necessario criar a imagem Docker. Vá até o diretorio do projeto e execute esse comando:
```
docker build --tag geofusion .
```
Agora a imagem já está salva na maquina local e você pode roda-la com esse comando:
```
docker run --publish 80:80  geofusion
```
Ao rodar o comando, poderá ver os logs da aplicação e o app já esta ativo na porta 80 da sua máquina. É possivel acessar nesse link: http://localhost
