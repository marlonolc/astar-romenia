# astar-romenia

Busca A* de Arad a Bucareste (Russell & Norvig, cap. 3),
feita em 6 fases na disciplina IIA-008 Inteligência Artificial I.

Aluno(a): Marlon Oliveira Costa

## Como rodar

Certifique-se de ter o Python 3 instalado. No terminal, dentro da pasta do repositório, execute o programa principal:

```bash
python a_estrela.py
```

Para executar as fases intermediárias ou os desafios individualmente:

```bash
python fase1_explorar.py
python fase2_caminhos.py
python fase3_fronteira.py
python fase4_expandir.py
python fase5_busca.py
python desafio6.py
```

## Resultado

```text
Arad -> Sibiu -> Rimnicu Vilcea -> Pitesti -> Bucharest
(418 km em 4 passos, igual à Figura 3.24 do livro)
```

---

## Fases do Projeto

| Arquivo | Conteúdo |
| :--- | :--- |
| `mapa.py` | Base de dados do problema (grafo de estradas e heurística $h(n)$ ). |
| `fase1_explorar.py` | Leitura e navegação nos dicionários, listas e tuplas + desafios de filtragem. |
| `fase2_caminhos.py` | Criação das primeiras funções (`def`) para calcular custos e valores $g(n)$, $h(n)$ e $f(n)$. |
| `fase3_fronteira.py` | Estruturação do nó de busca e manipulação manual da fronteira com ordenação `lambda`. |
| `fase4_expandir.py` | Modularização da expansão de nós e controle de ciclos com conjuntos (`set`). |
| `fase5_busca.py` | Implementação completa do laço `while` do algoritmo $A^*$ e comparação com busca gulosa. |
| `a_estrela.py` | Programa final estruturado com `main()`, rastro passo a passo e teste de regressão. |
| `desafio6.py` | Experimentos comparativos entre $A^*$ e Busca de Custo Uniforme ($h(n) = 0$). |

---

## Detalhamento das Funções

### Fase 1: `fase1_explorar.py` (Navegação nos Dados)
Executa instruções sequenciais diretamente para inspecionar `mapa.py`:
* **Execução principal:** Importa os dicionários, verifica o total de chaves com `len()`, acessa elementos encadeados (`mapa_romenia['Arad'][0][1]`) e desempacota tuplas em laços (`for vizinho, custo in ...`).
* **Desafios da Fase 1:**
  1. Filtra cidades sem saída (grau 1) testando `len(mapa_romenia[cidade]) == 1` (resultado: *Giurgiu, Eforie e Neamt*).
  2. Percorre `.items()` de `heuristica_bucareste` para listar cidades com $h(n) < 200\text{ km}$.
  3. Percorre todas as arestas do mapa acumulando o maior valor encontrado para identificar a estrada mais longa (*Fagaras–Bucharest*, 211 km).

---

### Fase 2: `fase2_caminhos.py` (Cálculo de Custos e $f = g + h$)

* **`def custo_da_estrada(origem, destino)`**
  * **Funcionamento:** Percorre a lista de tuplas `(vizinho, custo)` em `mapa_romenia[origem]`. Se encontrar `vizinho == destino`, retorna imediatamente o `custo` em km. Se o laço terminar sem encontrar ligação direta, retorna `None`.
* **`def custo_do_caminho(caminho)`**
  * **Funcionamento:** Inicializa `total = 0` e percorre os índices com tamanho `range(len(caminho) - 1)`, pois entre a quantidade de cidades citadas, existem `total de cidades - 1` estradas. A cada passo, chama `custo_da_estrada(caminho[i], caminho[i + 1])`, onde `caminho[i + 1]` é a próxima cidade inserida, e acumula o valor retornado em `total`.
* **`def mostrar_g_h_f(caminho)`**
  * **Funcionamento:** Imprime uma tabela formatada com os valores de $g(n)$, $h(n)$ e $f(n)$ para cada parada de uma rota. Usa fatiamento de lista (`caminho[:i + 1]`) passado para `custo_do_caminho()` para obter o custo acumulado $g(n)$ até aquele ponto, soma com `heuristica_bucareste[cidade]` ( $h(n)$ ) e exibe $f(n) = g(n) + h(n)$.
* **Chamadas e Desafios da Fase 2:**
  * Testa `custo_da_estrada('Arad', 'Sibiu')` (140 km) e `'Arad' -> 'Bucharest'` (`None`).
  * Compara a rota por Fagaras (450 km) com a rota por Pitesti (418 km) chamando `custo_do_caminho()` e `mostrar_g_h_f()`.
  * **Desafio:** Calcula a rota longa via Timisoara (`por_timisoara`, totalizando 733 km) e exibe sua tabela $g, h, f$, demonstrando que o $f(n)$ ultrapassa 418 km logo na primeira parada (*Timisoara*, com $f = 447$).

---

### Fase 3: `fase3_fronteira.py` (O Nó de Busca e a Fronteira)

* **Execução principal:** Cria a tupla `no_inicial = (366, 0, 'Arad', ['Arad'])`, insere na lista `fronteira`, remove com `fronteira.pop(0)`, gera os 3 vizinhos de Arad calculando `novo_g`, `novo_h` e `novo_f`, ordena a lista com `fronteira.sort(key=lambda no: no[0])` e extrai o próximo nó de menor $f$ (*Sibiu*, $f = 393$).
* **Desafios da Fase 3:**
  1. Expande manualmente os vizinhos de `'Sibiu'` e reordena por `no[0]` ($f$), evidenciando que `'Arad'` retorna à fronteira ($f = 646$) por ainda não haver controle de cidades já visitadas.
  2. Altera o critério de ordenação para `key=lambda no: no[1]` (ordenando apenas pelo custo real $g(n)$ ), simulando a **Busca de Custo Uniforme**, onde `'Zerind'` ($g = 75$) passa a ser o primeiro nó escolhido.

