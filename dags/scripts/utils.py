import os
import logging
from datetime import datetime, timedelta
from sqlalchemy import create_engine, func  # , Column, String, Integer, DateTime  # , MetaData
from sqlalchemy.orm import sessionmaker
from airflow.models import Variable

from scripts.models import Base

db_uri = os.environ.get('LOCAL_POSTGRES_URI')
# db_uri = "postgresql+psycopg2://myuser:mypassword@my-postgres-db:5432/mydatabase"
# db_uri = Variable.get("LOCAL_POSTGRES_URI")
engine = create_engine(db_uri)
logging.info("Connected to database.")
# Create table if not exists
Base.metadata.create_all(engine, checkfirst=True)


def get_max_date_as_string(DataClass):
    max_date_str = None
    Session = sessionmaker(bind=engine)
    with Session() as session:
        max_date = session.query(func.max(DataClass.date)).scalar()
        if max_date:
            max_date_str = max_date.strftime('%Y-%m-%d %H:%M:%S')
            return max_date_str
    return max_date_str


def calculate_dates(DataClass):
    db_last_date = get_max_date_as_string(DataClass=DataClass)
    logging.info(f"Last date in database: {db_last_date}")

    if db_last_date:
        # eğer last date, 23:00'dan önceyse, o günün tarihi (yyyy-mm-dd). 23:00 ise ertesi günün tarihi (yyyy-mm-dd)
        if db_last_date[11:13] != "23":
            print("db_last_date[11:13] != 23")
            start_date = db_last_date[0:10]
            end_date = db_last_date[0:10]
        else:
            start_date = (datetime.strptime(db_last_date[0:10], '%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
            # if start_date after today, set end_date to start_date. else set end_date to today
            if datetime.strptime(start_date, '%Y-%m-%d') > datetime.today():
                end_date = start_date
            else:
                end_date = datetime.today().strftime('%Y-%m-%d')
    else:
        start_date = os.getenv("DEFAULT_DB_START_DATE")
        db_last_date = os.getenv("DEFAULT_DB_START_DATE")
        end_date = datetime.today().strftime('%Y-%m-%d')

    return start_date, end_date, db_last_date


def insert_data_to_postgres(data_list: list, DataClass):
    Session = sessionmaker(bind=engine)
    with Session() as session:
        new_rows = [DataClass(**data) for data in data_list]
        session.add_all(new_rows)
        session.commit()
        logging.info(f"Inserted {len(new_rows)} rows in {DataClass.__tablename__} table.")

    return True
