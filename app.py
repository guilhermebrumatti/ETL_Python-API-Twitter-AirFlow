from sched import scheduler
import pandas as pd
import sqlite3
import tweepy as tw
from datetime import datetime
from datetime import datetime

import pendulum
from airflow.operators.python import PythonOperator
from airflow import DAG, Dataset
from airflow.operators.bash import BashOperator

def raspa_twitter():
    # Adicionando credenciais como variáveis
    consumer_key = 'SUA KEY'
    consumer_secret = 'SEU SECRET'
    bearer_token = 'SEU BEAR TOKEN'
    access_token = 'SEU ACCESS TOKEN'
    access_token_secret = 'SEU ACCESS TOKEN SECRET'

    # Criando client
    cliente = tw.Client(bearer_token, consumer_key, consumer_secret, access_token, access_token_secret)

    # Definindo data e hora atuais e o range de captação dos tweets
    data_e_hora_atuais = datetime.now()
    start = data_e_hora_atuais.strftime("%Y-%m-%dT08:00:00Z")
    end = data_e_hora_atuais.strftime("%Y-%m-%dT18:00:00Z")

    # Setando a(s) palavra(s) chave(s) para a busca no Twitter que neste caso é "flamengo"
    # A variavel result receberá o resultado da busca, que tem limite máximo de 100 tweets que foram postados entre a data e hora definidos nas variaveis 'start' e 'end'
    busca = ['flamengo']
    result = cliente.search_recent_tweets(query=busca,max_results=100,start_time=start,end_time=end)
    dados = result.data

    # Jogando o resultado da busca no dataframe do pandas.
    # Removi duas colunas e adicionei uma nova coluna informando a data e hora que os tweets foram capturados.
    df = pd.DataFrame(dados)
    df.drop('edit_history_tweet_ids', axis=1, inplace=True)
    df.drop('id', axis=1, inplace=True)
    df.insert(column='data_insert_db', value=data_e_hora_atuais, loc=1)

    # Conectando ao banco de dados no sqlite3
    database = "bancodedados.sqlite"
    conn = sqlite3.connect(database)

    # O 'to_sql' exporta o conteúdo do dataframe para o banco Sqlite3, de maneira automática
    df.to_sql(name='tabelasql', con=conn, if_exists="append", index=True)

    # Depois de salvo no banco de dados, defino uma query de consulta
    sql = ('SELECT "data_insert_db", "text" FROM tabelasql')

    # O 'read_sql' cria um DataFrame através da QUERY acima.
    df2 = pd.read_sql(sql, conn)

    #Exporto o DataFrame gerado a partir da consulta a tabela no Sqlite, em arquivo .xlsx
    df2.to_excel("conteudo_do_bd.xlsx")
    conn.close()

with DAG(dag_id='dag_twitter',catchup=False,start_date=datetime(2022, 10, 7, tz="UTC"),schedule='@daily') as dag1:
    # [START task_outlet]
    varBash = BashOperator(task_id='producing_task_1', bash_command="sleep 5")
    # [END task_outlet]

varBash >> raspa_twitter()
