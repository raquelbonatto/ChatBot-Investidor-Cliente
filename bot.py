import tweepy
import time
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Configurar credenciais da API do Twitter/X
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
bearer_token = os.getenv("BEARER_TOKEN")

# Autenticação com a API v2 do Twitter/X
client = tweepy.Client(
    bearer_token=bearer_token,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Autenticação com a API v1.1 para envio de DMs
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Estado para rastrear a conversa
user_state = {}

def send_dm(user_id, message):
    """Função para enviar DM para um usuário"""
    try:
        client.create_direct_message(participant_id=user_id, text=message)
        print(f"DM enviada para {user_id}: {message}")
    except Exception as e:
        print(f"Erro ao enviar DM: {e}")

def handle_dm(dm):
    """Função para processar DMs recebidas"""
    sender_id = dm.message_create['sender_id']
    message = dm.message_create['message_data']['text'].lower().strip()

    # Ignorar mensagens do próprio bot
    if sender_id == client.get_me().data.id:
        return

    # Verificar estado da conversa
    if sender_id not in user_state:
        # Primeira mensagem: pedir idioma
        user_state[sender_id] = "awaiting_language"
        send_dm(sender_id, "Escolha o idioma: Português ou Inglês")
    elif user_state[sender_id] == "awaiting_language":
        # Processar escolha do idioma
        if message in ["português", "portugues"]:
            user_state[sender_id] = "awaiting_role"
            send_dm(sender_id, (
                "Raquel Bonatto, Criatividade aliada à tecnologia.\n\n"
                "Raquel Bonatto é modelo, publicitária, programadora de computadores, "
                "digital influencer e microempreendedora individual. Atua há mais de 20 anos no mercado.\n\n"
                "Você deseja ser:\n- Cliente\n- Investidor"
            ))
        elif message == "inglês" or message == "ingles":
            user_state[sender_id] = "awaiting_role"
            send_dm(sender_id, (
                "Raquel Bonatto, Creativity combined with technology.\n\n"
                "Raquel Bonatto is a model, advertiser, computer programmer, digital influencer, "
                "and individual micro-entrepreneur. She has been active in the market for over 20 years.\n\n"
                "Do you want to be:\n- Client\n- Investor"
            ))
        else:
            send_dm(sender_id, "Por favor, escolha: Português ou Inglês")
    elif user_state[sender_id] == "awaiting_role":
        # Processar escolha de Cliente ou Investidor
        if message == "cliente":
            user_state[sender_id] = "awaiting_service"
            send_dm(sender_id, (
                "Para cliente, escolha o serviço:\n"
                "- Modelo\n"
                "- Digital influencer\n"
                "- Consultoria publicidade\n"
                "- Consultoria marketing digital\n"
                "- Editoração\n"
                "- Direção de arte\n"
                "- Programação de computadores\n"
                "- Atualização de sites\n"
                "- Promoção de criptoativos\n\n"
                "Solicite um orçamento"
            ))
        elif message == "investidor":
            user_state[sender_id] = "awaiting_meeting"
            send_dm(sender_id, (
                "Seja um investidor e tenha até 29% de Retorno sobre o seu investimento.\n"
                "Agendar uma reunião."
            ))
        else:
            send_dm(sender_id, "Por favor, escolha: Cliente ou Investidor")
    elif user_state[sender_id] == "awaiting_service":
        # Processar escolha do serviço
        services = [
            "modelo", "digital influencer", "consultoria publicidade",
            "consultoria marketing digital", "editoração", "direção de arte",
            "programação de computadores", "atualização de sites", "promoção de criptoativos"
        ]
        if message in services:
            send_dm(sender_id, f"Você escolheu: {message}. Por favor, envie detalhes do projeto para um orçamento personalizado.")
            user_state[sender_id] = "awaiting_details"
        else:
            send_dm(sender_id, "Por favor, escolha um serviço válido da lista.")
    elif user_state[sender_id] == "awaiting_meeting":
        # Processar agendamento de reunião
        send_dm(sender_id, "Por favor, envie sua disponibilidade para agendarmos a reunião.")
        user_state[sender_id] = "awaiting_details"

# Função para monitorar DMs
def check_dms():
    last_checked = None
    while True:
        try:
            dms = client.get_direct_messages()
            for dm in dms.data:
                if not last_checked or dm.created_at > last_checked:
                    handle_dm(dm)
            last_checked = dms.data[0].created_at if dms.data else last_checked
        except Exception as e:
            print(f"Erro ao verificar DMs: {e}")
        time.sleep(60)  # Verificar a cada 60 segundos

if __name__ == "__main__":
    check_dms()
