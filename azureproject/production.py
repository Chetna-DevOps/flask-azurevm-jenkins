#import os

# DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
#     dbuser=os.getenv('AZURE_POSTGRESQL_USER'),
#     dbpass=os.getenv('AZURE_POSTGRESQL_PASSWORD'),
#     dbhost=os.getenv('AZURE_POSTGRESQL_HOST'),
#     dbname=os.getenv('AZURE_POSTGRESQL_NAME')
# )

import os

DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.environ['DBUSER'],
    dbpass=os.environ['DBPASS'],
    dbhost=os.environ['DBHOST'],
    dbname=os.environ['DBNAME']
)

CACHE_TYPE = 'RedisCache'
CACHE_REDIS_URL = os.environ.get('CACHELOCATION')
