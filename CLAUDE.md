# Projeto Kallia-Home

Esté é um projeto grande que não envolverar linhas de codigo, mas sim um porjeto com hardwares diferentes do comum.
Será um espelho inteligente (smart mirror) com raspberry pi 4 e uma tela touchscreen de 7 polegadas, com alto falante, microfone e webcam. O sistema começará mostrando informações mais triviais como horário atual, previsão do tempo, notícias, criar lembretes, agenda, etc.. Só depois ele começará a ficar mais inteligente, com IA e tal.

## 1. Visão Geral da Arquitetura
A primeira interação do usuário com o smart mirror será a detecção facial para saber quem é que está interagindo com o espelho. Se for a primera interação é solicidado para que diga o nome dele, assim transcrevendo o nome e pegando a foto do rosto para salvar no banco de dados, dando um QRcode para conectar no WIFI da casa e vinculando o IP local e o MAC address do dispositivo ao seu nome. Caso seja um usuário recorrente, o sistema irá reconhecê-lo e irá cumprimentá-lo pelo nome, liberando as features do sistema (que explicarei mais abaixo).

O projeto terá um banco de dados com informações sobre o usuário.

Rodará um servidor web como interface e features do projeto

## 2. Stack Tecnológico

_(A ajustar conforme a realidade do projeto)_

- **Gerenciado de pacote:** uv
- **Backend:** Python + Django 
- **Banco de Dados:** SQLite para persistência
- **Visão Computacional:** Picamera2 (para acesso rápido via libcamera) + face_recognition (embeddings) + OpenCV (imagens/matrizes)
- **STT:** [faster_whisper ou assemblyai ou SpeechRecognition]
- **TTS:** [gTTS ou Edge-TTS ou qwen3TTS]
- **IA/Modelos:** Ollama (gpt-oss:120b-cloud)
- **Algums libs:** django, sqlite3, request, picamera2, opencv-python, pillow, face-recognition, mediapipe, assemblyai, faster-whisper, speech-recognition, edge-tts, pygame, qwen3, tavily, openai, ollama, qrcode, scapy


## 3. Lista de Compras (Hardware Essencial)

Para tornar o projeto físico uma realidade, precisaremos adquirir:

- **Computador:** Raspberry Pi 4 (Mínimo 4GB de RAM, mas 8GB é o ideal para IA)
- **Armazenamento:** Cartão MicroSD (32GB ou 64GB, preferencialmente classe A2 para leitura/escrita rápida)
- **Energia:** Fonte de alimentação oficial Raspberry Pi (5V/3A - 15W) ou superior
- **Display:** Tela de 7 polegadas, resolução 1024x600, display IPS LCD (define as fronteiras do layout CSS do Front-End)
- **Visão:** Câmera Módulo oficial Raspberry (rpicam) ou Webcam USB de boa resolução (e com microfone embutido, preferencialmente)
- **Áudio In/Out:** Microfone USB (caso a webcam não tenha) e um Mini Alto-falante (conexão P2 ou USB)
- **Refrigeração:** Kit de dissipadores de calor e Cooler (ventoinha) 5V para ligação nos pinos GPIO
- **Estrutura:** Vidro espelhado de duas vias (Two-way mirror) e Moldura customizada (madeira, plástico ou acrílico)
- **Outros:** Cabos, adaptadores HDMI/MicroHDMI, e um hub USB com alimentação externa (importante se os periféricos puxarem muita energia e causarem subtensão)


## 4. Serviços, Jobs e Models de Cada App

### app-users
Responsável por gerenciar quem está na frente do espelho e seus dispositivos.

- **Models:** `Profile: Nome, caminho para o arquivo de áudio (paraTTS) de cumprimento personalizado.`, `Device: Vinculado a um Profile, contendo mac_address, last_ip e date_connected`, `FaceData: Caminho das fotos tiradas durante o onboarding ou embeddings (vetores) matemáticos do rosto.`
- **Serviços:** `CreateUserService: Orquestra o primeiro cadastro (recebe o nome, salva as fotos, gera a resposta de voz).` , `DeviceRegistrationService: Recebe um IP/MAC detectado na rede e vincula ao Profile detectado.`
- **Jobs:** Não há jobs contínuos pesados aqui, apenas as chamadas assíncronas para processar os áudios ou embeddings após o primeiro cadastro.

### app-vision
Lida exclusivamente com a câmera e detecção.