---

### Fase 4: `fase4_expandir.py` (Modularização e Conjunto de Explorados)

* **`def mostrar_fronteira(fronteira)`**
  * **Funcionamento:** Desempacota cada tupla `(f, g, cidade, caminho)` da fronteira, formata como `'Cidade(f=...)'` numa lista auxiliar `partes` e imprime tudo em uma única linha separada por vírgulas usando `', '.join(partes)`.
* **`def expandir(no, explorados)`**
  * **Funcionamento:** Desempacota o `no` recebido, inicializa `filhos = []` e percorre `mapa_romenia[cidade_atual]`. Se `vizinho in explorados`, usa `continue` para ignorá-lo. Caso contrário, calcula `novo_g` e `novo_f` e adiciona a nova tupla `(novo_f, novo_g, vizinho, caminho + [vizinho])` à lista `filhos`, retornando-a ao final.
* **Chamadas e Desafio da Fase 4:**
  * Cria um conjunto vazio com `explorados = set()`, para uma busca mais eficiente futuramente, executa um laço `for rodada in [1, 2, 3]:` que ordena a fronteira, retira o menor nó com `.pop(0)`, adiciona a cidade ao conjunto `explorados.add(cidade)` e concatena os filhos retornados por `expandir(no, explorados)` à `fronteira`.
  * **Desafio:** Amplia o laço para `range(1, 7)`. Na rodada 6, `'Bucharest'` ($f = 418$) é extraída, mas o laço não interrompe porque ainda não existe o teste de condição de parada (objetivo atingido).

---

### Fase 5: `fase5_busca.py` (O Algoritmo $A^*$ Completo)

* **`def busca_a_estrela(inicio, objetivo)`**
  * **Funcionamento:** Inicializa `fronteira` com o nó de partida e `explorados = set()`. Enquanto houver nós na `fronteira` (`while fronteira:`):
    1. Ordena por $f$ (`no[0]`) e extrai o primeiro nó (`pop(0)`).
    2. **Teste de objetivo na retirada:** Verifica `if cidade_atual == objetivo:` e retorna `(caminho, g_atual)`. Testar na retirada (e não na geração) garante que o caminho ótimo (418 km) vença o subótimo (450 km via Fagaras).
    3. Ignora o nó se `cidade_atual in explorados`; caso contrário, adiciona ao conjunto.
    4. Expande os vizinhos não explorados calculando `novo_g` e `novo_f` e inserindo-os na `fronteira`.
    5. Se a fronteira esvaziar sem achar destino, retorna `(None, float('inf'))`.
* **Chamadas e Desafios da Fase 5:**
  * Chama `busca_a_estrela('Arad', 'Bucharest')` e imprime o caminho ótimo (418 km, 4 estradas).
  * **`def busca_a_estrela_desafio(inicio, objetivo)`:** Altera a ordenação para `key=lambda no: no[2]`, selecionando o terceiro elemento da lista ( $h(n)$ ) como objetivo de ordenação, resultando no caminho de 450 km via Fagaras.
  * **`def busca_a_estrela_desafio2(inicio, objetivo)`:** Move o teste `if vizinho == objetivo:` para dentro do laço `for` (no momento em que o filho é gerado). Assim que `'Fagaras'` gera `'Bucharest'`, a busca encerra prematuramente devolvendo 450 km antes de explorar `'Pitesti'` (418 km).

---

### Fase 6: `a_estrela.py` e `desafio6.py` (Programa Final e Análise de Desempenho)

* **`def resumo_fronteira(fronteira)`**
  * **Funcionamento:** Versão compacta de `mostrar_fronteira` que utiliza uma expressão geradora dentro de `', '.join(...)` para retornar a string formatada da fronteira sem imprimir diretamente.
* **`def busca_a_estrela(inicio, objetivo, grafo, heuristica, mostrar=True)`**
  * **Funcionamento:** Generaliza o algoritmo da Fase 5 recebendo o `grafo` e a `heuristica` como parâmetros, além de um contador `iteracao` e a flag opcional `mostrar=True` para exibir o rastro completo de cada expansão. Usa `grafo.get(cidade_atual, [])` para evitar `KeyError` caso uma cidade não tenha saídas cadastradas.
* **`def main()`**
  * **Funcionamento:** Orquestra a execução principal do programa:
    1. Chama `busca_a_estrela` de `'Arad'` para `'Bucharest'` com rastro ativado (`mostrar=True`).
    2. Executa um **teste de regressão** validando se `custo == 418` e `len(caminho) - 1 == 4`.
    3. Roda um laço `for` testando outras origens (`'Timisoara'`, `'Oradea'`, `'Craiova'`, `'Iasi'`) com `mostrar=False`.
* **Ponto de entrada (`if __name__ == '__main__':`)**
  * **Funcionamento:** Garante que `main()` só seja executada quando `a_estrela.py` for rodado diretamente no terminal, permitindo que suas funções sejam importadas por outros scripts sem disparar impressões indesejadas.
* **Desafios de `desafio6.py`:**
  * **Heurística zerada (`h_zero`):** Cria um dicionário por compreensão `{c: 0 for c in mapa_romenia}` onde todas as estimativas valem 0. Ao rodar a busca com `h_zero`, o algoritmo se comporta exatamente como a **Busca de Custo Uniforme**: encontra os mesmos 418 km, mas o trabalho sobe de **6 para 14 iterações**, comprovando como a heurística direciona a busca.
  * **Novas origens com contagem de iterações:** Executa a busca partindo de `'Lugoj'`, `'Mehadia'` e `'Eforie'`, exibindo custo total, número de iterações do laço `while` e a rota completa.