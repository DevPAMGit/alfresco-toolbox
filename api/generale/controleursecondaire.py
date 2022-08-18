from xml.etree.ElementTree import Element

from api.generale.controleurgenerale import ControleurGenerale
from libs.pythonconsolevue.consolevue import ConsoleVue
from api.generale.modelegenerale import ModeleGenerale


class ControleurSecondaire(ControleurGenerale):

    def __init__(self, vue: ConsoleVue, modele: ModeleGenerale):
        super().__init__(vue)
        self.MODELE = modele

    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe du modèle  __ARTIFACT_ID__. ;
        """
        self.MODELE.maj_artifact_id(artifact_id)

    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe du modèle __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe du modèle  __CHEMIN_ID__. ;
        """
        self.MODELE.maj_chemin_projet(chemin_projet)

    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe du modèle  __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe du modèle __GROUP_ID__. ;
        """
        self.MODELE.maj_group_id(group_id)

    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        self.MODELE.maj_chemin_dossier_ressources(chemin_dossier_ressource)

    @staticmethod
    def obt_xmlns(racine: Element) -> str:
        """
        Méthode permettant de récupérer le 'xmlns" de la racine d'un XML. ;
        :param racine: La racine d'un fichier XML. ;
        :return: Une chaîne de caractère
        """
        return racine.tag[0: racine.tag.rindex("}") + 1]