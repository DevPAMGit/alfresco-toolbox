import codecs
import re
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from api.modele.aspect import Aspect
from modules.modeles.modele import Modele
from api.modele.propriete import Propriete
from modules.modeles.type import Type
from modules.vue.vue import Vue


class ControleurGenerateurShare:

    def __init__(self, modele: Modele, vue: Vue):
        """
        Initialise une nouvelle instance de la classe 'ControleurGenerateurShare'. ;
        :param modele : Le modèle du projet. ;
        : param vue : La vue du projet. ;
        """
        self.VUE = vue
        self.MODELE = modele
        # self.CONFIG_CUSTOM_SHARE_CHEMIN = self.MODELE.get_chemin_config_custom_fichier()
        self.RACINE = None  # ElementTree.parse(self.CONFIG_CUSTOM_SHARE_CHEMIN).getroot()

    def maj_share_config_custom(self, aspects: dict[str, Aspect], types: dict[str, Type]):
        """
        Met à jour le fichier 'config_custom_share.xml' du projet. ;
        :param types : La listes de types à ajouter à la configuration.;
        :param aspects : Les aspects à jouter au projet. ;
        """
        self.ajouter_configuration(aspects)
        self.ajouter_configuration(types)

    @staticmethod
    def maj_liste_aspects(racine: Element, nom_complet_aspect: str):
        """
        Met à jour la liste des aspects visibles.;
        :param racine : La racine du fichier xml à mettre à jour. ;
        :param nom_complet_aspect : Le nom complet de l'aspect. ;
        """

        visible: Element = racine.findall(".//config[@condition='DocumentLibrary']/aspects/visible")[0]
        aspect: Element = visible.find(".//aspect[@name='" + nom_complet_aspect + "']")

        if aspect is not None:
            visible.remove(aspect)

        aspect = Element("aspect")
        aspect.set("name", nom_complet_aspect)

        visible.append(aspect)

    def maj_formulaires(self, racine: Element, element: (Aspect | Type)):
        config: Element = racine.find(".//config[@condition='" + element.get_nom_complet() + "']")
        if config is not None:
            racine.remove(config)
        if isinstance(element, Aspect):
            racine.append(self.get_noeud(element, "aspect"))
        else:
            racine.append(self.get_noeud(element, "node-type"))

    @staticmethod
    def maj_liste_types(racine: Element, t: Type):
        """
        Met à jour la liste des types. ;
        :param racine: La racine du DOM. ;
        :param t : Le type à ajouter la mise à jour.
        """

        types: Element = racine.find(".//config[@condition='DocumentLibrary']/types")
        typ: Element = types.find(".//type[@name='" + t.PARENT + "']")
        subtype: (Element | None) = None

        if typ is None:
            typ = Element("type")
            typ.set("name", t.PARENT)
            types.append(typ)

        subtype: Element = typ.find(".//subtype[@name='" + t.NOM_COMPLET + "']")

        if subtype is not None:
            typ.remove(subtype)

        subtype = Element("subtype")
        subtype.set("name", t.NOM_COMPLET)

        typ.append(subtype)

    def ajouter_configuration(self, models: dict[str, (Aspect | Type)]):
        """
        Ajoute une liste d'aspects dans le fichier de configuration 'config_custom_share.xml' du projet.;
        :param models: Le dictionnaire d'aspect à ajouter.;
        """
        self.RACINE = ElementTree.parse(self.MODELE.get_chemin_config_custom_fichier())
        root = self.RACINE.getroot()

        for key in models.keys():
            if isinstance(models[key], Aspect):
                self.maj_liste_aspects(root, models[key].get_nom_complet())
            else:
                self.maj_liste_types(root, models[key])
            self.maj_formulaires(root, models[key])

        fd = codecs.open(self.MODELE.get_chemin_config_custom_fichier(), "w", "utf-8")
        fd.write(re.sub("\\n\\s*\\n", "\\n",
                        minidom.parseString(ElementTree.tostring(root, "utf-8")).toprettyxml(indent="\t")))
        fd.close()

    def get_noeud(self, element: (Aspect | Type), typ: str):
        """
        Ajoute un aspect dans le fichier de configuration 'config_custom_share.xml' du projet.
        :param typ: Le type du noeud.
        :param element: L'aspect à ajouter. ;
        """

        # Création du noeud XML.
        config_noeud = Element("config")
        config_noeud.set("evaluator", typ)
        config_noeud.set("condition", element.get_nom_complet())

        forms_noeud: Element = Element("forms")
        form_noeud: Element = Element("form")

        noeud_field_visibility = Element("field-visibility")
        for propriete in element.get_proprietes():
            noeud_field_visibility.append(self.get_noeud_consultation(propriete))

        noeud_field_visibility.append(self.get_noeud_simple("cm:name"))
        noeud_field_visibility.append(self.get_noeud_force("cm:title"))
        noeud_field_visibility.append(self.get_noeud_force("cm:description"))

        noeud_field_visibility.append(self.get_noeud_force("cm:created"))
        noeud_field_visibility.append(self.get_noeud_force("cm:modifier"))
        noeud_field_visibility.append(self.get_noeud_force("cm:modified"))
        noeud_field_visibility.append(self.get_noeud_avec_mode("cm:creator"))

        form_noeud.append(noeud_field_visibility)
        forms_noeud.append(form_noeud)
        config_noeud.append(forms_noeud)

        return config_noeud

    @staticmethod
    def get_noeud_consultation(propriete: Propriete) -> Element:
        """
        Permet de récupérer un noeud 'show' de la propriété.;
        :param propriete: La propriété.;
        :return: Une instance de la classe Element, représentant le noeud xml "show".
        """
        result = Element("show")
        result.set("id", propriete.get_nom_complet())
        return result

    @staticmethod
    def get_noeud_force(nom_complet: str) -> Element:
        result = Element("show")
        result.set("id", nom_complet)
        result.set("force", "true")

        return result

    @staticmethod
    def get_noeud_simple(nom_complet):
        result = Element("show")
        result.set("id", nom_complet)
        return result

    @staticmethod
    def get_noeud_avec_mode(nom_complet):
        result = Element("show")
        result.set("id", nom_complet)
        result.set("for-mode", "view")
        return result
