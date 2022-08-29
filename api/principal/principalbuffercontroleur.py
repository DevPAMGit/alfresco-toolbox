from abc import ABC, abstractmethod

from api.generale.controleurgenerale import ControleurGenerale
from api.modele.modele import Modele
from libs.pythonconsolevue.consolevue import ConsoleVue


class PrincipalBufferControleur(ControleurGenerale, ABC):
    """
    Controleur principale de l'API
    """

    def __init__(self, vue: ConsoleVue):
        super().__init__(vue)

    @abstractmethod
    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe du modèle  __ARTIFACT_ID__. ;
        """
        pass

    @abstractmethod
    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe du modèle  __CHEMIN_ID__. ;
        """
        pass

    @abstractmethod
    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle  __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe du modèle __GROUP_ID__. ;
        """
        pass

    @abstractmethod
    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        pass

    @abstractmethod
    def ajt_aspect(self, aspect: Modele):
        """
        Méthode permettant d'ajouter un nouvel typecontenu au modèle de données. ;
        :param aspect: L'typecontenu à ajouter. ;
        """
        pass

    @abstractmethod
    def obt_aspect(self, reference) -> Modele:
        pass

    @abstractmethod
    def ajt_type(self, t: Modele):
        """
        Ajoute un type au modèle de données.
        :param t: Le type à ajouter.
        """
        pass

    @abstractmethod
    def obt_aspects(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects du projet.
        :return: Un dictionnaire des aspects du projet.
        """
        pass

    @abstractmethod
    def obt_types(self):
        """
        Méthode permettant de récupérer les types du projet.
        :return: Un dictionnaire des aspects du projet.
        """
        pass

    @abstractmethod
    def obt_type(self, reference):
        """
        Méthode permettant de récupérer un type grâce à sa référence.
        :param reference: La référence dont on souhaite récupérer le type.
        :return: Le type référencé par la référence ou None.
        """
        pass
