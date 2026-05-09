import time
from gpiozero import LED, Button
from src.hardware import M1_VERDE, M1_AMARELO, M1_VERMELHO, M1_PED_PRINCIPAL, M1_PED_CRUZAMENTO

class Modelo1:
    def __init__(self):
        self.verde = LED(M1_VERDE)
        self.amarelo = LED(M1_AMARELO)
        self.vermelho = LED(M1_VERMELHO)
        self.btn_principal = Button(M1_PED_PRINCIPAL, bounce_time=0.2)
        self.btn_cruzamento = Button(M1_PED_CRUZAMENTO, bounce_time=0.2)
        
        self.solicitacao = False
        self.btn_principal.when_pressed = self._registrar_pedido
        self.btn_cruzamento.when_pressed = self._registrar_pedido
        
        self.estado = "VERDE"
        self.inicio_estado = time.time()
        self.running = True

    def _registrar_pedido(self):
        print("[Modelo 1] Botão de pedestre detectado!")
        self.solicitacao = True

    def stop(self):
        self.running = False
        self.verde.off()
        self.amarelo.off()
        self.vermelho.off()

    def run(self):
        while self.running:
            agora = time.time()
            decorrido = agora - self.inicio_estado

            if self.estado == "VERDE":
                self.verde.on()
                self.amarelo.off()
                self.vermelho.off()
                if (decorrido >= 5 and self.solicitacao) or decorrido >= 10:
                    self.estado = "AMARELO"
                    self.solicitacao = False
                    self.inicio_estado = time.time()
            
            elif self.estado == "AMARELO":
                self.verde.off()
                self.amarelo.on()
                self.vermelho.off()
                if decorrido >= 2:
                    self.estado = "VERMELHO"
                    self.inicio_estado = time.time()
            
            elif self.estado == "VERMELHO":
                self.verde.off()
                self.amarelo.off()
                self.vermelho.on()
                if decorrido >= 10:
                    self.estado = "VERDE"
                    self.inicio_estado = time.time()
            
            time.sleep(0.1)
