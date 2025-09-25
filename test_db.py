from sqlalchemy import create_engine, text

# Example URL: replace with your credentials
engine = create_engine("mysql+pymysql://root:hamdia123@127.0.0.1:3306/incidents_db")

with engine.connect() as conn:
    result = conn.execute(text("SELECT NOW();"))  # wrap the query with text()
    print(result.fetchone())
