import time
from gpiozero import OutputDevice, Button
from src.hardware import M2_BIT0, M2_BIT1, M2_BIT2, M2_PED_PRINCIPAL, M2_PED_CRUZAMENTO

class Modelo2:
    def __init__(self):
        self.bits = [OutputDevice(M2_BIT0), OutputDevice(M2_BIT1), OutputDevice(M2_BIT2)]
        self.btn_principal = Button(M2_PED_PRINCIPAL, bounce_time=0.2)
        self.btn_cruzamento = Button(M2_PED_CRUZAMENTO, bounce_time=0.2)
        
        self.solicitacao_principal = False
        self.solicitacao_cruzamento = False
        
        self.btn_principal.when_pressed = lambda: self._registrar_pedido("principal")
        self.btn_cruzamento.when_pressed = lambda: self._registrar_pedido("cruzamento")
        
        self.estado = 1 # Estado inicial
        self.inicio_estado = time.time()
        self.running = True

    def _registrar_pedido(self, origem):
        print(f"[Modelo 2] Botão de pedestre detectado ({origem})!")
        if origem == "principal": self.solicitacao_principal = True
        else: self.solicitacao_cruzamento = True

    def stop(self):
        self.running = False
        for bit in self.bits:
            bit.off()

    def enviar_codigo(self, codigo):
        self.bits[0].value = (codigo >> 0) & 1
        self.bits[1].value = (codigo >> 1) & 1
        self.bits[2].value = (codigo >> 2) & 1

    def run(self):
        while self.running:
            # Estado 1: Via principal verde / Via cruzamento vermelho
            self.solicitacao_principal = False
            self._esperar_estado("Principal VERDE / Cruzamento VERMELHO", 1, 10, 20, "principal")
            if not self.running: break

            # Estado 2: Principal amarelo / Cruzamento vermelho
            self._estado_fixo("Principal AMARELO / Cruzamento VERMELHO", 2, 2)
            if not self.running: break

            # Estado 4: Ambos vermelhos
            self._estado_fixo("Principal VERMELHO / Cruzamento VERMELHO", 4, 2)
            if not self.running: break

            # Estado 5: Principal vermelho / Cruzamento verde
            self.solicitacao_cruzamento = False
            self._esperar_estado("Principal VERMELHO / Cruzamento VERDE", 5, 5, 10, "cruzamento")
            if not self.running: break

            # Estado 6: Principal vermelho / Cruzamento amarelo
            self._estado_fixo("Principal VERMELHO / Cruzamento AMARELO", 6, 2)
            if not self.running: break

            # Estado 4: Ambos vermelhos
            self._estado_fixo("Principal VERMELHO / Cruzamento VERMELHO", 4, 2)

    def _esperar_estado(self, nome, codigo, tempo_minimo, tempo_maximo, tipo_verde):
        self.enviar_codigo(codigo)
        inicio = time.time()
        while self.running:
            tempo = time.time() - inicio
            if tempo >= tempo_minimo:
                if tipo_verde == "principal" and self.solicitacao_principal:
                    break
                if tipo_verde == "cruzamento" and self.solicitacao_cruzamento:
                    break
            if tempo >= tempo_maximo:
                break
            time.sleep(0.1)

    def _estado_fixo(self, nome, codigo, duracao):
        self.enviar_codigo(codigo)
        inicio = time.time()
        while self.running:
            if time.time() - inicio >= duracao:
                break
            time.sleep(0.1)
