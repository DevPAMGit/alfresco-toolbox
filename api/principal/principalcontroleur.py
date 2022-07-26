import os
from abc import ABC

from api.typecontenu.aspectcontroleur import AspectControleur
from api.modele.modele import Modele
from api.typecontenu.typecontroleur import TypeControleur
from libs.pythonconsolevue.consolevue import ConsoleVue
from api.action.actioncontroleur import ActionControleur
from api.donnees.donneescontroleur import DonneesControleur
from api.principal.principalbuffercontroleur import PrincipalBufferControleur


class ControleurPrincipal(PrincipalBufferControleur, ABC):
    """
    Controleur principale de l'API
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'ControleurPrincipal'.
        """
        super().__init__(ConsoleVue(100))

        self.CTRL_TYPE = TypeControleur(100)
        self.CTRL_ASPECT = AspectControleur(100)
        self.CTRL_ACTIONS = ActionControleur(100)
        self.CTRL_DONNEES = DonneesControleur(self, 100)

    def formatter(self, argv: str):

        self.maj_chemin_dossier_ressources(os.getcwd() + "/ressources")

        self.VUE.titre("FORMATAGE DU PROJET")
        self.CTRL_DONNEES.extraire(argv)
        self.CTRL_ASPECT.creer_fichiers_sources()
        self.CTRL_ASPECT.generer_aspects()
        self.CTRL_TYPE.generer_type()
        self.CTRL_ACTIONS.controler()

    def ajt_aspect(self, aspect: Modele):
        """
        Méthode permettant d'ajouter un nouveau type de contenu au modèle de données.
        :param aspect: Le type de contenu à ajouter. ;
        """
        self.CTRL_ASPECT.ajt_modele(aspect)

    def obt_aspect(self, reference: str) -> (Modele | None):
        """
        Méthode permettant d'ajouter un type de contenu.
        :param reference: Le nom du type de contenu à récupérer.
        :return: Une instance de type Modele.
        """
        return self.CTRL_ASPECT.obt_modele(reference)

    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe du modèle  __ARTIFACT_ID__. ;
        """
        self.CTRL_ACTIONS.maj_artifact_id(artifact_id)
        self.CTRL_DONNEES.maj_artifact_id(artifact_id)
        self.CTRL_TYPE.maj_artifact_id(artifact_id)
        self.CTRL_ASPECT.maj_artifact_id(artifact_id)

    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe du modèle  __CHEMIN_ID__. ;
        """
        self.CTRL_ACTIONS.maj_chemin_projet(chemin_projet)
        self.CTRL_DONNEES.maj_chemin_projet(chemin_projet)
        self.CTRL_TYPE.maj_chemin_projet(chemin_projet)
        self.CTRL_ASPECT.maj_chemin_projet(chemin_projet)

    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle  __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe du modèle __GROUP_ID__. ;
        """
        self.CTRL_ACTIONS.maj_group_id(group_id)
        self.CTRL_DONNEES.maj_group_id(group_id)
        self.CTRL_TYPE.maj_group_id(group_id)
        self.CTRL_ASPECT.maj_group_id(group_id)

    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        self.CTRL_ACTIONS.maj_chemin_dossier_ressources(chemin_dossier_ressource)
        self.CTRL_DONNEES.maj_chemin_dossier_ressources(chemin_dossier_ressource)
        self.CTRL_DONNEES.maj_chemin_dossier_ressources(chemin_dossier_ressource)
        self.CTRL_ASPECT.maj_chemin_dossier_ressources(chemin_dossier_ressource)

    def ajt_type(self, modele: Modele):
        """
        Ajoute un type au modèle de données.
        :param modele: Le type à ajouter.
        """
        self.CTRL_TYPE.ajt_modele(modele)

    def obt_aspects(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects du projet.
        :return: Un dictionnaire des aspects du projet.
        """
        return self.CTRL_ASPECT.obt_modeles()

    def obt_types(self):
        """
        Méthode permettant de récupérer les types du projet.
        :return: Un dictionnaire des aspects du projet.
        """
        return self.CTRL_TYPE.obt_modeles()

    def obt_type(self, reference):
        """
        Méthode permettant de récupérer un type grâce à sa référence.
        :param reference: La référence dont on souhaite récupérer le type.
        :return: Le type référencé par la référence ou None.
        """
        return self.CTRL_TYPE.obt_modele(reference)
