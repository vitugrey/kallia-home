from picamera2 import Picamera2
import time

def test_picamera():
    print("Iniciando teste com a Picamera2...")
    picam2 = None
    try:
        picam2 = Picamera2()
        # Configura a câmera para capturar imagens estáticas (fotos)
        picam2.configure(picam2.create_still_configuration())
        picam2.start()
        
        print("Câmera acessada com sucesso! Aguardando 2 segundos para ajustar a luminosidade e o foco...")
        time.sleep(2)
        
        filename = "foto_via_picamera.jpg"
        picam2.capture_file(filename)
        
        print(f"SUCESSO! Uma foto foi tirada e salva como '{filename}' na pasta atual.")
        print("Essa abordagem (Picamera2) é a mais recomendada para as versões recentes do Raspberry Pi OS (Bullseye/Bookworm).")
        
    except Exception as e:
        print(f"ERRO ao testar a câmera: {e}")
    finally:
        if picam2:
            try:
                picam2.stop()
            except:
                pass

if __name__ == "__main__":
    test_picamera()
