
import os

db_URI = os.getenv(
    "DATABASE_URL", "postgresql://postgres:python123@localhost:5432/mma_db"
)
SECRET = os.getenv("SECRET", "tigersparklinglanternstars")

if db_URI.startswith("postgres://"):
    db_URI = db_URI.replace("postgres://", "postgresql://", 1)

