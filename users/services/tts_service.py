import os
from django.conf import settings

class TTSService:
    @staticmethod
    def generate_greeting(profile_name):
        """
        Gera um áudio de cumprimento usando o Edge TTS da Microsoft (Neural Voice).
        Salva na pasta media/audio/ e retorna a URL.
        """
        # Limpa o nome para virar nome de arquivo válido
        safe_name = profile_name.replace(" ", "_").lower()
        
        audio_dir = os.path.join(settings.BASE_DIR, 'media', 'audio')
        os.makedirs(audio_dir, exist_ok=True)
        
        filename = f"greeting_{safe_name}.mp3"
        filepath = os.path.join(audio_dir, filename)
        
        # Se o áudio já foi gerado antes para esse nome, reaproveita para ser rápido!
        if os.path.exists(filepath):
            return f"/media/audio/{filename}"
            
        # Gera novo áudio (Voz do Antonio é muito natural em pt-BR)
        # O Edge TTS aceita o comando via terminal, o que facilita pra gente chamar sincrono aqui
        text = f"Bem vindo de volta, {profile_name}."
        os.system(f'edge-tts --text "{text}" --voice pt-BR-AntonioNeural --write-media "{filepath}"')
        
        return f"/media/audio/{filename}"
