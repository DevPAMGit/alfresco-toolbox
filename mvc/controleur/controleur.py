from os import path
import os

from mvc.controleur.generateur_fichier_aide_source_controleur import GenerateurFichierControleur
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
        self.vue.information("[ETAPE 2] Création de l'arborescence pour les modèles")
        creer_dossier(self.modele.get_chemin_types())
        creer_dossier(self.modele.get_chemin_aspects())
        creer_dossier(self.modele.get_chemin_helper())
        self.vue.information("........[OK]\n")

    # Lance le projet.
    def run(self):
        self.vue.bienvenue()
        self.set_chemin_projet()
        self.creer_arborescence()

        generateur_fichier = GenerateurFichierControleur(self.modele, self.vue)
        generateur_fichier.creer_fichier_aide_source()

    # Modifie le chemin du projet.
    def set_chemin_projet(self):
        self.vue.information("[ETAPE 1] Initialisation du modèle")
        succes = False
        chemin_projet = None

        while not succes:
            chemin_projet = self.vue.demande_chemin_projet()

            # Vérification que le chemin existe.
            if not path.exists(chemin_projet):
                self.vue.print_erreur("Le chemin saisi n'existe pas! ")

            # Vérification que le chemin est un dossier
            elif not path.isdir(chemin_projet):
                self.vue.print_erreur("Le chemin saisi n'est pas un dossier! ")

            # Vérification que le chemin contient le POM d'un projet alfresco (maven).
            elif not path.exists(chemin_projet + "/" + "pom.xml"):
                self.vue.print_erreur("Le chemin saisi n'est pas un dossier Alfresco (ne contient pas le POM)! ")

            # Fin de boucle
            else:
                succes = True

        # Modification du chemin du projet sur le modèle.
        self.modele.set_chemin_projet(chemin_projet)

        self.vue.information("........[OK]\n")
