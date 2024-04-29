import mysql.connector
import datetime
import calendar
from decimal import Decimal

# fonction de connexion à la base de données MySQL
def connect_to_db():
    # connexion à la base de données MySQL
    connection = mysql.connector.connect(
        # adresse du serveur
        host="projet-trad.mysql.database.azure.com",
        # nom d'utilisateur de la base de données
        user="headofappli",
        # mot de passe de la base de données
        password="aPp*lxujD_ic@ti0n",
        # nom de la base de données
        database="factures"
    )

    # création d'un curseur pour exécuter des commandes SQL
    cursor = connection.cursor()

    # retourne la connexion et le curseur
    return connection, cursor

# fonction pour enregistrer une facture dans la base de données
def enregistrer_facture(connection, cursor, date_facture, emetteur, montant_original,
                        devise_originale, montant_euros, categorie, test=0):
    # création de la table factures si elle n'existe pas déjà
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS factures 
        (id INT AUTO_INCREMENT PRIMARY KEY, 
        date_ajout_BDD DATE DEFAULT (CURRENT_DATE()),
        date_facture DATE,
        emetteur VARCHAR(255), 
        montant_original FLOAT, 
        devise_originale VARCHAR(255),
        montant_euros FLOAT,
        categorie VARCHAR(255),
        nb_caracteres_traduits INT, 
        langue_cible VARCHAR(255),
        est_test INT
        )''')

    # insertion des données dans la table (seulement pour l'enregistrement de la facture)
    cursor.execute(
        "INSERT INTO factures (date_facture, emetteur, montant_original, devise_originale, "
        "montant_euros, categorie, est_test) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (date_facture, emetteur, montant_original, devise_originale, montant_euros, categorie, test))

    # validation des modifications de la base de données
    connection.commit()

    # récupération de l'identifiant de la dernière facture insérée
    id_facture = cursor.lastrowid
    # on renvoie l'ID de la facture qu'on vient d'insérer à la table
    return id_facture

# fonction qui ajoute les données relatives à la traduction pour une facture déjà enregistrée
def traduction_facture(id_facture, connection, cursor, langue_cible, texte):
    # calcul du nombre de caractères du texte
    nb_caracteres = len(texte)

    # mise à jour de la table factures avec les données de la traduction (pour une facture déjà existante)
    cursor.execute(
        "UPDATE factures SET langue_cible = %s, nb_caracteres_traduits = %s WHERE id = %s",
        (langue_cible, nb_caracteres, id_facture))

    # on enregistre les modifications
    connection.commit()


# fonction pour compter le nombre de factures reçues pendant une période donnée
def nb_facture_recues(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour compter le nombre de factures pour une période donnée
    query = """
    -- sélectionne et compte le nombre d'identifiants uniques de factures
    SELECT COUNT(id) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement les factures émises après une date spécifiée
    WHERE date_facture >= %s AND date_facture <= %s
    """

    # on lance la requête avec en argument la période de début
    cursor.execute(query, (debut, fin,))
    # extraction du résultat et si aucun résultat, retourne 0
    nombre_fact_recues = cursor.fetchone()[0] or 0

    # on renvoie le nombre de factures reçues
    return nombre_fact_recues

# fonction pour compter le nombre de factures traitées pendant une période donnée
def nb_facture_traitees(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le nombre de factures traitées pour la période donnée
    query = """
    -- sélectionne et compte le nombre d'identifiants uniques de factures
    SELECT COUNT(id) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement les factures traitées après une date spécifiée
    WHERE date_ajout_BDD >= %s AND date_facture <= %s
    """

    # on lance la requête avec en argument la période de début
    cursor.execute(query, (debut, fin,))
    # extraction du résultat et si aucun résultat, retourne 0
    nombre_fact_traitees = cursor.fetchone()[0] or 0

    # on renvoie le nombre de factures traitées
    return nombre_fact_traitees

# fonction pour calculer le prix moyen des factures sur une période donnée
def prix_moyen_facture(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le prix moyen des factures pour la période donnée
    query = """
    -- calcule la moyenne des montants des factures
    SELECT AVG(montant_euros) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement à partir d'une date donnée
    WHERE date_facture >= %s AND date_facture <= %s
    """

    # on lance la requête avec le début de la période donnée en argument
    cursor.execute(query, (debut, fin,))
    # on récupère le résultat ou on renvoie 0 s'il n'y a pas de résultat
    avg_price = cursor.fetchone()[0] or 0 # si aucun résultat, retourne 0

    # on retourne le prix moyen
    return avg_price

# fonction pour calculer le prix moyen d'un type de facture sur une période donnée
def prix_moyen_facture_categorie(mois, annee, categorie, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le prix moyen d'un type de facture sur une période donnée
    query = """
    -- calcule la moyenne des montants des factures
    SELECT AVG(montant_euros) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement à partir d'une date donnée et pour une catégorie donnée
    WHERE date_facture >= %s AND date_facture <= %s AND categorie = %s
    """

    # lance la requête et passe la période donnée et la catégorie en arguments
    cursor.execute(query, (debut, fin, categorie,))

    # récupère le résultat ou 0 s'il n'y pas de résultat
    avg_price = cursor.fetchone()[0] or 0

    # renvoie le prix moyen pour le type de facture
    return avg_price

# fonction pour calculer le prix moyende tous les types de facture sur une période donnée
def prix_moyen_toutes_categories(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le prix moyen d'un type de facture sur une période donnée
    query = """
    -- calcule la moyenne des montants des factures et récupère les catégories
    SELECT categorie, AVG(montant_euros) AS prix_moyen
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement à partir d'une date donnée et pour une catégorie donnée
    WHERE date_facture >= %s AND date_facture <= %s 
    -- on regroupe les factures par catégories 
    GROUP BY categorie
    """

    # lance la requête et passe la période donnée et la catégorie en arguments
    cursor.execute(query, (debut, fin, ))

    # récupère tous les résultats sous forme de liste de tuples (categorie, prix_moyen)
    resultats = cursor.fetchall() or []

    # retourne la liste des tuples (categorie, prix)
    return resultats


# fonction pour compter le nombre total de caractères traduits
def nb_caracteres_traduits(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le nombre total de caractères traduits sur une période donnée
    query = """
    -- calcule la somme totale des caractères traduits (par une addition)
    SELECT SUM(nb_caracteres_traduits) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement à partir d'une date donnée 
    -- on utilise date_ajout_BDD en raison de la limitation de 500 000 caractères par mois de DeepL
    WHERE date_ajout_BDD >= %s AND date_ajout_BDD <= %s
    """

    # lance la requête et passe la période donnée en argument
    cursor.execute(query, (debut, fin,))

    # récupère le résultat ou 0 s'il n'y a pas de résultat
    total_caracteres = cursor.fetchone()[0] or Decimal(0.0)

    # on renvoie le nombre total de caractères traduits sur la période
    return total_caracteres

# fonction pour calculer la fréquence d'utilisation d'une langue cible pour les traductions (%)
def frequence_langue_cible(mois, annee, langue, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir la fréquence en % d'utilisation d'une langue cible pour les traductions sur une période donnée
    query = """
    -- sélectionne la colonne 'langue_cible' pour afficher la langue des traductions
    SELECT langue_cible,    
    -- compte le nombre total de traductions pour chaque langue cible
    COUNT(*) AS nombre_traductions,
    -- calcule le pourcentage de traductions pour chaque langue par rapport au total des traductions
        -- sous-requête pour compter le total des traductions ayant une langue cible non nulle depuis la date spécifiée
    (COUNT(*) * 100.0 / GREATEST(1, (SELECT COUNT(*) FROM factures WHERE date_facture >= %s AND 
    date_facture <= %s AND langue_cible IS NOT NULL))) AS pourcentage
    -- à partir de la table 'factures'
    FROM factures
    -- filtre les factures ajoutées depuis une date donnée où la langue cible est spécifiée
    WHERE date_facture >= %s AND date_facture <= %s AND langue_cible IS NOT NULL
    -- groupe les résultats par langue cible pour faire les agrégations
    GROUP BY langue_cible;
    """

    # lance la requête et passe la période donnée en argument 2 fois (car il y a une sous-requête)
    cursor.execute(query, (debut, fin, debut, fin,))

    # boucle infinie pour récupérer les résultats
    while True:
        # récupère la prochaine ligne
        row = cursor.fetchone()
        # si la ligne est vide (fin des résultats), on sort de la boucle
        if row is None:
            # récupère toutes les lignes restantes pour nettoyer le curseur
            cursor.fetchall()
            break
        # si la langue cible correspond à celle recherchée
        if langue == row[0]:
            # récupère toutes les lignes restantes pour nettoyer le curseur
            cursor.fetchall()
            # on retourne le % correspondant à la langue recherchée
            return row[2]
    # récupère toutes les lignes restantes pour nettoyer le curseur
    cursor.fetchall()
    # si aucune correspondance, on retourne 0
    return 0;


def frequence_toutes_langues_cibles(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir la fréquence en % d'utilisation de chaque langue cible pour les traductions sur une période donnée
    query = """
    -- sélectionne la colonne 'langue_cible' pour afficher la langue des traductions
    SELECT langue_cible,    
    -- compte le nombre total de traductions pour chaque langue cible
    COUNT(*) AS nombre_traductions,
    -- calcule le pourcentage de traductions pour chaque langue par rapport au total des traductions
        -- sous-requête pour compter le total des traductions ayant une langue cible non nulle depuis la date spécifiée
    (COUNT(*) * 100.0 / GREATEST(1, (SELECT COUNT(*) FROM factures WHERE date_facture >= %s AND 
    date_facture <= %s AND langue_cible IS NOT NULL))) AS pourcentage
    -- à partir de la table 'factures'
    FROM factures
    -- filtre les factures ajoutées depuis une date donnée où la langue cible est spécifiée
    WHERE date_facture >= %s AND date_facture <= %s AND langue_cible IS NOT NULL
    -- groupe les résultats par langue cible pour faire les agrégations
    GROUP BY langue_cible;
    """

    # exécute la requête en passant la période donnée en argument 2 fois (car il y a une sous-requête)
    cursor.execute(query, (debut, fin, debut, fin,))

    # récupère tous les résultats
    resultats = cursor.fetchall()

    # construit une liste de tuples contenant seulement la langue cible et le pourcentage
    # on saute le nombre de traductions
    liste_langues_pourcentages = [(langue, pourcentage) for langue, _, pourcentage in resultats]

    # retourne la liste des tuples (langue, pourcentage)
    return liste_langues_pourcentages



# fonction pour obtenir la fréquence d'apparition d'une catégorie (en %) sur une période donnée
def frequence_categorie(mois, annee, categorie, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir la fréquence d'une catégorie dans les traductions depuis le début du temps spécifié
    query = """
    -- sélectionne la colonne 'categorie' pour grouper les résultats par catégorie
    SELECT categorie, 
     -- compte le nombre total de factures par catégorie
    COUNT(*) AS nombre_categorie,
    -- calcule le pourcentage de chaque catégorie par rapport au total des factures
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM factures WHERE date_facture >= %s 
    and date_facture <= %s)) AS pourcentage
    -- à partir de la table 'factures'
    FROM factures
    -- seulement pour une période donnée
    WHERE date_facture >= %s AND date_facture <= %s
    -- groupe les résultats par catégorie pour effectuer les calculs
    GROUP BY categorie;
    """

    # lance la requête et passe la période donnée en argument 2 fois (car sous-requête)
    cursor.execute(query, (debut, fin, debut, fin,))

    # boucle infinie pour récupérer les résultats
    while True:
        # récupère la prochaine ligne
        row = cursor.fetchone()
        # si la ligne est vide (fin des résultats), sort de la boucle
        if row is None:
            # récupère toutes les lignes restantes pour nettoyer le curseur
            cursor.fetchall()
            break
            # si la catégorie correspond à celle recherchée
        if categorie == row[0]:
            # récupère toutes les lignes restantes pour nettoyer le curseur
            cursor.fetchall()
            return row[2] # on retourne le pourcentage correspondant à la catégorie
    # récupère toutes les lignes restantes pour nettoyer le curseur
    cursor.fetchall()
    # si aucune correspondance, on retourne 0
    return 0


# fonction pour obtenir la fréquence d'apparition de toutes les catégories (en %) sur une période donnée
def frequence_toutes_categories(mois, annee, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir la fréquence d'une catégorie dans les traductions depuis le début du temps spécifié
    query = """
    -- sélectionne la colonne 'categorie' pour grouper les résultats par catégorie
    SELECT categorie, 
     -- compte le nombre total de factures par catégorie
    COUNT(*) AS nombre_categorie,
    -- calcule le pourcentage de chaque catégorie par rapport au total des factures
    (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM factures WHERE 
    date_facture >= %s and date_facture <= %s)) AS pourcentage
    -- à partir de la table 'factures'
    FROM factures
    -- seulement pour une période donnée
    WHERE date_facture >= %s AND date_facture <= %s
    -- groupe les résultats par catégorie pour effectuer les calculs
    GROUP BY categorie;
    """

    # lance la requête et passe la période donnée en argument 2 fois (car sous-requête)
    cursor.execute(query, (debut, fin, debut, fin,))

    resultats = cursor.fetchall()

    # construit une liste de tuples contenant seulement la catégorie et le pourcentage
    liste_categories_pourcentage = [(categorie, pourcentage) for categorie, _, pourcentage in resultats]

    return liste_categories_pourcentage


# fonction pour calculer le montant cumulé des factures par catégorie sur une période donnée
def somme_factures_categorie(mois, annee, categorie, cursor):
    # détermination de la date de début de la période
    debut, fin = temporalite(mois, annee)

    # requête pour obtenir le prix moyen d'un type de facture sur une période donnée
    query = """
    -- calcule la moyenne des montants des factures
    SELECT SUM(montant_euros) 
    -- à partir de la table 'factures'
    FROM factures 
    -- seulement à partir d'une date donnée et pour une catégorie donnée
    WHERE date_facture >= %s AND date_facture <= %s AND categorie = %s
    """

    # lance la requête et passe la période donnée et la catégorie en arguments
    cursor.execute(query, (debut, fin, categorie,))

    # récupère le résultat ou 0 s'il n'y pas de résultat
    sum_invoices = cursor.fetchone()[0] or 0

    # renvoie la somme des factures pour le type de facture
    return sum_invoices


# fonction pour récupérer le nombre total de caractères traduits ce mois-vci
def total_caracteres_mois():
    # on récupère la connexion et le curseur
    connection, cursor = connect_to_db()

    # Calculer le début du mois actuel
    debut_du_mois = datetime.date.today().replace(day=1)

    # Requête pour obtenir la somme des caractères traduits depuis le début du mois
    query = """
    SELECT SUM(nb_caracteres_traduits) 
    FROM factures 
    WHERE date_ajout_BDD >= %s
    """
    cursor.execute(query, (debut_du_mois,))
    total_caracteres_mois = cursor.fetchone()[0] or 0

    print(f"Total des caractères traduits depuis le début du mois : {total_caracteres_mois}")

    cursor.close()
    connection.close()  # Fermeture de la connexion à la base de données
    return int(total_caracteres_mois)


def afficher_informations_facture(id_facture):
    connection, cursor = connect_to_db()
    query = """
            SELECT id, date_ajout_BDD, date_facture, emetteur, montant_original, devise_originale, 
                   montant_euros, categorie, nb_caracteres_traduits, langue_cible, est_test 
            FROM factures 
            WHERE id = %s;
            """

    # Exécution de la requête avec l'ID de la facture
    cursor.execute(query, (id_facture,))

    # Récupération des résultats
    result = cursor.fetchone()

    if result:
        print(f"ID Facture: {result[0]}")
        print(f"Date d'ajout dans la BDD: {result[1]}")
        print(f"Date de la facture: {result[2]}")
        print(f"Émetteur: {result[3]}")
        print(f"Montant original: {result[4]} {result[5]}")
        print(f"Montant en euros: {result[6]}")
        print(f"Catégorie: {result[7]}")
        print(f"Nombre de caractères traduits: {result[8]}")
        print(f"Langue cible de la traduction: {result[9]}")
        print(f"Test (0=non, 1=oui): {result[10]}")
    else:
        print("Aucune facture trouvée avec cet ID.")


# fonction pour déterminer la temporalité (toujours, année, mois)
def temporalite(mois, annee):
    # gestion des cas pour toutes les factures depuis le début
    if mois == None and annee == "toutes":
        # début de la période donnée: 1er janvier 2020
        date_debut = datetime.date.today().replace(day=1, month=1, year=2020)
        date_fin = datetime.date.today()
        return date_debut, date_fin

    # gestion des cas pour une année spécifique entière
    elif (mois == None or mois == "tous") and annee != "toutes" and annee:
        # début de la période donnée: le début de l'année courante
        date_debut = datetime.date(year=int(annee), month=1, day=1)
        date_fin = datetime.date(year=int(annee), month=12, day=31)
        return date_debut, date_fin

    # gestion des cas pour un mois spécifique dans une année
    elif mois and annee != "toutes" and annee:
        mois_dict = {
            "janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
            "juin": 6, "juillet": 7, "août": 8, "septembre": 9,
            "octobre": 10, "novembre": 11, "décembre": 12
        }

        if mois in mois_dict:
            annee_int = int(annee)
            mois_int = mois_dict[mois]
            date_debut = datetime.date(annee_int, mois_int, 1)
            dernier_jour = calendar.monthrange(annee_int, mois_int)[1]
            date_fin = datetime.date(annee_int, mois_int, dernier_jour)
            return date_debut, date_fin

    # erreur si mois spécifique mais toutes les années
    elif mois != None and annee == "toutes":
        print("Veuillez sélectionner une année")

    # erreur si autre chose
    else:
        print("Entrée invalide")


# fonction de fermeture de la connexion à la base de données
def fermeture_bdd(connection, cursor):
    # on ferme le curseur
    cursor.close()
    # on ferme la connexion à la base de données
    connection.close()
