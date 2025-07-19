import tls_client
from lxml import html
from bs4 import BeautifulSoup

team_adress_A = {}
def team_search(time:str):
    session = tls_client.Session(client_identifier="chrome_115")
    base_url= "https://api.sofascore.com/api/v1/team/"

session = tls_client.Session(client_identifier="chrome_115")
url = "https://www.sofascore.com/api/v1/unique-tournament/325/season/72034/standings/total"

# Requisição com redirecionamento permitido
res = session.get(url, allow_redirects=True)

# Verifica se deu certo
if res.status_code == 200:
    data = res.json()
    
    print("🏆 Tabela de Classificação - Brasileirão:")
    print("-" * 40)

    # Loop nos times
    for time in data["standings"][0]["rows"]:
        print(time["team"]["id"], "-", time["team"]["name"])
