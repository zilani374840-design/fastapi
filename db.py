# ==========================================
# db.py  ->  Connection to the database
# ==========================================
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# Render PostgreSQL Full External Database URL
# Render-এ ডাটাবেস আগে থেকেই তৈরি থাকে, তাই আলাদা করে CREATE DATABASE করার দরকার নেই
DATABASE_URL = "postgresql+psycopg2://trainning_user:qzjFI0sv8Z10NhePuGB7k3uRqmS2MKV6@dpg-dc3666c0916s73frrmg0-a.oregon-postgres.render.com/trainning"

engine = create_engine(DATABASE_URL)

# ডাটাবেস কানেকশন ঠিক আছে কি না তা যাচাই করা
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Successfully connected to Render PostgreSQL!")
except Exception as error:
    print("\n" + "=" * 60)
    print(" ERROR: Could not connect to PostgreSQL!")
    print(" Check your DATABASE_URL and internet connection in db.py")
    print(" Details:", error)
    print("=" * 60 + "\n")
    raise SystemExit(1)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()


# Opens a database session for each request
# and closes it when the work is done.
# Used in routers like this:  db: Session = Depends(get_db)
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()
