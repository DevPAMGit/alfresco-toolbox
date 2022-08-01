import codecs


# Classe permettant de générer le fichier java AlfrescoModeleHelper.
import os.path

from modules.modeles.modele import Modele
from modules.vue.vue import Vue


class GenerateurAlfrescoHelperFichier:

    # Intialise une nouvelle instance de la classe 'GenerateurFichierControleur'.
    # modele Le modele de controleur.
    # vue La vue du controleur
    def __init__(self, modele: Modele, vue: Vue):
        self.modele = modele
        self.vue = vue
        self.chemin_fichier = self.modele.get_chemin_modele_sources() + "/AlfrescoServiceNoeud.java"
        self.fd = codecs.open(self.chemin_fichier, "w", "utf-8")

    # Méthode permetant de créer la classe/fichier 'AlfrescoHelper'.
    def creer_fichier_aide_source(self):
        # self.vue.information("Génération du fichier java 'AlfrescoHelper.java'.")
        succes = True

        self.fd.write("package " + self.modele.get_package_modele_sources() + ";\n\n")

        # Ecriture des imports.
        self.ecrire_imports()

        # Ecritures de l'ouverture de classe
        self.fd.write(
            "/** Classe permettant de simplifier la gestion des nœuds  Alfresco. */\n"
            "public class AlfrescoHelper {\n\n")

        # Ecriture des paramètres de classe
        self.fd.write(
            "\t/** Le service de gestion des nœuds d'Alfresco. */\n"
            "\tprotected NodeService serviceNoeud;\n\n")

        self.ecrire_constructeurs()
        self.ecrire_methodes_aspects()
        self.ecrire_methodes_type()
        self.ecrire_methodes_propriete()
        self.ecrire_methodes_ancetre()
        self.ecrire_methodes_contenu()

        # Ecriture de la fin de fichier et fermeture
        self.fd.write("}")

        self.fd.close()
        exit() if not succes else self.vue.succes()

    # Méthode permettant d'écrire les imports nécessaire de la classe.
    def ecrire_imports(self):
        self.fd.write("import java.util.ArrayList;\n"
                      "import org.alfresco.model.ContentModel;\n"
                      "import org.alfresco.service.namespace.QName;\n"
                      "import org.alfresco.service.cmr.repository.NodeRef; \n"
                      "import org.alfresco.service.cmr.repository.NodeService; \n"
                      "import org.alfresco.service.cmr.repository.ChildAssociationRef; \n\n"

                      "import java.util.Map; \n"
                      "import java.util.List; \n"
                      "import java.io.Serializable; \n\n")

    # Méthode permettant d'ecrire sur un descripteur de fichier les constructeurs de la classe d'aide Alfresco.
    def ecrire_constructeurs(self):
        self.fd.write(
            "\t/** Initialise une nouvelle instance de la classe {@link AlfrescoHelper}.\n"
            "\t* @param serviceNoeud Le service de gestion des nœuds d'Alfresco. */\n"
            "\tpublic AlfrescoHelper(NodeService serviceNoeud) { \n"
            "\t\tthis.serviceNoeud = serviceNoeud;\n"
            "\t}\n\n")

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécéssaires à manipulation des aspects d'un nœud.
    def ecrire_methodes_aspects(self):
        self.fd.write(
            # Ecriture de la méthode vérifiant que l'aspect existe sue un nœud
            "\t/** Permet de vérifier qu'un nœud possède l'aspect désigné en paramètre. \n"
            "\t* @param noeud Le nœud dont on souhaite vérifier la présence de l'aspect. \n"
            "\t* @param aspect L'aspect dont on souhaite vérifier la présence. \n"
            "\t* @return <c>true</c> si l'aspect est présent, sinon <c>false</c>. */\n"
            "\tpublic boolean hasAspect(NodeRef noeud, QName aspect){ \n"
            "\t\treturn this.serviceNoeud.hasAspect(noeud, aspect);\n"
            "\t}\n\n"

            # Ecriture de la méthode permettant d'ajouter un aspect.
            "\t/** Ajoute un aspect à un nœud.\n"
            "\t* @param noeud Le nœud auquel on souhaite ajouter l'aspect.\n"
            "\t* @param aspect L'aspect à ajouter.\n"
            "\t* @param valeurs Les valeurs de l'aspect à sa création. */"
            "\tpublic void addAspect(NodeRef noeud, QName aspect, Map<QName, Serializable> valeurs) { \n"
            "\t\tif(this.hasAspect(noeud, aspect)) this.majProprietes(noeud, valeurs);\n"
            "\t\telse this.serviceNoeud.addAspect(noeud, aspect, valeurs); \n"
            "\t}\n\n"

            # Ecriture de la méthode permettant de supprimer un aspect.
            "\t/** Supprime un aspect d'un noeud.\n"
            "\t* @param noeud Le nœud auquel on souhaite retirer l'aspect.\n"
            "\t* @param aspect L'aspect que l'on souhaite retirer du nœud. */\n"
            "\tpublic void supprimeAspect(NodeRef noeud, QName aspect) { \n"
            "\t\tif(!this.hasAspect(noeud, aspect)) return;\n"
            "\t\tthis.serviceNoeud.removeAspect(noeud, aspect);\n \n"
            "\t}\n\n"
        )

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaires à la manipulation du type d'un nœud.
    def ecrire_methodes_type(self):
        self.fd.write(
            # Méthode vérifiant le type d'un nœud.
            "\t/** Vérifie si le nœud est du type en en paramètre.\n"
            "\t* @param noeud Le nœud dont on souhaite savoir s'il est du type en paramètre."
            "\t* @param type Le type de nœud attendu.\n"
            "\t* return <c>true</c> si le nœud est du type en paramètre sinon <c>false</c>.*/ \n"
            "\tpublic boolean hasType(NodeRef noeud, QName type) { \n"
            "\t\treturn this.serviceNoeud.getType(noeud).isMatch(type);\n"
            "\t}\n\n"

            # Méthode modifiant le type d'un nœud.
            "\t/** Ajoute un type au nœud.\n"
            "\t* @param noeud Le nœud auquel on ajoute un type.\n"
            "\t* @param type Le type à ajouter. */\n"
            "\tpublic void addType(NodeRef noeud, QName type){\n"
            "\t\tif(this.hasType(noeud, type)) \n"
            "\t\t\treturn;\n"
            "\t\tthis.serviceNoeud.setType(noeud, type);\n"
            "\t}\n\n")

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaires pour manipuler les propriétés d'un nœud.
    def ecrire_methodes_propriete(self):
        self.fd.write(
            # Méthode permettant de récupérer la valeur d'une propriété d'un nœud.
            "\t/** Permet d'obtenir la valeur d'une propriété d'un nœud. \n"
            "\t* @param noeud Le nœud dont on souhaite récupérer la valeur de la propriété. \n"
            "\t* @param propriete La propriété dont on souhaite récupérer la valeur.\n"
            "\t* @return La valeur de la propriété. */\n"
            "\tprotected Serializable getPropriete(NodeRef noeud, QName propriete){\n"
            "\t\treturn this.serviceNoeud.getProperty(noeud, propriete);\n"
            "\t}\n\n"

            # Méthode permettant de modifier la propriété d'un nœud.
            "\t/** Modifie la valeur d'une propriété d'un nœud en paramètre. \n"
            "\t* @param noeud Le nœud dont on souhaite modifier la propriété.\n"
            "\t* @param propriete La propriété dont on souhaite modifier la valeur.*/\n"
            "\tprotected void majPropriete(NodeRef noeud, QName propriete, Serializable valeur){\n"
            "\t\tthis.serviceNoeud.setProperty(noeud, propriete, valeur);\n"
            "\t}\n\n"

            # Méthode permettant de modifier plusieurs propriétés d'un nœud.
            "\t/** Modifie la valeur d'une propriété d'un nœud en paramètre.\n"
            "\t* @param noeud Le nœud dont on souhaite modifier la valeur des propriétés. \n"
            "\t* @param valeurs La propriété dont on souhaite modifier la valeur. */\n"
            "\tprotected void majProprietes(NodeRef noeud, Map<QName, Serializable> valeurs){ \n"
            "\t\tthis.serviceNoeud.setProperties(noeud, valeurs);\n"
            "\t}\n\n"
        )

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaires récupérer le contenu d'un nœud.
    def ecrire_methodes_contenu(self):
        self.fd.write(
            "\t/** Permet d'obtenir la liste des nœuds contenus dans le nœud en paramètre.\n"
            "\t* @param noeud Le nœud dont on veut récupérer le contenu.\n"
            "\t* @return La liste des nœuds contenue dans le nœud. */\n"
            "\tprotected List<NodeRef> obtenirContenu(NodeRef noeud) {\n"
            "\t\tArrayList<NodeRef> noeuds = new ArrayList<>();\n"
            "\t\tfor(ChildAssociationRef child : this.serviceNoeud.getChildAssocs(noeud))\n"
            "\t\t\tnoeuds.add(child.getChildRef());\n"
            "\t\treturn noeuds;\n"
            "\t}\n\n"
        )

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaire pour manipuler les ancêtres du nœud.
    def ecrire_methodes_ancetre(self):
        self.fd.write(
            "\t/** Permet de récupérer le nœud parent au noeud mis en paramètre. \n"
            "\t* @param noeud Le noeud dont on souhaite récupérer le parent. \n"
            "\t* @return Une instance de type {@link NodeRef} représentant le parent du nœud parent. */ \n"
            "\tprotected NodeRef getNoeudParent(NodeRef noeud){ \n"
            "\t\treturn this.serviceNoeud.getPrimaryParent(noeud).getParentRef(); \n"
            "\t}\n\n"

            "\t/** Permet de récupérer un ancêtre du nœud mis en paramètre.\n"
            "\t* @param noeud Le nœud dont on souhaite récupérer l'ancêtre'.\n"
            "\t* @param generation La génération antérieure à laquelle on souhaite accéder.\n"
            "\t* @return Une instance de type {@link NodeRef} représentant l'ancêtre nœud en paramètre. */\n"
            "\tprotected NodeRef obtenirAncetre(NodeRef noeud, int generation) {\n"
            "\t\tNodeRef ancetre = noeud;\n"
            "\t\tfor (int i=0; i<generation; i++) \n"
            "\t\t\tancetre = this.getNoeudParent(ancetre);\n"
            "\t\treturn ancetre;\n"
            "\t}\n\n"
        )