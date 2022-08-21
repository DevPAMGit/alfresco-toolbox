from api.generale.modelegenerale import ModeleGenerale
from api.modele.modele import Modele


class ModeleModele(ModeleGenerale):
    """
    Modèle de données pour l'api gérant les aspects du projet.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'AspectModele'.
        """
        super().__init__()
        self.MODELES: dict[str, Modele] = {}

    def ajt_modele(self, modele: Modele):
        """
        Ajoute un modèle dans le modèle de données.
        :param modele: Le modèle à ajouter.
        """
        self.MODELES[modele.NOM_COMPLET] = modele

    def obt_modele(self, reference: str) -> (Modele | None):
        """
        Méthode permettant d'obtenir un modèle par son nom.
        :param reference: Le nom du modèle à récupérer.
        :return: Le modèle référencé par le nom.
        """
        if reference in self.MODELES.keys():
            resultat: (Modele | None) = self.MODELES[reference]
        else:
            resultat = None

        return resultat

    def obt_modeles(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects du modèle.
        :return: Un dictionnaire des aspects du modèle.
        """
        return self.MODELES

    def obt_chemin_modele(self, genre: str, modele: Modele) -> str:
        """
        Méthode permettant de récupérer le chemin vers le dossier d'un modèle.
        :param genre: Le type du modèle (aspect ou type)
        :param modele: Le modèle
        :return: Le chemin vers le dossier d'un modèle.
        """
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" + \
               self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/modeles/typescontenus/" + \
               modele.PREFIX.lower() + "/" + genre.lower() + "/" + modele.NOM.lower()

    def obt_java_modele_package(self, modele: Modele, genre: str):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.typescontenus." + modele.PREFIX + \
               "." + genre.lower() + "." + modele.NOM.lower()

    def obt_alfresco_sources_classes_package(self):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.sources"

    def obt_chemin_alfresco_sources_classes(self):
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" + \
               self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/modeles/sources"

    def get_chemin_config_custom_fichier(self):
        """
        Permet d'obtenir le chemin vers le fichier 'share-config-custom.xml".
        :return: Le chemin vers le fichier 'share-config-custom.xml".
        """
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + \
               "-share/src/main/resources/META-INF/share-config-custom.xml"

