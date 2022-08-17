import codecs
import os
from os import path

from modules.controleurs.controleurdonnees import ControleurDonnees
from modules.controleurs.generateurs.controleurgenerateur import ControleurGenerateur
from api.action.actioncontroleur import ActionControleur
from modules.controleurs.generateurs.controleurgenerateuraspect import ControleurGenerateurAspect
from modules.controleurs.generateurs.controleurgenerateurshare import ControleurGenerateurShare
from modules.controleurs.generateurs.controleurgenerateurtype import ControleurGenerateurType
from modules.modeles.modele import Modele
from modules.vue.vue import Vue


class Controleur:
    """
    Le controleur du script.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'Controleur'.
        """
        self.VUE = Vue()
        self.MODELE = Modele()
        self.CONTROLEUR_DONNEES = ControleurDonnees(self.VUE, self.MODELE)
        self.GENERATEUR_GENERAL = ControleurGenerateur(self.MODELE, self.VUE)
        self.GENERATEUR_TYPES = ControleurGenerateurType(self.MODELE, self.VUE)
        self.GENERATEUR_ASPECTS = ControleurGenerateurAspect(self.MODELE, self.VUE)
        self.CONTROLEUR_SHARE = ControleurGenerateurShare(self.MODELE, self.VUE)

        self.CONTROLEUR_ACTION = ActionControleur(self.MODELE, self.VUE)

    # Génère les fichiers modèles du projet.
    # chemin Le chemin vers
    def generer_projet(self, chemin):
        self.VUE.welcome()

        if not self.verifier_chemin(chemin):
            exit()

        self.nettoyage_pom(chemin + "/pom.xml")

        self.CONTROLEUR_DONNEES.charger_donnees_projet(chemin)
        if not self.creer_arborescence():
            exit()

        self.generer_fichiers()
        self.CONTROLEUR_SHARE.maj_share_config_custom(self.MODELE.get_aspects(), self.MODELE.get_types())
        self.CONTROLEUR_ACTION.controler()

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
        """
        Génère les fichiers du projet.
        """
        self.VUE.creation_fichier_generaux()
        self.GENERATEUR_GENERAL.creer_service_noeud()
        self.GENERATEUR_GENERAL.creer_noeud_modele()
        self.VUE.creation_aspects()
        self.GENERATEUR_ASPECTS.creer_fichiers_aspects()
        self.VUE.creation_types()
        self.GENERATEUR_TYPES.creer_fichiers_types()

    def nettoyage_pom(self, chemin_pom):
        """
        Méthode permettant de nettoyer le pom. ;
        :param chemin_pom : Le chemin vers le pom. ;
        """
        self.VUE.nettoyage_pom()

        fd = codecs.open(chemin_pom, "r", "utf-8")
        contenu = ""

        for ligne in fd:
            if not ligne.isspace():
                contenu += ligne

        fd.close()

        fd = codecs.open(chemin_pom, "w", "utf-8")
        fd.write(contenu)
        fd.close()

        self.VUE.succes()
