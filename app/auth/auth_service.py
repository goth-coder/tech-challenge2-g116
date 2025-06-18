import bcrypt
from app.core.db import Database
from app.auth.auth_utils import generate_token

class AuthService:
    @staticmethod
    def login(email, password):
        db = Database()
        result = db.run_query("SELECT id, password_hash FROM app.users WHERE email = %s", (email,))
        db.close()
        if result and len(result) > 0:
            user_id, hash_from_db = result[0]
            if bcrypt.checkpw(password.encode('utf-8'), hash_from_db.encode('utf-8')):
                token = generate_token(user_id)
                return {"message": "Login successful", "token": token}, 200
            else:
                return {"error": "Invalid credentials"}, 401
        else:
            return {"error": "User not found"}, 404

    @staticmethod
    def signup(name, username, email, age, password):
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        db = Database()
        try:
            db.cur.execute("""
                INSERT INTO app.users (name, username, email, age, password_hash)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, username, email, age, password_hash))
            db.conn.commit()
        except Exception as e:
            db.conn.rollback()
            return {"error": str(e)}, 400
        finally:
            db.close()
        return {"message": "User registered successfully"}, 201
