import codecs
import re
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from libs.pythonconsolevue.consolevue import ConsoleVue


class ControleurGenerale:
    """
    Controleur générale pour toute les apis du scripts.
    """

    def __init__(self, vue: ConsoleVue):
        """
        Initialise une nouvelle instance de la classe 'ActionControleur'.
        :param vue : La vue liée au controleur.
        """
        self.VUE = vue

    @staticmethod
    def ecrire_xml(chemin: str, racine: Element):
        """
        Ecrit un fichier XML. ;
        :param chemin : Le chemin vers ce fichier XML. ;
        :param racine : La racine du noeud. ;
        """
        fd = codecs.open(chemin, "w", "utf-8")

        fd.write(re.sub("\\n\\s*\\n", "\\n",
                        minidom.parseString(ElementTree.tostring(racine, "utf-8")).toprettyxml(indent="\t")))
        fd.close()
