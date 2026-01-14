# test_db.py
import psycopg2

conn = psycopg2.connect(
    host="ep-curly-voice-agp3o2vc-pooler.c-2.eu-central-1.aws.neon.tech",
    dbname="neondb",
    user="neondb_owner",
    password="npg_KN6wGF4cBxef",
    sslmode="require"
)

cur = conn.cursor()
cur.execute("SELECT NOW();")
print("Connected! Time:", cur.fetchone())

cur.close()
conn.close()
