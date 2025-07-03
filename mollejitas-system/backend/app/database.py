from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# IMPORTANTE: Reemplaza con la URL de tu base de datos PostgreSQL
# Formato: "postgresql://<user>:<password>@<host>/<dbname>"
# Asegúrate de que la base de datos 'mollejitas_db' exista.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/mollejitas_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
