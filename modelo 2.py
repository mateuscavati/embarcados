from gpiozero import LED, Button
from time import sleep, time

# Saídas - Modelo 2
bit0 = LED(24)
bit1 = LED(8)
bit2 = LED(7)

# Botões - Modelo 2
botao_ped_principal = Button(25, bounce_time=0.2)
botao_ped_cruzamento = Button(22, bounce_time=0.2)

pedido_principal = False
pedido_cruzamento = False


def limpar_linha():
    print("\r" + " " * 60, end="")


def enviar_codigo(codigo):
    bit0.value = codigo & 0b001
    bit1.value = (codigo >> 1) & 0b001
    bit2.value = (codigo >> 2) & 0b001


def botao_principal_pressionado():
    global pedido_principal
    pedido_principal = True
    print("\nBotão pedestre PRINCIPAL detectado")


def botao_cruzamento_pressionado():
    global pedido_cruzamento
    pedido_cruzamento = True
    print("\nBotão pedestre CRUZAMENTO detectado")


botao_ped_principal.when_pressed = botao_principal_pressionado
botao_ped_cruzamento.when_pressed = botao_cruzamento_pressionado


def esperar_estado(nome, codigo, tempo_minimo, tempo_maximo, tipo_verde=None):
    global pedido_principal, pedido_cruzamento

    enviar_codigo(codigo)
    inicio = time()

    while True:
        tempo = time() - inicio

        limpar_linha()
        print(f"\rEstado {codigo} - {nome}: {tempo:.1f}s", end="")

        if tempo >= tempo_minimo:
            if tipo_verde == "principal" and pedido_principal:
                break

            if tipo_verde == "cruzamento" and pedido_cruzamento:
                break

        if tempo >= tempo_maximo:
            break

        sleep(0.1)


def estado_fixo(nome, codigo, duracao):
    enviar_codigo(codigo)

    inicio = time()

    while True:
        tempo = time() - inicio

        limpar_linha()
        print(f"\rEstado {codigo} - {nome}: {tempo:.1f}s", end="")

        if tempo >= duracao:
            break

        sleep(0.1)


def semaforo_modelo2():
    global pedido_principal, pedido_cruzamento

    while True:
        

        # Estado 1: Via principal verde / Via cruzamento vermelho
        pedido_principal = False
        esperar_estado(
            nome="Principal VERDE / Cruzamento VERMELHO",
            codigo=1,
            tempo_minimo=10,
            tempo_maximo=20,
            tipo_verde="principal"
        )

        # Estado 2: Principal amarelo / Cruzamento vermelho
        estado_fixo(
            nome="Principal AMARELO / Cruzamento VERMELHO",
            codigo=2,
            duracao=2
        )

        # Estado 4: Ambos vermelhos
        estado_fixo(
            nome="Principal VERMELHO / Cruzamento VERMELHO",
            codigo=4,
            duracao=2
        )

        # Estado 5: Principal vermelho / Cruzamento verde
        pedido_cruzamento = False
        esperar_estado(
            nome="Principal VERMELHO / Cruzamento VERDE",
            codigo=5,
            tempo_minimo=5,
            tempo_maximo=10,
            tipo_verde="cruzamento"
        )

        # Estado 6: Principal vermelho / Cruzamento amarelo
        estado_fixo(
            nome="Principal VERMELHO / Cruzamento AMARELO",
            codigo=6,
            duracao=2
        )

        # Estado 4: Ambos vermelhos
        estado_fixo(
            nome="Principal VERMELHO / Cruzamento VERMELHO",
            codigo=4,
            duracao=2
        )


try:
    semaforo_modelo2()

except KeyboardInterrupt:
    enviar_codigo(0)
    limpar_linha()
    print("\nPrograma encerrado")