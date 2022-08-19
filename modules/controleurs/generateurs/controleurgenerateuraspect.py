import codecs
import os.path

from api.modele.aspect import Aspect
from modules.modeles.modele import Modele
from api.modele.propriete import Propriete
from modules.vue.vue import Vue


# Classe générant les fichiers modèle pour les aspects.
class ControleurGenerateurAspect:

    # Initialise une nouvelle instance de la classe 'ControleurGenerateurAspect'.
    # modele Le modele du controleur.
    # vue La vue du controleur.
    def __init__(self, modele: Modele, vue: Vue):
        self.VUE = vue
        self.MODELE = modele

    # Crée les fichiers nécessaires pour les aspects.
    def creer_fichiers_aspects(self):
        aspects = self.MODELE.get_aspects()
        for aspect_name in aspects.keys():
            self.creer_fichier_modele_aspect(aspects[aspect_name])
            self.creer_fichier_helper_aspect(aspects[aspect_name])

    # Crée un fichier modèle pour un typecontenu.
    # typecontenu L'typecontenu dont on va créer le fichier modèle.
    def creer_fichier_modele_aspect(self, aspect):
        nom_fichier = self.get_nom_class(aspect) + "AspectModele.java"
        chemin = self.get_chemin_dossier_aspect(aspect) + "/" + nom_fichier

        self.VUE.creation_fichier(nom_fichier)
        self.creer_arborescence(aspect)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write("package " + self.get_aspect_package(aspect) + ";\n\n")

        fd.write("import org.alfresco.service.namespace.QName;\n\n")

        fd.write("/** Classe modèle personnalisée pour l'typecontenu '" + aspect.get_nom_complet() + "'. */\n " +
                 "public class " + aspect.get_nom().capitalize() + "AspectModele" + " {\n\n ")

        fd.write("\t/** Le prefix du type de contenu. */\n"
                 "\tpublic final static String PREFIX = \"" + aspect.get_prefix() + "\";\n\n")

        fd.write("\t/** L'URI du type de contenu. */\n"
                 "\tpublic final static String URI =  \"" + aspect.get_uri() + "\";\n\n")

        fd.write("\t/** Le nom de l'typecontenu. */\n"
                 "\tpublic final static QName NOM = QName.createQName( URI , \"" + aspect.get_nom() + "\");\n\n")

        for propriete in aspect.get_proprietes():
            fd.write(self.get_model_propriete(propriete))

        fd.write("}\n")
        fd.close()

        self.VUE.succes()

    # Crée un fichier helper modèle pour un typecontenu.
    # typecontenu L'typecontenu dont on va créer le fichier helper modèle.
    def creer_fichier_helper_aspect(self, aspect):
        nom_fichier = self.get_nom_class(aspect) + "AspectHelperModele.java"
        chemin = self.get_chemin_dossier_aspect(aspect) + "/" + nom_fichier

        self.VUE.creation_fichier(nom_fichier)
        self.creer_arborescence(aspect)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write("package " + self.get_aspect_package(aspect) + ";\n\n")

        fd.write("import org.alfresco.service.cmr.repository.NodeService;\n"
                 "import org.alfresco.service.cmr.repository.NodeRef;\n"
                 "import org.alfresco.service.namespace.QName;\n\n"
                 "import " + self.MODELE.get_package_modele_sources() + ".AlfrescoModeleHelper;\n\n" +
                 "import java.io.Serializable;\n"
                 "import java.util.Date;\n"
                 "import java.util.Map;\n\n")

        fd.write("/** Classe modèle d'aide personnalisée pour l'typecontenu '" + aspect.get_nom_complet() + "'. */\n " +
                 "public class " + self.get_nom_class(aspect) + "AspectHelperModele extends AlfrescoModeleHelper {\n\n ")

        fd.write("\t/** Initialise une nouvelle instance de la classe {@link " + self.get_nom_class(aspect)
                 + "AspectHelperModele}. \n" +
                 "\t * @param serviceNoeud Le service de gestion des nœuds d'Alfresco. \n" +
                 "\t * @param noeud Le nœud de référence. */\n"
                 "\tpublic " + self.get_nom_class(aspect) +
                 "AspectHelperModele(NodeService serviceNoeud, NodeRef noeud){\n" +
                 "\t\tsuper(serviceNoeud, noeud);\n" +
                 "\t}\n\n" +
                 "\t/** Permet de vérifier que le nœud du modèle possède l'typecontenu désigné en paramètre.\n" +
                 "\t * @return <c>true</c> si l'typecontenu est présent, sinon <c>false</c>. */ \n" +
                 "\tpublic boolean hasAspect(){ \n" +
                 "\t\treturn this.hasAspect(" + self.get_nom_class(aspect) + "AspectModele.NOM);\n" +
                 "\t}\n\n"
                 "\t/** Supprime un typecontenu du nœud. */\n"                 
                 "\tpublic void supprimeAspect() { \n"
                 "\t\tthis.supprimeAspect(this.noeud, " + self.get_nom_class(aspect) + "AspectModele.NOM); \n"
                 "\t}\n\n"
                 "\t/** Ajoute un typecontenu à un nœud.\n"
                 "\t * @param valeurs Les valeurs de l'typecontenu à sa création. */\n" +
                 "\tpublic void addAspect(Map<QName,Serializable> valeurs) {\n"
                 "\t\tthis.addAspect(this.noeud, " + self.get_nom_class(aspect) + "AspectModele.NOM, valeurs);\n;"
                 "\t}\n\n")

        a_propriete_mandatory = False

        for propriete in aspect.get_proprietes():
            if propriete.get_mandatory():
                a_propriete_mandatory = True
            fd.write(self.get_model_helper_methodes(aspect, propriete))

        if a_propriete_mandatory:
            fd.write(self.get_aspect_methode_validite(aspect))

        fd.write("}\n")
        fd.close()

        self.VUE.succes()

    # Crée l'arborescence de l'typecontenu.
    # typecontenu L'typecontenu dont il faut créer l'arborescence.
    def creer_arborescence(self, aspect: Aspect):
        chemin = self.get_chemin_dossier_aspect(aspect)

        if not os.path.exists(chemin):
            os.makedirs(chemin)

    def get_chemin_dossier_aspect(self, aspect):
        return self.MODELE.get_chemin_modele_contenus() + "/" + aspect.get_prefix().lower() + "/aspects/" \
            + aspect.get_nom().lower()

    def get_aspect_package(self, aspect):
        return self.MODELE.get_package_modele_contenus() + "." + aspect.get_prefix().lower() + ".aspects." \
               + aspect.get_nom().lower()

    # Récupère le modèle de la propriété.
    # Retourne le modèle de la propriété.
    @staticmethod
    def get_model_propriete(propriete: Propriete):
        return "\t/** Modèle pour la propriété '" + propriete.get_nom_complet() + "'. */\n" \
               "\tpublic final static QName " + propriete.get_nom().upper() + " = QName.createQName( URI , \"" \
               + propriete.get_nom() + "\");\n\n"

    @staticmethod
    def get_nom_class(aspect: Aspect):
        return aspect.get_nom().capitalize()

    # Permet de récupérer les méthodes nécessaires pour un modèle.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer les méthodes.
    # Retourne une chaîne de caractères.
    def get_model_helper_methodes(self, aspect: Aspect, propriete: Propriete):
        resultat = self.get_methode_getter(aspect, propriete)
        resultat += self.get_methode_setter(aspect, propriete)
        if propriete.get_mandatory():
            resultat += self.get_methode_validite(aspect, propriete)
        return resultat

    # Permet de récupérer la méthode getter de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    def get_methode_getter(self, aspect: Aspect, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = aspect.get_nom_complet()
        prop_modele = self.get_nom_class(aspect) + "AspectModele." + propriete.get_nom().upper()

        return "\t/** Méthode permettant de récupérer la valeur de la propriété '" + prop_nom_entier + "'. \n" + \
               "\t * @return " + prop_type + " La valeur de la propriété '" + prop_nom_entier + "'.  */\n" + \
               "\tpublic " + prop_type + " get" + propriete.get_nom().capitalize() + "() { \n" + \
               "\t\treturn (" + prop_type + ") this.getPropriete(" + prop_modele + ");\n" + \
               "\t}\n\n"

    # Permet de récupérer la méthode setter de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    def get_methode_setter(self, aspect: Aspect, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = aspect.get_nom_complet()
        prop_modele = self.get_nom_class(aspect) + "AspectModele." + propriete.get_nom().upper()

        return "\t/** Méthode permettant de récupérer la valeur de la propriété '" + prop_nom_entier + "'. \n" + \
               "\t * @param valeur La nouvelle valeur de la propriété '" + prop_nom_entier + "'. */ \n" + \
               "\tpublic void set" + propriete.get_nom().capitalize() + "(" + prop_type + " valeur) { \n" + \
               "\t\tthis.majPropriete(" + prop_modele + ", valeur);\n" + \
               "\t}\n\n"

    # Permet de récupérer la méthode de validité de la propriété en paramètre.
    # typecontenu L'typecontenu de la propriété.
    # propriete La propriété dont on souhaite récupérer la méthode getter.
    # Retourne une chaîne de caractères.
    @staticmethod
    def get_methode_validite(aspect: Aspect, propriete: Propriete):
        prop_type = propriete.get_type()
        prop_nom_entier = aspect.get_nom_complet()

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

    @staticmethod
    def get_aspect_methode_validite(aspect: Aspect):
        re = "\t/** Méthode permettant de vérifier la validité de l'typecontenu '" + aspect.get_nom_complet() + "'. \n" + \
             "\t * @return <c>true</c> si l'typecontenu à toutes ces propriétés valides sinon <c>false</c>. */ \n" + \
             "\tpublic boolean estAspectValide() { \n" + \
             "\t\treturn ( this.hasAspect()"

        for propriete in aspect.get_proprietes():
            if propriete.get_mandatory():
                re += "\n\t\t         && this.est" + propriete.get_nom().capitalize() + "Valide()"

        re += "\n\t\t);\n\t}\n\n"
        return re
