from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
from inicializacao import gera_posicao_desocupada
 # O seu código deve desenhar a tela do jogo aqui a partir dos valores no dicionário "estado"
    # APAGUE ESTA LINHA E A LINHA ABAIXO E ESCREVA SEU CÓDIGO AQUI
import random
def desenha_tela(janela, estado, altura_tela, largura_tela):
    # Utilize o dicionário estado para saber onde o jogador e os outros objetos estão.
    # Por exemplo, para saber a posição do jogador, use estado['pos_jogador']
    # O mapa esta armazenado em estado['mapa'].
    motor.preenche_fundo(janela, PRETO)
    obejetos = estado['objetos']
    mapa = estado['mapa']
    pos_jogador = estado['pos_jogador']
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    coracoes_vazios = estado['max_vidas'] - estado['vidas']
    posiçoes = estado['posicoes_ocupadas']
    dx = (largura_tela - largura_mapa)// 2
    dy = (altura_tela - altura_mapa) // 2
    for i in range(len(mapa)): 
        for j in range(len(mapa[i])):
            fundo = VERDE_CLARO
            frente = VERDE_CLARO
            # v =  i + j 
            # if v%2 == 0:
            #     fundo = VERDE_ESCURO
            #     frente = VERDE_CLARO
            
            motor.desenha_string(janela, j + dx,i + dy, mapa[i][j], frente, fundo)
           
            motor.desenha_string(janela, 0 ,0, estado['vidas'] * (CORACAO + ' '), PRETO, VERMELHO )
            if estado['vidas'] < estado['max_vidas']:
                motor.desenha_string(janela,estado['vidas'] * 2 ,0, coracoes_vazios * (CORACAO_BRANCO + ''), PRETO, BRANCO )
            motor.desenha_string(janela, 0,altura_tela - 1, estado['mensagem'], PRETO, BRANCO )
            motor.desenha_string(janela, pos_jogador[0] + dx,pos_jogador[1] + dy, JOGADOR , VERDE_CLARO, BRANCO)


    for objeto in obejetos:
        if objeto['tipo'] == PAREDE:
            motor.desenha_string(janela, objeto['posicao'][0]+dx, objeto['posicao'][1]+dy, objeto['tipo'], MARROM_ESCURO, MARROM_MAIS_ESCURO)        


    for objeto in obejetos:
        if objeto['tipo'] == CORACAO:
            motor.desenha_string(janela, objeto['posicao'][0]+dx,objeto['posicao'][1]+dy,objeto['tipo'], frente, VERMELHO )
        
    for objeto in obejetos:
            if objeto['tipo'] == ESPINHO:
                motor.desenha_string(janela, objeto['posicao'][0]+dx,objeto['posicao'][1]+dy,objeto['tipo'], frente, VERDE_ESCURO)
            
    for objeto in obejetos:
         if objeto['tipo'] == MONSTRO:
                motor.desenha_string(janela, objeto['posicao'][0]+dx, objeto['posicao'][1]+dy, objeto['tipo'], frente , BRANCO)
        
                 

    



    


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1
    estado['mensagem'] = ''
    mapa = estado['mapa']
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
    objetos = estado['objetos']
    achou_monstro = ''
    for objeto in objetos:
                if [estado['pos_jogador'][0], estado['pos_jogador'][1] - 1] == objeto['posicao']:
                     if objeto['tipo'] == MONSTRO:
                          achou_monstro = 'sim em cima'
                if [estado['pos_jogador'][0], estado['pos_jogador'][1]+1] == objeto['posicao']:
                    if objeto['tipo'] == MONSTRO:
                        achou_monstro = 'sim em baixo'
                if [estado['pos_jogador'][0] -1, estado['pos_jogador'][1]] == objeto['posicao']:
                    if objeto['tipo'] == MONSTRO:
                        achou_monstro = 'sim na esquerda'
                if [estado['pos_jogador'][0] + 1, estado['pos_jogador'][1]] == objeto['posicao']:
                                    if objeto['tipo'] == MONSTRO:
                                        achou_monstro = 'sim na direita'    


    if tecla == motor.SETA_ESQUERDA:       
        if not [estado['pos_jogador'][0] - 1,estado['pos_jogador'][1]] in estado['paredes_no_jogo']:
            if achou_monstro != 'sim na esquerda':
                estado['pos_jogador'][0] = estado['pos_jogador'][0] - 1
        else:
            estado['mensagem'] = 'parede no caminho'

   
    if tecla == motor.SETA_DIREITA:
    
        if not [estado['pos_jogador'][0] + 1,estado['pos_jogador'][1]] in estado['paredes_no_jogo']:
            if achou_monstro != 'sim na direita':
                estado['pos_jogador'][0] = estado['pos_jogador'][0] + 1
        else:
            estado['mensagem'] = 'parede no caminho'


    if tecla == motor.SETA_CIMA:
        if not [estado['pos_jogador'][0] ,estado['pos_jogador'][1] -1] in estado['paredes_no_jogo']:
            if achou_monstro != 'sim em cima':
                estado['pos_jogador'][1] = estado['pos_jogador'][1] - 1
        else:
            estado['mensagem'] = 'parede no caminho'


    if tecla == motor.SETA_BAIXO:
        
        
        if not [estado['pos_jogador'][0],estado['pos_jogador'][1] + 1] in estado['paredes_no_jogo']:
            if achou_monstro != 'sim em baixo':
                estado['pos_jogador'][1] = estado['pos_jogador'][1] + 1
            else:
                sorteado = random.random()
                if sorteado < objeto['probabilidade_de_ataque']:
                    if estado['vidas'] > 0:
                       estado['vidas'] = estado['vidas'] -1
                else:
                    if objeto['vida'] > 0:
                        objeto['vida'] = objeto['vida'] -1
                        if objeto['vida'] == 0:
                            estado['objeto'].remove(objeto)
                    


        else:
            estado['mensagem'] = 'parede no caminho'

    # criando objetos
    for objeto in objetos:
        if objeto['posicao'] == estado['pos_jogador']:
            if objeto['tipo'] == CORACAO:
                estado['objetos'].remove(objeto)
                estado['mensagem'] = 'sua vida ja esta cheia'
                if estado['vidas'] < estado['max_vidas']:
                    estado['vidas'] = estado['vidas'] + 1
                    estado['mensagem'] = 'voce ganhou uma vida!'
                    
        if objeto['posicao'] == estado['pos_jogador']:
                    if objeto['tipo'] == ESPINHO:
                        if estado['vidas'] > 0:
                            estado['vidas'] = estado['vidas'] -1
                            estado['mensagem'] = 'voce perdeu uma vida!'
        
                             
                            

    if estado['vidas'] == 0:
        estado['tela_atual'] = SAIR

    # Mude o valor da chave 'tela_atual' para mudar de tela
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR