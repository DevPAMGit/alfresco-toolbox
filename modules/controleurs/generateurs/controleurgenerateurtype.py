import codecs
import os.path

from modules.modeles.modele import Modele
from api.modele.propriete import Propriete
from modules.modeles.type import Type
from modules.vue.vue import Vue


# Classe générant les fichiers modèle pour les types.
class ControleurGenerateurType:

    # Initialise une nouvelle instance de la classe 'ControleurGenerateurType'.
    # modele Le modele du controleur.
    # vue La vue du controleur.
    def __init__(self, modele: Modele, vue: Vue):
        self.VUE = vue
        self.MODELE = modele

    # Crée les fichiers nécessaires pour les types.
    def creer_fichiers_types(self):
        types = self.MODELE.get_types()
        for type_name in types.keys():
            self.creer_fichier_modele_type(types[type_name])
            self.creer_fichier_helper_type(types[type_name])

    # Crée un fichier modèle pour un type.
    # typ Le type dont on va créer le fichier modèle.
    def creer_fichier_modele_type(self, typ: Type):
        nom_fichier = self.get_nom_class(typ) + "TypeModele.java"
        chemin = self.get_chemin_dossier_type(typ) + "/" + nom_fichier

        self.VUE.creation_fichier(nom_fichier)
        self.creer_arborescence(typ)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write("package " + self.get_type_package(typ) + ";\n\n")

        fd.write("import org.alfresco.service.namespace.QName;\n\n")

        fd.write("/** Classe modèle personnalisée pour le type '" + typ.get_nom_complet() + "'. */\n " +
                 "public class " + typ.get_nom().capitalize() + "TypeModele" + " {\n\n ")

        fd.write("\t/** Le prefix du type de contenu. */\n"
                 "\tpublic final static String PREFIX = \"" + typ.get_prefix() + "\";\n\n")

        fd.write("\t/** L'URI du type de contenu. */\n"
                 "\tpublic final static String URI =  \"" + typ.get_uri() + "\";\n\n")

        fd.write("\t/** Le nom du type. */\n"
                 "\tpublic final static QName NOM = QName.createQName( URI , \"" + typ.get_nom() + "\");\n\n")

        for propriete in typ.get_proprietes():
            fd.write(self.get_model_propriete(propriete))

        fd.write("}\n")
        fd.close()

        self.VUE.succes()

    # Crée un fichier helper modèle pour un type.
    # typ Le type dont on va créer le fichier helper modèle.
    def creer_fichier_helper_type(self, typ):
        nom_fichier = self.get_nom_class(typ) + "TypeHelperModele.java"
        chemin = self.get_chemin_dossier_type(typ) + "/" + nom_fichier

        self.VUE.creation_fichier(nom_fichier)
        self.creer_arborescence(typ)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write("package " + self.get_type_package(typ) + ";\n\n")

        fd.write("import org.alfresco.service.cmr.repository.NodeService;\n"
                 "import org.alfresco.service.cmr.repository.NodeRef;\n"
                 "import org.alfresco.service.namespace.QName;\n\n"
                 "import " + self.MODELE.get_package_modele_sources() + ".AlfrescoModeleHelper;\n\n" +
                 "import java.util.Date;\n\n")

        fd.write("/** Classe modèle d'aide personnalisée pour le type '" + typ.get_nom_complet() + "'. */\n " +
                 "public class " + self.get_nom_class(typ) + "TypeHelperModele extends AlfrescoModeleHelper {\n\n ")

        fd.write("\t/** Initialise une nouvelle instance de la classe {@link " + self.get_nom_class(typ)
                 + "TypeHelperModele}. \n" +
                 "\t * @param serviceNoeud Le service de gestion des nœuds d'Alfresco. \n" +
                 "\t * @param noeud Le nœud de référence. */\n"
                 "\tpublic " + self.get_nom_class(typ) + "TypeHelperModele(NodeService serviceNoeud, NodeRef noeud){"
                 "\n\t\tsuper(serviceNoeud, noeud);\n" +
                 "\t}\n\n" +
                 "\t/** Permet de vérifier que le nœud du modèle possède l'typecontenu désigné en paramètre.\n" +
                 "\t * @return <c>true</c> si l'typecontenu est présent, sinon <c>false</c>. */ \n" +
                 "\tpublic boolean hasType(){ \n" +
                 "\t\treturn this.hasType(" + self.get_nom_class(typ) + "TypeModele.NOM);\n" +
                 "\t}\n\n")

        a_propriete_mandatory = False

        for propriete in typ.get_proprietes():
            if propriete.get_mandatory():
                a_propriete_mandatory = True
            fd.write(self.get_model_helper_methodes(typ, propriete))

        if a_propriete_mandatory:
            fd.write(self.get_aspect_methode_validite(typ))

        fd.write("}\n")
        fd.close()

        self.VUE.succes()

    # Crée l'arborescence de l'typecontenu.
    # typecontenu L'typecontenu dont il faut créer l'arborescence.
    def creer_arborescence(self, typ: Type):
        chemin = self.get_chemin_dossier_type(typ)

        if not os.path.exists(chemin):
            os.makedirs(chemin)

    def get_chemin_dossier_type(self, typ: Type):
        return self.MODELE.get_chemin_modele_contenus() + "/" + typ.get_prefix().lower() + "/types/" \
            + typ.get_nom().lower()

    def get_type_package(self, typ):
        return self.MODELE.get_package_modele_contenus() + "." + typ.get_prefix().lower() + ".types." \
               + typ.get_nom().lower()

    # Récupère le modèle de la propriété.
    # Retourne le modèle de la propriété.
    @staticmethod
    def get_model_propriete(propriete: Propriete):
        return "\t/** Modèle pour la propriété '" + propriete.get_nom_complet() + "'. */\n" \
               "\tpublic final static QName " + propriete.get_nom().upper() + " = QName.createQName( URI , \"" \
               + propriete.get_nom() + "\");\n\n"

    @staticmethod
    def get_nom_class(typ: Type):
        return typ.get_nom().capitalize()

    # Permet de récupérer les méthodes nécessaires pour un modèle.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer les méthodes.
    # Retourne une chaîne de caractères.
    def get_model_helper_methodes(self, typ: Type, propriete: Propriete):
        resultat = self.get_methode_getter(typ, propriete)
        resultat += self.get_methode_setter(typ, propriete)
        if propriete.get_mandatory():
            resultat += self.get_methode_validite(typ, propriete)
        return resultat

    # Permet de récupérer la méthode getter de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    def get_methode_getter(self, typ: Type, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = typ.get_nom_complet()
        prop_modele = self.get_nom_class(typ) + "TypeModele." + propriete.get_nom().upper()

        return "\t/** Méthode permettant de récupérer la valeur de la propriété '" + prop_nom_entier + "'. \n" + \
               "\t * @return " + prop_type + " La valeur de la propriété '" + prop_nom_entier + "'.  */\n" + \
               "\tpublic " + prop_type + " get" + propriete.get_nom().capitalize() + "() { \n" + \
               "\t\treturn (" + prop_type + ") this.getPropriete(" + prop_modele + ");\n" + \
               "\t}\n\n"

    # Permet de récupérer la méthode setter de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    def get_methode_setter(self, typ: Type, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = typ.get_nom_complet()
        prop_modele = self.get_nom_class(typ) + "TypeModele." + propriete.get_nom().upper()

        return "\t/** Méthode permettant de récupérer la valeur de la propriété '" + prop_nom_entier + "'. \n" + \
               "\t * @param valeur La nouvelle valeur de la propriété '" + prop_nom_entier + "'." + \
               "\t * @return " + prop_type + " a valeur de la propriété '" + prop_nom_entier + "'.  */\n" + \
               "\tpublic void set" + propriete.get_nom().capitalize() + "(" + prop_type + " valeur) { \n" + \
               "\t\tthis.majPropriete(" + prop_modele + ", valeur);\n" + \
               "\t}\n\n"

    # Permet de récupérer la méthode de validité de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    @staticmethod
    def get_methode_validite(typ: Type, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = typ.get_nom_complet()

        resultat = "\t/** Méthode permettant de vérifier si la valeur de la propriété '" + \
                   prop_nom_entier + "' est valide. \n" + \
                   "\t * @return <c>true</c> si la valeur est valide; sinon <c>false</c>'.  */\n" + \
                   "\tpublic boolean est" + propriete.get_nom().capitalize() + "Valide() { \n"

        if prop_type == "int" or prop_type == "float" or prop_type == "double" or prop_type == "boolean":
            resultat += "\t\treturn true;\n"

        elif prop_type == "Date":
            resultat += "\t\treturn (this.get" + propriete.get_nom().capitalize() + "() != null);"

        else:
            resultat += "\t\treturn ( this.get" + propriete.get_nom().capitalize() + "() != null && " + \
                        "!this.get" + propriete.get_nom().capitalize() + "().isBlank());\n"

        resultat += "\t}\n\n"

        return resultat

    # Permet de récupérer la méthode permettant de vérifier la validité du type.
    # typ Le type dont on souhaite récupérer la méthode de validité.
    @staticmethod
    def get_aspect_methode_validite(typ: Type):
        re = "\t/** Méthode permettant de vérifier la validité de l'typecontenu '" + typ.get_nom_complet() + "'. \n" + \
             "\t * @return <c>true</c> si l'typecontenu à toutes ces propriétés valides sinon <c>false</c>. */\n" + \
             "\tpublic boolean estAspectValide() { \n" + \
             "\t\treturn ( "

        plus = False

        for propriete in typ.get_proprietes():
            if propriete.get_mandatory():

                if plus:
                    re += "\t\t         && "

                re += "this.est" + propriete.get_nom().capitalize() + "Valide()\n"
                plus = True

        re += "\t\t);\n\t}\n\n"
        return re
