import codecs
import re
from abc import ABC, abstractmethod
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from libs.pythonconsolevue.consolevue import ConsoleVue


class ControleurGenerale(ABC):
    """
    Controleur générale pour toute les apis du script.
    """

    def __init__(self, vue: ConsoleVue):
        """
        Initialise une nouvelle instance de la classe 'ActionControleur'. ;
        """
        self.VUE = vue

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

    @staticmethod
    def ecrire_xml(chemin: str, racine: Element):
        """
        Écrit un fichier XML. ;
        :param chemin : Le chemin vers ce fichier XML. ;
        :param racine : La racine du noeud. ;
        """
        fd = codecs.open(chemin, "w", "utf-8")

        fd.write(re.sub("\\n\\s*\\n", "\\n",
                        minidom.parseString(ElementTree.tostring(racine, "utf-8")).toprettyxml(indent="\t")))
        fd.close()
