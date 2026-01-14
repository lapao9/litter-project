# send_to_db.py
import psycopg2

# send_to_db.py 
def send_detection_to_db(material, description, image_url, latitude, longitude, stick_id):
    """
    Insere uma deteção de lixo na base de dados NeonDB.

    Args:
        material (str): categoria detectada (plastic, metal, etc.)
        description (str): descrição da AI
        image_url (str): caminho local ou URL da imagem
        latitude (float): latitude
        longitude (float): longitude
        stick_id: identificador do stick

    Returns:
        bool: True se sucesso, False se erro
    """
    try:
        conn = psycopg2.connect(
            host="ep-curly-voice-agp3o2vc-pooler.c-2.eu-central-1.aws.neon.tech",
            dbname="neondb",
            user="neondb_owner",
            password="npg_KN6wGF4cBxef",
            sslmode="require"
        )
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO litter (category, ai_description, image_url, latitude, longitude, stick_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (material, description, image_url, latitude, longitude, stick_id))

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        print(f"Saved to DB with id {new_id}")
        return True

    except Exception as e:
        print("DB ERROR:", e)
        return False
