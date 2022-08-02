import os
from os import path

from modules.controleurs.controleurdonnees import ControleurDonnees
from modules.controleurs.generateurs.controleurgenerateur import ControleurGenerateur
from modules.controleurs.generateurs.controleurgenerateuraspect import ControleurGenerateurAspect
from modules.modeles.modele import Modele
from modules.vue.vue import Vue


# Le controleur du script.
class Controleur:

    # Initialise une nouvelle instance de la classe 'Controleur'.
    def __init__(self):
        self.VUE = Vue()
        self.MODELE = Modele()
        self.CONTROLEUR_DONNEES = ControleurDonnees(self.VUE, self.MODELE)
        self.GENERATEUR_GENERAL = ControleurGenerateur(self.MODELE, self.VUE)
        self.GENERATEUR_ASPECTS = ControleurGenerateurAspect(self.MODELE, self.VUE)

    # Génère les fichiers modèles du projet.
    # chemin Le chemin vers
    def generer_projet(self, chemin):
        self.VUE.welcome()

        exit() if not self.verifier_chemin(chemin) else self.CONTROLEUR_DONNEES.charger_donnees_projet(chemin)
        exit() if not self.creer_arborescence() else self.generer_fichiers()

    # Vérifie que le chemin mis en paramètre est un dossier 'maven'.
    # chemin Le chemin vers le dossier maven 'Alfresco'.
    # Retourne vrai si le chemin est valide, sinon faux
    def verifier_chemin(self, chemin):
        self.VUE.verification_chemin()

        if not path.exists(chemin):
            self.VUE.chemin_non_existant()
            return False

        elif not path.isdir(chemin):
            self.VUE.dossier_non_valide()
            return False

        elif not path.exists(chemin + "/pom.xml"):
            self.VUE.maven_non_valide()
            return False

        self.VUE.succes()
        return True

    # Méthode permettant de créer l'arborescence projet.
    def creer_arborescence(self):
        try:
            self.VUE.creation_arborescence()
            if not path.exists(self.MODELE.get_chemin_modele_sources()):
                os.makedirs(self.MODELE.get_chemin_modele_sources())

            if not path.exists(self.MODELE.get_chemin_modele_contenus()):
                os.makedirs(self.MODELE.get_chemin_modele_contenus())

            self.VUE.succes()
        except Exception as e:
            self.VUE.erreur_exception(e, "Une erreur est survenue lors de la création de l'arborescence.")
            return False
        return True

    # Méthode permettant de générer les fichiers du projet.
    def generer_fichiers(self):
        self.VUE.creation_fichier_generaux()
        self.GENERATEUR_GENERAL.creer_service_noeud()
        self.GENERATEUR_GENERAL.creer_noeud_modele()
        self.VUE.creation_aspects()
        self.GENERATEUR_ASPECTS.creer_fichiers_aspects()


