import base64
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from io import BytesIO
import os


def select_image():
    """Ouvre une boîte de dialogue pour sélectionner une image et enregistre son chemin."""
    file_path = filedialog.askopenfilename(
        title="Sélectionnez un fichier image",
        filetypes=[("Fichiers d'images", "*.png;*.jpg;*.jpeg")]
    )
    if file_path:
        image_path_var.set(file_path)


def resize_image_if_needed(image_path):
    """
    Vérifie la taille de l'image et redimensionne si nécessaire.
    Retourne l'image redimensionnée ou l'image d'origine si aucun redimensionnement n'est nécessaire.
    """
    try:
        with Image.open(image_path) as img:
            # Vérifie les dimensions
            width, height = img.size
            if max(width, height) > 200:
                # Redimensionne en maintenant le ratio
                img.thumbnail((200, 200))
                return img
            return img
    except Exception as e:
        raise Exception(f"Erreur lors du redimensionnement de l'image : {e}")


def convert_to_base64():
    """Convertit l'image sélectionnée (redimensionnée si nécessaire) en chaîne Base64."""
    image_path = image_path_var.get()
    if not image_path:
        messagebox.showwarning("Avertissement", "Veuillez d'abord sélectionner une image !")
        return

    try:
        # Redimensionne l'image si nécessaire
        img = resize_image_if_needed(image_path)
        
        # Convertit l'image en Base64
        buffered = BytesIO()
        img_format = "PNG" if img.format == "PNG" else "JPEG"
        img.save(buffered, format=img_format)
        base64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

        base64_string_var.set(base64_str)
        messagebox.showinfo("Succès", "Image convertie en Base64.")
        # Active le bouton copier après la conversion
        copy_button.config(state='normal')
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de la conversion de l'image : {e}")


def copy_to_clipboard():
    """Copie la chaîne Base64 dans le presse-papier."""
    base64_str = base64_string_var.get()
    if not base64_str:
        messagebox.showwarning("Avertissement", "Aucune chaîne Base64 à copier !")
        return

    root.clipboard_clear()
    root.clipboard_append(base64_str)
    root.update()  # Met à jour le presse-papier
    messagebox.showinfo("Copié", "Chaîne Base64 copiée dans le presse-papier !")


# Initialisation de la fenêtre principale Tkinter
root = tk.Tk()
root.title("Convertisseur d'image en Base64")

# Configuration de l'icône de l'application
icon_path = os.path.join(os.path.dirname(__file__), "logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)
root.geometry("600x400")

# Variables Tkinter pour stocker le chemin du fichier et la chaîne Base64
image_path_var = tk.StringVar()
base64_string_var = tk.StringVar()

# Composants de l'interface utilisateur
tk.Label(root, text="Convertisseur d'image en Base64", font=("Arial", 16)).pack(pady=10)

tk.Label(root, text="Image sélectionnée :").pack()
tk.Entry(root, textvariable=image_path_var, width=50, state='readonly').pack(pady=5)

tk.Button(root, text="Sélectionner une image", command=select_image).pack(pady=5)
tk.Button(root, text="Convertir en Base64", command=convert_to_base64).pack(pady=5)

# Bouton copier initialisé comme désactivé
copy_button = tk.Button(root, text="Copier dans le presse-papier", command=copy_to_clipboard, state='disabled')
copy_button.pack(pady=5)

# Boucle principale pour exécuter l'application
root.mainloop()
