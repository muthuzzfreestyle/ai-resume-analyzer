class UserModel:

    def __init__(self, db_connection):
        self.db = db_connection

    def create_user(self, name, email, password_hash):

        cursor = self.db.cursor()

        query = """
        INSERT INTO users
        (name, email, password_hash)
        VALUES (%s, %s, %s)
        """

        cursor.execute(
            query,
            (name, email, password_hash)
        )

        self.db.commit()

        user_id = cursor.lastrowid

        cursor.close()

        return user_id

    def get_user_by_email(self, email):

        cursor = self.db.cursor()

        query = """
        SELECT *
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (email,))

        user = cursor.fetchone()

        cursor.close()

        return user