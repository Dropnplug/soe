DEBUG = True

# --- flask Config ---
FL_HOST = "0.0.0.0"
FL_PORT = 5000
FL_DEBUG = DEBUG

# --- memo Config ---
MANAGER_PORT = FL_PORT+1
MANAGER_KEY = b"aKh2fe9npV6BDpCV2FSDmkbhc"
MANAGER_ADDRESS = "127.0.0.1"

# --- php Config ---
PHP_ENABLE = True
PHP_PORT = FL_PORT+2