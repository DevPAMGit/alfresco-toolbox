import codecs
from xml.etree import ElementTree


# Classe permettant de parser un fichier modèle.
def get_type_propriete(t):
    if t.text == "d:text":
        return "String"

    return None


def ecrire_modele_propriete(fd, propriete):
    nom = propriete.tag["name"][propriete.tag["name"].rindex(':') + 1:len(propriete.tag["name"])]
    # type_propriete = self.get_type_propriete( propriete.find("type").text )
    description = propriete.find("description")
    if description is not None :
        fd.write("/** "+ description.text +" */\n")

    fd.write("public static final QName NOM = QName.createQName(URI, \"" + nom.upper() + "\");\n\n")


class ModeleParseur:

    # Initialise une nouvelle instanec de la classe 'ModeleParseur'
    # chemin_projet_platform Chemin vers le projet platform.
    def __init__(self, chemin_projet_platform, group_id):
        self.URI = None
        self.NAME = None
        self.XMLNS = None
        self.PREFIX = None
        self.ARTIFACT_ID = None
        self.GROUP_ID = group_id
        self.charger_pom(chemin_projet_platform + "/pom.xml")
        self.DOSSIER_RESSOURCES = chemin_projet_platform + "src/main/resources"
        self.FICHIER_BOOTSTRAP = self.DOSSIER_RESSOURCES + "/alfresco/module/" + self.ARTIFACT_ID + "/context/bootstrap-context.xml"

    # Charge l'artifact id du projet.
    # chemin_pom Le chemin vers le fichier pom.xml du projet platform du projet maven alfresco all-inn-one.
    def charger_artifact_id(self, chemin_pom):
        self.ARTIFACT_ID = ElementTree.parse(chemin_pom).getroot().find(".//" + self.XMLNS + "artifactId").text

    # Charge les modèles du fichier bootstrap.
    def charger_modeles(self):
        racine = ElementTree.parse(self.FICHIER_BOOTSTRAP).getroot()
        xmlns = "{" + racine.tag[1:racine.tag.rindex('}')] + "}"
        for noeud_modele in racine.find(".//" + xmlns + "bean").find(xmlns + "property[@name='models']").find(xmlns + "list").findall( xmlns + "value")
            self.charger_modele(self.DOSSIER_RESSOURCES + "/" + noeud_modele.text.replace("${project.artifactId}", self.ARTIFACT_ID))

    def charger_modele(self, fichier_modele):
        racine = ElementTree.parse(fichier_modele).getroot()
        self.XMLNS = "{" + racine.tag[1:racine.tag.rindex('}')] + "}"
        namespace = racine.find(".//" + self.XMLNS + "namespaces/namespace")

        self.URI = namespace.tag["uri"]
        self.PREFIX = namespace.tag["prefix"]

        # self.charger_type(racine, fd)
        self.charger_aspects(racine)

    #
    def charger_aspects(self, racine):
        for aspect in racine.find(".//" + self.XMLNS + "aspects").findall(self.XMLNS + "aspect"):
            nom = aspect.tag["name"][aspect.tag["name"].rindex(':') + 1:len(aspect.tag["name"])]
            nom_fichier_modele = nom.capitalize() + "Modele.java"
            nom_fichier_helper = nom.capitalize() + "HelperModele.java"
            self.charger_aspect(
                codecs.open(self.DOSSIER_ASPECT+ "/" + nom_fichier_modele, "w", "utf-8"),
                # codecs.open(self.DOSSIER_ASPECT + "/" + nom_fichier_helper, "w", "utf-8"),
                None,
                aspect, nom)

    def charger_aspect(self, fd_modele, fd_helper, aspect, nom):
        self.vue.information("Génération du fichier java 'AlfrescoModeleHelper'.")
        succes = True

        self.ecrire_modele(fd_modele, aspect, nom)


    def ecrire_modele(self, fd_modele, aspect, nom):
        fd_modele.write("package " + self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.aspect;\n\n")

        fd_modele.write(
            "/** Classe pour l'aspect '" + aspect.tag["name"] + "'. */\n"
            "public class " + nom.capitalize() + "Modele extends AlfrescoModeleHelper {\n\n"

            "\t/** Le prefixe  du type de contenu. */\n"
            "\tpublic final static String PREFIXE = \"" + self.PREFIX + "\";\n\n"

            "\t/** Le nom  du type de contenu. */\n"
            "\tpublic static final QName NOM = QName.createQName(URI, \"" + nom.upper() + "\");\n\n
        )


    def charger_propriete(self, fd, aspect):
        try:
            for propriete in aspect.find(self.XMLNS + "properties").findall("property"):
                ecrire_modele_propriete(fd, propriete)
        except Exception as e :
            pass
