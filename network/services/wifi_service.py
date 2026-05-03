import os
import qrcode
from django.conf import settings

class WifiGuestService:
    @staticmethod
    def generate_guest_qr_code(ssid="MinhaCasa_Kallia", password="senha_super_secreta"):
        """
        Gera um QR Code no padrão WPA/WPA2 para conexão automática em redes Wi-Fi.
        Retorna a URL da imagem para o frontend renderizar.
        """
        # String de formatação padrão para Wi-Fi
        wifi_data = f"WIFI:S:{ssid};T:WPA;P:{password};;"
        
        # Garante que o diretório de media/network exista
        network_dir = os.path.join(settings.BASE_DIR, 'media', 'network')
        os.makedirs(network_dir, exist_ok=True)
        
        filename = "guest_wifi_qr.png"
        filepath = os.path.join(network_dir, filename)
        
        # Se o arquivo não existir ou se quisermos forçar a geração:
        if not os.path.exists(filepath):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(wifi_data)
            qr.make(fit=True)

            # Gera a imagem do QR com cores que combinam com o dark mode do espelho (fundo transparente/preto)
            # Para o celular ler bem, o QR code geralmente precisa de alto contraste (branco no preto ou preto no branco).
            # Vamos gerar o clássico fundo branco e linha preta para máxima legibilidade pelos celulares.
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(filepath)
            
        return f"/media/network/{filename}"
