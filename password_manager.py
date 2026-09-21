import os
import json
import base64
import secrets
import threading
import time
import customtkinter as ctk
from tkinter import messagebox
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

# ==========================
# CONFIGURAZIONE DI BASE
# ==========================
VAULT_FILE = "vault.json"
CLIPBOARD_TIMEOUT = 15  # secondi
KDF_ITERATIONS = 200_000
SALT_SIZE = 16

# ==========================
# FUNZIONI DI CIFRATURA
# ==========================
def derive_key(master_password: str, salt: bytes) -> bytes:
    """Deriva una chiave sicura dalla master password e dal salt (per Fernet)."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
    )
    key = kdf.derive(master_password.encode())
    return base64.urlsafe_b64encode(key)


def encrypt_data(data: dict, master_password: str, salt: bytes) -> str:
    """Cifra un dizionario Python e restituisce il token Fernet (stringa base64)."""
    key = derive_key(master_password, salt)
    f = Fernet(key)
    plaintext = json.dumps(data).encode()
    token = f.encrypt(plaintext)
    return token.decode()


def decrypt_data(token_str: str, master_password: str, salt: bytes) -> dict:
    """Decifra un token Fernet (stringa base64) e restituisce un dizionario Python."""
    key = derive_key(master_password, salt)
    f = Fernet(key)
    plaintext = f.decrypt(token_str.encode())
    return json.loads(plaintext.decode())


# ==========================
# FILE HANDLER
# ==========================
def create_vault_file(master_password: str):
    """Crea un nuovo file vault cifrato vuoto."""
    salt = secrets.token_bytes(SALT_SIZE)
    encrypted = encrypt_data({}, master_password, salt)
    data = {"salt": base64.b64encode(salt).decode(), "data": encrypted}
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_vault(master_password: str) -> tuple[dict, bytes]:
    """Carica e decifra il vault; restituisce (entries, salt)."""
    if not os.path.exists(VAULT_FILE):
        raise FileNotFoundError("Vault non trovato.")
    with open(VAULT_FILE, "r", encoding="utf-8") as f:
        vault = json.load(f)
    salt = base64.b64decode(vault["salt"])
    entries = decrypt_data(vault["data"], master_password, salt)
    return entries, salt


def save_vault(entries: dict, master_password: str, salt: bytes):
    """Salva le entries cifrate nel vault."""
    encrypted = encrypt_data(entries, master_password, salt)
    data = {"salt": base64.b64encode(salt).decode(), "data": encrypted}
    with open(VAULT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ==========================
# FUNZIONE CLIPBOARD TEMPORANEA
# ==========================
def copy_temporary(app, text: str, timeout: int = CLIPBOARD_TIMEOUT):
    app.clipboard_clear()
    app.clipboard_append(text)
    messagebox.showinfo("Copiata", f"La password è stata copiata.\nSparirà dagli appunti tra {timeout} secondi.")
    def clear_clipboard():
        time.sleep(timeout)
        try:
            app.clipboard_clear()
        except Exception:
            pass
    threading.Thread(target=clear_clipboard, daemon=True).start()


# ==========================
# GUI PRINCIPALE
# ==========================
class PasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Password Manager")
        self.geometry("600x390")
        self.resizable(False, False)
        # self.iconbitmap("icons/padlock_ico.ico")

        self.master_password = None
        self.salt = None
        self.entries = {}

        # Layout base
        self.build_login_ui()

    # =====================
    # LOGIN / CREAZIONE
    # =====================
    def build_login_ui(self):
        self.clear_window()

        ctk.CTkLabel(self, text="🔒 Password Manager", font=("Arial", 20, "bold")).pack(pady=20)
        ctk.CTkLabel(self, text="Inserisci la tua master password:").pack()

        self.master_entry = ctk.CTkEntry(self, show="*", width=250)
        self.master_entry.pack(pady=10)
        
        # --- MODIFICA QUI: Collega il tasto INVIO ---
        self.master_entry.bind('<Return>', lambda event: self.try_open_vault())

        ctk.CTkButton(self, text="Apri Vault", command=self.try_open_vault).pack(pady=5)

        if not os.path.exists(VAULT_FILE):
            ctk.CTkButton(self, text="Crea nuovo Vault", command=self.create_new_vault).pack(pady=5)

    def create_new_vault(self):
        pw = self.master_entry.get()
        if not pw:
            messagebox.showwarning("Errore", "Inserisci una master password.")
            return
        create_vault_file(pw)
        messagebox.showinfo("OK", "Vault creato con successo!")
        self.try_open_vault()

    def try_open_vault(self):
        pw = self.master_entry.get()
        if not pw:
            messagebox.showwarning("Errore", "Inserisci una master password.")
            return
        try:
            self.entries, self.salt = load_vault(pw)
        except Exception as e:
            messagebox.showerror("Errore", f"Impossibile aprire il vault: {e}")
            return
        self.master_password = pw
        self.build_main_ui()

    # =====================
    # INTERFACCIA PRINCIPALE
    # =====================
    def build_main_ui(self):
        self.clear_window()

        ctk.CTkLabel(self, text="🔐 Gestione Password", font=("Arial", 18, "bold")).pack(pady=10)

        # Lista password
        self.listbox = ctk.CTkTextbox(self, width=560, height=150, state="disabled")
        self.listbox.pack(pady=10)
        self.refresh_list()

        # Campi input
        form = ctk.CTkFrame(self)
        form.pack(pady=10)

        ctk.CTkLabel(form, text="Sito:").grid(row=0, column=0, sticky="e", padx=5)
        self.site_entry = ctk.CTkEntry(form, width=200)
        self.site_entry.grid(row=0, column=1)

        ctk.CTkLabel(form, text="Username:").grid(row=1, column=0, sticky="e", padx=5)
        self.user_entry = ctk.CTkEntry(form, width=200)
        self.user_entry.grid(row=1, column=1)

        ctk.CTkLabel(form, text="Password:").grid(row=2, column=0, sticky="e", padx=5)
        self.pass_entry = ctk.CTkEntry(form, width=200, show="*")
        self.pass_entry.grid(row=2, column=1)

        # Bottoni
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Aggiungi / Aggiorna", command=self.add_entry).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_frame, text="Copia Password", command=self.copy_password).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_frame, text="Elimina", fg_color="#AF0000", command=self.delete_entry).grid(row=0, column=2, padx=5)
        ctk.CTkButton(btn_frame, text="Esci", fg_color="gray", command=self.logout).grid(row=0, column=3, padx=5)

    def refresh_list(self):
        self.listbox.configure(state="normal")
        self.listbox.delete("1.0", "end")
        if not self.entries:
            self.listbox.insert("end", "(Nessuna voce salvata)\n")
        else:
            for site, data in self.entries.items():
                self.listbox.insert("end", f"{site} — {data['username']}\n")
        self.listbox.configure(state="disabled")

    # =====================
    # OPERAZIONI CRUD
    # =====================
    def add_entry(self):
        site = self.site_entry.get().strip()
        user = self.user_entry.get().strip()
        pw = self.pass_entry.get().strip()

        if not site or not user or not pw:
            messagebox.showwarning("Errore", "Compila tutti i campi.")
            return

        self.entries[site] = {"username": user, "password": pw}
        save_vault(self.entries, self.master_password, self.salt)
        messagebox.showinfo("OK", f"Voce '{site}' salvata.")
        
        # --- MODIFICA QUI: Svuota i campi dopo il salvataggio ---
        self.site_entry.delete(0, 'end')
        self.user_entry.delete(0, 'end')
        self.pass_entry.delete(0, 'end')
        
        self.refresh_list()

    def copy_password(self):
        site = self.site_entry.get().strip()
        if site not in self.entries:
            messagebox.showerror("Errore", "Voce non trovata.")
            return
        pw = self.entries[site]["password"]
        copy_temporary(self, pw)

    def delete_entry(self):
        site = self.site_entry.get().strip()
        if site not in self.entries:
            messagebox.showerror("Errore", "Voce non trovata.")
            return
        del self.entries[site]
        save_vault(self.entries, self.master_password, self.salt)
        messagebox.showinfo("OK", f"Voce '{site}' eliminata.")
        self.refresh_list()

    def logout(self):
        self.master_password = None
        self.entries = {}
        self.build_login_ui()

    # =====================
    # UTILITY
    # =====================
    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


# ==========================
# AVVIO DELL'APPLICAZIONE
# ==========================
if __name__ == "__main__":
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    app = PasswordManager()
    app.mainloop()