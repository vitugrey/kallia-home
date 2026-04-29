import os
import cv2
from django.conf import settings
from users.models import Profile, FaceData

class CreateUserService:
    @staticmethod
    def execute(name: str, face_image_bgr=None):
        """
        Orquestra o primeiro cadastro do usuário.
        Recebe o nome e a foto de referência capturada pelo app-vision.
        """
        # 1. Cria o Profile do usuário
        profile = Profile.objects.create(name=name)
        print(f"[CreateUserService] Perfil de '{name}' criado com ID: {profile.id}")

        # 2. Salva a imagem facial se fornecida
        if face_image_bgr is not None:
            # Cria a pasta de destino (ex: media/faces) de forma segura
            faces_dir = os.path.join(settings.BASE_DIR, 'media', 'faces')
            os.makedirs(faces_dir, exist_ok=True)

            # Define o nome do arquivo usando o ID único para evitar conflitos
            filename = f"face_{profile.id}.jpg"
            file_path = os.path.join(faces_dir, filename)

            # Grava fisicamente no disco
            cv2.imwrite(file_path, face_image_bgr)

            # 3. Registra o FaceData atrelado ao Profile
            FaceData.objects.create(
                profile=profile,
                image_path=file_path
            )
            print(f"[CreateUserService] Foto salva e vinculada em: {file_path}")

        # 4. (Futuro) Aqui nós chamaremos o serviço de TTS para gerar o áudio:
        # audio_path = TTSService.generate_greeting(f"Olá {name}, que bom te ver!")
        # profile.greeting_audio_path = audio_path
        # profile.save()

        return profile
