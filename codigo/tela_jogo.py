from constantes import *  # Você pode usar as constantes definidas em constantes.py, se achar útil
                          # Por exemplo, usar a constante CORACAO é o mesmo que colocar a string '❤'
                          # diretamente no código
import motor_grafico as motor  # Utilize as funções do arquivo motor_grafico.py para desenhar na tela
                               # Por exemplo: motor.preenche_fundo(janela, [0, 0, 0]) preenche o fundo de preto
from inicializacao import gera_posicao_desocupada

def desenha_tela(janela, estado, altura_tela, largura_tela):
    # Utilize o dicionário estado para saber onde o jogador e os outros objetos estão.
    # Por exemplo, para saber a posição do jogador, use estado['pos_jogador']
    # O mapa esta armazenado em estado['mapa'].
    motor.preenche_fundo(janela, PRETO)
    obejetos = estado['objetos']
    mapa = estado['mapa']
    largura_mapa = len(mapa[0])
    altura_mapa = len(mapa)
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
            motor.desenha_string(janela, 0,altura_tela - 1, estado['mensagem'], PRETO, BRANCO )
            
    for objeto in obejetos:
        posicao = gera_posicao_desocupada(posiçoes,largura_mapa, altura_mapa)
        if objeto['tipo'] == CORACAO:
            motor.desenha_string(janela, posicao[0]+dx,posicao[1]+dy,objeto['tipo'], frente, VERMELHO )
        else:
            pass
    for objeto in obejetos:
            posicao = gera_posicao_desocupada(posiçoes,largura_mapa, altura_mapa)
            if objeto['tipo'] == ESPINHO:
                motor.desenha_string(janela, posicao[0]+dx,posicao[1]+dy,objeto['tipo'], frente, VERDE_ESCURO )
            else:
                pass

    

    
    # O seu código deve desenhar a tela do jogo aqui a partir dos valores no dicionário "estado"
    # APAGUE ESTA LINHA E A LINHA ABAIXO E ESCREVA SEU CÓDIGO AQUI


    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla):
    # O seu código deve atualizar o dicionário "estado" com base na tecla apertada pelo jogador
    # Por exemplo, se o jogador apertar a seta para a esquerda (o valor da variável será "ESQUERDA"), 
    # o seu código deve atualizar o dicionário estado['pos_jogador'][0] -= 1

    # Mude o valor da chave 'tela_atual' para mudar de tela
    
    # Começamos apagando a mensagem anterior, pois ela já foi mostrada no frame anterior
    estado['mensagem'] = ''

    # Escreva seu código para atualizar o dicionário "estado" com base na tecla apertada pelo jogador aqui
    # APAGUE ESTA LINHA E ESCREVA SEU CÓDIGO AQUI

    # Ao apertar a tecla 'i', o jogador deve ver o inventário
    if tecla == 'i':
        estado['tela_atual'] = TELA_INVENTARIO
    # Termina o jogo se o jogador apertar ESC ou 'q'
    elif tecla == motor.ESCAPE or tecla =='q':
        estado['tela_atual'] = SAIR