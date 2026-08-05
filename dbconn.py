from sqlalchemy import create_engine, text as sql_text
from sqlalchemy.exc import SQLAlchemyError

dbconn = create_engine("mysql+pymysql://root@localhost:3306/simbba",pool_size=20, max_overflow=0)