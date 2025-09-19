pip install tweepy

# Credenciais da API do X
API_KEY = "egqDhnoaAKYGlYK2WuWDtxDuv"
API_SECRET = "KXhf2iTt1LjLgAHBkppN0VcBXeOSIZFRKzshGmj0SF7egZ04hg"
ACCESS_TOKEN = "1780070664335941632-hP02jmYg2mjReGVHVZCr3JJMDivQ9e"
ACCESS_TOKEN_SECRET = "NitGhzijEwdcXNGpsbdxjid2ffWs8BTmq3P9sUG4dgnwi"

# Autenticação
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
# Função para responder DMs
def respond_to_dms():
    dms = api.get_direct_messages()
    for dm in dms:
        sender_id = dm.message_create['sender_id']
        message = dm.message_create['message_data']['text']
        # Resposta automática
        response = f"Olá! Obrigado por entrar em contato. Sou [Raquel] e            ofereço [serviços de modelo, publicidade, programação, digital              influencer]. Como posso ajudar você a alcançar seus objetivos?              Visite meu portfólio: [raquelcansada.github.io/raquelcansada/] ou           agende uma reunião."
        api.send_direct_message(recipient_id=sender_id, text=response)
        print(f"Respondi para {sender_id}: {response}")

# Executar o bot
respond_to_dms()