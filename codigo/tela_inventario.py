from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):
    
    mensagem = estado['mensagem_inventario']
    motor.preenche_fundo(janela, BRANCO)

    motor.desenha_string(janela, 1, 1, 'INVENTARIO', BRANCO, PRETO)
    motor.desenha_string(janela, 1, 2, '----------', BRANCO, PRETO)
    motor.desenha_string(janela, 0, altura - 1, mensagem, BRANCO, PRETO)
    

    linha = 4
    for item in estado['inventario']:
        if item == ESPADA:
            motor.desenha_string(janela, 1, linha, item + '    pressione p para usar', BRANCO, PRETO)
        if item == ESCUDO:
            motor.desenha_string(janela, 1, linha, item + '    pressione o para usar', BRANCO, PRETO)
        linha = linha + 1

    if len(estado['inventario']) == 0:
        motor.desenha_string(janela, 1, 4, 'vazio', BRANCO, PRETO)

    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla_apertada):
    if tecla_apertada == 'i':
        estado['tela_atual'] = estado['tela_anterior']
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR
    if tecla_apertada == 'p':
        if ESPADA in estado['inventario']:
            estado['tem_espada'] = True
            estado['espadas_usadas'] = estado['espadas_usadas'] + 1
            estado['inventario'].remove(ESPADA)
            estado['mensagem_inventario'] = 'espada ativada'
            if estado['espadas_usadas'] >= 2:
                estado['mensagem_inventario'] = 'duas espadas ativadas, voce luta melhor'
        else:
            estado['mensagem_inventario'] = 'voce nao tem espada'
    if tecla_apertada == 'o':
        if ESCUDO in estado['inventario']:
            estado['inventario'].remove(ESCUDO)
            estado['max_vidas'] = estado['max_vidas'] + 2
            estado['vidas'] = estado['vidas'] + 2
            estado['mensagem_inventario'] = 'escudo ativado, voce ganhou 2 vidas'
        else:
            estado['mensagem_inventario'] = 'voce nao tem escudo'
