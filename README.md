# shortest_route
O objetivo deste projeto é o cálculo de menor rota do grafo para a análise de melhor custo de uma transportadora.

## Utilitários

###Linguagem utilizada
Python versão 3.5.6

###Frameworks utilizados
Django versão 2.0.6 
<br>
Django Rest Framework
<br>
Unittest

###Bibliotecas utilizadas
Os frameworks e bibliotecas foram instalados utilizando o PIP (gerenciador de dependências do Python).

###Ferramentas de auxílio
PyCharm: IDE utilizada para auxiliar o desenvolvimento do código.
<br>
Cacoo: utilizado para desenhar rascunhos e diagramas simples.

## Sobre a proposta (análise inicial)
O problema proposto envolve o cálculo de rotas para uma transportadora reduzir seu custo. 
Esse tema é conhecido como problema do caminho mínimo, na qual por meio de grafos temos os pontos de origem e destino 
(representado pelos vértices/nós) e arestas que representam o valor.
<br>

##Rascunhos e Diagramas
Os diagramas de classe e de caso de uso deste projeto podem ser encontrados por meio do link: 
https://cacoo.com/diagrams/xHm9XwjKjV4ZlTnd 

##Classes Utilizadas
<b>Class FileMap</b>
<br>
Dentro dessa classe, estão implementadas as funções responsáveis por manipular e validar o arquivo de mapas e armazenar 
seu registo no banco.
<br>

<b>Class Map</b>
<br>
Dentro dessa classe, estão implementadas as funções responsáveis por salvar todo o conteúdo de mapa recebido no 
banco de dados.
<br>

<b>Class Route</b>
<br>
Dentro dessa classe, estão implementadas as funções responsáveis por salvar o resultado do cálculo de menor rota em no
banco de dados, sendo utilizado como cache.
<br>

<b>Class Graph</b>
<br>
Nessa classe, as funções recebem os dados para estruturar o modelo de grafo a ser utilizado no cálculo de menor rota.
<br>

<b>Class TestShortestRoute</b>
<br>
Nessa classe, foram implementados todos os testes unitários do projeto.
<br>

<b>Views</b>
<br>
Foram implementadas algumas classes para interface da framework REST.
<br>
As solicitações passadas para os métodos do manipulador são instâncias de solicitação do framework REST.

## Solução implementada
A ideia da solução implementada é receber arquivos de mapa no formato pré definido, validar este formato e armazenar o 
mesmo em uma pasta de upload, além de armazenar seu conteúdo no banco de dados (classe fileMap e Map).
<br>
Para a solução do problema de menor caminho foi baseada na ideia de que o grafo (mapa) é bidirecional, ou seja, o valor 
de A->B é o mesmo que de B->A
Um dos algoritmos conhecidos para solucionar este problema é o algoritmo de Dijkstra, sendo esta a solução adaptada e 
utilizada  para este desafio.
O algoritmo foi adaptado para as nossas necessidades, sendo desde adaptações consméticas para o melhor entendimento e 
também adaptações no conteúdo e forma de retorno da função.
<br>
Algumas regras e decisões foram implementadas, como em caso de ter mais de um valor representando 2 pontos no mapa usar
sempre o menor valor (e sempre salvar o menor no banco de dados)
<br>
A abordagem utilizada implementa as idéias de cache e de cálculo dinâmico, onde o sistema recebe uma requisição de 
consulta do usuário ele procura se existe essa requisição já registrada no model Route, se já existe ele retorna esse 
resultado, senão ele calcula a rota e armazena a rota calculada no banco.
<br>
Além da API de recebimento de arquivos no formato de mapa foi implementada a mesma solução para recebimento de JSON, 
permitindo que o formato de entrada seja escolhido pelo usuário.

## Guia de execução
Para criar o ambiente e instalar os registros necessários de banco de dados deverá ser executado o seguinte comando:

> pipenv install 
<br>
> python manage.py migrate
<br>
#
Para a execução dos testes unitários implementados é necessário executar o seguinte comando:
<br>
> python manage.py test
#
Para criar o mapa deve ser acessado: <b>http://127.0.0.1:8000/api/map/</b>, onde será requisitado por método POST o 
arquivo e o nome a ser atribuído a ele.
Ainda com relação à API do arquivo de mapas é possível realizar GET, POST e DELETE de um arquivo específico passando o 
id do mapa salvo como parâmetro, por exemplo: <b>http://127.0.0.1:8000/api/map/ID</b>
<br>
Para listar todas as entradas da tabela Map (todas as origens, destinos e valores de cada mapa registrado) é necessário
acessar <b>http://127.0.0.1:8000/api/points/</b>
<br>
Para solicitar um cálculo de rota é necessário acessar:
<b>
http://127.0.0.1:8000/api/shortest_route/<nome do mapa\>/<ponto de origem\>/<ponto de destino\>/<autonomia do carro\>/<valor do combustível\>/
</b>

## Testes
Os testes unitários foram realizados e podem ser encontrados na pasta tests, arquivo <i>test_shortest_route.py</i>.
Devido a dificuldade encontrada para utilizar testes uniários no arquivo de mapas, abordagem inicial do projeto, foi 
criada a alternativa por JSON, na qual os testes também podem ser encontrados no arquivo de testes.
Para realizar testes utilizando o arquivo deve ser acessada a interface de API, alguns arquivos de teste encontram-se na
pasta <b>tests</b>
### Formato esperado
O arquivo de texto deve ter como conteúdo duas strings e um número, cada um destes separado por espaço.
O JSON esperado possui o seguinte formato:
> {
    "name": "nome do mapa",<br>
    "map": [<br>
        {"first_edge": "A", <br>
          "second_edge": "B", <br>
          "value": 10},<br>
        [...]<br>
    ]<br>
}

## Outras possíveis soluções e observações
Dependendo do requisito da empresa de logistica poderiam ser realizadas diferentes abordagens.
<br>
Um exemplo seria fazer o carregamento do arquivo seguido do processamento de todos os caminhos de origem-destino e 
armazenar no banco de dados, assim dispensaria a chamada de cálculo do menor caminho a cada solicitação, substituindo 
por uma requisição ao banco de dados.
<br>
Outra solução seria o oposto da acima citada, ou seja, realizar o cálculo a cada requisição, porém quando forem 
realizadas consultas anteriormente processadas o cálculo seria refeito da mesma maneira, sem um cache para consulta.
<br>
Com relação à malha de rotas, no caso de rotas passadas por arquivos não existe uma necessidade de armazenar a 
informação do arquivo no banco (fileMap), visto que o mapa todo foi salvo no Map, a escolha de salvar essas informações 
foi devido a possibilidade de recuperar o historico e dados do arquivo.
<br>
Não foi implementado token para controle de acesso, mas seria uma melhoria interessante boa para o projeto.
<br>
Outra sugestão de melhoria que poderia ser implementada seria a utilização de UUID no lugar do ID incremental utilizado.
<br> 
Para a implementação do cálculo de menor caminho tratar de caminhos unidirecionais é necessário realizar  modificações 
no arquivo Graph.py, retirando as duas ultimas linhas que representam a aresta no caminho inverso.
Sendo assim, poderia inclusive implementar uma solução mista onde um é passado um parâmetro na chamada que defini se 
deve ser considerado caminho uni ou bidirecional.