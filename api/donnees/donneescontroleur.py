from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from api.donnees.donneesmodele import DonneesModele
from api.generale.controleursecondaire import ControleurSecondaire
from api.modele.aspect import Aspect
from api.modele.modele import Modele
from api.modele.propriete import Propriete
from api.principal.principalbuffercontroleur import PrincipalBufferControleur
from libs.pythonconsolevue.consolevue import ConsoleVue


class DonneesControleur(ControleurSecondaire):
    """
    Contrôleur pour l'API de données.
    """

    def __init__(self, ctrl_principal: PrincipalBufferControleur, maximum: int):
        """
        Initialise une nouvelle instance de la classe 'ControleurDonnees' ;
        :param maximum: La largeur maximum (en caractère) de la vue.
        """
        super().__init__(ConsoleVue(maximum), DonneesModele())
        self.MODELE.__class__ = DonneesModele
        self.__CONTROLEUR_PRINCIPALE__ = ctrl_principal

    def controler(self, chemin_projet: str):
        self.VUE.titre("CHARGEMENT DES DONNEES DU PROJET")

        self.VUE.info("Chargement du fichier 'boostrap-context.xml' du sous-projet 'platform'.")
        self.__charger_donnees_pom__(chemin_projet)

        for modele in self.recuperer_liste_modeles():
            self.__charger_modele_contenu__(self.MODELE.obt_chemin_ressource() +
                                            modele.text.replace("${project.artifactId}",
                                                                self.MODELE.get_artifact_id() + "-platform"), modele)

    def __charger_modele_contenu__(self, chemin_fichier_modele, nom_fichier_modele):
        self.VUE.info("Chargement du fichier modèle '" + nom_fichier_modele + "'")

        racine: Element = ElementTree.parse(chemin_fichier_modele).getroot()
        xmlns: str = self.obt_xmlns(racine)
        uri: str = racine.find(".//" + xmlns + "namespaces").find(xmlns + "namespace").attrib["uri"]

        self.__charger_aspects__(racine, xmlns, uri)
        pass

    def __charger_aspects__(self, racine: Element, xmlns: str, uri: str):
        aspects = racine.find(".//" + xmlns + "aspects")

        if aspects is not None:
            for aspect in aspects.findall(xmlns + "aspect"):
                self.__charger_aspect__(xmlns, uri, aspects, aspect)

    def __charger_aspect__(self, xmlns: str, uri: str, parent: Element, noeud_aspect: Element):
        nom: str = noeud_aspect.attrib["name"]
        self.VUE.info("Chargement de l'aspect '" + nom + "'.")

        aspect: Modele = Modele()

        aspect.maj_nom(nom)
        aspect.ajt_proprietes(self.__charger_proprietes__(xmlns, noeud_aspect))
        aspect.ajt_proprietes(self.__charger_proprietes_mandatory__(xmlns, parent, noeud_aspect))

        # asp.set_description(self.charge_description(aspect.find(xmlns + "description")))
        # asp.set_titre(self.charger_titre(aspect.find(xmlns + "title")))

        # self.__CONTROLEUR_PRINCIPALE__.ajt_aspect(asp)

    def __charger_proprietes_mandatory__(self, xmlns: str, parent: Element, noeud: Element) -> list[Propriete]:
        """
        Charge les propriétés des d'un élément obligatoire.
        :param xmlns: L'"xmlns" du fichier xml du fichier XML.
        :param parent: Le noeud parent du noeud auquel on extrait les données.
        :param noeud: Le noeud auquel on extrait les données.
        :return: La liste des propriétés.
        """
        noeuds_mandatory: Element = noeud.find(xmlns, "mandatory-aspects")
        if noeuds_mandatory is None:
            return []

        proprietes: list[Propriete] = []
        for noeud_mandatory in noeuds_mandatory.findall(xmlns, "mandatory-aspects"):
            proprietes += self.obt_proprietes_aspect(xmlns, parent, noeud_mandatory.text)

        pass

    def obt_proprietes_aspect(self, xmlns: str, parent: Element, reference: str) -> list[Propriete]:
        if reference.__eq__("cm:folder") or reference.__eq__("cm:content"):
            return []

        modele: Modele = self.__CONTROLEUR_PRINCIPALE__.obt_aspect(reference)




    def __charger_proprietes__(self, xmlns: str, noeud: Element) -> list[Propriete]:
        """
        Méthode permettant de charger les propriétés d'un modèle.
        :param xmlns: L'"xmlns" du fichier xml du fichier XML.
        :param noeud: Le noeud contenant les propriétés.
        :return: Liste des propriétés.
        """
        noeuds_proprietes = noeud.find(xmlns + "properties")

        if noeuds_proprietes is not None:

            proprietes: list[Propriete] = []

            # Chargement des propriétés "sources" du projet.
            for noeud_propriete in noeuds_proprietes.findall(xmlns + "property"):
                proprietes.append(self.__charger_propriete__(xmlns, noeud_propriete))

            self.VUE.info(str(len(proprietes)) + " éléments trouvés")
            return proprietes

        else:
            self.VUE.info("Aucune propriété.")

        return []

    def __charger_propriete__(self, xmlns: str, noeud_propriete: Element) -> Propriete:
        """
        Charge la propriété d'un d'un aspect ou un type. ;
        :param xmlns : Le XMLNS du fichier XML. ;
        :param noeud_propriete : Le noeud contenant la propriété. ;
        :return : Une instance de type Propriete.
        """
        nom_complet: str = noeud_propriete.attrib["name"]

        self.VUE.action("Chargement de la propriété '" + nom_complet + "'.")

        propriete: Propriete = Propriete()
        propriete.maj_nom(nom_complet)
        propriete.set_titre(self.charger_titre(noeud_propriete.find(xmlns + "title")))
        propriete.maj_type(self.charger_type(noeud_propriete.find(xmlns + "type").text))
        propriete.set_mandatory(self.charger_mandatory(noeud_propriete.find(xmlns + "mandatory")))

        self.VUE.succes(None)
        return propriete

    def recuperer_liste_modeles(self) -> list[Element]:
        self.VUE.action("Récupération de la liste des modèles de contenus disponibles")
        racine_pom: Element = ElementTree.parse(self.obt_chemin_pom_platform()).getroot()
        self.MODELE.maj_platform_artifact_id(racine_pom.find(self.obt_xmlns(racine_pom) + "artifactId").text)

        racine_bootstrap: Element = ElementTree.parse(self.MODELE.CHEMIN_FICHIER_BOOTSTRAP).getroot()
        xmlns: str = self.obt_xmlns(racine_bootstrap)

        modeles: list[Element] = racine_bootstrap.find(".//" + xmlns + "bean").find(xmlns + "property[@name='models']")\
            .find(xmlns + "list").findall(xmlns + "value")

        self.VUE.succes(None)
        self.VUE.info("Nombre de modèles : " + str(len(modeles)))

        return modeles

    def __charger_donnees_pom__(self, chemin_projet: str):
        """
        Méthode permettant de charger les données nécessaire du fichier 'pom.xml' du projet. ;
        :param chemin_projet : Le chemin vers la racine du projet Alfresco.
        """
        self.VUE.info("Chargement des données du fichier 'pom.xml' du projet.")
        racine: Element = ElementTree.parse(chemin_projet + "/pom.xml").getroot()
        xmlns_projet = self.obt_xmlns(racine)

        self.VUE.action("Récupération du 'group id'")
        self.__CONTROLEUR_PRINCIPALE__.maj_artifact_id(racine.find(".//" + xmlns_projet + "groupId").text)
        self.VUE.succes(None)
        self.VUE.info("group id " + self.MODELE.GROUP_ID)

        self.VUE.action("Récupération de 'artifact id'")
        self.__CONTROLEUR_PRINCIPALE__.maj_artifact_id(racine.find(".//" + xmlns_projet + "artifactId").text)
        self.VUE.succes(None)
        self.VUE.info("Artifact id " + self.MODELE.ARTIFACT_ID)

        self.__CONTROLEUR_PRINCIPALE__.maj_chemin_projet(chemin_projet)

        self.VUE.succes(None)

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

    @staticmethod
    def charger_titre(noeud_titre) -> (str | None):
        """
        Méthode permettant de charger le titre d'un type ou d'un aspect. ;
        :param noeud_titre : Le noeud XML contenant la valeur du titre. ;
        :return : Le titre du noeud ou None.
        """
        resultat = None if noeud_titre is None else resultat = noeud_titre.text
        return resultat
