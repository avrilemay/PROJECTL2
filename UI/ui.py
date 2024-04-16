import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

# Variables globales pour les coordonnées de chaque catégorie
global destinataire, emetteur, prix, produit, numero_facture, date, echeance
destinataire = emetteur = prix = produit = numero_facture = date = echeance = None

# Variables globales pour la gestion des sélections
rect_id = None
selecting = False
start_x, start_y = None, None

# importer une image dans l'application
def import_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        show_image(file_path, canvas)

# affiche l'image importée sur le canvas
def show_image(file_path, canvas):
    image = Image.open(file_path)  # ouvre le fichier image spécifié par 'file_path'
    photo = ImageTk.PhotoImage(image)  # convertit l'image en format utilisable par tkinter
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)  # place l'image en haut à gauche du canvas
    canvas.img_photo = photo  # garde une référence à 'photo' pour éviter que l'image ne soit effacée par le gc

# prépare une section de sélection dans l'interface utilisateur pour chaque catégorie :
def setup_selection_section(frame, label_text):
    frame.pack(side='top', fill='x', padx=10, pady=5)  # positionne le cadre en haut
    # les cadres s'empilent les uns en dessous des autres et occupent tout l'espace horizontal nécessaire
    frame.validated = False  # initialise "validated" pour suivre si la sélection dans ce cadre a été validée
    label = tk.Label(frame, text=label_text)  # crée une étiquette avec le texte fourni
    label.pack(side='left')  # positionne l'étiquette à gauche dans le cadre
    btn_select = tk.Button(frame, text="Sélectionner", command=lambda: toggle_selection(frame) if not frame.validated else None)
    btn_select.pack(side='left', padx=5)  # ajoute un bouton pour commencer la sélection, désactivé si déjà validé
    btn_validate = tk.Button(frame, text="Valider", command=lambda: validate_selection(frame, label_text), state="disabled")
    btn_validate.pack(side='left', padx=5)  # ajoute un bouton pour valider la sélection, désactivé initialement
    btn_na = tk.Button(frame, text="N/A", command=lambda: na_selection(frame, label_text), state="disabled")
    btn_na.pack(side='left', padx=5)  # ajoute un bouton pour marquer la section comme non applicable, désactivé initialement
    btn_clear = tk.Button(frame, text="Effacer", command=lambda: clear_selection(frame), state="disabled")
    btn_clear.pack(side='left', padx=5)  # ajoute un bouton pour effacer la sélection, désactivé initialement
    frame.btn_select = btn_select # stocke des références aux boutons dans le cadre
    frame.btn_validate = btn_validate # pour pouvoir modifier leur état plus tard
    frame.btn_na = btn_na
    frame.btn_clear = btn_clear


# active ou désactive le mode de sélection
def toggle_selection(frame):
    global selecting, rect_id  # déclaration de variables globales
    if not selecting:  # vérifie si le mode sélection n'est pas actif
        selecting = True  # active le mode sélection
        frame.btn_validate.config(state="normal")  # active le bouton de validation
        frame.btn_na.config(state="normal")  # active le bouton non applicable
        frame.btn_clear.config(state="normal")  # active le bouton de nettoyage
        # avec selecting True, on peut créer le rectangle avec les interactions souris (on_canvas_click, etc)
    else:
        selecting = False  # désactive le mode sélection
        frame.btn_validate.config(state="disabled")  # désactive le bouton de validation
        frame.btn_na.config(state="disabled")  # désactive le bouton non applicable
        frame.btn_clear.config(state="disabled")  # désactive le bouton de nettoyage
        if rect_id:
            canvas.delete(rect_id)  # supprime le rectangle du canvas si existant
            rect_id = None  # réinitialise l'id du rectangle

# valide la sélection d'une zone spécifique et enregistre les coordonnées
def validate_selection(frame, label):
    global destinataire, emetteur, prix, produit, numero_facture, date, echeance  # déclaration de variables globales
    if rect_id:
        coords = canvas.coords(rect_id)  # récupère les coordonnées du rectangle
        if coords:
            # assigne les coordonnées aux variables globales selon le label
            if label == "Destinataire":
                destinataire = coords
            elif label == "Emetteur":
                emetteur = coords
            elif label == "Prix":
                prix = coords
            elif label == "Produits Commandés":
                produit = coords
            elif label == "N° Facture":
                numero_facture = coords
            elif label == "Date":
                date = coords
            elif label == "Echéance":
                echeance = coords
            messagebox.showinfo("Validation", f"Sélection validée pour {label} avec les coordonnées : {coords}")  # affiche un message de validation
        clear_selection(frame)  # efface la sélection
        frame.btn_select.config(state="disabled")  # désactive le bouton de sélection

# marque comme N/A la sélection d'une zone pour une catégorie
def na_selection(frame, label):
    global destinataire, emetteur, prix, produit, numero_facture, date, echeance  # déclaration de variables globales
    # assigne None aux variables globales selon le label indiquant non applicable
    if label == "Destinataire":
        destinataire = None
    elif label == "Emetteur":
        emetteur = None
    elif label == "Prix":
        prix = None
    elif label == "Produits Commandés":
        produit = None
    elif label == "N° Facture":
        numero_facture = None
    elif label == "Date":
        date = None
    elif label == "Echéance":
        echeance = None
    messagebox.showinfo("N/A", f"Sélection marquée comme non applicable pour {label}.")  # affiche un message de non applicabilité
    clear_selection(frame)  # efface la sélection

