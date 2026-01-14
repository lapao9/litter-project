# send_to_db.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def send_detection_to_db(material, description, image_url, latitude, longitude, stick_id):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode=os.getenv("DB_SSLMODE", "require")
        )

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO litter
            (category, ai_description, image_url, latitude, longitude, stick_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (material, description, image_url, latitude, longitude, stick_id))

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        print(f"Saved to DB with id {new_id}")
        return new_id

    except Exception as e:
        print("DB ERROR:", e)
        return -1