- **Models:** Geralmente não possui models no banco de dados. Ele apenas processa as imagens e consome os models do app users para bater os rostos.
- **Serviços:** `FaceRecognitionService: Pega o frame do picamera2, transforma os rostos em vetores e retorna o Profile do usuário (ou "Desconhecido").`, `StreamService: Gerencia a inicialização e o buffer da câmera garantindo que ele rode de forma otimizada no Pi sem travar o sistema.`
- **Jobs:** `vision_watcher_job: Esse é o processo contínuo (uma thread ou script secundário) que fica constantemente analisando o feed de vídeo.`

### app-network
Responsável por colocar o usuário na mesma rede e rastreá-lo.

- **Models:** `NetworkConfig: Pode guardar o SSID e a Senha da sua rede local (criptografados) para não ficarem expostos diretamente no código.`
- **Serviços:** `QRCodeGeneratorService: Monta a string do Wi-Fi e gera o arquivo PNG do QR Code na hora.`, `NetworkScanService: Executa varreduras na rede local (ex: usando arp -a ou scapy) para descobrir quem acabou de entrar.`
- **Jobs:** `arp_monitor_job: Quando um onboarding começa, esse job é acionado para ficar "escutando" a rede a cada 2 segundos. Assim que um novo IP/MAC aparece na tabela ARP do Raspberry Pi, ele captura esse dado, vincula ao usuário em frente ao espelho e encerra o job.`

### app-widgets ✅ (Concluído)
Os módulos visuais como clima, agenda e notícias.

- **Models:** `WidgetPreference: Tabela que liga um Profile a uma configuração.`
- **Serviços:** `WeatherFetcherService: Bate na API de clima (Open-Meteo) com Cache FileBased.`, `NewsFetcherService: Traz as manchetes do RSS do G1 com embaralhamento e cache.`
- **Jobs:** `update_widgets_job: Job contínuo que roda a cada hora limpando e atualizando o cache para a tela responder na velocidade da luz.`


---

## 5. "Common Hurdles" (Obstáculos Comuns) e Soluções Documentadas

Este é o nosso registro de aprendizado. Sempre que batermos a cabeça em um problema, documentamos a solução aqui.

1. **Subtensão (Undervoltage) e Queda de Energia**
 - **O Obstáculo**: O Raspberry Pi 4 precisa de energia estável (5V/3A). Ao ligar uma tela touchscreen de 7 polegadas, câmera e microfone diretamente nele, você pode ver um ícone de raio amarelo na tela, causando lentidão severa ou reinicializações aleatórias.
 - **A Solução**: Use uma fonte de alimentação oficial ou de alta qualidade (15W+). Se a tela puxar muita energia, alimente a tela separadamente com outra fonte ou use um Hub USB energizado.
 
2. **Aquecimento Térmico (Thermal Throttling)**
 - **O Obstáculo**: O processamento de reconhecimento facial contínuo faz a CPU do Pi trabalhar no limite. Dentro da caixa fechada de um espelho inteligente, a temperatura passa dos 80°C rápido, e o Pi corta o próprio desempenho para não queimar.
 - **A Solução**: Instalação obrigatória de dissipadores de calor e mais de uma ventoinha (cooler) de 5V ligada nos pinos GPIO. Deixar frestas de ventilação no case do espelho.

3. **Conflitos de Banco de Dados (SQLite Lock)**
 - **O Obstáculo**: O SQLite grava as coisas em um único arquivo local. Se o Job em background tentar salvar o log de um rosto reconhecido no exato milissegundo em que a View do Django tenta carregar a página de clima, você receberá o erro database is locked.
 - **A Solução**: Configurar o parâmetro timeout nas opções do banco de dados no settings.py do Django (ex: timeout: 20), dando tempo para as threads esperarem umas pelas outras, ou usar queries extremamente rápidas/em lote.

4. **O Bloqueio da Main Thread (Travamentos da Interface)**
 - **O Obstáculo**: Colocar o loop infinito da câmera (while True: capturar_frame()) dentro do ciclo de request/response padrão do Django fará o servidor congelar e o espelho parar de atualizar.
 - **A Solução**: Isolar a captura de vídeo. O script de visão computacional deve rodar em um processo separado (como um Job gerenciado pelo systemd ou Celery) e apenas enviar "sinais" (via WebSockets ou gravando no banco) para o Django ler.