# supprime la sélection effectuée et réinitialise l'id du rectangle
def clear_selection(frame):
    global rect_id, selecting  # déclaration de variables globales
    if rect_id:
        canvas.delete(rect_id)  # supprime le rectangle du canvas
        rect_id = None  # réinitialise l'id du rectangle
    frame.btn_validate.config(state="disabled")  # désactive le bouton de validation
    frame.btn_na.config(state="disabled")  # désactive le bouton non applicable
    frame.btn_clear.config(state="disabled")  # désactive le bouton de nettoyage
    selecting = False  # désactive le mode sélection


root = tk.Tk()  # crée la fenêtre principale
root.geometry('1368x768')  # définit les dimensions de la fenêtre
root.title("ProjectL2")  # définit le titre de la fenêtre

tab_control = ttk.Notebook(root)  # crée un contrôle d'onglets dans la fenêtre principale
tab1 = ttk.Frame(tab_control)  # crée un onglet dans le contrôle d'onglets

left_frame = tk.Frame(tab1)  # crée un cadre à gauche pour le contenu principal
left_frame.pack(side='left', fill='both', expand=True)  # positionne le cadre gauche

right_frame = tk.Frame(tab1)  # crée un cadre à droite pour les contrôles
right_frame.pack(side='left', fill='y', padx=10, pady=10)  # positionne le cadre droit

canvas = tk.Canvas(left_frame)  # crée un canvas dans le cadre gauche pour dessiner des formes
canvas.pack(fill='both', expand=True)  # permet au canvas de remplir le cadre et de s'étendre

btn_import_image = tk.Button(right_frame, text="Importer Image", command=import_image)  # bouton pour importer une image
btn_import_image.pack(pady=10)  # positionne le bouton avec un padding vertical

sections = ["Destinataire", "Emetteur", "N° Facture", "Date", "Prix", "Produits Commandés", "Echéance"]
for section in sections:
    frame = tk.Frame(right_frame, name=section.lower().replace(' ', '_'))  # crée un cadre pour chaque section dans le cadre droit
    setup_selection_section(frame, section)  # configure le cadre de la section (avec l'appel à la fonction set_selection_section
        # > création des boutons, etc)

# gère l'événement de clic sur le canvas
def on_canvas_click(event):
    global start_x, start_y, rect_id, selecting  # utilise des variables globales
    if selecting:  # vérifie si la sélection est active
        start_x, start_y = event.x, event.y  # enregistre les coordonnées initiales où l'utilisateur a cliqué
        rect_id = canvas.create_rectangle(start_x, start_y, start_x + 1, start_y + 1, outline='red')  # dessine un rectangle minuscule
        # crée un petit rectangle (quasi-point) à l'emplacement du clic initial
        # rect_id : identifiant du rectangle créé > permet de le manipuler par la suite.

# gère le glissement de la souris sur le canvas
def on_canvas_drag(event):
    global rect_id, selecting  # utilise des variables globales
    if selecting and rect_id:  # vérifie si un rectangle est en cours de dessin
        end_x, end_y = event.x, event.y  # met à jour les coordonnées de fin avec les coordonnées actuelles de la souris
        canvas.coords(rect_id, start_x, start_y, end_x, end_y)  # redimensionne le rectangle
        # met à jour les coordonnées du rectangle pour l'étendre entre le point de départ et la position actuelle de la souris

# gère la fin du glissement, lorsque l'utilisateur relâche le bouton de la souris
def on_canvas_release(event):
    global end_x, end_y, selecting  # utilise des variables globales
    if selecting:  # vérifie si la sélection est toujours active
        end_x, end_y = event.x, event.y  # met à jour les coordonnées FINALES après le relâchement
        selecting = False  # désactive le mode sélection empêchant les modifications ultérieures du rectanlge

canvas.bind("<ButtonPress-1>", on_canvas_click)  # associe l'événement de pression sur le bouton à la fonction
canvas.bind("<B1-Motion>", on_canvas_drag)  # associe l'événement de mouvement avec le bouton pressé à la fonction
canvas.bind("<ButtonRelease-1>", on_canvas_release)  # associe l'événement de relâchement du bouton à la fonction

tab_control.add(tab1, text='Affichage Image')  # ajoute l'onglet au contrôle d'onglets
tab_control.pack(expand=1, fill='both')  # affiche le contrôle d'onglets en remplissant et en étendant

langues = {"Anglais": "en", "Espagnol": "es", "Allemand": "de"}  # dictionnaire des options de langue
langue_var = tk.StringVar(value="en")  # variable de contrôle avec une valeur par défaut
langue_menu = ttk.Combobox(right_frame, textvariable=langue_var, values=list(langues.keys()))  # crée une liste déroulante pour la langue
langue_menu.pack(pady=10)  # positionne la liste déroulante


# Fonction mise à jour pour afficher les coordonnées (à compléter)
def extraction_aude():
    global destinataire, emetteur, prix, produit, numero_facture, date, echeance
    categories = {
        "Destinataire": destinataire,
        "Emetteur": emetteur,
        "Prix": prix,
        "Produits Commandés": produit,
        "N° Facture": numero_facture,
        "Date": date,
        "Echéance": echeance
    }
    # Construire et afficher le message avec les coordonnées
    message = "Coordonnées des catégories sélectionnées :\n"
    for label, coords in categories.items():
        if coords:
            message += f"{label}: {coords}\n"
        else:
            message += f"{label}: Non défini\n"
    print(message)

# Bouton pour lancer la traduction (à faire....)
btn_show_coords = tk.Button(right_frame, text="Afficher Coordonnées", command=extraction_aude)
btn_show_coords.pack(pady=10)


root.mainloop()
