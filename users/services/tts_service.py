import os
from django.conf import settings
from datetime import datetime

class TTSService:
    @staticmethod
    def generate_greeting(profile_name, is_new_guest=False):
        """
        Gera um áudio de cumprimento usando o Edge TTS da Microsoft (Neural Voice).
        Salva na pasta media/audio/ e retorna a URL.
        """
        # Limpa o nome para virar nome de arquivo válido
        safe_name = profile_name.replace(" ", "_").lower()
        
        audio_dir = os.path.join(settings.BASE_DIR, 'media', 'audio')
        os.makedirs(audio_dir, exist_ok=True)

        if is_new_guest:
            # Mensagem exclusiva de primeiro acesso
            filename = f"greeting_new_guest_{safe_name}.mp3"
            filepath = os.path.join(audio_dir, filename)
            text = f"Olá {profile_name}, seja muito bem-vindo à nossa casa. Por favor, escaneie o código na tela para se conectar ao nosso Wi-Fi automaticamente."
        else:
            # Descobre qual é o período do dia para a saudação normal
            hour = datetime.now().hour
            if 5 <= hour < 12:
                greeting = "Bom dia"
                period = "manha"
            elif 12 <= hour < 18:
                greeting = "Boa tarde"
                period = "tarde"
            else:
                greeting = "Boa noite"
                period = "noite"
            
            # Salva um cache diferente para cada período do dia
            filename = f"greeting_{period}_{safe_name}.mp3"
            filepath = os.path.join(audio_dir, filename)
            text = f"{greeting}, {profile_name}."
        
        # Se o áudio já foi gerado antes para esse contexto, reaproveita!
        if os.path.exists(filepath):
            return f"/media/audio/{filename}"
            
        # Gera novo áudio com a voz feminina (Kallia)
        os.system(f'edge-tts --text "{text}" --voice pt-BR-FranciscaNeural --write-media "{filepath}"')
        
        return f"/media/audio/{filename}"
