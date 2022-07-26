from xml.etree import ElementTree


# Méthode pour gérer les données du script
def get_xmlns(element):
    return "{" + element.tag[1:element.tag.rindex('}')] + "}"


class Modele:

    # Initialise une nouvelle instance de la classe Vue.
    def __init__(self):
        # Les types disponibles dans le modèle.
        self.types = {}

        # Les aspects disponibles dans le modèle.
        self.aspects = {}

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
        # Le groupe id du projet
        self.GROUP_ID = None
        # Le chemin vers le fichier bootstrap du projet.
        self.CHEMIN_ACTIONS = None
        self.CHEMIN_BOOTSTRAP = None
        self.CHEMIN_RESSOURCE = None

    # Modifie le chemin vers le dossier du projet Alfresco.
    # chemin_projet Chemin vers le dossier du projet Alfresco.
    def set_chemin_projet(self, chemin_projet):
        # Mise à jour du chemin du projet.
        self.CHEMIN_PROJET = chemin_projet

        # Mise à jour du POM en conséquence.
        self.POM = self.CHEMIN_PROJET + "/" + "pom.xml"

        # Récupération de la racine du fichier POM
        self.RACINE = ElementTree.parse(self.POM).getroot()

        # Chargement des éléments projets.
        self.chager_pom_variables()
        # Chargement des éléments projets.
        self.charger_platform_variables()
        # Intialisation des ressources.
        self.charger_resources_variables()
        # Charge le modèle.
        self.charger_modeles()

    # Chargement des éléments projets.
    def chager_pom_variables(self):
        # Mise à jour du XMLNS.
        self.XMLNS = get_xmlns(self.RACINE)
        # Mise à jour du groupe id.
        self.GROUP_ID = self.RACINE.find(".//" + self.XMLNS + "groupId").text
        # Mise à jour de l'artifact id.
        self.ARTIFACT_ID = self.RACINE.find(".//" + self.XMLNS + "artifactId").text

    # Charge les variables necessaire pour gérer les éléments de la platform.
    def charger_platform_variables(self):
        # Mise à jour de chemin vers la plateforme.
        self.CHEMIN_PLATFORME = self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform"

        # Chemin vers les modèles à construire.
        chemin_modele = self.CHEMIN_PLATFORME + "/src/main/java/" + self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace('-', '') + "/" + "modeles"

        # Mise à jour du chemin vers le dossier de types.
        self.CHEMIN_TYPES = chemin_modele + "/types"
        # Mise à jour du chemin vers le dossier des d'aspects.
        self.CHEMIN_ASPECTS = chemin_modele + "/aspects"
        # Mise à jour du chemin vers le dossier des helpers.
        self.CHEMIN_HELPERS = chemin_modele + "/helpers"
        # Mise à jour du chemin vers le dossier des actions.
        self.CHEMIN_ACTIONS = chemin_modele + "/actions"

        root = ElementTree.parse(self.CHEMIN_PLATFORME + "/pom.xml")

    # Méthode permettant d'initialiser les éléments ressources.
    def charger_resources_variables(self):
        # Mise à jour du chemin vers le dossier resource.
        self.CHEMIN_RESSOURCE = self.CHEMIN_PLATFORME + "/src/main/resources"
        # Mise à jour du chemin vers le fichier bootstap de la platrforme.
        self.CHEMIN_BOOTSTRAP = self.CHEMIN_RESSOURCE + "/alfresco/module/" + self.ARTIFACT_ID + "-platform/context/bootstrap-context.xml"

    # Méthode permettant de chargers les aspects définient.
    def charger_modeles(self):
        root = ElementTree.parse(self.CHEMIN_BOOTSTRAP).getroot()
        xmlns = get_xmlns(root)
        for fichier_modele in root.find(".//" + xmlns + "bean").find(xmlns + "property[@name='models']").find(xmlns + "list").findall( xmlns + "value"):
            self.charger_modele(fichier_modele.text)

    # Méthode permettant de charger un fichier
    def charger_modele(self, model):
        print(self.CHEMIN_RESSOURCE + "/" + model.replace("${project.artifactId}", self.ARTIFACT_ID))
        racine = ElementTree.parse(self.CHEMIN_RESSOURCE + "/alfresco/module/" + self.ARTIFACT_ID +"-platform/context/").getroot()
        xmlns = get_xmlns(racine)
        # name = racine.tag[name]

    def get_chemin_types(self):
        return self.CHEMIN_TYPES

    def get_chemin_helper(self):
        return self.CHEMIN_HELPERS

    def get_chemin_aspects(self):
        return self.CHEMIN_ASPECTS

    def get_group_id(self):
        return self.GROUP_ID

    def get_helpers_package(self):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.helpers"


