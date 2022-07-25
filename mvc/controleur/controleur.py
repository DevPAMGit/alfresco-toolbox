from os import path
import os

from mvc.controleur.generateurs.generateur_alfresco_helper_fichier import GenerateurAlfrescoHelperFichier
from mvc.controleur.generateurs.generateur_alfresco_modele_helper_fichier import GenerateurAlfrescoModeleHelperFichier
from mvc.vue.vue import Vue
from mvc.modele.modele import Modele


# Classe controleur du script
def creer_dossier(chemin):
    if not path.exists(chemin) and not path.isdir(chemin):
        os.makedirs(chemin)


# Controleur ddu projet.
class Controleur:

    # Initialise une nouvelle instance de la classe Vue.
    def __init__(self):
        self.vue = Vue("GENERATEUR DE MODELES ALFRESCO")
        self.modele = Modele()

    # Créé in dossier.
    # chemin Le chemin du dossier.
    # Crée l'arborescence du projet.
    def creer_arborescence(self):
        self.vue.information("Création de l'arborescence")
        try:
            creer_dossier(self.modele.get_chemin_types())
            creer_dossier(self.modele.get_chemin_aspects())
            creer_dossier(self.modele.get_chemin_helper())
        except Exception as e:
            self.vue.print_erreur("")
            self.vue.print_erreur("Voici l'exception qui a été levée :")
            print(e)
            exit()

        self.vue.succes()

    # Lance le projet.
    # chemin_projet Le chemin vers le projet ALfresco.
    def run(self, chemin_projet):
        self.vue.bienvenue()
        self.set_chemin_projet(chemin_projet)
        self.creer_arborescence()
        # Ecriture du fichier 'AlfrescoHelper.java'
        GenerateurAlfrescoHelperFichier(self.modele, self.vue).creer_fichier_aide_source()
        # Ecriture du fichier 'AlfrescoModeleHelper.java'
        GenerateurAlfrescoModeleHelperFichier(self.modele, self.vue).creer_fichier_aide_modele_source()

    # Modifie le chemin du projet.
    def set_chemin_projet(self, chemin_projet):
        self.vue.information("Vérification du chemin vers le projet")

        # Vérification que le chemin existe.
        if not path.exists(chemin_projet):
            self.vue.print_erreur("")
            self.vue.print_erreur("Le chemin saisi n'existe pas! ")
            exit()

        # Vérification que le chemin est un dossier
        elif not path.isdir(chemin_projet):
            self.vue.print_erreur("")
            self.vue.print_erreur("Le chemin saisi n'est pas un dossier! ")
            exit()

        # Vérification que le chemin contient le POM d'un projet alfresco (maven).
        elif not path.exists(chemin_projet + "/" + "pom.xml"):
            self.vue.print_erreur("")
            self.vue.print_erreur("Le chemin saisi n'est pas un dossier Alfresco (ne contient pas le POM)! ")
            exit()

        # Modification du chemin du projet sur le modèle.
        self.vue.succes()
        self.modele.set_chemin_projet(chemin_projet)
