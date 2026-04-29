import os
import cv2
import face_recognition
from users.models import Profile, FaceData

class FaceRecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_profiles = []
        self._load_known_faces()

    def _load_known_faces(self):
        """
        Carrega as fotos do banco de dados (FaceData), 
        extrai as características matemáticas (embeddings) e guarda na memória RAM.
        Isso evita ler do HD toda vez que um frame for processado.
        """
        print("[FaceRecognitionService] Carregando rostos conhecidos do banco...")
        all_face_data = FaceData.objects.select_related('profile').all()
        
        for face_data in all_face_data:
            if face_data.image_path and os.path.exists(face_data.image_path):
                # Carrega a imagem nativamente com a biblioteca (lê em RGB)
                image = face_recognition.load_image_file(face_data.image_path)
                
                # Extrai o vetor de 128 dimensões do rosto. 
                # Pega apenas o primeiro rosto (índice 0) encontrado na foto de cadastro
                encodings = face_recognition.face_encodings(image)
                if encodings:
                    self.known_face_encodings.append(encodings[0])
                    self.known_face_profiles.append(face_data.profile)
                else:
                    print(f"  -> Aviso: Nenhum rosto claro na foto do perfil {face_data.profile.name}")
            else:
                print(f"  -> Aviso: Foto não encontrada para {face_data.profile.name}")
                
        print(f"[FaceRecognitionService] {len(self.known_face_encodings)} rostos carregados na memória com sucesso!")

    def recognize_frame(self, frame_bgr):
        """
        Recebe um frame da câmera, procura rostos e compara com o banco.
        :param frame_bgr: Numpy array da imagem (OpenCV/Picamera2)
        :return: Lista de Profiles que foram reconhecidos nesta imagem.
        """
        # A biblioteca face_recognition precisa de cores no formato RGB
        rgb_frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        
        # Acha AS COORDENADAS de todos os rostos no frame
        face_locations = face_recognition.face_locations(rgb_frame)
        
        if not face_locations:
            return [] # Nenhum rosto na frente do espelho
            
        # Extrai os vetores matemáticos apenas dos rostos detectados agora
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        recognized_profiles = []
        
        for face_encoding in face_encodings:
            # Compara este rosto da câmera com todos os salvos na memória
            # tolerance=0.55 é um bom balanço entre falso positivo e falso negativo (o padrão é 0.6)
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance=0.55)
            
            # Se deu True em algum match, significa que achou o dono do rosto!
            if True in matches:
                first_match_index = matches.index(True)
                matched_profile = self.known_face_profiles[first_match_index]
                recognized_profiles.append(matched_profile)
                
        return recognized_profiles
