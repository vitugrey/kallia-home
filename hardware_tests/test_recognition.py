import os
import sys
import django
import time
from picamera2 import Picamera2

# Inicializar o Django
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from vision.services.face_recognition_service import FaceRecognitionService

def run_recognition_test():
    print("=== INICIANDO INTELIGÊNCIA ARTIFICIAL: RECONHECIMENTO FACIAL ===")
    
    # Inicia o Serviço de Visão (ele vai carregar as fotos do banco automaticamente)
    recognition_service = FaceRecognitionService()
    
    # Liga a Câmera
    picam2 = None
    try:
        print("\nLigando a Picamera2...")
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())
        picam2.start()
        
        print("Aguardando 2 segundos para focar e olhar pra você...")
        time.sleep(2)
        
        print("Capturando frame...")
        # A biblioteca picamera2 já tira em RGB e formato numpy, que é perfeito para a IA.
        # No entanto, a nossa função FaceRecognitionService pede BGR (formato do OpenCV).
        # Vamos passar direto, ou podemos apenas simular o BGR
        import cv2
        rgb_image = picam2.capture_array()
        bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
        
        # Pede para a Inteligência Artificial tentar achar quem está na foto
        print("Enviando foto para o cérebro analisar...")
        rostos_reconhecidos = recognition_service.recognize_frame(bgr_image)
        
        if not rostos_reconhecidos:
            print(">>> Resultado: DESCONHECIDO (Não achei ninguém que eu conheça na imagem)")
        else:
            for perfil in rostos_reconhecidos:
                print(f">>> Resultado: BEM-VINDO DE VOLTA, {perfil.name.upper()}! (Perfil ID: {perfil.id})")
                
    except Exception as e:
        print(f"ERRO CRÍTICO: {e}")
    finally:
        if picam2:
            try:
                picam2.stop()
            except:
                pass

if __name__ == "__main__":
    run_recognition_test()
