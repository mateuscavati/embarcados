import threading
import time
from src.modelo1 import Modelo1
from src.modelo2 import Modelo2

def main():
    m1 = Modelo1()
    m2 = Modelo2()

    thread1 = threading.Thread(target=m1.run)
    thread2 = threading.Thread(target=m2.run)

    thread1.start()
    thread2.start()

    try:
        while thread1.is_alive() or thread2.is_alive():
            thread1.join(timeout=0.1)
            thread2.join(timeout=0.1)
    except KeyboardInterrupt:
        print("\nEncerrando o programa...")
        m1.stop()
        m2.stop()
    
    thread1.join()
    thread2.join()
    print("Programa finalizado.")

if __name__ == "__main__":
    main()
