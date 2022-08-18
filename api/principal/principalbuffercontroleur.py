from abc import ABC, abstractmethod

from api.action.actioncontroleur import ActionControleur
from api.donnees.donneescontroleur import DonneesControleur
from api.generale.controleurgenerale import ControleurGenerale
from libs.pythonconsolevue.consolevue import ConsoleVue


class PrincipalBufferControleur(ControleurGenerale, ABC):
    """
    Controleur principale de l'API
    """

    def __init__(self):
        super().__init__(ConsoleVue(100))

    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe du modèle  __ARTIFACT_ID__. ;
        """
        self.CTRL_ACTIONS.maj_artifact_id(artifact_id)
        self.CTRL_DONNEES.maj_artifact_id(artifact_id)

    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe du modèle  __CHEMIN_ID__. ;
        """
        self.CTRL_ACTIONS.maj_chemin_projet(chemin_projet)
        self.CTRL_DONNEES.maj_chemin_projet(chemin_projet)

    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle  __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe du modèle __GROUP_ID__. ;
        """
        self.CTRL_ACTIONS.maj_group_id(group_id)
        self.CTRL_DONNEES.maj_group_id(group_id)

    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        self.CTRL_ACTIONS.maj_chemin_dossier_ressources(chemin_dossier_ressource)
        self.CTRL_DONNEES.maj_chemin_dossier_ressources(chemin_dossier_ressource)

    @abstractmethod
    def ajt_aspect(self, aspect):
        """
        Méthode permettant d'ajouter un nouvel aspect au modèle de données. ;
        :param aspect: L'aspect à ajouter. ;
        """
        pass

    @abstractmethod
    def obt_aspect(self, reference):
        pass
