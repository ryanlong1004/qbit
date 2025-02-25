from cryptography.fernet import Fernet
import typer

app = typer.Typer()


class Crypt:
    def __init__(self, key: str):
        self.key = key.encode()
        self.cipher = Fernet(self.key)

    def encrypt(self, plaintext: str) -> str:
        encrypted_text = self.cipher.encrypt(plaintext.encode())
        return encrypted_text.decode()

    def decrypt(self, encrypted_text: str) -> str:
        decrypted_text = self.cipher.decrypt(encrypted_text.encode())
        return decrypted_text.decode()


def generate_key() -> str:
    return Fernet.generate_key().decode()


@app.command()
def encrypt(key: str, plaintext: str):
    crypt = Crypt(key)
    encrypted = crypt.encrypt(plaintext)
    typer.echo(encrypted)


@app.command()
def decrypt(key: str, encrypted_text: str):
    crypt = Crypt(key)
    decrypted = crypt.decrypt(encrypted_text)
    typer.echo(decrypted)


@app.command()
def generate():
    key = generate_key()
    typer.echo(key)


if __name__ == "__main__":
    app()
