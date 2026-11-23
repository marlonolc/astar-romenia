# -*- coding: utf-8 -*-
# fase5_busca.py — Fase 5: o laço while que repete a expansão até chegar.
# Rode com: python fase5_busca.py

# ----- PASSO 1: importar os dados -----
from mapa import mapa_romenia, heuristica_bucareste

# ----- PASSO 2: a função de busca A* -----
def busca_a_estrela(inicio, objetivo):
    """Devolve (caminho, custo) do melhor caminho, ou (None, infinito)."""
    fronteira = [(heuristica_bucareste[inicio], 0, inicio, [inicio])]
    explorados = set()

    while fronteira:
        # escolhe o nó de menor f
        fronteira.sort(key=lambda no: no[0])
        f_atual, g_atual, cidade_atual, caminho = fronteira.pop(0)

        # teste de objetivo: feito ao RETIRAR o nó, não ao gerar
        if cidade_atual == objetivo:
            return caminho, g_atual

        # cidade já explorada por um caminho melhor: descarta
        if cidade_atual in explorados:
            continue
        explorados.add(cidade_atual)

        # gera os filhos e coloca na fronteira
        for vizinho, custo_estrada in mapa_romenia[cidade_atual]:
            if vizinho not in explorados:
                novo_g = g_atual + custo_estrada
                novo_f = novo_g + heuristica_bucareste[vizinho]
                fronteira.append((novo_f, novo_g, vizinho, caminho + [vizinho]))

    return None, float('inf')

# ----- PASSO 3: chamar a função e mostrar o resultado -----
caminho, custo = busca_a_estrela('Arad', 'Bucharest')
print('Caminho:', ' -> '.join(caminho))
print('Custo :', custo, 'km')
print('Passos :', len(caminho) - 1, 'estradas')

# ----- DESAFIO -----
print('\n----- DESAFIO -----')

# Mude a ordenação para key=lambda no: heuristica_bucareste[no[2]] (só h). Você acabou de
# escrever a busca gulosa: o resultado vira 450 km. Depois desfaça.
def busca_a_estrela_desafio(inicio, objetivo):
    """Devolve (caminho, custo) do melhor caminho, ou (None, infinito)."""
    fronteira = [(heuristica_bucareste[inicio], 0, inicio, [inicio])]
    explorados = set()

    while fronteira:
        # escolhe o nó de menor f
        fronteira.sort(key=lambda no: no[2])
        f_atual, g_atual, cidade_atual, caminho = fronteira.pop(0)

        # teste de objetivo: feito ao RETIRAR o nó, não ao gerar
        if cidade_atual == objetivo:
            return caminho, g_atual

        # cidade já explorada por um caminho melhor: descarta
        if cidade_atual in explorados:
            continue
        explorados.add(cidade_atual)

        # gera os filhos e coloca na fronteira
        for vizinho, custo_estrada in mapa_romenia[cidade_atual]:
            if vizinho not in explorados:
                novo_g = g_atual + custo_estrada
                novo_f = novo_g + heuristica_bucareste[vizinho]
                fronteira.append((novo_f, novo_g, vizinho, caminho + [vizinho]))

    return None, float('inf')

caminho, custo = busca_a_estrela_desafio('Arad', 'Bucharest')
print('Caminho:', ' -> '.join(caminho))
print('Custo :', custo, 'km')
print('Passos :', len(caminho) - 1, 'estradas')

# Mova o teste de objetivo para dentro do for, logo depois de calcular novo_g:
# if vizinho == objetivo: return caminho + [vizinho], novo_g. O resultado vira 450 km.
print()
def busca_a_estrela_desafio2(inicio, objetivo):
    """Devolve (caminho, custo) do melhor caminho, ou (None, infinito)."""
    fronteira = [(heuristica_bucareste[inicio], 0, inicio, [inicio])]
    explorados = set()

    while fronteira:
        # escolhe o nó de menor f
        fronteira.sort(key=lambda no: no[0])
        f_atual, g_atual, cidade_atual, caminho = fronteira.pop(0)

        # cidade já explorada por um caminho melhor: descarta
        if cidade_atual in explorados:
            continue
        explorados.add(cidade_atual)

        # gera os filhos e coloca na fronteira
        for vizinho, custo_estrada in mapa_romenia[cidade_atual]:
            if vizinho not in explorados:
                novo_g = g_atual + custo_estrada
                novo_f = novo_g + heuristica_bucareste[vizinho]
                fronteira.append((novo_f, novo_g, vizinho, caminho + [vizinho]))

                # teste de objetivo
                if vizinho == objetivo:
                    return caminho + [vizinho], novo_g

    return None, float('inf')

caminho, custo = busca_a_estrela_desafio2('Arad', 'Bucharest')
print('Caminho:', ' -> '.join(caminho))
print('Custo :', custo, 'km')
print('Passos :', len(caminho) - 1, 'estradas')

# Explique por quê com a árvore da Fase 6.
# Com o teste de objetivo no final do for, está verificando se um dos vizinhos é o objetivo,
# e nesse caso encontrará a string de destino, porém antes de verificar se é o melhor resultado