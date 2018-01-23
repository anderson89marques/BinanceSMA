# Binance API (SMA)

O Código foi escrito em python e o serviço roda na Amazon AWS Lambda usando [Serverless Framework](https://github.com/serverless/serverless).

O serviço tem dependência de um pacote externo (`requests`) e expõe 1 API como endpoint.

| **Endpoint** |**Descrição**|
|-------|------|
| `GET /klines/sma/{interval}` | Retorna o sma para o intervalo passado como parâmetro (e.g. `GET /klines/sma/1m`) |
 
# Como acessar o serviço na amazon?

basta acessar o link https://af7ufwavh4.execute-api.us-east-1.amazonaws.com/dev/klines/sma/1m.

# Como usar sem precisar do serveless?

- Clone o projeto do github
- Crie um ambiente virtual(usando python >= 3.6)
- Ative o ambiente virtual
- Instale as dependências (requests)
- Execute o módulo

```console
$ git clone https://github.com/anderson89marques/BinanceSMA.git

$ python -m venv .venv

$ source .venv/bin/activate

$ pip install -r requirements.txt

$ python binanceapi/core.py
```

obs: Se for executar os teste é preciso instalar o pytest. O ambiente virtual deve está ativado.

```console
$ pip install pytest
```


