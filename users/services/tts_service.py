import os
from django.conf import settings
from datetime import datetime

class TTSService:
    @staticmethod
    def generate_greeting(profile_name):
        """
        Gera um áudio de cumprimento usando o Edge TTS da Microsoft (Neural Voice).
        Salva na pasta media/audio/ e retorna a URL.
        """
        # Limpa o nome para virar nome de arquivo válido
        safe_name = profile_name.replace(" ", "_").lower()
        
        # Descobre qual é o período do dia para a saudação
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
        
        audio_dir = os.path.join(settings.BASE_DIR, 'media', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        # Salva um cache diferente para cada período do dia
        filename = f"greeting_{period}_{safe_name}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        # Se o áudio já foi gerado antes para esse nome neste período, reaproveita!
        if os.path.exists(filepath):
            return f"/media/audio/{filename}"
            
        # Gera novo áudio com a voz feminina (Kallia)
        text = f"{greeting}, {profile_name}."
        os.system(f'edge-tts --text "{text}" --voice pt-BR-FranciscaNeural --write-media "{filepath}"')
        
        return f"/media/audio/{filename}"
