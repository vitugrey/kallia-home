from picamera2 import Picamera2
import time
import cv2
import numpy as np

def test_face_detection():
    print("Iniciando a câmera para detectar rosto...")
    picam2 = None
    try:
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())
        picam2.start()
        
        print("Aguardando 2 segundos para o sensor focar...")
        time.sleep(2)
        
        print("Capturando frame...")
        # array_capture retorna um numpy array. Por padrão, em 'still', é RGB.
        image_rgb = picam2.capture_array()
        
        print(f"Frame capturado! Resolução: {image_rgb.shape}")
        
        # Converter RGB para BGR (padrão OpenCV) e depois para Cinza (para a detecção)
        image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        
        # Carregar o classificador padrão de rostos do OpenCV
        print("Procurando rostos na imagem...")
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Detectar rostos
        # scaleFactor e minNeighbors ajudam na precisão
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        
        if len(faces) == 0:
            print("Nenhum rosto foi detectado na imagem. Tente ficar mais de frente para a luz.")
            # Salvar a imagem do mesmo jeito para debug
            cv2.imwrite("debug_rosto.jpg", image_bgr)
            print("Imagem salva como 'debug_rosto.jpg' para você ver o que a câmera viu.")
        else:
            print(f"SUCESSO! {len(faces)} rosto(s) detectado(s)!")
            
            # Desenhar um retângulo verde ao redor de cada rosto
            for (x, y, w, h) in faces:
                cv2.rectangle(image_bgr, (x, y), (x+w, y+h), (0, 255, 0), 3)
                
            cv2.imwrite("sucesso_rosto.jpg", image_bgr)
            print("Imagem salva como 'sucesso_rosto.jpg' com marcações verdes nos rostos!")
            
    except Exception as e:
        print(f"ERRO: {e}")
    finally:
        if picam2:
            try:
                picam2.stop()
            except:
                pass

if __name__ == "__main__":
    test_face_detection()
