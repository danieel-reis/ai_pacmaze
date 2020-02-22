# Resolvedor do N-puzzle utilizando Inteligência Artificial

## Execução e testes

Segue um exemplo:

Estado inicial:
```
[8 6 7]
[2 5 4]
[3 0 1]
```

Estado objetivo:
```
[1 2 3]
[4 5 6]
[7 8 0]
```

Observe abaixo como executar o código:
```
python3 tp_ia_daniel_reis.py dim_x dim_y estado_inicial estado_final algoritmo name_save
python3 tp_ia_daniel_reis.py 3 3 [[8,6,7],[2,5,4],[3,0,1]] [[1,2,3],[4,5,6],[7,8,0]] 0 31
```

Em que:
* dim_x e dim_y remetem ao tamanho da matriz;
* estado_inicial remete aos valores da matriz inicial;
* estado_final remete aos valores da matriz objetivo;
* algoritmo se refere ao algoritmo escolhido para executar, como descrito logo abaixo;
* name_save se refere ao nome do arquivo a ser salvo com a solução do problema obtida pelo(s) algoritmo(s) executado(s).

Descreve-se os parâmetros do algoritmo:
* 0 - Executar todos os algoritmos;
* 1 - Executar apenas o Breadth First Search;
* 2 - Executar apenas o Uniform Cost Search;
* 3 - Executar apenas o Iterative Deepening Search;
* 4 - Executar apenas o A Star Search Heuristic 1;
* 5 - Executar apenas o A Star Search Heuristic 2;
* 6 - Executar apenas o Greedy Best First Search Heuristic 1;
* 7 - Executar apenas o Greedy Best First Search Heuristic 2;
* 8 - Executar apenas o Hill Climbing Search Heuristic 1;
* 9 - Executar apenas o Hill Climbing Search Heuristic 2.
