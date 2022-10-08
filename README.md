# Python + API Twitter + AirFlow

Neste projeto utilizei Python: https://www.python.org/ e a API oficial do Twitter: https://developer.twitter.com/en/docs/twitter-api

A ideia é buscar diariamente, tweets sobre determinado assunto(neste exemplo são todos os tweets que contenham a palavra "flamengo"), exclui algumas colunas dispensáveis e adicionando uma nova coluna afim de registrar as datas de quando cada tweet foi capturado. Tudo isso através do Pandas.

Cada resultado é armazenado no sqlite diariamente, para futuras consultas.

Todo esse processo é repetido diariamente utilizando o Airflow.

Requerimentos:<br>
pip install pandas<br>
pip install sqlite3<br>
pip install tweepy<br>
