# Controle de Semáforo (Fundamentos de Sistemas Embarcados)

Este projeto implementa dois modelos de controle de semáforo para Raspberry Pi, utilizando threads para execução simultânea e independente.

## Estrutura do Projeto
- `src/main.py`: Ponto de entrada que gerencia as threads dos dois modelos.
- `src/modelo1.py`: Semáforo simples com 3 LEDs e botão de pedestre.
- `src/modelo2.py`: Semáforo controlado por bits (máquina de estados avançada) com tempos variáveis.
- `src/hardware.py`: Configuração centralizada dos pinos GPIO.

## Instalação
1. Clone o repositório.
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução
Para executar os modelos:
```bash
python3 -m src.main
```

## Funcionalidades Implementadas
- **Execução Simultânea:** Uso de `threading` para rodar ambos os semáforos ao mesmo tempo.
- **Encerramento Gracioso:** Captura de `Ctrl+C` para desligar todos os LEDs e saídas antes de sair.
- **Lógica de Pedestres:**
  - **Modelo 1:** Reduz o tempo de verde de 10s para 5s se o botão for pressionado.
  - **Modelo 2:** Tempos variáveis (10-20s na principal, 5-10s no cruzamento) baseados em demanda.
- **Debounce:** Tratamento de ruído nos botões via `gpiozero`.
