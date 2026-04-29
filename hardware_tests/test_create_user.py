import os
import sys
import cv2
import django

# Adiciona a raiz do projeto ao path do Python para o Django encontrar as configurações
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Inicia o Django para conseguirmos usar o banco de dados fora de uma request web
django.setup()

from users.services.create_user_service import CreateUserService
from users.models import Profile

def test_user_creation():
    print("=== INICIANDO TESTE INTEGRADOR: BANCO DE DADOS + OPENCV ===")
    
    # 1. Procurar a foto do teste anterior (sucesso_rosto.jpg)
    paths_to_try = [
        os.path.join(project_root, "sucesso_rosto.jpg"),
        os.path.join(project_root, "hardware_tests", "sucesso_rosto.jpg")
    ]
    
    img = None
    for path in paths_to_try:
        if os.path.exists(path):
            print(f"Foto encontrada em: {path}")
            img = cv2.imread(path)
            break
            
    if img is None:
        print("Aviso: A foto 'sucesso_rosto.jpg' não foi encontrada. O perfil será criado SEM foto apenas para testar o banco de dados.")
    
    # 2. Chamar a nossa lógica de negócio (Serviço)
    print("\nChamando CreateUserService para cadastrar 'Vitor'...")
    profile = CreateUserService.execute(name="Vitor", face_image_bgr=img)
    
    # 3. Validar se gravou mesmo no SQLite
    print("\n=== VERIFICANDO O BANCO DE DADOS ===")
    todos_perfis = Profile.objects.all()
    print(f"Total de usuários no banco: {todos_perfis.count()}")
    
    for p in todos_perfis:
        print(f"\nUsuário: {p.name} (ID: {p.id})")
        faces = p.face_data.all()
        if not faces:
            print("  -> Nenhuma foto/FaceData registrada.")
        else:
            for face in faces:
                print(f"  -> FaceData ID: {face.id}")
                print(f"  -> Caminho da Foto no DB: {face.image_path}")
                # Validar se o arquivo realmente foi parar na pasta /media/faces
                if os.path.exists(face.image_path):
                    print("  -> [VERIFICADO] A foto física existe no disco de forma segura!")
                else:
                    print("  -> [FALHA] O caminho está no banco, mas o arquivo físico sumiu.")

if __name__ == "__main__":
    test_user_creation()
