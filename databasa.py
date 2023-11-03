import psycopg2

class Data:
    def __init__(self, host1, port1, data, user1, password1):
        self.connect = psycopg2.connect(
            host=host1,
            port=port1,
            database=data,
            user=user1,
            password=password1
        )
        self.cursor = self.connect.cursor()

    def add_user(self, id, first_name, username):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, first_name, username) VALUES(%s, %s, %s)",
                                (id, first_name, username,))
            self.connect.commit()

    def check_user(self, id):
        with self.connect:
            self.cursor.execute("SELECT id FROM users WHERE id=%s", (id,))
            return bool(len(self.cursor.fetchall()))

    def add_admin(self, id):
        with self.connect:
            self.cursor.execute("UPDATE users SET adm=1 WHERE id=%s", (id,))
            self.connect.commit()

    def select_admin(self, id):
        with self.connect:
            self.cursor.execute("SELECT adm FROM users WHERE id=%s", (id,))
            return self.cursor.fetchone()[0]

    def add_cashe_create(self, id, api_id):
        with self.connect:
            self.cursor.execute("INSERT INTO cashe_create (id, api_id) VALUES(%s, %s)", (id, api_id,))
            self.connect.commit()

    def update_cashe_create_hash(self, id, api_hash):
        with self.connect:
            self.cursor.execute("UPDATE cashe_create SET api_hash=%s WHERE id=%s", (api_hash, id,))
            self.connect.commit()

    def update_cashe_create_number_phone(self, id, number_phone):
        with self.connect:
            self.cursor.execute("UPDATE cashe_create SET number_phone=%s WHERE id=%s", (number_phone, id,))
            self.connect.commit()

    def delete_cashe_create(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM cashe_create WHERE id=%s", (id,))
            self.connect.commit()

    def select_cashe_create(self, id):
        with self.connect:
            self.cursor.execute("SELECT api_id, api_hash, number_phone FROM cashe_create WHERE id=%s", (id,))
            a = self.cursor.fetchone()
            return a

db = Data("192.168.1.37", "5432", "sender", "sender_user", "sender_pass")