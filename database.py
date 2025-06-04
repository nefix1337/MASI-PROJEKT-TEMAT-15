import psycopg2




class DataBaseManager:
    def __init__(self, host, dbname, user, password, port=5433):
        self.conn = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password,
            port=port
        )
        self.ensure_table()

    def ensure_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS uniterm (
                    id SERIAL PRIMARY KEY,
                    name TEXT,
                    description TEXT,
                    x1 TEXT,
                    y1 TEXT,
                    z1 TEXT,
                    x2 TEXT,
                    y2 TEXT,
                    z2 TEXT,
                    replacement_done BOOLEAN,
                    replacement_position TEXT
                );
            """)
            self.conn.commit()

    def add_uniterm(self, name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO uniterm (name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position))
            self.conn.commit()
            return cur.fetchone()[0]

    def update_uniterm(self, uniterm_id, name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE uniterm
                SET name=%s, description=%s, x1=%s, y1=%s, z1=%s, x2=%s, y2=%s, z2=%s, replacement_done=%s, replacement_position=%s
                WHERE id=%s;
            """, (name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position, uniterm_id))
            self.conn.commit()

    def get_uniterms(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position
                FROM uniterm
                ORDER BY id DESC;
            """)
            return cur.fetchall()

    def get_uniterm(self, uniterm_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, description, x1, y1, z1, x2, y2, z2, replacement_done, replacement_position
                FROM uniterm
                WHERE id = %s;
            """, (uniterm_id,))
            return cur.fetchone()

    def delete_uniterm(self, uniterm_id):
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM uniterm WHERE id = %s;", (uniterm_id,))
            self.conn.commit()

    def close(self):
        self.conn.close()