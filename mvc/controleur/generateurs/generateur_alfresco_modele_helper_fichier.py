import codecs


# Classe permettant de générer le fichier java AlfrescoModeleHelper.
class GenerateurAlfrescoModeleHelperFichier:

    # Initialise une nouvelle instance de la classe GenerateurAlfrescoModeleHelperFichier.
    # modele Le modele Le modèle du controleur
    # vue La vue du contrôleur.
    def __init__(self, modele, vue):
        self.vue = vue
        self.modele = modele
        self.fd = codecs.open(self.modele.get_chemin_helper() + "/AlfrescoModeleHelper.java", "w", "utf-8")

    def creer_fichier_aide_modele_source(self):
        self.vue.information("Génération du fichier java 'AlfrescoModeleHelper'.")
        succes = True

        try:
            # Ecriture du package de la classe.
            self.fd.write("package " + self.modele.get_aide_package() + ";\n\n")
            # Ecriture des imports.
            self.ecrire_imports()
            # Ecritures de l'ouverture de classe
            self.fd.write(
                "/** Classe permettant de simplifier la gestion des modèles liées à des nœuds Alfresco. */\n"
                "public class AlfrescoModeleHelper extends AlfrescoHelper {\n\n"
                "\t/** Le nœud modèle de référence. */\n"
                "\tprotected final NodeRef noeud;\n\n")
            # Ecritures des contructeurs
            self.ecrire_constructeurs()
            # Ecritures des méthodes permettant de manipuler les aspects du nœud.
            self.ecrire_methodes_aspects()
            # Ecritures des méthodes permettant de manipuler le type du nœud.
            self.ecrire_methodes_type()
            # Ecritures des méthodes permettant de manipuler les propriétés du nœud.
            self.ecrire_methodes_propriete()
            # Ecritures des méthodes permettant de manipuler les nœuds parents du nœud.
            self.ecrire_methodes_ancetre()
            # Ecritures des méthodes permettant de manipuler le contenu du nœud.
            self.ecrire_methodes_contenu()

            self.fd.write("}\n")
        except Exception as e:
            self.vue.print_erreur("")
            self.vue.print_erreur("Voici l'exception qui a été levée :")
            succes = False
            print(e)
        finally:
            self.fd.close()

        exit() if not succes else self.vue.succes()

    def ecrire_constructeurs(self):
        self.fd.write(
            "\t/** Initialise une nouvelle instance de la classe {@link AlfrescoModeleHelper}.\n"
            "\t* @param serviceNoeud Le service de gestion des noeuds d'Alfresco.\n"
            "\t* @param noeud Le noeud de référence. */\n"
            "\tpublic AlfrescoModeleHelper(NodeService serviceNoeud, NodeRef noeud) {\n"
            "\t\tsuper(serviceNoeud);\n"
            "\t\tthis.noeud = noeud;\n"
            "\t}\n\n"
        )

    def ecrire_imports(self):
        self.fd.write(
            "import org.alfresco.service.cmr.repository.NodeService;\n"
            "import org.alfresco.service.cmr.repository.NodeRef;\n"            
            "import org.alfresco.service.namespace.QName;\n\n"
            
            "import java.io.Serializable;\n"            
            "import java.util.List;\n"
            "import java.util.Map;\n\n"
        )

    def ecrire_methodes_aspects(self):
        self.fd.write(
            # Ecriture de la méthode vérifiant que l'aspect existe sue un nœud
            "\t/** Permet de vérifier que le nœud di modèle possède l'aspect désigné en paramètre. \n"            
            "\t* @param aspect L'aspect dont on souhaite vérifier la présence. \n"
            "\t* @return <c>true</c> si l'aspect est présent, sinon <c>false</c>. */\n"
            "\tpublic boolean hasAspect(QName aspect){ \n"
            "\t\treturn this.hasAspect(this.noeud, aspect);\n"
            "\t}\n\n"

            # Ecriture de la méthode permettant d'ajouter un aspect.
            "\t/** Ajoute un aspect à un nœud.\n"            
            "\t* @param aspect L'aspect à ajouter.\n"
            "\t* @param valeurs Les valeurs de l'aspect à sa création. */"
            "\tpublic void addAspect(QName aspect, Map<QName, Serializable> valeurs) { \n"            
            "\t\tthis.addAspect(this.noeud, aspect, valeurs); \n"
            "\t}\n\n"

            # Ecriture de la méthode permettant de supprimer un aspect.
            "\t/** Supprime un aspect d'un noeud.\n"            
            "\t* @param aspect L'aspect que l'on souhaite retirer du nœud. */\n"
            "\tpublic void supprimeAspect(QName aspect) { \n"            
            "\t\tthis.supprimeAspect(this.noeud, aspect);\n \n"
            "\t}\n\n"
        )

    # Méthode permettant d'écrire sur le descripteur de fichier les méthodes nécessaires à la manipulation du type d'un nœud.
    def ecrire_methodes_type(self):
        self.fd.write(
            # Méthode vérifiant le type d'un nœud.
            "\t/** Vérifie si le nœud du modèle est du type en en paramètre.\n"                
            "\t* @param type Le type de nœud attendu.\n"
            "\t* return <c>true</c> si le nœud est du type en paramètre sinon <c>false</c>.*/ \n"
            "\tpublic boolean hasType(QName type) { \n"
            "\t\treturn this.hasType(this.noeud, type);\n"
            "\t}\n\n"

            # Méthode modifiant le type d'un nœud.
            "\t/** Ajoute un type au nœud du modèle.\n"            
            "\t* @param type Le type à ajouter. */\n"
            "\tpublic void addType(QName type){\n"                
            "\t\tthis.addType(this.noeud, type);\n"
            "\t}\n\n"
        )

    def ecrire_methodes_propriete(self):
        self.fd.write(
            # Méthode permettant de récupérer la valeur d'une propriété d'un nœud.
            "\t/** Permet d'obtenir la valeur d'une propriété du nœud modèle. \n"            
            "\t* @param propriete La propriété dont on souhaite récupérer la valeur.\n"
            "\t* @return La valeur de la propriété. */\n"
            "\tpublic Serializable getPropriete(QName propriete){\n"
            "\t\treturn this.getPropriete(this.noeud, propriete);\n"
            "\t}\n\n"

            # Méthode permettant de modifier la propriété d'un nœud.
            "\t/** Modifie la valeur d'une propriété du nœud modèle nœud. \n"            
            "\t* @param propriete La propriété dont on souhaite modifier la valeur.*/\n"
            "\tpublic void majPropriete(QName propriete, Serializable valeur){\n"
            "\t\tthis.majPropriete(this.noeud, propriete, valeur);\n"
            "\t}\n\n"

            # Méthode permettant de modifier plusieurs propriétés d'un nœud.
            "\t/** Modifie la valeur d'une propriété du nœud modèle .\n"            
            "\t* @param valeurs La propriété dont on souhaite modifier la valeur. */\n"
            "\tpublic void majProprietes(Map<QName, Serializable> valeurs){ \n"
            "\t\tthis.majProprietes(this.noeud, valeurs);\n"
            "\t}\n\n"
        )

    def ecrire_methodes_ancetre(self):
        self.fd.write(
            "\t/** Permet de récupérer le nœud parent au noeud modèle. \n"            
            "\t* @return Une instance de type {@link NodeRef} représentant le parent du nœud parent. */ \n"
            "\tpublic NodeRef getNoeudParent(){ \n"
            "\t\treturn this.getNoeudParent(this.noeud); \n"
            "\t}\n\n"

            "\t/** Permet de récupérer un ancêtre du nœud du modèle.\n"            
            "\t* @param generation La génération antérieure à laquelle on souhaite accéder.\n"
            "\t* @return Une instance de type {@link NodeRef} représentant l'ancêtre nœud du modèle. */\n"
            "\tpublic NodeRef obtenirAncetre(int generation) {\n"            
            "\t\treturn  this.obtenirAncetre(this.noeud, generation);\n"
            "\t}\n\n"
        )

    def ecrire_methodes_contenu(self):
        self.fd.write(
            "\t/** Permet d'obtenir la liste des nœuds contenus dans le nœud du modèle.\n"
            "\t* @return La liste des nœuds contenue dans le nœud. */\n"
            "\tprotected List<NodeRef> obtenirContenu() {\n"            
            "\t\treturn this.obtenirContenu(this.noeud);\n"
            "\t}\n\n"
        )
