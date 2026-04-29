from django.db import models
import uuid

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Nome")
    greeting_audio_path = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Caminho do Áudio de Cumprimento",
        help_text="Caminho para o arquivo gerado pelo TTS."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="devices")
    mac_address = models.CharField(max_length=17, unique=True, verbose_name="Endereço MAC")
    last_ip = models.GenericIPAddressField(blank=True, null=True, verbose_name="Último IP Conhecido")
    date_connected = models.DateTimeField(auto_now=True, verbose_name="Última Conexão")

    def __str__(self):
        return f"{self.mac_address} ({self.profile.name})"

class FaceData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="face_data")
    image_path = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name="Caminho da Foto de Referência"
    )
    embedding = models.JSONField(
        blank=True, 
        null=True, 
        verbose_name="Embeddings (Vetores do Rosto)",
        help_text="Representação matemática do rosto usada para o reconhecimento rápido."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FaceData de {self.profile.name}"