5. **Reconhecimento facil e Captura de microfone**
 - **O Obstáculo**: Pessoa passa longe e a câmera captar o rosto e destravar o microfone, mas a pessoa só passou
 - **A Solução**: Colocar um periodo de tempo para a pessoa ficar no campo de visão e uma distância minima para começar a o reconhecimento do rosto e destravar o microfone. O mesmo serve para o deslog do usuário, colocar um tempo para deslogar do usuário. 

6. **Acesso à Câmera (libcamera) no Ambiente Virtual**
 - **O Obstáculo**: O Raspberry Pi usa a biblioteca do sistema `picamera2`, mas nosso projeto roda isolado dentro do ambiente virtual do `uv`. Se tentarmos rodar scripts lá dentro, ele dá "ModuleNotFoundError: picamera2".
 - **A Solução**: Precisamos criar nosso ambiente virtual ativando a flag `--system-site-packages` (ex: `uv venv --system-site-packages`). Assim, o Python do ambiente virtual consegue "enxergar" os drivers globais de hardware instalados via `apt` no Linux.

---

## 6. Design Patterns do Projeto

1. **Model-View-Template (MVT)**
 - O que é: É a variação do clássico MVC (Model-View-Controller) que o próprio Django utiliza por padrão.

 - Como se aplica no Kallia-Home: 
    - Model: Seus dados no SQLite (os perfis, o registro de IP/MAC do QR Code).
    - View: As funções em Python que recebem o pedido do espelho (ex: "carregar tela inicial") e buscam os dados.
    - Template: O HTML/CSS com fundo preto e texto branco que será renderizado no navegador Chromium em tela cheia.

2. **Service Layer (Camada de Serviço)**
    - O que é: Consiste em retirar as "regras de negócio" de dentro das Views do Django e colocá-las em classes ou funções separadas (os Services). As Views ficam "magras" e os Services fazem o trabalho pesado.
    - Como se aplica no Kallia-Home: Quando o usuário lê o QR Code, a lógica de varrer a rede (NetworkScanService), encontrar o MAC address e vinculá-lo a um perfil (DeviceRegistrationService) fica isolada. Se amanhã você quiser trocar a forma como rastreia a rede, você não mexe nas Views, apenas no Serviço.

3. **Singleton (Instância Única)**
    - O que é: Garante que uma classe tenha apenas uma única instância rodando em toda a aplicação e fornece um ponto global de acesso a ela.
    - Como se aplica no Kallia-Home: Câmera e Microfone. O hardware do Raspberry Pi não permite que dois processos abram a mesma câmera (via rpicam) ao mesmo tempo. Se o módulo de reconhecimento facial e o módulo de tirar foto tentarem acessar a câmera juntos, o sistema trava. Você cria uma classe CameraManager usando o padrão Singleton: quem precisar da imagem pede ao Manager, que gerencia uma única conexão física com o hardware.
   
4. **Observer / Publish-Subscribe (Event-Driven)**
    - O que é: Um objeto (o "Sujeito") mantém uma lista de dependentes (os "Observadores") e os notifica automaticamente sobre qualquer mudança de estado.
    - Como se aplica no Kallia-Home: Perfeito para o reconhecimento facial contínuo.
    - O script que analisa o vídeo (Job) atua como o Sujeito.
    - O frontend (a tela do espelho via WebSockets/HTMX) atua como o Observador.
    - Quando a IA detecta o rosto do "Vitor", ela "publica" um evento. A interface, que estava apenas "escutando", reage instantaneamente trocando o widget de clima neutro para "Bom dia, Vitor!". O backend não precisa ficar perguntando a cada segundo "tem alguém aí?".

5. **Facade (Fachada)**
    - O que é: Fornece uma interface unificada e simplificada para um conjunto de interfaces mais complexas em um subsistema.
    - Como se aplica no Kallia-Home: A detecção facial envolve capturar o frame do rpicam, converter a matriz de cores, passar pela rede neural do MediaPipe/OpenCV, extrair os landmarks do rosto e comparar com o banco de dados. Isso é muito código.
    - Você cria uma classe Facade chamada KalliaVision. O resto do seu sistema só precisará chamar KalliaVision.get_current_user(). Toda a complexidade matemática e de hardware fica escondida atrás dessa "fachada" limpa.
---



## 7. Checklist Pós-Implementação

Após cada nova sessão de codificação ou refatoração, verifique:

