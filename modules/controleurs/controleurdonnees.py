from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from modules.modeles.propriete import Propriete
from modules.modeles.aspect import Aspect
from modules.modeles.modele import Modele
from modules.modeles.type import Type
from modules.vue.vue import Vue


# Classe controleur pour charger les données d'un projet Alfresco.
class ControleurDonnees:

    # Initialise une nouvelle instance de la classe 'ControleurDonnees'.
    # vue La vue du script.
    # modele Le modèle du script.
    def __init__(self, vue: Vue, modele: Modele):
        self.VUE = vue
        self.MODELE = modele

    # Charge les données du projet.
    # chemin Le chemin vers le projet.
    def charger_donnees_projet(self, chemin):
        self.VUE.chargement_donnees()
        for chemin_type_contenu in self.get_bootstrap_root(chemin):
            self.charger_type_contenu(self.MODELE.get_chemin_projet() + "/" + self.MODELE.get_artifact_id()
                                      + "-platform/src/main/resources/"
                                      + chemin_type_contenu.text.replace("${project.artifactId}",
                                                                         self.MODELE.get_artifact_id() + "-platform"))

    # Méthode per
    def get_bootstrap_root(self, chemin):
        self.VUE.recuperation_bootstrap()

        try:

            pom_projet = ElementTree.parse(chemin + "/pom.xml").getroot()
            xmlns_projet = pom_projet.tag[0: pom_projet.tag.rindex("}") + 1]
            self.MODELE.set_group_id(pom_projet.find(".//" + xmlns_projet + "groupId").text)

            self.MODELE.set_artifact_id(pom_projet.find(".//" + xmlns_projet + "artifactId").text)

            chemin_platform = chemin + "/" + self.MODELE.get_artifact_id() + "-platform"
            pom_platform = ElementTree.parse(chemin_platform + "/pom.xml").getroot()

            bootstrap = ElementTree.parse(chemin_platform + "/src/main/resources/alfresco/module/" +
                                          pom_platform.find(pom_platform.tag[0:pom_platform.tag.rindex("}") + 1]
                                                            + "artifactId").text
                                          + "/context/bootstrap-context.xml").getroot()
            xmlns_bootstrap = bootstrap.tag[0:bootstrap.tag.rindex("}") + 1]

            resultat = bootstrap.find(".//" + xmlns_bootstrap + "bean") \
                .find(xmlns_bootstrap + "property[@name='models']").find(xmlns_bootstrap + "list") \
                .findall(xmlns_bootstrap + "value")

            self.MODELE.set_chemin_projet(chemin)
            self.VUE.succes()
            return resultat

        except Exception as e:
            self.VUE.erreur_exception(e, "Une erreur est survenue lors de la récupération du fichier 'bootstrap.xml'")
            exit()

    # Charge le type de contenu.
    # chemin_type_contenu Le chemin vers le type de contenu.
    def charger_type_contenu(self, chemin_type_contenu):
        self.VUE.chargement_type_contenu(chemin_type_contenu)

        racine = ElementTree.parse(chemin_type_contenu).getroot()
        xmlns = racine.tag[0:racine.tag.rindex("}") + 1]
        uri = racine.find(".//" + xmlns + "namespaces").find(xmlns + "namespace").attrib["uri"]

        self.charger_aspects(racine, uri, xmlns)
        self.charger_types(racine, uri, xmlns)

    # Charge les aspects d'un fichier de type de contenu.
    # racine La racine du fichier XML de type de contenu.
    def charger_aspects(self, racine, uri: str, xmlns):
        aspects = racine.find(".//" + xmlns + "aspects")

        if aspects is not None:
            for aspect in aspects.findall(xmlns + "aspect"):
                self.charge_aspect(xmlns, uri, aspects, aspect)

    def charger_types(self, racine, uri, xmlns):
        types = racine.find(".//" + xmlns + "types")

        if types is not None:
            for t in types.findall(xmlns + "type"):
                self.charge_type(xmlns, uri, types, t)

    # Charge un aspect dans le modèle.
    # xmlns Le xmlns du fichier XML.
    # aspects Le noeud XML contenant tous les aspects.
    # aspect Le noeud XML de l'aspect à ajouter.
    def charge_aspect(self, xmlns, uri: str, aspects, aspect: Element):
        asp = Aspect(uri, aspect.attrib["name"])

        self.VUE.chargement_aspect(asp.get_nom())

        self.charger_proprietes(xmlns, aspects, asp, aspect)
        asp.set_description(self.charge_description(aspect.find(xmlns + "description")))
        asp.set_titre(self.charger_titre(aspect.find(xmlns + "title")))

        self.MODELE.add_aspect(asp)

    @staticmethod
    def charge_description(noeud_description):
        if noeud_description is not None:
            return noeud_description.text
        else:
            return None

    # Charge dans le modèle aspect ses propriétés
    # xmlns Le xmlns du fichier XML.
    # aspects Le noeud XML contenant tous les aspects.
    # asp L'objet modele
    # aspect Le noeud XML de l'aspect contenant toutes les propriétés.
    def charger_proprietes(self, xmlns: str, aspects: Element, asp, aspect: Element):
        proprietes = aspect.find(xmlns + "properties")

        if proprietes is not None:
            for propriete in proprietes.findall(xmlns + "property"):
                prop = Propriete(propriete.attrib["name"])

                self.VUE.chargement_propriete(prop.get_nom_complet())

                prop.set_type(self.charger_type(propriete.find(xmlns + "type").text))
                prop.set_mandatory(self.charger_mandatory(propriete.find(xmlns + "mandatory")))
                prop.set_titre(self.charger_titre(propriete.find(xmlns + "title")) if propriete is not None else None)
                asp.add_propriete(prop)

                self.VUE.succes()

        mandatory_aspects = aspect.find(xmlns + "mandatory-aspects")
        if mandatory_aspects is not None and len(mandatory_aspects) > 0:

            for mandatory_aspect in mandatory_aspects.findall(xmlns + "aspect"):

                self.VUE.ajout_propriete_aspect(mandatory_aspect.text)

                for propriete in self.get_aspect_proprietes(xmlns, aspects, mandatory_aspect.text):

                    self.VUE.chargement_propriete(propriete.get_nom_complet())
                    asp.add_propriete(propriete)
                    self.VUE.succes()

        parent = aspect.find(xmlns + "parent")
        if parent is not None:
            nom_parent = parent.text
            if not nom_parent == "cm:folder" and not nom_parent == "cm:content":
                self.VUE.chargement_proprietes_parent(parent.text)
                for propriete in self.get_aspect_proprietes(xmlns, aspects, parent.text):
                    print("HERE")
                    self.VUE.chargement_propriete(propriete.get_nom_complet())
                    asp.add_propriete(propriete)
                    self.VUE.succes()

    @staticmethod
    def charger_type(valeur):
        if valeur == "d:text":
            return "String"

        elif valeur == "d:int":
            return "int"

        elif valeur == "d:float":
            return "float"

        elif valeur == "d:double":
            return "double"

        elif valeur == "d:date" or valeur == "d:datetime":
            return "Date"

        elif valeur == "d:boolean":
            return "boolean"

        return None

    @staticmethod
    def charger_mandatory(noeud_mandatory):
        if noeud_mandatory is None:
            return False

        if noeud_mandatory.text.lower() == "true":
            return True

        return False

    # Récupère les propriétés d'un aspect dont le nom (complet) est mi en paramètre.
    # xmlns Le xmlns du fichier XML.
    # aspects Le noeud contenant tous les aspects.
    # nom_aspect Le nom de l'aspect dont on souhaite récupérer le nom.
    def get_aspect_proprietes(self, xmlns, aspects, nom_aspect):
        if nom_aspect == "cm:folder" or nom_aspect == "cm:content":
            return []

        asps = self.MODELE.get_aspects()
        if nom_aspect in asps:
            return asps[nom_aspect].get_proprietes()

        self.charge_aspect(xmlns, aspects, aspects.find(xmlns + "aspect[@name='" + nom_aspect + "']"))

    # Méthode permettant de charger le titre d'un type ou d'un aspect.
    # noeud_titre Le noeud XML contenant la valeur du titre.
    @staticmethod
    def charger_titre(noeud_titre):
        if noeud_titre is None:
            return None
        return noeud_titre.text

    def charge_type(self, xmlns: str, uri: str, types: Element, t: Element):
        typ = Type(uri, t.attrib["name"])

        self.VUE.chargement_type(typ.get_nom_complet())

        self.charger_proprietes(xmlns, types, typ, t)
        typ.set_description(self.charge_description(t.find(xmlns + "description")))

        self.MODELE.add_type(typ)
