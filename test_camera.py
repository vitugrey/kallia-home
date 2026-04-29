import cv2
import time
import sys

def test_camera():
    print("Iniciando teste da câmera...")
    # '0' geralmente é a câmera principal. 
    # Em alguns Raspberry Pis com módulo oficial, pode ser necessário testar índices 0, 1 ou usar 'rpicam' (libcamera) dependendo do OS.
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("ERRO: Não foi possível acessar a câmera (índice 0).")
        print("Verifique se ela está conectada fisicamente e ativada nas configurações do Raspberry Pi.")
        sys.exit(1)

    print("Câmera acessada com sucesso! Aguardando 2 segundos para o sensor ajustar o brilho e o foco...")
    time.sleep(2) 
    
    ret, frame = cap.read()
    
    if ret:
        filename = "test_capture.jpg"
        cv2.imwrite(filename, frame)
        print(f"SUCESSO! Uma foto foi tirada e salva como '{filename}' na pasta atual.")
        print("Dica: você pode transferir essa foto para o seu PC ou abri-la para ver se a imagem está nítida e no ângulo certo.")
    else:
        print("ERRO: A câmera foi reconhecida, mas o OpenCV não conseguiu capturar o frame/imagem.")
        
    cap.release()

if __name__ == "__main__":
    test_camera()
