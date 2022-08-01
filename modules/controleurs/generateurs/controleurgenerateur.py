import codecs
import os

from modules.modeles.modele import Modele


# Classe controleur pour générer les fichiers.
class ControleurGenerateur:

    # Initialise une nouvelle instance de la classe 'ControleurGenerateur'.
    # modele Le modèle de donnée du script.
    def __init__(self, modele: Modele):
        self.MODELE = modele

    # Méthode permettant de créer le fichier de services de nœuds personnalisés du projet.
    def creer_service_noeud(self):
        fd2 = codecs.open(self.MODELE.get_chemin_modele_sources() + "/AlfrescoHelper.java", "w", "utf-8")
        fd1 = codecs.open(self.get_chemin_service_noeud(), "r", "utf-8")

        fd2.write("package " + self.MODELE.get_package_modele_sources() + "\n")
        for ligne in fd1:
            fd2.write(ligne)

    @staticmethod
    def get_chemin_service_noeud():
        chemin = os.path.realpath(__file__)
        return chemin[0:chemin.rindex("\\")+1] + "../../../ressources/alfrescoservicenoeud.java.sauv"

    @staticmethod
    def get_chemin_modele_noeud():
        chemin = os.path.realpath(__file__)
        return chemin[0:chemin.rindex("\\") + 1] + "../../../ressources/alfrescomodelenoeud.java.sauv"

    def creer_noeud_modele(self):
        fd2 = codecs.open(self.MODELE.get_chemin_modele_sources() + "/AlfrescoModeleHelper.java", "w", "utf-8")
        fd1 = codecs.open(self.get_chemin_modele_noeud(), "r", "utf-8")

        fd2.write("package " + self.MODELE.get_package_modele_sources() + "\n")
        for ligne in fd1:
            fd2.write(ligne)

