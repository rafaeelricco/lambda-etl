import os
import sys
import csv
import boto3
import psycopg2
import pandas as pd


def connect():
    """Connect to the PostgreSQL database server."""

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )
        print("connect: Conectado ao banco de dados!")
        return conn
    except:
        print("connect: Erro ao conectar ao banco de dados!")
        sys.exit(1)


def save_data(data):
    """Save in the PostgreSQL database server."""

    conn = connect()
    cur = conn.cursor()
    with conn.cursor() as cur:
        try:
            query = "INSERT INTO cessao_fundo (originador, doc_originador, cedente, doc_cedente, ccb, id_externo, cliente, cpf_cnpj, endereco, cep, cidade, uf, valor_do_emprestimo, valor_parcela, total_parcelas, parcela, data_de_emissao, data_de_vencimento, preco_de_aquisicao) VALUES (%s, %s ,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(query, data)
            conn.commit()
            print("save_data: Dados salvos com sucesso!")
            cur.close()
        except:
            print("Oops! parece que algo deu errado:", sys.exc_info()[0])


def read_csv(bucket_name, object_key):
    """Read csv file from s3 bucket, transform and save in database."""

    # access the s3 bucket
    s3_file = boto3.resource(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # get the object from the bucket
    obj = s3_file.Object(bucket_name, object_key)

    # read the object and decode the bytes to string
    body = obj.get()["Body"].read().decode("latin-1")

    # read the csv file
    csv_reader = csv.reader(body.splitlines(), delimiter=";")

    # read the csv file and pop the header
    csv_reader = list(csv_reader)[1:]

    # transform the csv file in a pandas dataframe
    df = pd.DataFrame(
        csv_reader,
        columns=[
            "ORIGINADOR",
            "DOC_ORIGINADOR",
            "CEDENTE",
            "DOC_CEDENTE",
            "CCB",
            "ID_EXTERNO",
            "CLIENTE",
            "CPF/CNPJ",
            "ENDERECO",
            "CEP",
            "CIDADE",
            "UF",
            "VALOR_DO_EMPRESTIMO",
            "TAXA_DE_JUROS",
            "PARCELA",
            "VALOR_PARCELA",
            "PRINCIPAL",
            "JUROS",
            "IOF",
            "COMISSAO",
            "TOTAL_PARCELAS",
            "MULTA",
            "MORA",
            "DATA_DE_EMISSAO",
            "DATA_DE_VENCIMENTO",
            "DATA_DE_COMPRA_CBB",
            "PRECO_DE_AQUISICAO",
        ],
    )

    # drop the columns that will not be used
    df = df.drop(
        [
            "TAXA_DE_JUROS",
            "PRINCIPAL",
            "JUROS",
            "IOF",
            "COMISSAO",
            "MULTA",
            "MORA",
            "DATA_DE_COMPRA_CBB",
        ],
        axis=1,
    )

    # remove mask from the columns
    df["DOC_ORIGINADOR"] = (
        df["DOC_ORIGINADOR"]
        .str.replace(".", "")
        .str.replace("-", "")
        .str.replace("/", "")
    )

    # remove mask from cpf/cnpj column
    df["CPF/CNPJ"] = (
        df["CPF/CNPJ"].str.replace(".", "").str.replace("-", "").str.replace("/", "")
    )

    # remove mask from data de emissao column
    df["DATA_DE_EMISSAO"] = pd.to_datetime(df["DATA_DE_EMISSAO"]).dt.strftime(
        "%Y-%m-%d"
    )

    # remove mask from data de vencimento column
    df["DATA_DE_VENCIMENTO"] = pd.to_datetime(df["DATA_DE_VENCIMENTO"]).dt.strftime(
        "%Y-%m-%d"
    )

    # remove mask from doc originador column
    df[["DOC_ORIGINADOR", "DOC_CEDENTE", "CCB", "ID_EXTERNO", "TOTAL_PARCELAS",]] = df[
        [
            "DOC_ORIGINADOR",
            "DOC_CEDENTE",
            "CCB",
            "ID_EXTERNO",
            "TOTAL_PARCELAS",
        ]
    ].astype(int)

    # remove mask and remove the currency symbol from the columns
    df[["VALOR_DO_EMPRESTIMO", "VALOR_PARCELA", "PRECO_DE_AQUISICAO", "PARCELA"]] = (
        df[["VALOR_DO_EMPRESTIMO", "VALOR_PARCELA", "PRECO_DE_AQUISICAO", "PARCELA"]]
        .replace(",", ".", regex=True)
        .replace("[a-zA-Z]", "", regex=True)
        .astype(float)
    )

    # save the dataframe in json format
    df.to_json("./data/tranformed-data.json", orient="records")

    # transform the dataframe in a list
    data = df.values.tolist()

    # crate a loop to save the data in the database
    for row in data:
        save_data(row)
        print("read_csv: Salvou os dados do cliente: ", row[6])
        sys.exit(0)


def lambda_handler(event, context):
    """Lambda handler to read csv file from s3 bucket."""

    read_csv("ricco-storage", "RH_Edge/arquivo_exemplo.csv")
    print("lambda_handler: Arquivo lido com sucesso!")
    sys.exit(0)


if __name__ == "__main__":
    lambda_handler(None, None)
