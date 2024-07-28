import json
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_database_credentials(secret_name, region_name):
    # grabs a secret manager
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    else:
        secret = get_secret_value_response['SecretString']
        return json.loads(secret)


region = "us-east-1"
secret = 'postgresql'
credentials = get_database_credentials(secret_name=secret, region_name=region)
DATABASE_URI = f"postgresql://{credentials['username']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}"
engine = create_engine(DATABASE_URI, pool_pre_ping=True)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)