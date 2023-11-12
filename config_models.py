from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host, port = "dpg-cl8e4776e7vc73a56bpg-a", 5432
login, password = "admin", 'tO7TsKPwarM40UVmoDAMcQkSJpzcXQpG'
db_name = "postgres_test_jcu8"

engine = create_engine(url=f"postgresql://{login}:{password}@{host}/{db_name}", echo=True)
