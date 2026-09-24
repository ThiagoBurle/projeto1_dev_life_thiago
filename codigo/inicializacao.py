from random import randint

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
paredes_no_jogo = [
    [0,0], [1,0], [2,0], [3,0], [4,0], [5,0], [6,0], [7,0],
    [8,0], [9,0], [10,0], [11,0], [12,0], [13,0], [14,0], [15,0],
    [16,0], [17,0], [18,0], [19,0], [20,0], [21,0], [22,0], [23,0],
    [24,0], [25,0], [26,0], [27,0], [28,0], [29,0], [30,0], [31,0],
    [32,0], [33,0], [34,0], [35,0], [36,0], [37,0], [38,0], [39,0],
    [40,0], [41,0], [42,0], [43,0], [44,0], [45,0], [46,0], [47,0],
    [48,0], [49,0],
    [0,1], [49,1], [0,2], [49,2], [0,3], [49,3], [0,4], [49,4],
    [0,5], [49,5], [0,6], [49,6], [0,7], [49,7], [0,8], [49,8],
    [0,9], [49,9], [0,10], [49,10], [0,11], [49,11], [0,12], [49,12],
    [0,13], [49,13],
    [0,14], [1,14], [2,14], [3,14], [4,14], [5,14], [6,14], [7,14],
    [8,14], [9,14], [10,14], [11,14], [12,14], [13,14], [14,14], [15,14],
    [16,14], [17,14], [18,14], [19,14], [20,14], [21,14], [22,14], [23,14],
    [24,14], [25,14], [26,14], [27,14], [28,14], [29,14], [30,14], [31,14],
    [32,14], [33,14], [34,14], [35,14], [36,14], [37,14], [38,14], [39,14],
    [40,14], [41,14], [42,14], [43,14], [44,14], [45,14], [46,14], [47,14],
    [48,14], [49,14],
    [10,2], [10,3], [10,4], [10,5], [10,6], [10,9], [10,10], [10,11],
    [10,12], [39,2], [39,3], [39,4], [39,5], [39,6], [39,9], [39,10],
    [39,11], [39,12], [17,3], [18,3], [19,3], [20,3], [21,3], [22,3],
    [23,3], [26,11], [27,11], [28,11], [29,11], [30,11], [31,11], [32,11],
    [20,7], [21,7], [28,7], [29,7],
]

def gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa):
    x = randint(1, largura_mapa-2)
    y = randint(1, altura_mapa-2)
    posicao = [x,y]
    while [x,y] in posicoes_ocupadas:
       x = randint(1, largura_mapa-2)
       y = randint(1, altura_mapa-2)
       posicao = [x, y]
    posicoes_ocupadas.append(posicao)
    return posicao


def gera_objetos(quantidade, tipo, cor, largura_mapa, altura_mapa, posicoes_ocupadas):
    """
    Esta função já está pronta, você não precisa modificá-la.

    Gera uma lista de objetos do tipo especificado, com a quantidade especificada.
    Cada objeto é um dicionário com as chaves 'tipo', 'posicao' e 'cor'.

    Parâmetros:
    quantidade: quantidade de objetos a serem gerados
    tipo: tipo do objeto a ser gerado. É uma string como '❤'
    cor: cor do objeto a ser gerado. É uma lista com três elementos, como [255, 0, 0]
    largura_mapa: largura do mapa do jogo em caracteres
    altura_mapa: altura do mapa do jogo em caracteres
    posicoes_ocupadas: lista de posições ocupadas no mapa. Cada posição é uma lista com exatamente dois elementos: a posição x e a posição y.
    """
    objetos = []

    for i in range(quantidade):
        posicao = gera_posicao_desocupada(posicoes_ocupadas, largura_mapa, altura_mapa)
        objetos.append({
            'tipo': tipo,
            'posicao': posicao,
            'cor': cor,
        })

    return objetos


def inicializa_estado():
    # Cria lista de listas, cada uma com 50 espaços em branco
    # Você pode mudar esta lista, inclusive seu tamanho, à vontade
    mapa = [
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,
        [' '] * 50,

        
        
       
    ]
    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    

    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]  # Meio do mapa
    
    # Cria outros objetos do mapa
    posicoes_ocupadas = [pos_jogador]
    objetos = []
    for posicao in paredes_no_jogo:
        objetos.append({
                    'tipo': PAREDE,
                    'posicao': posicao,
                    'cor': MARROM_ESCURO,
                })
        posicoes_ocupadas.append(posicao)
    
        

    objetos += gera_objetos(8, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(6, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(3, MONSTRO, BRANCO, largura_mapa, altura_mapa, posicoes_ocupadas)

    for objeto in objetos:
            if objeto['tipo'] == MONSTRO:
                objeto['vida'] = 5
                objeto['probabilidade_de_ataque'] = 0.3
    
    
    return {
        'tela_atual': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'mensagem': '', # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'posicoes_ocupadas': posicoes_ocupadas,
        'paredes_no_jogo' : paredes_no_jogo
        
        

    }
