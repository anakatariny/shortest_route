# shortest_route
O objetivo deste projeto é o cálculo de menor rota do grafo para a análise de melhor custo de uma transportadora.

## Utilitários

###Linguagem utilizada
Python versão 3.5.6

###Frameworks utilizados
Django versão 2.0.6 
<br>
Django Rest Framework

###Bibliotecas utilizadas
Os frameworks e bibliotecas foram instalados utilizando o PIP (gerenciador de dependencias do Python).

###Ferramentas de auxílio
PyCharm: IDE utilizada para auxiliar o desenvolvimento do código.
<br>
Cacoo: utilizado para desenhar rascunhos e diagramas simples.

## Sobre a proposta (análise inicial)
O problema proposto envolve o cálculo de rotas para uma transportadora reduzir seu custo. 
Esse tema é conhecido como problema do caminho mínimo, na qual por meio de grafos temos os pontos de origem e destino (representado pelos vértices/nós) e arestas que representam o valor.
<br>
Um dos algoritmos conhecidos para solucionar este problema é o algoritmo de Dijkstra, sendo esta a solução utilizada para este desafio.

##Rascunhos e Diagramas
Alguns rascunhos deste projeto podem ser encontrados por meio do link: https://cacoo.com/diagrams/xHm9XwjKjV4ZlTnd 

##Classes Utilizadas


##API Rest
Foi implementado uma API Rest utilizando o Django Rest Framework.
<br>
Mais descrições sobre o desenvolvimento da API em breve.


## Solução implementada
A ideia da solução implementada é receber arquivos de mapa no formato pré definido, validar este formato e armazenar o mesmo em uma pasta de upload, além de armazenar seu conteúdo no banco de dados (classe fileMap e Map).
<br>
Quando o sistema recebe uma requisição de consulta do usuário ele procura se existe essa requisição já registrada no model Route, se já existe ele retorna esse resultado, senão ele calcula a rota e armazena a rota calculada no banco.


## Guia de execução

## Testes

## Outras possíveis soluções e sugestões
Dependendo do requisito da empresa de logistica poderiam ser realizadas diferentes abordagens.
<br>
Um exemplo seria fazer o carregamento do arquivo seguido do processamento de todos os caminhos de origem-destino e armazenar no banco de dados, assim dispensaria a chamada de cálculo do menor caminho a cada solicitação, substituindo por uma requisição ao banco de dados.
<br>
Outra solução seria o oposto da acima citada, ou seja, realizar o cálculo a cada requisição, porém quando forem realizadas consultas anteriormente processadas o cálculo seria refeito da mesma maneira, sem um cache para consulta.
<br>
Com relação à malha de rotas, no caso de rotas passadas por arquivos não existe uma necessidade de armazenar a informação do arquivo no banco (fileMap), visto que o mapa todo foi salvo no Map, a escolha de salvar essas informações foi devido a possibilidade de recuperar o historico e dados do arquivo.
