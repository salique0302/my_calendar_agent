import bcrypt
import sys

if len(sys.argv) > 1:
    password_to_hash = sys.argv[1]
else:
    password_to_hash = input("Please enter the password you want to hash: ")

if not password_to_hash:
    print("Error: No password provided.")
else:
    password_bytes = password_to_hash.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    hashed_password_str = hashed_password_bytes.decode('utf-8')

    print("\n✅ Password hashed successfully!")
    print("\nCopy this hashed password and paste it into your config.yaml file:")
    print("---------------------------------------------------------------")
    print(hashed_password_str)
    print("---------------------------------------------------------------")