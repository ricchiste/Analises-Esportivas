import tls_client
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

team_adress_A = {
    'red bull bragantino': '1999',
    'bahia': '1955',
    'palmeiras': '1963',
    'botafogo': '1958',
    'fluminense': '1961',
    'atletico mineiro': '1977',
    'corinthians': '1957',
    'ceará': '2001',
    'mirassol': '21982',
    'grêmio': '5926',
    'santos': '1968',
    'internacional': '1966',
    'vasco da gama': '1974',
    'são paulo': '1981',
    'vitória': '1962',
    'juventude': '1980',
    'fortaleza': '2020',
    'sport recife': '1959',
    'cruzeiro': '1954',
    'flamengo': '5981'
}

team_adress_B={
'goiás': '1960',
'coritiba': '1982',
'novorizontino': '135514',
'chapecoense': '21845',
'remo': '2012',
'cuiabá': '49202',
'avaí': '7315',
'vila nova fc': '2021',
'athletico': '1967',
'criciúma': '1984',
'crb': '22032',
'atlético goianiense': '7314',
'athletic club': '342775',
'américa mineiro': '1973',
'operário-pr': '39634',
'paysandu sc': '1997',
'ferroviária': '35285',
'volta redonda': '6982',
'botafogo-sp': '1979',
'amazonas fc': '336664'
}

base_api = 'https://www.sofascore.com/api/v1/team/'
end_api = '/statistics/overall'


def choose_team(time: str):
    data_list = []
    cont_url_list = 0
    cont_data_list = 0

    division = input(str('Em qual divisão está o time? ')).upper()

    if division == 'A':
        serie = '325'
        id_time = team_adress_A[time.lower()]
        end_point_25 = '72034'
        end_point_24 = '58766'
        end_point_23 = '48982'
    elif division == 'B':
        serie = '390'
        id_time = team_adress_B[time.lower()]
        end_point_25 = '72603'
        end_point_24 = '59015'
        end_point_23 = '49058'

    middle_api = f'/unique-tournament/{serie}/season/'

    url_25 = base_api + id_time + middle_api + end_point_25 + end_api
    url_24 = base_api + id_time + middle_api + end_point_24 + end_api
    url_23 = base_api + id_time + middle_api + end_point_23 + end_api

    urls_list = [url_23, url_24, url_25]

    for url in urls_list:
        session = tls_client.Session(client_identifier="chrome_115")
        api_link = session.get(url, allow_redirects=True).json()
        if not 'error' in api_link:
            data_list.append(api_link['statistics'])
            if urls_list.index(urls_list[cont_url_list]) == 0:
                data_list[cont_data_list]['ano'] = 2023
            elif urls_list.index(urls_list[cont_url_list]) == 1:
                data_list[cont_data_list]['ano'] = 2024
            elif urls_list.index(urls_list[cont_url_list]) == 2:
                data_list[cont_data_list]['ano'] = 2025
            cont_data_list += 1
        cont_url_list+=1
    return data_list

def build_dataframe(time:str):
    team = choose_team(time.lower())
    team_dataframe = pd.DataFrame(index=team[0].keys())

    for i in range(len(team)):
        team_dataframe[str(team[i]['ano'])] = team[i].values()
        team_dataframe[str(team[i]['ano'])] = team_dataframe[str(team[i]['ano'])].apply(lambda x: float('{:.1f}'.format(x)))
    
    team_dataframe['Média'] = team_dataframe.mean(axis = 1).apply(lambda x: float('{:.1f}'.format(x)))

    return team_dataframe

def build_chart(team1: str, team2: str, metric:str):
    df_team1 = build_dataframe(team1.lower())
    df_team2 = build_dataframe(team2.lower())

    anos = ['2023', '2024', '2025']
    
    fig = px.Figure(
        data = [
            px.Bar(name=team1, x=anos, y=[df_team1['2023'][metric], df_team1['2024'][metric], df_team1['2025'][metric]]),
            px.Bar(name=team2, x=anos, y=[df_team2['2023'][metric], df_team2['2024'][metric], df_team2['2025'][metric]])

        ],
        layout_title_text = metric
    )

    return fig.show()

def build_chart2(team1: str, metric: str):
    df_team1 = build_dataframe(team1.lower())  # Supondo que retorna um dicionário

    # Organizando os dados em um DataFrame para o plotly
    anos = ['2023', '2024', '2025']
    valores = [df_team1['2023'][metric], df_team1['2024'][metric], df_team1['2025'][metric]]
    
    df_plot = pd.DataFrame({
        'Ano': anos,
        metric: valores
    })

    fig = px.scatter(df_plot, x='Ano', y=metric, title=f"{metric} - {team1.title()}", trendline='ols')  # 'ols' = regressão linear

    fig.show()








'''#Serve para pegar os nomes e os códigos dos time
session = tls_client.Session(client_identifier="chrome_115")
#O url pode substituir pela URL do ano e do campeonato que você quer escolher
url = "https://www.sofascore.com/api/v1/unique-tournament/325/season/72034/standings/total" 
res = session.get(url, allow_redirects=True)
if res.status_code == 200:
    data = res.json()
    for time in data["standings"][0]["rows"]:
        print(time["team"]["name"].lower(),",",time["team"]["id"] )'''