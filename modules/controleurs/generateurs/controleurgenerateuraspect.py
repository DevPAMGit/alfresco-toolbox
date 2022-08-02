import codecs
import os.path

from modules.modeles.aspect import Aspect
from modules.modeles.modele import Modele
from modules.modeles.propriete import Propriete
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

    # Crée un fichier modèle pour un aspect.
    # aspect L'aspect dont on va créer le fichier modèle.
    def creer_fichier_modele_aspect(self, aspect):
        nom_fichier = aspect.get_nom().capitalize() + "Modele.java"
        chemin = self.MODELE.get_chemin_modele_contenus() + "/" + aspect.get_prefix().lower() + "/aspects/" \
            + aspect.get_nom().lower() + "/" + nom_fichier

        self.VUE.creation_fichier(nom_fichier)
        self.creer_arborescence(aspect)

        fd = codecs.open(chemin, "w", "utf-8")

        fd.write("package " + self.MODELE.get_package_modele_contenus() + "." + aspect.get_prefix().lower() + ".aspects."
                 + aspect.get_nom().lower() + ";\n\n")

        fd.write("import org.alfresco.service.namespace.QName;\n\n")

        fd.write("/** Classe modèle personnalisée pour l'aspect '" + aspect.get_nom_complet() + "'. */\n " +
                 "public class " + aspect.get_nom().capitalize() + "Modele" + " {\n\n ")

        fd.write("\t/** Le prefix du type de contenu. */\n"
                 "\tpublic final static String PREFIX = \"" + aspect.get_prefix() + "\";\n\n")

        fd.write("\t/** Le prefix du type de contenu. */\n"
                 "\tpublic final static String URI =  \"" + aspect.get_uri() + "\";\n\n")

        for propriete in aspect.get_proprietes():
            fd.write(self.get_model_propriete(propriete))

        fd.write("}\n")
        fd.close()

        self.VUE.succes()

    # Crée l'arborescence de l'aspect.
    # aspect L'aspect dont il faut créer l'arborescence.
    def creer_arborescence(self, aspect: Aspect):
        chemin = self.MODELE.get_chemin_modele_contenus() + "/" + aspect.get_prefix().lower() + "/aspects/" \
                 + aspect.get_nom().lower()

        if not os.path.exists(chemin):
            os.makedirs(chemin)

    # Récupère le modèle de la propriété.
    # Retourne le modèle de la propriété.
    @staticmethod
    def get_model_propriete(propriete: Propriete):
        return "\t/** Modèle pour la propriété '" + propriete.get_nom_complet() + "'. */\n" \
               "\tpublic final static QName " + propriete.get_nom().upper() + " = QName.createQName( URI , \"" \
               + propriete.get_nom() + "\");\n\n"
