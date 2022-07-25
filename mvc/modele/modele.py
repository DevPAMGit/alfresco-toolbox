from xml.etree import ElementTree


# Méthode pour gérer les données du script
def get_xmlns(element):
    return "{" + element.tag[1:element.tag.rindex('}')] + "}"


class Modele:

    # Initialise une nouvelle instance de la classe Vue.
    def __init__(self):
        # Les types disponibles dans le modèle.
        self.types = []

        # Les aspects disponibles dans le modèle.
        self.aspects = []

        # Chemin vers le dossier du projet Alfresco.
        self.CHEMIN_PROJET = None

        # Chemin vers le fichier POM du projet Alfresco.
        self.POM = None

        # La racine du fichier XML
        self.RACINE = None

        # Le XMLNS du fichier POM
        self.XMLNS = None

        # L'artifact id.
        self.ARTIFACT_ID = None
        # Le chemin vers la plateforme.
        self.CHEMIN_PLATFORME = None
        # Le chemin vers le dossier modèle.
        # Self.CHEMIN_MODELE = None

        # Le chemin vers le dossier modèle.
        self.CHEMIN_TYPES = None
        # Le chemin vers le dossier modèle.
        self.CHEMIN_ASPECTS = None
        # Le chemin vers le dossier modèle.
        self.CHEMIN_HELPERS = None
        #
        self.GROUP_ID = None

    # Modifie le chemin vers le dossier du projet Alfresco.
    # chemin_projet Chemin vers le dossier du projet Alfresco.
    def set_chemin_projet(self, chemin_projet):
        # Mise à jour du chemin du projet.
        self.CHEMIN_PROJET = chemin_projet

        # Mise à jour du POM en conséquence.
        self.POM = self.CHEMIN_PROJET + "/" + "pom.xml"

        # Récupération de la racine du fichier POM
        self.RACINE = ElementTree.parse(self.POM).getroot()

        # Mise à jour du XMLNS.
        self.XMLNS = get_xmlns(self.RACINE)

        # Mise à jour de l'artifact id.
        self.ARTIFACT_ID = self.RACINE.find(".//" + self.XMLNS + "artifactId").text
        # Mise à jour du chemin vers la plateforme.
        self.CHEMIN_PLATFORME = self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform"

        #
        self.GROUP_ID = self.RACINE.find(".//" + self.XMLNS + "groupId").text

        # Chemin vers les modèles à construire.
        chemin_modele = self.CHEMIN_PLATFORME + "/src/main/java/" + self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace('-', '') + "/" + "modeles"

        # Mise à jour du chemin vers le dossier de types.
        self.CHEMIN_TYPES = chemin_modele + "/types"
        # Mise à jour du chemin vers le dossier de d'aspects.
        self.CHEMIN_ASPECTS = chemin_modele + "/aspects"
        # Mise à jour du chemin vers le dossier des helpers.
        self.CHEMIN_HELPERS = chemin_modele + "/helpers"

    def get_chemin_types(self):
        return self.CHEMIN_TYPES

    def get_chemin_helper(self):
        return self.CHEMIN_HELPERS

    def get_chemin_aspects(self):
        return self.CHEMIN_ASPECTS

    def get_group_id(self):
        return self.GROUP_ID

    def get_aide_package(self):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.helpers"
