from constantes import *
import motor_grafico as motor


def desenha_tela(janela, estado, altura, largura):
    motor.preenche_fundo(janela, BRANCO)

    motor.desenha_string(janela, 1, 1, 'INVENTARIO', BRANCO, PRETO)
    motor.desenha_string(janela, 1, 2, '----------', BRANCO, PRETO)

    linha = 4
    for item in estado['inventario']:
        motor.desenha_string(janela, 1, linha, item, BRANCO, PRETO)
        linha = linha + 1

    if len(estado['inventario']) == 0:
        motor.desenha_string(janela, 1, 4, 'vazio', BRANCO, PRETO)

    motor.mostra_janela(janela)


def atualiza_estado(estado, tecla_apertada):
    if tecla_apertada == 'i':
        estado['tela_atual'] = estado['tela_anterior']
    elif tecla_apertada in (motor.ESCAPE, 'q'):
        estado['tela_atual'] = SAIR
