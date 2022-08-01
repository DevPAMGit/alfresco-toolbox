import os
from os import path

from modules.controleurs.controleurdonnees import ControleurDonnees
from modules.controleurs.generateurs.GenerateurAlfrescoHelper import GenerateurAlfrescoHelperFichier
from modules.controleurs.generateurs.controleurgenerateur import ControleurGenerateur
from modules.modeles.modele import Modele
from modules.vue.vue import Vue


# Le controleur du script.
class Controleur:

    # Initialise une nouvelle instance de la classe 'Controleur'.
    def __init__(self):
        self.VUE = Vue()
        self.MODELE = Modele()
        self.GENERATEUR = ControleurGenerateur(self.MODELE)
        self.CONTROLEUR_DONNEES = ControleurDonnees(self.VUE, self.MODELE)

    # Génère les fichiers modèles du projet.
    # chemin Le chemin vers
    def generer_projet(self, chemin):
        self.VUE.welcome()

        exit() if not self.verifier_chemin(chemin) else self.CONTROLEUR_DONNEES.charger_donnees_projet(chemin)
        if not self.creer_arborescence():
            exit()

        self.GENERATEUR.creer_service_noeud()
        self.GENERATEUR.creer_noeud_modele()



        # GenerateurAlfrescoHelperFichier(self.MODELE, self.VUE).creer_fichier_aide_source()


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



