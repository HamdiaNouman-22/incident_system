from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://root:hamdia123@127.0.0.1:3306/incidents_db")

with engine.connect() as conn:
    result = conn.execute(text("SELECT NOW();"))
    print(result.fetchone())
