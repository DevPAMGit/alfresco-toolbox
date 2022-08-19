

# Classe gérant la sortie standard du script.
class Vue:
    def __init__(self):
        self.OK = "[OK]"
        self.INFO = "  [INFO] "
        self.ERROR = "[ERREUR] "
        self.ACTION = "[ACTION] "
        self.PREVIOUS = None

    def succes(self):
        index = self.PREVIOUS
        message = ""
        while index < 96:
            message += "."
            index += 1

        print(message + self.OK)

    def erreur(self, m: str):
        index = self.PREVIOUS
        message = ""
        while index < 99:
            message += "."
            index += 1

        print(message + self.ERROR + "\n" + self.ERROR + m)

    def erreur_exception(self, e: Exception, m: str):
        index = self.PREVIOUS
        message = ""
        while index < 99:
            message += "."
            index += 1

        print(message + self.ERROR + "\n" + self.ERROR + m + "\n" + e)

    @staticmethod
    def welcome():
        print("============= GENERATION DES MODELES ALFRESCO =============")

    # Imprime sur la sortie standard un message signalant l'exécution de l'action de vérification d'un chemin."
    def verification_chemin(self):
        message = self.ACTION + "Vérification du chemin en paramètre."
        self.PREVIOUS = len(message)
        print(message, end="")

    # Imprime sur la sortie standard un message signalant qu'un chemin n'existe pas."
    def chemin_non_existant(self):
        self.erreur("Le chemin saisit n'existe pas.")

    # Imprime sur la sortie standard un message signalant qu'un chemin n'est pas un dossier."
    def dossier_non_valide(self):
        self.erreur("Le chemin saisit n'est pas un dossier.")

    # Imprime sur la sortie standard un message signalant qu'un dossier ne possède pas le fichier xml valide."
    def maven_non_valide(self):
        self.erreur("Le dossier ne contient pas le fichier 'pom.xml'.")

    # Imprime sur la sortie standard signalant le chargement de données."
    def chargement_donnees(self):
        print("\n" + self.INFO + "Chargement des données du projet.")

    # Imprime sur la sortie standard un message signalant le chargement d'un type de contenu.
    def chargement_type_contenu(self, chemin_fichier: str):
        print("\n" + self.INFO + "Chargement des données du fichier '" +
              chemin_fichier[chemin_fichier.rfind('/') + 1: len(chemin_fichier)] + "'.")

    # Imprime sur la sortie standard un message signalant l'exécution de l'action de chargement du fichier
    # 'bootstrap.xml' du sous projet 'platform'.
    def recuperation_bootstrap(self):
        message = self.ACTION + "Chargement du fichier 'boostrap.xml' du sous-projet 'platform'."
        self.PREVIOUS = len(message)
        print(message, end="")

    # Imprime sur la sortie standard un message signalant le chargement d'un typecontenu.
    # nom_aspect Le nmo de l'typecontenu.
    def chargement_aspect(self, nom_aspect):
        print("\n" + self.INFO + "Chargement de l'typecontenu '" + nom_aspect + "'.")

    def chargement_propriete(self, nom_propriete):
        message = self.ACTION + "\tChargement de la propriété '" + nom_propriete + "'."
        self.PREVIOUS = len(message)+6
        print(message, end="")

    def chargement_propriete_mandatory(self, nom_aspect):
        print(self.INFO + "Chargement des propriétés 'mandatory' de l'typecontenu '" + nom_aspect + "'.")

    def ajout_propriete_aspect(self, nom_aspect):
        message = self.INFO + "Chargement des propriétés de l'typecontenu '" + nom_aspect + "'."
        print(message)

    def chargement_type(self, nom_type):
        print("\n" + self.INFO + "Chargement du type '" + nom_type + "'.")

    def chargement_proprietes_parent(self, nom_aspect_parent):
        print(self.INFO + "Chargement des propriétés du parent '" + nom_aspect_parent + "' de l'typecontenu.")

    def creation_arborescence(self):
        message = self.ACTION + "Création de l'arborescence du projet."
        self.PREVIOUS = len(message)
        print(message, end="")

    def erreur_creation_arborescence(self, e: Exception):
        print(self.ERROR + "")

    def creation_fichier_generaux(self):
        print("\n" + self.INFO + "Création des fichiers généraux.")

    def creation_fichier(self, nom_fichier):
        message = self.ACTION + "Création du fichier '" + nom_fichier + "'."
        self.PREVIOUS = len(message)
        print(message, end="")

    def creation_aspects(self):
        print("\n" + self.INFO + "Création des fichiers aspects.")

    def creation_types(self):
        print("\n" + self.INFO + "Création des fichiers types.")

    def nettoyage_pom(self):
        message = "\n" + self.ACTION + "Nettoyage du POM du projet."
        self.PREVIOUS = len(message)
        print(message, end="")

    def info(self, message):
        """
        Message permettant d'imprimer sur la sortie standard une information. ;
        :param message: Le message à imprimer sur la sortie standard. ;
        """
        print("\n" + self.INFO + "Création des fichiers aspects.")

    def action(self, message):
        """
        Message permettant d'imprimer sur la sortie standard une action. ;
        :param message : Le message à imprimer sur la sortie standard. ;
        """
        a_imprimer = self.ACTION + message
        self.PREVIOUS = len(a_imprimer)
        print(a_imprimer, end="")