- [ ] **Teste do "Puxão de Tomada"**: Simule uma queda de energia tirando o espelho da tomada e ligando novamente. O sistema operacional (Raspberry Pi OS) deu boot, carregou o servidor Django e abriu o navegador em tela cheia automaticamente sem intervenção manual?
- [ ] **Teste Térmico (Thermal Throttling)**: Deixe o reconhecimento facial rodando continuamente por 2 horas. Acesse o terminal e verifique a temperatura (vcgencmd measure_temp). A temperatura se manteve abaixo de 75°C? Se estiver alta, melhore o sistema de ventilação do espelho.
- [ ] **Teste de Subtensão**: Durante o funcionamento máximo (câmera, tela no brilho máximo, IA processando), o ícone de "raio amarelo" (undervoltage) apareceu na tela em algum momento? Se sim, a fonte de energia precisa ser trocada.
- [ ] **Teste de Iluminação Variável**: A câmera consegue reconhecer o usuário "Vitor" tanto durante o dia (com luz natural) quanto à noite (apenas com a luz do próprio espelho e do quarto)?
- [ ] **Falsos Positivos**: O sistema lida corretamente quando duas pessoas aparecem na frente do espelho ao mesmo tempo? (Ex: cumprimenta apenas o usuário principal ou divide a tela).
- [ ] **Teste de Eco Acústico**: Quando o espelho "fala" (Text-to-Speech) cumprimentando o usuário, o microfone interno ignora esse áudio e não entra em loop ou tenta transcrever a própria fala?
- [ ] **Geração Dinâmica**: O QR Code gerado na tela foi lido com sucesso por pelo menos um dispositivo Android e um dispositivo iOS?
- [ ] **Captura de MAC/IP**: O network_watcher (Job em background) conseguiu capturar com precisão o IP e o MAC da pessoa que acabou de ler o QR Code no tempo estipulado?
- [ ] **Teste de Reconexão**: Quando um usuário já cadastrado sai de casa (desconecta do Wi-Fi) e volta horas depois, o espelho reconhece o dispositivo entrando na rede e atualiza o status de presença (caso você use essa métrica)?
- [ ] **Contraste no Vidro**: A cor de fundo do template base do Django está configurada como PRETO PURO (#000000)? Qualquer tom de cinza ficará visível através do vidro espelhado e estragará a ilusão.
- [ ] **Invisibilidade do Cursor**: O ponteiro do mouse está completamente oculto usando o pacote unclutter?
- [ ] **Prevenção de Hibernação**: O espelho ficou ligado por mais de 30 minutos sem que a tela "apagasse" sozinha por inatividade do protetor de tela (Screen Blanking/DPMS desativados)?
- [ ] **Limites de Tela**: Os widgets estão posicionados com margens de segurança para que não fiquem escondidos atrás das bordas internas da moldura de madeira/plástico?
- [ ] **Teste de Concorrência do SQLite**: Ao forçar múltiplas ações simultâneas (ex: atualizar o clima via web enquanto a câmera salva um novo rosto no banco de dados), não houve o erro database is locked?
- [ ] **Isolamento de Imagens**: As fotos de referência tiradas durante o onboarding estão sendo salvas em uma pasta segura (ex: media/faces/) e não estão acessíveis publicamente caso alguém descubra o IP do espelho na rede?
- [ ] **Rotação de Logs**: Os logs gerados pelo script de reconhecimento facial não estão crescendo indefinidamente e lotando o cartão SD (configuração de log rotation ativada)?

---

## 8. Regras de Colaboração (Nossa Conversa)

Para mantermos o projeto no trilho e nossa comunicação eficiente, seguiremos estas regras:

- **Passos Curtos:** Vamos implementar um sistema por vez. Não tentaremos fazer o app inteiro funcionar em um único script. Ex: primeiro a estrutura Django, depois a visão isolada, depois a integração.
- **Documentação Viva:** Qualquer nova biblioteca importante, mudança de arquitetura ou variável de ambiente será primeiramente anotada neste documento (`CLAUDE.md`).
- **Pequenos Testes Unitários/Scripts:** Antes de injetar regras pesadas no Django, faremos testes com scripts isolados (por exemplo, um `test_camera.py` no terminal) para garantir que a parte física/hardware do Raspberry Pi está respondendo.
- **Transparência:** Se um código der erro de "database is locked" ou falhar devido aos recursos limitados do Pi 4, reportarei o erro para decidirmos qual a melhor estratégia em vez de tentar silenciar o erro.