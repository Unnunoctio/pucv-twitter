
class User:
    username: str
    email: str
    password: str

    def __init__(self, username: str | None, email: str | None, password: str | None):
        if (username is None) or (email is None) or (password is None):
            raise ValueError("Error: Faltan datos del usuario")

        self.username = username
        self.email = email
        self.password = password

    def __str__(self) -> str:
        return (f"Username: {self.username}\n"
                f"Email: {self.email}\n"
                f"Password: {self.password}")