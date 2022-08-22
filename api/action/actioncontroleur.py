import re
from xml.dom import minidom
from xml.etree import ElementTree
import codecs
import os
from xml.etree.ElementTree import Element

from api.action.actionmodele import ActionModele
from api.action.modele.champinfomodele import ChampInfoModele
from api.action.modele.classeinfomodele import ClasseInfoModele
from api.generale.controleursecondaire import ControleurSecondaire
from api.generale.exception.exceptionpersonnalisee import ExceptionPersonnalisee
from libs.pythonconsolevue.consolevue import ConsoleVue


class ActionControleur(ControleurSecondaire):
    """
    Classe permettant de gérer les actions d'un projet Alfresco.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe 'ActionControleur'.
        :param maximum: La largeur maximum (en caractère) de la vue.
        """
        super().__init__(ConsoleVue(maximum), ActionModele())
        self.MODELE.__class__ = ActionModele

    def __maj_fichier_context_action__(self):
        """
        Méthode permettant de mettre à jour le contenu du fichier 'action-context.xml'
        """
        self.VUE.action("Mise à jour du fichier 'action-context.xml'")
        racine: Element = ElementTree.parse(self.MODELE.obt_chemin_fichier_action_context()).getroot()

        for action in self.MODELE.obt_actions():
            racine.append(self.__obt_noeud_bean__(racine, action))

        fd = open(self.MODELE.obt_chemin_fichier_action_context(), "w")
        fd.write(
            "<?xml version='1.0' encoding='UTF-8'?>\n"
            "<!DOCTYPE beans PUBLIC '-//SPRING//DTD BEAN/EN' 'http://www.springframework.org/dtd/spring-beans.dtd'>\n"
        )
        fd.write(
            re.sub("\\n\\s*\\n", "\\n",
                        minidom.parseString(ElementTree.tostring(racine, "utf-8"))
                   .childNodes[0].toprettyxml(indent="\t"))
        )
        fd.close()

        self.VUE.succes(None)

    @staticmethod
    def __obt_noeud_bean__(racine: Element, action: ClasseInfoModele) -> Element:
        bean = racine.find(".//bean[@class='" + action.PACKAGE + "." + action.NOM_CLASSE + "']")
        if bean is not None:
            racine.remove(bean)

        # Création ou Recréation du noeud.
        bean = Element("bean")
        bean.set("id", action.NOM)
        bean.set("class", action.PACKAGE + "." + action.NOM_CLASSE)
        bean.set("parent", "action-executer")

        if action.UTILISE_SERVICE_REGISTRE:
            propriete: Element = Element("property")
            propriete.set("name", action.REGISTRE_SERVICE_NOM)

            ref: Element = Element("ref")
            ref.set("bean", "ServiceRegistry")

            propriete.append(ref)

            bean.append(propriete)

        return bean

    def controler(self):
        """
        Contrôle les actions nécessaires pour la gestion des actions d'un projet Alfresco.
        """
        self.VUE.titre("PRISE EN COMPTE DES ACTIONS")
        self.__initialiser__()
        self.__extraire_donnees__()
        self.__maj_module_context__()
        self.__maj_fichier_context_action__()

    def __extraire_donnees__(self):
        """
        Extrait les données des fichiers .java d'actions.
        """

        self.VUE.info("Extraction des données des classes d'actions.")

        for contenu in os.listdir(self.MODELE.obt_chemin_dossier_classes_actions()):
            self.MODELE.ajt_classe_action(
                self.__extraire_donnees_classe__(self.MODELE.obt_chemin_dossier_classes_actions() + "/" + contenu,
                                                 contenu)
            )

    def __extraire_donnees_classe__(self, chemin_fichier_classe_action, nom_fichier: str) -> ClasseInfoModele:
        """
        Extrait les données d'une seule classe. ;
        :param chemin_fichier_classe_action : Le chemin vers le fichier .java. ;
        :param nom_fichier : Le nom du fichier .java. ;
        :return: Un modèle de données réunissant toutes les informations nécessaire pour une classe action.
        """
        self.VUE.info("Extraction de données du fichier '" + nom_fichier + "'")

        self.VUE.action("Lecture du fichier")
        fd_l = codecs.open(chemin_fichier_classe_action, "r", "utf-8")
        contenu: str = ' '.join(fd_l.read().split())
        fd_l.close()
        self.VUE.succes(None)

        classe: ClasseInfoModele = ClasseInfoModele()
        classe.maj_nom(self.__extraire_nom_classe__(contenu))
        classe.maj_package(self.__extraire_package__(contenu))
        classe.maj_description(self.__extraire_description_classe__(contenu, classe.NOM_CLASSE))
        classe.maj_utilisation_registre_service(self.__extraire_utilisation_registre_service(contenu))
        classe.maj_champs(self.__extraire_champs__(contenu))

        return classe

    def __extraire_champs__(self, contenu_fichier: str) -> list[ChampInfoModele]:
        """
        Extrait la liste de champs disponible dans la classe action. ;
        :param contenu_fichier : Le contenu du fichier java action. ;
        :return : La liste des champs.
        """

        self.VUE.info("Extraction des paramètres de l'action.")

        regex_parametres: str = "(private|public)\\s+static\\s+final\\s+[^\\s]+\\s+[^\\s]+\\s+=\\s+\"([^\\s]+)\"\\s*;"
        match_parametres = re.findall(regex_parametres, contenu_fichier)

        resultat: list[ChampInfoModele] = []

        if match_parametres is not None:
            for t1, t2 in match_parametres:
                self.VUE.action("Gestion du champ '" + t2 + "'")
                champ: ChampInfoModele = ChampInfoModele()
                champ.NOM = t2

                match_param = re.search(
                    "// @label ([^;]+);\\s*(private|public)\\s+static\\s+final\\s+\\S+\\s+\\S+\\s+=\\s+\"" +
                    t2 + "\"\\s*;", contenu_fichier)

                if match_param is not None:
                    champ.LABEL = match_param.group(1)

                resultat.append(champ)
                self.VUE.succes(None)

        return resultat

    def __extraire_utilisation_registre_service(self, contenu_fichier: str) -> (bool, str):
        self.VUE.action("Extraction de l'utilisation du registre des services.")

        match_description_service = re.search("(private|public)\\s+ServiceRegistry\\s+(\\S+);", contenu_fichier)

        if match_description_service is None:
            resultat: bool = False
        else:
            resultat = True

        self.VUE.succes(None)
        self.VUE.info("Utilisation du registre des services : " + ("oui" if resultat else "non"))

        return resultat, match_description_service.group(2)

    def __extraire_description_classe__(self, contenu_fichier: str, nom_classe: str) -> (str | None):
        """
        Extrait le nom du package du contenu fichier de fichier java. ;
        :param contenu_fichier : Le contenu d'un fichier java. ;
        :return : Le nom du package du contenu fichier de fichier java. ;
        """
        self.VUE.action("Extraction de la description de la classe")

        match_description_classe = re.search(".*/\*\*(.*)\*/.*" + nom_classe +
                                             "\\s+extends\\s+ActionExecuterAbstractBase", contenu_fichier)

        if match_description_classe is None:
            self.VUE.erreur("Aucune description trouvée", None)
            return None

        self.VUE.succes(None)
        return match_description_classe.group(1).replace("*", "")

    def __extraire_nom_classe__(self, contenu_fichier: str) -> str:
        """
        Extrait le nom du package du contenu fichier de fichier java. ;
        :param contenu_fichier : Le contenu d'un fichier java. ;
        :return : Le nom du package du contenu fichier de fichier java. ;
        :raise CustomException : Si aucun package n'a été trouvé. ;
        """

        self.VUE.action("Extraction du nom de la classe")

        match_nom_classe = re.search(".* class\\s+(\\S+)\\s+extends\\s+ActionExecuterAbstractBase .*", contenu_fichier)

        if match_nom_classe is None:
            raise ExceptionPersonnalisee("Aucun nom de classe trouvé!")

        self.VUE.succes(None)
        self.VUE.info("classe '" + match_nom_classe.group(1) + "'")
        return match_nom_classe.group(1)

    def __extraire_package__(self, contenu_fichier: str) -> str:
        """
        Extrait le nom du package du contenu fichier de fichier java. ;
        :param contenu_fichier : Le contenu d'un fichier java. ;
        :return : Le nom du package du contenu fichier de fichier java. ;
        :raise CustomException : Si aucun package n'a été trouvé. ;
        """
        self.VUE.action("Extraction du nom de package de la classe")

        match_package = re.search(".*package\\s+([^;]+)\\s*;", contenu_fichier)
        if match_package is None:
            raise ExceptionPersonnalisee("Aucun package trouvé!")

        self.VUE.succes(None)
        self.VUE.info("package '" + match_package.group(1) + "'")
        return match_package.group(1)

    def __maj_module_context__(self):
        """
        Met à jour le fichier 'module_context.xml'
        """

        self.VUE.action("Mise à jour du fichier 'module_context.xml'")

        ElementTree.register_namespace('', "http://www.springframework.org/schema/beans")
        racine = ElementTree.parse(self.MODELE.obt_chemin_fichier_module_context()).getroot()
        xmlns = self.obt_xmlns(racine)

        importation: Element = racine.find(".//" + xmlns + "import[@resource='classpath:alfresco/module/"
                                                           "${project.artifactId}/context/action-context.xml']")

        if importation is not None:
            self.VUE.succes(None)
            return

        importation = Element("import")
        importation.set("resource", "classpath:alfresco/module/${project.artifactId}/context/action-context.xml")

        racine.append(importation)

        self.ecrire_xml(self.MODELE.obt_chemin_fichier_module_context(), racine)
        self.VUE.succes(None)

    def __initialiser__(self):
        """
        Génère les dossiers nécessaires à la création d'actions, modifie les fichiers nécessaires à la prise en compte
         des actions. ;
        """

        self.VUE.info("Gestion des actions du projet")

        chemin_fichier_action_context: str = self.MODELE.obt_chemin_fichier_action_context()
        chemin_dossiers_classes_actions: str = self.MODELE.obt_chemin_dossier_classes_actions()

        # Création du dossier d'action s'il n'existe pas.
        if not os.path.exists(chemin_dossiers_classes_actions):
            self.VUE.action("Créations du dossier contenant les actions")
            os.makedirs(chemin_dossiers_classes_actions)
            self.VUE.succes(None)

        # Création du fichier 'action_context' s'il n'existe pas.
        if os.path.exists(chemin_fichier_action_context):
            os.remove(chemin_fichier_action_context)
        self.__init_action_context__()

    def __init_action_context__(self):
        """
        Méthode permettant d'initier le fichier 'action-context'. ;
        """
        self.VUE.action("Création du fichier 'action-context.xml'.")

        fd_e = codecs.open(self.MODELE.obt_chemin_fichier_action_context(), "w", "utf-8")
        fd_l = codecs.open(self.MODELE.obt_chemin_fichier_modele(), "r", "utf-8")

        fd_e.write(fd_l.read())

        fd_e.close()
        fd_l.close()

        self.VUE.succes(None)
