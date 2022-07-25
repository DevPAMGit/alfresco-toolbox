class GenerateurFichierControleur:

    # Intialise une nouvelle instance de la classe 'GenerateurFichierControleur'.
    # modele Le modele de controleur.
    # vue La vue du controleur
    def __init__(self, modele, vue):
        self.modele = modele
        self.vue = vue
        self.fd = open(self.modele.get_chemin_helper() + "/AlfrescoHelper.java", "w")

    # Méthode permetant de créer la classe/fichier 'AlfrescoHelper'.
    def creer_fichier_aide_source(self):
        self.vue.information("[ETAPE 3] Création de la classe d'aide Alfresco")
        self.fd.write(self.modele.get_aide_package())

        # Ecriture des imports.
        self.ecrire_imports()

        # Ecritures de l'ouverture de classe
        self.fd.write(
            "/** Classe permettant de simplifier la gestion des noeuds  Alfresco. */\n"
            "public class AlfrescoHelper {\n\n")

        # Ecriture des paramètres de classe
        self.fd.write(
            "\t/** Le service de gestion des nœuds d'Alfresco. */\n"
            "\tprotected NodeService serviceNoeud;\n\n")

        self.ecrire_constructeurs()
        self.ecrire_methodes_aspects()
        self.ecrire_methodes_type()
        self.ecrire_methodes_propriete()

        # Ecriture de la fin de fichier et fermeture
        self.fd.write("}")
        self.fd.close()

    # Méthode permettant d'écrire les imports nécessaire de la classe.
    def ecrire_imports(self):
        self.fd.write("import org.alfresco.model.ContentModel;\n"
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
            "\t/** Initialise une nouvelle instance de la classe {@link AideAlfresco}.\n"
            "\t* @param serviceNoeud Le service de gestion des noeuds d'Alfresco. */\n"
            "\tpublic AideAlfresco(NodeService serviceNoeud) { \n"
            "\t\this.serviceNoeud = serviceNoeud;\n"
            "\t}\n\n")

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécéssaires à manipulation des aspects d'un nœud.
    def ecrire_methodes_aspects(self):
        self.fd.write(
            # Ecriture de la méthode vérifiant que l'aspect existe sue un nœud
            "\t/** Permet de vérifier qu'un noeud possède l'aspect désigné en paramètre. \n"
            "\t* @param noeud Le noeud dont on souhaite vérifier la présence de l'aspect. \n"
            "\t* @param aspect L'aspect dont ont souhaite vérifier la présence. \n"
            "\t* @return <c>true</c> si l'aspect est présent; sinon <c>false</c>. */\n"
            "\tpublic boolean hasAspect(NodeRef noeud, QName aspect){ \n"
            "\t\tboolean resultat = this.serviceNoeud.hasAspect(noeud, aspect);\n"
            "\t\treturn resultat;\n"
            "\t}\n\n"

            # Ecriture de la méthode permettant de mettre à jour les propriétés d'un nœud.
            "\t/** Modifie la valeur d'une propriété d'un noeud en paramètre.\n"
            "\t* @param noeud Le noeud dont on souhaite modifier la valeur des propriété.\n"
            "\t* @param valeurs La propriété dont on souhaite modifier la valeur. */\n"
            "\tpublic void majProprietes(NodeRef noeud, Map<QName, Serializable> valeurs){\n"
            "\t\tthis.serviceNoeud.setProperties(noeud, valeurs); "
            "\t\tfor(QName propriete : valeurs.keySet())\n"
            "\t\t\tthis.modifiePropriete(noeud, propriete, valeurs.get(propriete));\n"
            "\t}\n\n"

            # Ecriture de la méthode permettant d'ajouter un aspect.
            "\t/** Ajoute un aspect à un noeud.\n"
            "\t* @param noeud Le noeud auquel on souhaite ajouter l'aspect.\n"
            "\t* @param aspect L'aspect à ajouter.\n"
            "\t* @param valeurs Les valeurs de l'aspect à sa création. */"
            "\tpublic void addAspect(NodeRef noeud, QName aspect, Map<QName, Serializable> valeurs) { \n"
            "\t\tif(this.hasAspect(noeud, aspect)) this.majProprietes(noeud, valeurs);\n"
            "\t\telse this.serviceNoeud.addAspect(noeud, aspect, valeurs); \n"
            "\t}\n\n"

            # Ecriture de la méthode permettant de supprimer un aspect.
            "\t/** Supprime un aspect d'un noeud.\n"
            "\t* @param noeud Le noeud auquel on souhaite retiré l'aspect.\n"
            "\t* @param aspect L'aspect que l'on souhaite retiré du noeud. */\n"
            "\tpublic void supprimeAspect(NodeRef noeud, QName aspect) { \n"
            "\t\tif(!this.hasAspect(noeud, aspect)) return;\n"
            "\t\tthis.serviceNoeud.removeAspect(noeud, aspect);\n \n"
            "\t}\n\n"
        )

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaires à la manipulation du type d'un nœud.
    def ecrire_methodes_type(self):
        self.fd.write("\t/** Vérifie si le nœud est du type en en paramètre.\n"
                      "\t* @param noeud Le nœud dont on souhaite savoir s'il est du type en paramètre."
                      "\t* @param type Le type de nœud attendu.\n"
                      "\t* return <c>true</c> si le nœud est du type en paramètre sinon <c>false</c>.*/ \n"
                      "\tpublic boolean hasType(NodeRef noeud, QName type) { \n"
                      "\t\treturn this.serviceNoeud.getType(noeud).isMatch(type);\n"
                      "\t}\n\n"
                      
                      "\t/** Ajoute un type au nœud."
                      "\t* @param noeud Le nœud auquel on ajoute un type."
                      "\t* @param type Le type à ajouter. */\n"
                      "\tpublic void addType(NodeRef noeud, QName type){"
                      "\t\tif(this.hasType(noeud, type)) \n"
                      "\t\t\treturn;\n"
                      "\t\tthis.serviceNoeud.setType(noeud, type); "
                      "\t}\n\n")

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaire pour manipuler les propriétés d'un nœud.
    def ecrire_methodes_propriete(self):
        self.fd.write(
            ""
        )
