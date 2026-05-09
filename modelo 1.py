from gpiozero import LED, Button
from time import sleep, time

verde = LED(17)
amarelo = LED(18)
vermelho = LED(23)

pp1 = Button(1, bounce_time=0.2)
pc1 = Button(12, bounce_time=0.2)


pedido_pedestre = False


def botao_pressionado():
    global pedido_pedestre
    pedido_pedestre = True
    print("\nBotão de pedestre detectado no Modelo 1")


pp1.when_pressed = botao_pressionado
pc1.when_pressed = botao_pressionado



def set_semaforop(v, a, r):
    verde.value = v
    amarelo.value = a
    vermelho.value = r



def semaforo_modelo1():
    global pedido_pedestre

    while True:
        # Verde
        pedido_pedestre = False
        set_semaforop(1, 0, 0)

        inicio = time()

        while True:
            tempo = time() - inicio
            print(f"\rVerde: {tempo:.1f}s            ", end="")

            if pedido_pedestre and tempo >= 5:
                break

            if tempo >= 10:
                break

            sleep(0.1)
        
        # Amarelo
        inicio = time()
        set_semaforop(0, 1, 0)
        while True:
            tempo = time() - inicio
            print(f"\rAmarelo: {tempo:.1f}s          ", end="")
            if tempo >= 2:
                break
                  
        # Vermelho
        inicio = time()
        set_semaforop(0, 0, 1)
        while True:
            tempo = time() - inicio
            print(f"\rVermelho: {tempo:.1f}s         ", end="")
            if tempo >= 10:
                break


try:
    semaforo_modelo1()

except KeyboardInterrupt:
    set_semaforop(0, 0, 0)
    print("\nPrograma encerrado")