from random import randint

from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
# as paredes sao carregadas do arquivo mapa.txt, por isso a lista comeca vazia
paredes_no_jogo = []
paredes_sala_secreta = [
]
# corredor e salinha que levam pra passagem secreta
# essas posicoes entram em posicoes_ocupadas pra nao nascer nada em cima delas
area_da_portinha = [
    [92,11], [93,11], [94,11], [93,12], [93,13], [93,14], [93,15],
    [93,16], [93,17], [93,18], [90,19], [91,19], [92,19], [93,19],
    [94,19], [95,19], [96,19], [90,20], [91,20], [92,20], [93,20],
    [94,20], [95,20], [96,20], [90,21], [91,21], [92,21], [93,21],
    [94,21], [95,21], [96,21],
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
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
        [' '] * 100,
     

        
        
       
    ]
    
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)

    mapa_escondido = [
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
    [' '] * 30,
           
       
     

        
        
       
    ]
    
    largura_mapa_escondido = len(mapa_escondido[0])
    altura_mapa_escondido = len(mapa_escondido)
    
    # le o mapa do arquivo: cada # do arquivo virou uma parede
    # linha e a coordenada y e elemento e a coordenada x
    with open('mapa.txt','r') as arquivo:
        linhas = arquivo.read().split('\n')
        for linha in range(len(linhas)):
            for elemento in range(len(linhas[linha])):
                if linhas[linha][elemento] == '#':
                    paredes_no_jogo.append([elemento,linha])

    # mesma coisa, mas pro mapa da sala secreta
    with open('mapa_secreto.txt','r') as arquivo:
            linhas = arquivo.read().split('\n')
            for linha in range(len(linhas)):
                for elemento in range(len(linhas[linha])):
                    if linhas[linha][elemento] == '#':
                        paredes_sala_secreta.append([elemento,linha])
                    

    
    # Você pode colocar o jogador em outro lugar, se preferir
    pos_jogador = [largura_mapa//2, altura_mapa//2]
    pos_jogador_tela_escondida =[15,1]  # Meio do mapa
    
    # Cria outros objetos do mapa
    posicoes_ocupadas = [pos_jogador]
    posicoes_ocupadas_secreta = [[15 , 1]]
    for posicao in area_da_portinha:
            posicoes_ocupadas.append(posicao)
    
    objetos = []
    objetos_secretos = []
    # transforma cada coordenada de parede em um objeto pra poder desenhar depois
    for posicao in paredes_no_jogo:
        objetos.append({
                    'tipo': PAREDE,
                    'posicao': posicao,
                    'cor': MARROM_ESCURO,
                })
        posicoes_ocupadas.append(posicao)

    for posicao in paredes_sala_secreta:
        objetos_secretos.append({
                    'tipo': PAREDE,
                    'posicao': posicao,
                    'cor': MARROM_ESCURO,
                })
        posicoes_ocupadas_secreta.append(posicao)

    objetos += gera_objetos(15, CORACAO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(25, ESPINHO, VERDE_CLARO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(3, MONSTRO, BRANCO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(3, MORCEGO, BRANCO, largura_mapa, altura_mapa, posicoes_ocupadas)
    objetos += gera_objetos(4, OGRO, VERMELHO, largura_mapa, altura_mapa, posicoes_ocupadas)

    # da vida e chance de ataque pra cada tipo de monstro
    for objeto in objetos:
        if objeto['tipo'] == MONSTRO:
            objeto['vida'] = 6
            objeto['probabilidade_de_ataque'] = 0.45
        if objeto['tipo'] == MORCEGO:
            objeto['vida'] = 3
            objeto['probabilidade_de_ataque'] = 0.55
        if objeto['tipo'] == OGRO:
            objeto['vida'] = 9
            objeto['probabilidade_de_ataque'] = 0.45

    for posicao in [[25, 8], [15, 12]]:
        objetos_secretos.append({
            'tipo': CORACAO,
            'posicao': posicao,
            'cor': VERMELHO,
        })
        posicoes_ocupadas_secreta.append(posicao)

    for posicao in [[4, 8], [25, 10]]:
        objetos_secretos.append({
            'tipo': ESPADA,
            'posicao': posicao,
            'cor': AMARELO,
        })
        posicoes_ocupadas_secreta.append(posicao)

    for posicao in [[7, 3], [22, 12]]:
        objetos_secretos.append({
            'tipo': ESCUDO,
            'posicao': posicao,
            'cor': AZUL,
        })
        posicoes_ocupadas_secreta.append(posicao)

    # o chefao fica fixo no meio da sala secreta e ocupa 4 casas
    objetos_secretos.append({
        'tipo': CHEFAO,
        'posicao': [13, 7],
        'cor': VERDE_CLARO,
        'vida': 10,
        'probabilidade_de_ataque': 0.4,
    })
    posicoes_ocupadas_secreta.append([13, 7])
    posicoes_ocupadas_secreta.append([14, 7])
    posicoes_ocupadas_secreta.append([15, 7])
    posicoes_ocupadas_secreta.append([16, 7])
    
    
    return {
        'tela_atual': TELA_INICIAL,
        'tela_anterior': TELA_JOGO,
        'pos_jogador': pos_jogador,
        'vidas': 5,  # Quantidade atual de vidas do jogador - ele pode perder vidas ao colidir com espinhos ou ganhar vidas ao pegar corações
        'max_vidas': 5,  # Quantidade máxima de vidas que o jogador pode ter - o valor da chave 'vidas' nunca pode ser maior que o valor da chave 'max_vidas'
        'objetos': objetos,
        'mapa': mapa,
        'mensagem': '', # Use esta mensagem para mostrar mensagens ao jogador, como "Você perdeu uma vida" ou "Você ganhou uma vida"
        'posicoes_ocupadas': posicoes_ocupadas,
        'paredes_no_jogo' : paredes_no_jogo,
        'mapa_escondido' : mapa_escondido,
        'objetos_secretos' : objetos_secretos,
        'pos_jogador_tela_escondida': pos_jogador_tela_escondida,
        'posicoes_ocupadas_secreta': posicoes_ocupadas_secreta,
        'paredes_sala_secreta': paredes_sala_secreta,
        'tem_espada': False,
        'espadas_usadas': 0,
        'inventario': [],
        'mensagem_inventario' : ''
        

        
        

    }
