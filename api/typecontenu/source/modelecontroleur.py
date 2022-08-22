import codecs
import os
import re
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from api.modele.propriete import Propriete
from api.typecontenu.source.modelemodele import ModeleModele
from api.generale.controleursecondaire import ControleurSecondaire
from api.modele.modele import Modele
from api.typecontenu.variable.modeleconstante import EN_TETE_MODELE, DEFINITION_CLASSE_MODELE, PROPRIETE_MODELE, \
    EN_TETE_HELPER, DEFINITION_CLASSE_HELPER_CONTENU, METHODE_GETTER_HELPER, METHODE_SETTER_HELPER, METHODE_VALIDITE, \
    METHODE_MODELE_VALIDITE, METHODE_MODELE_VALIDITE_2
from libs.pythonconsolevue.consolevue import ConsoleVue


class ModeleControleur(ControleurSecondaire):
    """
    Controleur pour gérer les aspects.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe
        :param maximum: La largeur maximum de la vue en caractères.
        """
        super().__init__(ConsoleVue(maximum), ModeleModele())
        self.MODELE.__class__ = ModeleModele

    def ajt_modele(self, modele: Modele):
        """
        Ajoute un type de contenu dans le modèle de données.
        :param modele: Le type de contenu à ajouter.
        """
        self.MODELE.ajt_modele(modele)

    def obt_modele(self, reference: str) -> (Modele | None):
        """
        Permet d'obtenir un type de contenu.
        :param reference: La référence au type de contenu (son nom).
        :return: Le type de contenu trouvé sinon None.
        """
        return self.MODELE.obt_modele(reference)

    def obt_modeles(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects de l'api.
        :return: Un dictionnaire des aspects de l'api.
        """
        return self.MODELE.obt_modeles()

    def creer_fichiers_java(self, genre: str):
        """
        Méthode permettant de créer les fichiers de developments.
        """

        self.VUE.sous_titre_1("Création des fichiers java modèles et helper")

        modeles: dict[str, Modele] = self.obt_modeles()
        for nom_modele in modeles:
            self.creer_fichier_modele(modeles[nom_modele], genre)
            self.creer_fichier_helper(modeles[nom_modele], genre)

    def creer_fichiers_sources(self):
        """
        Méthode permettant de créer les fichiers sources java pour les modèles.
        """
        chemin: str = self.MODELE.obt_chemin_alfresco_sources_classes()

        if not os.path.exists(chemin):
            os.makedirs(chemin)

        self.VUE.action("Création de la classe 'AlfrescoHelper.java'")
        self.__copier_fichier__(self.MODELE.CHEMIN_DOSSIER_RESOURCE + "/alfrescoservicenoeud.java.sauv",
                                chemin + "/AlfrescoHelper.java")
        self.VUE.succes(None)

        self.VUE.action("Création de la classe 'AlfrescoModeleHelper.java'")
        self.__copier_fichier__(self.MODELE.CHEMIN_DOSSIER_RESOURCE + "/alfrescomodelenoeud.java.sauv",
                                chemin + "/AlfrescoModeleHelper.java")
        self.VUE.succes(None)

    def __copier_fichier__(self, source: str, destination: str):
        """
        Copie un fichier.
        :param source: Le chemin du fichier source.
        :param destination: Le chemin du fichier de destination.
        """
        fd2 = codecs.open(destination, "w", "utf-8")
        fd1 = codecs.open(source, "r", "utf-8")

        fd2.write("package {0};\n\n".format(self.MODELE.obt_alfresco_sources_classes_package()))
        fd2.write(fd1.read())

        fd1.close()
        fd2.close()

    def creer_fichier_helper(self, modele: Modele, genre: str):
        """
        Méthode permettant de créer un fichier helper pour un type de contenu.
        :param modele: Le modèle de type de contenu.
        :param genre: Le type du modèle de type de contenu.
        """
        nom_classe_modele: str = modele.NOM[0].upper() + modele.NOM[1:] + genre.capitalize() + "Modele"
        nom_classe: str = modele.NOM[0].upper() + modele.NOM[1:] + genre.capitalize() + "HelperModele"
        nom_fichier: str = nom_classe + ".java"
        chemin = self.MODELE.obt_chemin_modele(genre, modele) + "/" + nom_fichier

        self.VUE.info("Création du fichier helper " + nom_fichier)

        if not os.path.exists(self.MODELE.obt_chemin_modele(genre, modele)):
            self.VUE.action("Création du dossier")
            os.makedirs(self.MODELE.obt_chemin_modele(genre, modele))
            self.VUE.succes(None)

        self.VUE.action("Écriture du fichier '" + nom_fichier + "'")

        if os.path.exists(chemin):
            os.remove(chemin)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write(EN_TETE_HELPER.format(self.MODELE.obt_java_modele_package(modele, genre),
                 self.MODELE.obt_alfresco_sources_classes_package() + ".AlfrescoModeleHelper"))
        fd.write(DEFINITION_CLASSE_HELPER_CONTENU.format(nom_classe, nom_classe_modele))

        a_methode_mandatory: bool = False

        for propriete in modele.obt_proprietes():
            fd.write(METHODE_GETTER_HELPER.format(propriete.NOM_COMPLET, propriete.TYPE, propriete.NOM[0].upper() +
                                                  propriete.NOM[1:], modele.NOM[0].upper() + modele.NOM[1:] +
                                                  genre.capitalize() + "Modele." + re.sub("(\w)([A-Z])", r"\1_\2",
                                                                                          propriete.get_nom()).upper()))

            fd.write(METHODE_SETTER_HELPER.format(propriete.NOM_COMPLET, propriete.TYPE, propriete.NOM[0].upper() +
                                                  propriete.NOM[1:], modele.NOM[0].upper() + modele.NOM[1:] +
                                                  genre.capitalize() + "Modele." + re.sub("(\w)([A-Z])", r"\1_\2",
                                                                                          propriete.get_nom()).upper()))

            if propriete.MANDATORY:
                fd.write(METHODE_VALIDITE.format(propriete.NOM_COMPLET, propriete.NOM[0].upper() + propriete.NOM[1:]))
                fd.write(self.__obt_methode_propriete_validite(propriete))
                a_methode_mandatory = True

        if a_methode_mandatory:
            fd.write(METHODE_MODELE_VALIDITE.format(modele.NOM_COMPLET))
            for propriete in modele.obt_proprietes():
                if propriete.MANDATORY:
                    fd.write(METHODE_MODELE_VALIDITE_2.format(propriete.NOM[0].upper() + propriete.NOM[1:]))

            fd.write(");\n\t}\n\n")

        fd.write("}\n")
        fd.close()

        self.VUE.succes(None)

    @staticmethod
    def __obt_methode_propriete_validite(propriete: Propriete) -> str:
        resultat: str = ""
        nom_methode: str = propriete.NOM[0].upper() + propriete.NOM[1:]

        if propriete.TYPE.__eq__("int") or propriete.TYPE.__eq__("float") or propriete.TYPE.__eq__(
                "double") or propriete.TYPE.__eq__("boolean"):
            resultat += "\t\treturn true;\n"

        elif propriete.TYPE.__eq__("Date"):
            resultat += "\t\treturn (this.get" + nom_methode + "() != null);"

        else:
            resultat += "\t\treturn ( this.get" + nom_methode + "() != null && !this.get" + nom_methode + \
                        "().isBlank());\n"

        resultat += "\t}\n\n"
        return resultat

    def creer_fichier_modele(self, modele: Modele, genre: str):
        """
        Création du fichier modèle.
        :param modele: Le modèle dont on souhaite tirer un fichier.
        :param genre: Le genre du modèle.
        """
        nom_classe: str = modele.NOM[0].capitalize() + modele.NOM[1:] + genre.capitalize() + "Modele"
        nom_fichier: str = nom_classe + ".java"
        chemin = self.MODELE.obt_chemin_modele(genre, modele) + "/" + nom_fichier

        self.VUE.sous_titre_1("Création du fichier modèle " + nom_fichier)

        if not os.path.exists(self.MODELE.obt_chemin_modele(genre, modele)):
            self.VUE.action("Création du dossier")
            os.makedirs(self.MODELE.obt_chemin_modele(genre, modele))
            self.VUE.succes(None)

        self.VUE.action("Écriture du fichier '" + nom_fichier + "'")

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write(EN_TETE_MODELE.format(self.MODELE.obt_java_modele_package(modele, genre)))
        fd.write(DEFINITION_CLASSE_MODELE.format(nom_classe, modele.PREFIX, modele.URI, modele.NOM))

        for propriete in modele.obt_proprietes():
            fd.write(PROPRIETE_MODELE.format(propriete.get_nom_complet(),
                                             re.sub("(\w)([A-Z])", r"\1_\2", propriete.get_nom()).upper(),
                                             propriete.get_nom()))

        fd.write("}")
        fd.close()

        self.VUE.succes(None)

    def maj_fichier_share_config_custom(self, genre: str):
        """
        Méthode permettant de mettre à jour le fichier 'share_config_custom.xml' avec les aspects du modèle.
        """
        self.VUE.sous_titre_1("Ajout des " + genre + "s dans 'share-config-custom.xml'")
        racine = ElementTree.parse(self.MODELE.get_chemin_config_custom_fichier()).getroot()

        modeles: dict[str, Modele] = self.obt_modeles()
        for nom_modele in modeles:
            if genre.__eq__("aspect"):
                self.maj_liste_aspects(racine, modeles[nom_modele].NOM_COMPLET)
            else:
                self.maj_liste_types(racine, modeles[nom_modele])
            self.maj_formulaires(racine, modeles[nom_modele], genre)

        fd = codecs.open(self.MODELE.get_chemin_config_custom_fichier(), "w", "utf-8")
        fd.write(re.sub("\\n\\s*\\n", "\\n",
                        minidom.parseString(ElementTree.tostring(racine, "utf-8")).toprettyxml(indent="\t")))
        fd.close()

    @staticmethod
    def maj_liste_aspects(racine: Element, nom_complet_aspect: str):
        """
        Met à jour la liste des aspects visibles.;
        :param racine : La racine du fichier xml à mettre à jour. ;
        :param nom_complet_aspect : Le nom complet de . ;
        """

        visible: Element = racine.findall(".//config[@condition='DocumentLibrary']/aspects/visible")[0]
        aspect: Element = visible.find(".//aspect[@name='" + nom_complet_aspect + "']")

        if aspect is not None:
            visible.remove(aspect)

        aspect = Element("aspect")
        aspect.set("name", nom_complet_aspect)

        visible.append(aspect)

    @staticmethod
    def maj_liste_types(racine: Element, modele: Modele):
        """
        Met à jour la liste des types. ;
        :param racine: La racine du DOM. ;
        :param modele : Le type à ajouter la mise à jour.
        """

        types: Element = racine.find(".//config[@condition='DocumentLibrary']/types")
        typ: Element = types.find(".//type[@name='" + modele.PARENT + "']")
        subtype: (Element | None) = None

        if typ is None:
            typ = Element("type")
            typ.set("name", modele.PARENT)
            types.append(typ)

        subtype: Element = typ.find(".//subtype[@name='" + modele.NOM_COMPLET + "']")

        if subtype is not None:
            typ.remove(subtype)

        subtype = Element("subtype")
        subtype.set("name", modele.NOM_COMPLET)

        typ.append(subtype)

    def maj_formulaires(self, racine: Element, modele: Modele, genre: str):
        config: Element = racine.find(".//config[@condition='" + modele.NOM_COMPLET + "']")
        if config is not None:
            racine.remove(config)
        if genre.__eq__("aspect"):
            racine.append(self.get_noeud(modele, "aspect"))
        else:
            racine.append(self.get_noeud(modele, "node-type"))

    def get_noeud(self, modele: Modele, genre: str):
        """
        Ajoute un type de contenu dans le fichier de configuration 'config_custom_share.xml' du projet.
        :param genre: Le type du noeud.
        :param modele: Le type de contenu à ajouter. ;
        """

        # Création du noeud XML.
        config_noeud = Element("config")
        config_noeud.set("evaluator", genre)
        config_noeud.set("condition", modele.NOM_COMPLET)

        forms_noeud: Element = Element("forms")
        form_noeud: Element = Element("form")

        noeud_field_visibility = Element("field-visibility")
        for propriete in modele.PROPRIETES:
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
    def get_noeud_simple(nom_complet):
        result = Element("show")
        result.set("id", nom_complet)
        return result

    @staticmethod
    def get_noeud_force(nom_complet: str) -> Element:
        result = Element("show")
        result.set("id", nom_complet)
        result.set("force", "true")

        return result

    @staticmethod
    def get_noeud_avec_mode(nom_complet):
        result = Element("show")
        result.set("id", nom_complet)
        result.set("for-mode", "view")
        return result
