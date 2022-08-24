EN_TETE_MODELE: str = "package {0} ;\n\n" \
               "import org.alfresco.service.namespace.QName;\n\n"

DEFINITION_CLASSE_MODELE: str = "/** Classe modèle personnalisée pour le type de contenu {{@link {0}}}. */\n" \
                    "public class {0} {{\n\n\t/** Le prefix du type de contenu. */" \
                    "\n\tpublic final static String PREFIX = \"{1}\";\n\n\t/** L'URI du type de contenu. */\n" \
                    "\tpublic final static String URI =  \"{2}\";\n\n\t/** Le nom du type de contenu. */\n" \
                    "\tpublic final static QName NOM = QName.createQName( URI , \"{3}\");\n\n"

PROPRIETE_MODELE: str = "\t/** Modèle pour la propriété '{0}'. */\n" \
                 "\tpublic final static QName {1} = QName.createQName( URI , \"{2}\");\n\n"

EN_TETE_HELPER: str = "package {0} ;\n\n" \
                      "import org.alfresco.service.cmr.repository.NodeService;\n" \
                      "import org.alfresco.service.cmr.repository.NodeRef;\n" \
                      "import org.alfresco.service.namespace.QName;\n\nimport {1};\n\n" \
                      "import java.io.Serializable;\nimport java.util.Date;\nimport java.util.Map;\n\n"

DEFINITION_CLASSE_HELPER_CONTENU: str = "/** Classe modèle d'aide personnalisée pour le type de contenu" \
                                        " {{@link {0}}}.*/\npublic class {0} extends AlfrescoModeleHelper {{\n\n" \
                                        "\t/** Initialise une nouvelle instance de la classe {{@link {0}}}. " \
                                        "\n\t * @param serviceNoeud Le service de gestion des nœuds d'Alfresco. \n" \
                                        "\t * @param noeud Le nœud de référence. */\n" \
                                        "\tpublic {0}(NodeService serviceNoeud, NodeRef noeud){{\n" \
                                        "\t\tsuper(serviceNoeud, noeud);\n\t}}\n\n" \
                                        "\t/** Permet de vérifier que le nœud du modèle possède le type de contenu" \
                                        " désigné en paramètre.\n\t * @return <c>true</c> si le type de contenu est " \
                                        "présent, sinon <c>false</c>. */\n\tpublic boolean hasAspect() {{ " \
                                        "\n\t\treturn this.hasAspect({1}.NOM);\n\t}}\n\n" \
                                        "\t/** Supprime un type de contenu du nœud. " \
                                        "*/\n\tpublic void supprimeAspect() {{ \n\t\tthis.supprimeAspect(this.noeud, " \
                                        "{1}.NOM); \n\t}}\n\n\t/** Ajoute un type de contenu à un nœud.\n" \
                                        "\t * @param valeurs Les valeurs du type de contenu à sa création. */\n" \
                                        "\tpublic void addAspect(Map<QName,Serializable> valeurs) {{\n" \
                                        "\t\tthis.addAspect(this.noeud, {1}.NOM, valeurs);\n" \
                                        "\t}}\n\n\t/**\n\t* Vérifie si le nœud du modèle est du type en en paramètre.*" \
                                        " \n\t@return <c>true</c> si le nœud est du type en paramètre sinon " \
                                        "<c>false</c>.\n\t*/\n\tpublic boolean hasType() {{\n\t\treturn " \
                                        "this.hasType({1}.NOM);\n\t}}\n\n\t/**\n\t* Ajoute le type au nœud.\n\t*/" \
                                        "\n\tpublic void addType(){{\n\t\tthis.addType({1}.NOM);\n\t}}\n\n"

METHODE_GETTER_HELPER: str = "\t/** Méthode permettant de récupérer la valeur de la propriété '{0}'. \n" \
                             "\t * @return {1} La valeur de la propriété '{0}'. */\n" \
                             "\tpublic {1} get{2}() {{ \n" \
                             "\t\treturn ({1}) this.getPropriete({3});\n" \
                             "\t}}\n\n"

METHODE_SETTER_HELPER: str = "\t/** Méthode permettant de récupérer la valeur de la propriété '{0}'. \n" \
                             "\t * @param valeur La nouvelle valeur de la propriété '{0}'. */ \n" \
                             "\tpublic void set{2}({1} valeur) {{ \n" \
                             "\t\tthis.majPropriete({3}, valeur);" \
                             "\n\t}}\n\n"

METHODE_VALIDITE: str = "\t/** Méthode permettant de vérifier si la valeur de la propriété '{0}' est valide. \n" \
                        "\t * @return <c>true</c> si la valeur est valide; sinon <c>false</c>'.  */\n" \
                        "\tpublic boolean est{1}Valide() {{ \n"

METHODE_MODELE_VALIDITE: str = "\t/** Méthode permettant de vérifier la validité de le type de contenu '{0}'. \n" \
                               "\t * @return <c>true</c> si le type de contenu à toutes ces propriétés valides sinon " \
                               "<c>false</c>. */ \n" \
                               "\tpublic boolean estAspectValide() {{ \n" \
                               "\t\treturn ( this.hasAspect()"

METHODE_MODELE_VALIDITE_2: str = "\n\t\t&& this.est{0}Valide()"