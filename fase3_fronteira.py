# -*- coding: utf-8 -*-
# fase3_fronteira.py — Fase 3: o nó de busca e a fronteira, feitos à mão.
# Rode com: python fase3_fronteira.py

# ----- PASSO 1: importar os dados -----
from mapa import mapa_romenia, heuristica_bucareste

# ----- PASSO 2: montar o nó inicial e a fronteira -----
# Um nó é uma tupla com 4 posições: (f, g, cidade, caminho)
inicio = 'Arad'
g = 0
h = heuristica_bucareste[inicio]
no_inicial = (g + h, g, inicio, [inicio])

fronteira = [no_inicial]
print('Fronteira no começo:', fronteira)

# ----- PASSO 3: tirar o primeiro nó da fronteira -----
no = fronteira.pop(0)
f_atual, g_atual, cidade_atual, caminho = no
print()
print('Nó retirado:', no)
print(' f =', f_atual, '| g =', g_atual, '| cidade =', cidade_atual, '| caminho =', caminho)
print('Fronteira agora:', fronteira)

# ----- PASSO 4: gerar os filhos (vizinhos) do nó retirado -----
for vizinho, custo_estrada in mapa_romenia[cidade_atual]:
    novo_g = g_atual + custo_estrada
    novo_h = heuristica_bucareste[vizinho]
    novo_f = novo_g + novo_h
    novo_caminho = caminho + [vizinho]
    fronteira.append((novo_f, novo_g, vizinho, novo_caminho))

print()
print('Fronteira depois de expandir Arad (ordem de inserção):')
for item in fronteira:
    print(' ', item)

# ----- PASSO 5: ordenar a fronteira pelo f -----
fronteira.sort(key=lambda no: no[0])
print()
print('Fronteira ordenada pelo f (posição 0 da tupla):')
for item in fronteira:
    print(' ', item)

# ----- PASSO 6: o próximo nó a ser expandido -----
proximo = fronteira.pop(0)
print()
print('Próximo nó a expandir:', proximo[2], 'com f =', proximo[0])

# ----- DESAFIO -----
print('\n----- DESAFIO -----')
# Copie o Passo 4 e expanda Sibiu à mão. A fronteira ordenada deve ser: Rimnicu Vilcea(413), Fagaras(415),
# Timisoara(447), Zerind(449), Arad(646) e Oradea(671).
for vizinho, custo_estrada in mapa_romenia['Sibiu']:
    novo_g = g_atual + custo_estrada
    novo_h = heuristica_bucareste[vizinho]
    novo_f = novo_g + novo_h
    novo_caminho = caminho + [vizinho]
    fronteira.append((novo_f, novo_g, vizinho, novo_caminho))

fronteira.sort(key=lambda no: no[0])
print('Fronteira ordenada depois de expandir Sibiu:')
for item in fronteira:
    print(' ', item)

# Por que Arad apareceu? (A Fase 4 resolve.)
# Resposta: Arad aparece pois é vizinho de Sibiu, e o código mostra todos os vizinhos da cidade escolhida

# Ordene por no[1] (o g) em vez de no[0].
fronteira.sort(key=lambda no: no[1])
print('\nFronteira ordenada depois de expandir o nó na posição 1:')
for item in fronteira:
    print(' ', item)
# Que nó sai primeiro? Esse critério é a busca de custo uniforme.
# Resposta: O primeiro nó fica sendo Zerind, que possui g = 75, o menor entre os presentes.