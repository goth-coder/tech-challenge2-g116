import psycopg2
from app.core.config import DB_CONFIG

class Database:
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cur = self.conn.cursor()

    def run_query(self, query, params=None):
        self.cur.execute(query, params)
        # Only commit if not a SELECT
        if not query.strip().lower().startswith('select'):
            self.conn.commit()
        if self.cur.description:
            return self.cur.fetchall()
        return None

    def close(self):
        self.cur.close()
        self.conn.close()

if __name__ == "__main__":
    db = Database()
    # Example query to test the connection
    output = db.run_query("""
    SELECT * from app.users  
    """)
    print(output)
    db.close()