from constantes import *
import motor_grafico as motor
from inicializacao import gera_posicao_desocupada
import random
def desenha_tela_campeao(janela, estado, altura_tela, largura_tela):
    mensagem = 'parabéns jogador voce eliminou todos os monstros, aperte q para sair'
    motor.preenche_fundo(janela, PRETO)
    motor.desenha_string(janela, largura_tela //2 - len(mensagem) // 2, altura_tela // 2, mensagem, PRETO, BRANCO)
    motor.mostra_janela(janela)

def atualiza_estado_campeao(estado , tecla):
    if tecla == 'q':
        estado['tela_anterior'] = TELA_CAMPEAO
        estado['tela_atual'] = SAIR

def desenha_tela_perdeu(janela, estado, altura_tela, largura_tela):
    mensagem = 'os monstros dominaram o mapa aperte q para sair'
    motor.preenche_fundo(janela, PRETO)
    motor.desenha_string(janela, largura_tela //2 - len(mensagem) // 2, altura_tela // 2, mensagem, PRETO, BRANCO)
    motor.mostra_janela(janela)

def atualiza_estado_perdeu(estado , tecla):
    if tecla == 'q':
        estado['tela_anterior'] = TELA_PERDEU
        estado['tela_atual'] = SAIR

def desenha_tela_inicial(janela, estado, altura_tela, largura_tela):
    mensagem = 'aperte a tecla j para jogar'
    mensagem2 = 'aperte a tecla h para ver as instrucoes'
    motor.preenche_fundo(janela, PRETO)
    motor.desenha_string(janela, largura_tela // 2 - len(mensagem) // 2, altura_tela // 2, mensagem, PRETO, BRANCO)
    motor.desenha_string(janela, largura_tela // 2 - len(mensagem2) // 2, altura_tela // 2 + 2, mensagem2, PRETO, BRANCO)
    motor.mostra_janela(janela)


def atualiza_estado_inicial(estado , tecla):
    if tecla == 'j':
        estado['tela_anterior'] = TELA_INICIAL
        estado['tela_atual'] = TELA_JOGO
    if tecla == 'h':
        estado['tela_anterior'] = TELA_INICIAL
        estado['tela_atual'] = TELA_INSTRUCOES


def desenha_tela_instrucoes(janela, estado, altura_tela, largura_tela):
    titulo = 'INSTRUCOES'
    linhas = [
        'setas: mover o personagem',
        'coracao: ganha uma vida',
        'espinho: perde uma vida',
        'andar contra um monstro: comeca a batalha',
        'i: abre o inventario',
        'v: volta da sala secreta para o mapa',
        'q ou esc: sai do jogo',
        '',
        'procure a passagem escondida no canto do mapa',
        'la dentro tem uma espada e o chefao',
        'sem a espada o chefao tira 3 vidas por golpe',
        '',
        'aperte j para comecar',
    ]
    motor.preenche_fundo(janela, PRETO)
    motor.desenha_string(janela, largura_tela // 2 - len(titulo) // 2, 2, titulo, PRETO, BRANCO)
    linha_atual = 4
    for texto in linhas:
        motor.desenha_string(janela, largura_tela // 2 - len(texto) // 2, linha_atual, texto, PRETO, BRANCO)
        linha_atual = linha_atual + 1
    motor.mostra_janela(janela)


def atualiza_estado_instrucoes(estado , tecla):
    if tecla == 'j':
        estado['tela_anterior'] = TELA_INSTRUCOES
        estado['tela_atual'] = TELA_JOGO
    if tecla == motor.ESCAPE or tecla == 'q':
        estado['tela_atual'] = SAIR

def desenha_tela(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    objetos = estado['objetos']
    mapa = estado['mapa']
    pos_jogador = estado['pos_jogador']
    coracoes_vazios = estado['max_vidas'] - estado['vidas']
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    dx = (largura_tela - largura_mapa) // 2
    dy = (altura_tela - altura_mapa) // 2
    

    for i in range(len(mapa)):
        for j in range(len(mapa[i])):
            motor.desenha_string(janela, j + dx, i + dy, mapa[i][j], CINZA_CLARO, CINZA_CLARO)

    for objeto in objetos:
        if objeto['tipo'] == PAREDE:
            motor.desenha_string(janela, objeto['posicao'][0] + dx, objeto['posicao'][1] + dy, objeto['tipo'], CINZA_PEDRA_ESCURO, CINZA_PEDRA)
        if objeto['tipo'] == CORACAO:
            motor.desenha_string(janela, objeto['posicao'][0] + dx, objeto['posicao'][1] + dy, objeto['tipo'], CINZA_CLARO, VERMELHO)
        if objeto['tipo'] == ESPINHO:
            motor.desenha_string(janela, objeto['posicao'][0] + dx, objeto['posicao'][1] + dy, objeto['tipo'], CINZA_CLARO, VERDE_ESCURO)
        if objeto['tipo'] in TIPOS_MONSTRO:
            motor.desenha_string(janela, objeto['posicao'][0] + dx, objeto['posicao'][1] + dy, objeto['tipo'], CINZA_CLARO, objeto['cor'])

    motor.desenha_string(janela, 0, 0, estado['vidas'] * (CORACAO + ' '), PRETO, VERMELHO)
    if estado['vidas'] < estado['max_vidas']:
        motor.desenha_string(janela, estado['vidas'] * 2, 0, coracoes_vazios * CORACAO_BRANCO, PRETO, BRANCO)
    motor.desenha_string(janela, 0, altura_tela - 1, estado['mensagem'], PRETO, BRANCO)

    if estado['tem_espada']:
        motor.desenha_string(janela, pos_jogador[0] + dx, pos_jogador[1] + dy, JOGADOR_COM_ESPADA, CINZA_CLARO, BRANCO)
    else:
        motor.desenha_string(janela, pos_jogador[0] + dx, pos_jogador[1] + dy, JOGADOR, CINZA_CLARO, BRANCO)

    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    estado['mensagem'] = ''
    objetos = estado['objetos']
    pos_jogador = estado['pos_jogador']
    achou_monstro = ''
    condicao = False
    monstro_atacado = None
    objetos_secretos = estado['objetos_secretos']
    monstros_vivos = 0

    for objeto in objetos:
        if objeto['tipo'] in TIPOS_MONSTRO:
            if [pos_jogador[0], pos_jogador[1] - 1] == objeto['posicao']:
                achou_monstro = 'sim em cima'
            if [pos_jogador[0], pos_jogador[1] + 1] == objeto['posicao']:
                achou_monstro = 'sim em baixo'
            if [pos_jogador[0] - 1, pos_jogador[1]] == objeto['posicao']:
                achou_monstro = 'sim na esquerda'
            if [pos_jogador[0] + 1, pos_jogador[1]] == objeto['posicao']:
                achou_monstro = 'sim na direita'

    if tecla == motor.SETA_ESQUERDA:
        condicao = True
        destino = [pos_jogador[0] - 1, pos_jogador[1]]
        if destino in estado['paredes_no_jogo']:
            estado['mensagem'] = 'parede no caminho'
        elif achou_monstro != 'sim na esquerda':
            pos_jogador[0] = pos_jogador[0] - 1
        else:
            for objeto in objetos:
                if objeto['tipo'] in TIPOS_MONSTRO and objeto['posicao'] == destino:
                    monstro_atacado = objeto
                    chance = objeto['probabilidade_de_ataque']
                    dano = 1
                    if estado['tem_espada']:
                        dano = 2
                    if estado['espadas_usadas'] >= 2:
                        chance = chance * 0.75
                    sorteado = random.random()
                    if sorteado < chance:
                        estado['vidas'] = estado['vidas'] - 1
                        estado['mensagem'] = 'o monstro atacou voce!'
                    else:
                        objeto['vida'] = objeto['vida'] - dano
                        estado['mensagem'] = 'voce atacou o monstro!'
                        if objeto['vida'] <= 0:
                            objetos.remove(objeto)
                            estado['mensagem'] = 'voce matou o monstro!'
                            monstros_vivos -= 1
                    break

    if tecla == motor.SETA_DIREITA:
        condicao = True
        destino = [pos_jogador[0] + 1, pos_jogador[1]]
        if destino in estado['paredes_no_jogo']:
            estado['mensagem'] = 'parede no caminho'
        elif achou_monstro != 'sim na direita':
            pos_jogador[0] = pos_jogador[0] + 1
        else:
            for objeto in objetos:
                if objeto['tipo'] in TIPOS_MONSTRO and objeto['posicao'] == destino:
                    monstro_atacado = objeto
                    chance = objeto['probabilidade_de_ataque']
                    dano = 1
                    if estado['tem_espada']:
                        dano = 2
                    if estado['espadas_usadas'] >= 2:
                        chance = chance * 0.75
                    sorteado = random.random()
                    if sorteado < chance:
                        estado['vidas'] = estado['vidas'] - 1
                        estado['mensagem'] = 'o monstro atacou voce!'
                    else:
                        objeto['vida'] = objeto['vida'] - dano
                        estado['mensagem'] = 'voce atacou o monstro!'
                        if objeto['vida'] <= 0:
                            objetos.remove(objeto)
                            estado['mensagem'] = 'voce matou o monstro!'
                            monstros_vivos -= 1
                    break

    if tecla == motor.SETA_CIMA:
        condicao = True
        destino = [pos_jogador[0], pos_jogador[1] - 1]
        if destino in estado['paredes_no_jogo']:
            estado['mensagem'] = 'parede no caminho'
        elif achou_monstro != 'sim em cima':
            pos_jogador[1] = pos_jogador[1] - 1
        else:
            for objeto in objetos:
                if objeto['tipo'] in TIPOS_MONSTRO and objeto['posicao'] == destino:
                    monstro_atacado = objeto
                    chance = objeto['probabilidade_de_ataque']
                    dano = 1
                    if estado['tem_espada']:
                        dano = 2
                    if estado['espadas_usadas'] >= 2:
                        chance = chance * 0.75
                    sorteado = random.random()
                    if sorteado < chance:
                        estado['vidas'] = estado['vidas'] - 1
                        estado['mensagem'] = 'o monstro atacou voce!'
                    else:
                        objeto['vida'] = objeto['vida'] - dano
                        estado['mensagem'] = 'voce atacou o monstro!'
                        if objeto['vida'] <= 0:
                            objetos.remove(objeto)
                            estado['mensagem'] = 'voce matou o monstro!'
                            monstros_vivos -= 1
                    break

    if tecla == motor.SETA_BAIXO:
        condicao = True
        destino = [pos_jogador[0], pos_jogador[1] + 1]
        if destino in estado['paredes_no_jogo']:
            estado['mensagem'] = 'parede no caminho'
        elif achou_monstro != 'sim em baixo':
            pos_jogador[1] = pos_jogador[1] + 1
        else:
            for objeto in objetos:
                if objeto['tipo'] in TIPOS_MONSTRO and objeto['posicao'] == destino:
                    monstro_atacado = objeto
                    chance = objeto['probabilidade_de_ataque']
                    dano = 1
                    if estado['tem_espada']:
                        dano = 2
                    if estado['espadas_usadas'] >= 2:
                        chance = chance * 0.75
                    sorteado = random.random()
                    if sorteado < chance:
                        estado['vidas'] = estado['vidas'] - 1
                        estado['mensagem'] = 'o monstro atacou voce!'
                    else:
                        objeto['vida'] = objeto['vida'] - dano
                        estado['mensagem'] = 'voce atacou o monstro!'
                        if objeto['vida'] <= 0:
                            objetos.remove(objeto)
                            estado['mensagem'] = 'voce matou o monstro!'
                            monstros_vivos -= 1
                    break

    for objeto in list(objetos):
        if objeto['posicao'] == pos_jogador:
            if objeto['tipo'] == CORACAO:
                objetos.remove(objeto)
                if estado['vidas'] < estado['max_vidas']:
                    estado['vidas'] = estado['vidas'] + 1
                    estado['mensagem'] = 'voce ganhou uma vida!'
                else:
                    estado['mensagem'] = 'sua vida ja esta cheia'
            if objeto['tipo'] == ESPINHO:
                estado['vidas'] = estado['vidas'] - 1
                estado['mensagem'] = 'voce perdeu uma vida!'

    direcao_monstro = [motor.SETA_BAIXO, motor.SETA_CIMA, motor.SETA_ESQUERDA, motor.SETA_DIREITA]
    direcao_ogro = [motor.SETA_BAIXO, motor.SETA_CIMA]
    diagonais = [[1, -1], [-1, -1], [1, 1], [-1, 1]]
    if condicao == True:
        for objeto in objetos:
            if objeto['tipo'] in TIPOS_MONSTRO:
                if objeto is monstro_atacado:
                    continue
                if objeto['tipo'] is MONSTRO:
                    direcao = random.choice(direcao_monstro)
                    destino = [objeto['posicao'][0], objeto['posicao'][1]]
                    if direcao == motor.SETA_CIMA:
                        destino[1] = destino[1] - 1
                    if direcao == motor.SETA_BAIXO:
                        destino[1] = destino[1] + 1
                    if direcao == motor.SETA_ESQUERDA:
                        destino[0] = destino[0] - 1
                    if direcao == motor.SETA_DIREITA:
                        destino[0] = destino[0] + 1
                if objeto['tipo'] is MORCEGO:
                    d = random.choice(diagonais)
                    destino = [objeto['posicao'][0], objeto['posicao'][1]]
                    destino = [objeto['posicao'][0] + d[0], objeto['posicao'][1] + d[1]]
                if objeto['tipo'] is OGRO:
                    direcao = random.choice(direcao_ogro)
                    destino = [objeto['posicao'][0], objeto['posicao'][1]]
                    if direcao == motor.SETA_CIMA:
                        destino[1] = destino[1] - 1
                    if direcao == motor.SETA_BAIXO:
                        destino[1] = destino[1] + 1
                livre = True
                if destino == pos_jogador:
                    livre = False
                for outro in objetos:
                    if outro['posicao'] == destino:
                        livre = False

                if livre:
                    objeto['posicao'] = destino

    if estado['vidas'] <= 0:
        estado['vidas'] = 0
        estado['tela_anterior'] = TELA_JOGO
        estado['tela_atual'] = TELA_PERDEU


    if tecla == 'i':
        estado['tela_anterior'] = TELA_JOGO
        estado['tela_atual'] = TELA_INVENTARIO
    elif tecla == motor.ESCAPE or tecla == 'q':
        estado['tela_atual'] = SAIR
    elif pos_jogador == [93, 20]:
        estado['tela_atual'] = TELA_SECRETA


    chefao_vivo = 0
    for objeto in objetos_secretos:
        if objeto['tipo'] == CHEFAO:
            chefao_vivo = chefao_vivo + 1
    
    monstros_vivos = 0
    for objeto in objetos:
        if objeto['tipo'] in TIPOS_MONSTRO:
            monstros_vivos = monstros_vivos + 1
    
    if monstros_vivos == 0 and chefao_vivo == 0:
        estado['tela_anterior'] = TELA_JOGO
        estado['tela_atual'] = TELA_CAMPEAO


def desenha_tela_secreta(janela, estado, altura_tela, largura_tela):
    motor.preenche_fundo(janela, PRETO)
    mapa_escondido = estado['mapa_escondido']
    objetos_secretos = estado['objetos_secretos']
    pos = estado['pos_jogador_tela_escondida']
    coracoes_vazios = estado['max_vidas'] - estado['vidas']
    largura_mapa_escondido = len(mapa_escondido[0])
    altura_mapa_escondido = len(mapa_escondido)
    deltax = (largura_tela - largura_mapa_escondido) // 2
    deltay = (altura_tela - altura_mapa_escondido) // 2
    
    for i in range(len(mapa_escondido)):
        for j in range(len(mapa_escondido[i])):
            motor.desenha_string(janela, j + deltax, i + deltay, mapa_escondido[i][j], AZUL, AZUL)
    texto = 'aperte v para voltar ao mapa'
    motor.desenha_string(janela, largura_tela - len(texto) - 1, altura_tela - 1, texto, PRETO, BRANCO)
    for objeto in objetos_secretos:
        if objeto['tipo'] == PAREDE:
            motor.desenha_string(janela, objeto['posicao'][0] + deltax, objeto['posicao'][1] + deltay, objeto['tipo'], MARROM_ESCURO, MARROM_MAIS_ESCURO)
        if objeto['tipo'] == CORACAO:
            motor.desenha_string(janela, objeto['posicao'][0] + deltax, objeto['posicao'][1] + deltay, objeto['tipo'], AZUL, VERMELHO)
        if objeto['tipo'] == ESPADA:
            motor.desenha_string(janela, objeto['posicao'][0] + deltax, objeto['posicao'][1] + deltay, objeto['tipo'], AZUL, AMARELO)
        if objeto['tipo'] == ESCUDO:
            motor.desenha_string(janela, objeto['posicao'][0] + deltax, objeto['posicao'][1] + deltay, objeto['tipo'], AZUL, CINZA_CLARO)
        if objeto['tipo'] == CHEFAO:
            motor.desenha_string(janela, objeto['posicao'][0] + deltax, objeto['posicao'][1] + deltay, '╠', AZUL, ROXO)
            motor.desenha_string(janela, objeto['posicao'][0] + 3 + deltax, objeto['posicao'][1] + deltay, '╣', AZUL, ROXO)
            motor.desenha_string(janela, objeto['posicao'][0] + 1 + deltax, objeto['posicao'][1] + deltay, objeto['tipo'], AZUL, VERDE_CLARO)

    motor.desenha_string(janela, 0, 0, estado['vidas'] * (CORACAO + ' '), PRETO, VERMELHO)
    if estado['vidas'] < estado['max_vidas']:
        motor.desenha_string(janela, estado['vidas'] * 2, 0, coracoes_vazios * CORACAO_BRANCO, PRETO, BRANCO)
    motor.desenha_string(janela, 0, altura_tela - 1, estado['mensagem'], PRETO, BRANCO)

    if estado['tem_espada']:
        motor.desenha_string(janela, pos[0] + deltax, pos[1] + deltay, JOGADOR_COM_ESPADA, AZUL, BRANCO)
    else:
        motor.desenha_string(janela, pos[0] + deltax, pos[1] + deltay, JOGADOR, AZUL, BRANCO)

    motor.mostra_janela(janela)


def atualiza_estado_secreta(estado, tecla):
    estado['mensagem'] = ''
    pos = estado['pos_jogador_tela_escondida']
    objetos_secretos = estado['objetos_secretos']
    mapa_escondido = estado['mapa_escondido']
    objetos = estado['objetos']
    chefao_vivo = 0
    monstros_vivos = 0

    if tecla == 'i':
        estado['tela_anterior'] = TELA_SECRETA
        estado['tela_atual'] = TELA_INVENTARIO
        return
    if tecla == 'v':
        estado['tela_atual'] = TELA_JOGO
        estado['pos_jogador'] = [93, 19]
        return
    if tecla == motor.ESCAPE or tecla == 'q':
        estado['tela_atual'] = SAIR
        return

    destino = [pos[0], pos[1]]
    if tecla == motor.SETA_ESQUERDA:
        destino[0] = destino[0] - 1
    if tecla == motor.SETA_DIREITA:
        destino[0] = destino[0] + 1
    if tecla == motor.SETA_CIMA:
        destino[1] = destino[1] - 1
    if tecla == motor.SETA_BAIXO:
        destino[1] = destino[1] + 1

    if destino == pos:
        return

    bloqueado = False
    chefao_atacado = None
    for objeto in list(objetos_secretos):
        casas = [objeto['posicao']]
        if objeto['tipo'] == CHEFAO:
            casas = [objeto['posicao'],
                     [objeto['posicao'][0] + 1, objeto['posicao'][1]],
                     [objeto['posicao'][0] + 2, objeto['posicao'][1]],
                     [objeto['posicao'][0] + 3, objeto['posicao'][1]]]
        if destino in casas:
            if objeto['tipo'] == PAREDE:
                bloqueado = True
                estado['mensagem'] = 'parede no caminho'
            if objeto['tipo'] == CHEFAO:
                bloqueado = True
                chefao_atacado = objeto
                if estado['tem_espada']:
                    sorteado = random.random()
                    if sorteado < objeto['probabilidade_de_ataque']:
                        estado['vidas'] = estado['vidas'] - 2
                        estado['mensagem'] = 'o chefao te acertou! -2 vidas'
                    else:
                        objeto['vida'] = objeto['vida'] - 5
                        estado['mensagem'] = 'voce acertou o chefao com a espada!'
                        if objeto['vida'] <= 0:
                            objetos_secretos.remove(objeto)
                            estado['mensagem'] = 'voce derrotou o chefao!'
                            chefao_vivo -= 1
                else:
                    estado['vidas'] = estado['vidas'] - 3
                    estado['mensagem'] = 'sem a espada o chefao te arrasou! -3 vidas'
            if objeto['tipo'] == CORACAO:
                objetos_secretos.remove(objeto)
                if estado['vidas'] < estado['max_vidas']:
                    estado['vidas'] = estado['vidas'] + 1
                    estado['mensagem'] = 'voce ganhou uma vida!'
                else:
                    estado['mensagem'] = 'sua vida ja esta cheia'
            if objeto['tipo'] == ESPADA:
                objetos_secretos.remove(objeto)
                estado['inventario'].append(ESPADA)
                estado['mensagem'] = 'voce pegou a espada!'
            if objeto['tipo'] == ESCUDO:
                objetos_secretos.remove(objeto)
                estado['inventario'].append(ESCUDO)
                estado['mensagem'] = 'voce pegou o escudo!'
            break

    if bloqueado == False:
        pos[0] = destino[0]
        pos[1] = destino[1]

    direcao_monstro = [motor.SETA_BAIXO, motor.SETA_CIMA, motor.SETA_ESQUERDA, motor.SETA_DIREITA]
    for objeto in objetos_secretos:
        if objeto['tipo'] == CHEFAO:
            if objeto is chefao_atacado:
                continue
            direcao = random.choice(direcao_monstro)
            novo = [objeto['posicao'][0], objeto['posicao'][1]]
            if direcao == motor.SETA_CIMA:
                novo[1] = novo[1] - 1
            if direcao == motor.SETA_BAIXO:
                novo[1] = novo[1] + 1
            if direcao == motor.SETA_ESQUERDA:
                novo[0] = novo[0] - 1
            if direcao == motor.SETA_DIREITA:
                novo[0] = novo[0] + 1

            casas = [novo, [novo[0] + 1, novo[1]], [novo[0] + 2, novo[1]], [novo[0] + 3, novo[1]]]
            livre = True
            if pos in casas:
                livre = False
            for outro in objetos_secretos:
                if outro is objeto:
                    continue
                if outro['posicao'] in casas:
                    livre = False
            if livre:
                objeto['posicao'] = novo
    
    for objeto in objetos_secretos:
        if objeto['tipo'] == CHEFAO:
            chefao_vivo = chefao_vivo + 1
    
    
    for objeto in objetos:
        if objeto['tipo'] in TIPOS_MONSTRO:
            monstros_vivos = monstros_vivos + 1
    
    if monstros_vivos == 0 and chefao_vivo == 0:
        estado['tela_anterior'] = TELA_JOGO
        estado['tela_atual'] = TELA_CAMPEAO
                        
                        
    if estado['vidas'] <= 0:
        estado['vidas'] = 0
        estado['tela_anterior'] = TELA_JOGO
        estado['tela_atual'] = TELA_PERDEU
