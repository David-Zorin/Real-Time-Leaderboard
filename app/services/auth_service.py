from psycopg2.extras import RealDictCursor
from app.core.security import get_password_hash, verify_password, create_access_token
from app.schemas.auth import RegisterRequest, LoginRequest
from fastapi import HTTPException, status


class AuthService:
    @staticmethod
    def register_user(conn, user_data: RegisterRequest):
        """Creates a new user in the database."""
        hashed_password = get_password_hash(user_data.password)

        try:
            with conn.cursor() as cur:
                # Check if user already exists
                cur.execute(
                    "SELECT id FROM users WHERE username = %s OR email = %s",
                    (user_data.username, user_data.email),
                )
                if cur.fetchone():
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Username or email already registered",
                    )

                # Insert new user
                cur.execute(
                    "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s) RETURNING id",
                    (user_data.username, user_data.email, hashed_password),
                )
                conn.commit()
                return {"message": "User registered successfully"}
        except Exception as e:
            conn.rollback()
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=str(e))

    # LOGIN
    @staticmethod
    def authenticate_user(conn, login_data: LoginRequest):
        """Verifies user credentials and returns an access token."""
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                "SELECT * FROM users WHERE username = %s", (login_data.username,)
            )
            user = cur.fetchone()

            if not user or not verify_password(
                login_data.password, user["password_hash"]
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Create JWT Token
            access_token = create_access_token(
                data={"sub": user["username"], "user_id": user["id"]}
            )
            return {"access_token": access_token, "token_type": "bearer"}
