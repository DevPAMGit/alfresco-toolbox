# Modèle du script.
class Modele:
    # Initialize une nouvelle instance de la classe 'Modele'.
    # vue La vue du script.
    def __init__(self):
        self.TYPES = {}
        self.ASPECTS = {}
        self.CHEMIN = None
        self.GROUP_ID = None
        self.ARTIFACT_ID = None

    # Ajoute un aspect au modèle.
    # aspect L'aspect à ajouter.
    def add_aspect(self, aspect):
        self.ASPECTS[aspect.get_nom_complet()] = aspect

    # Modifie l'identifiant du groupe.
    # group_id La nouvelle valeur de l'identifiant du groupe.
    def set_group_id(self, group_id):
        self.GROUP_ID = group_id

    # Récupère l'identifiant du groupe.
    # Retourne l'identifiant du groupe.
    def get_group_id(self):
        return self.GROUP_ID

    # Récupère un map des aspects.
    # Retourne le map des aspects.
    def get_aspects(self):
        return self.ASPECTS

    # Modifie la valeur de l'artifact id du projet.
    # La nouvelle valeur de l'artifact id du projet.
    def set_artifact_id(self, artifact_id):
        self.ARTIFACT_ID = artifact_id

    # Récupère la valeur de l'artifact id.
    # return La valeur de l'artifact id.
    def get_artifact_id(self):
        return self.ARTIFACT_ID

    # Modifie le chemin vers le projet.
    # chemin Le chemin vers le projet.
    def set_chemin_projet(self, chemin):
        print("SET CHEMIN_PROJET " + chemin)
        self.CHEMIN = chemin

    # Récupère la valeur du chemin du projet.
    # Retourne la valeur du chemin du projet.
    def get_chemin_projet(self):
        return self.CHEMIN

    # Ajoute un type au modèle.
    # typ Le type à ajouter.
    def add_type(self, typ):
        self.TYPES[typ.get_nom_complet()] = typ

    # Récupère le chemin vers le dossier contenant les classes pour les types de contenu
    def get_chemin_contenu(self):
        return self.CHEMIN + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" \
               + self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/typescontenus"

    # Récupère le chemin vers le dossier contenant les classes pour les types de contenu
    def get_chemin_modele_sources(self):
        return self.CHEMIN + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" \
               + self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/modeles/sources"

    def get_chemin_modele_contenus(self):
        return self.CHEMIN + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" \
               + self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/modeles/typescontenus"

    def get_package_modele_sources(self):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.sources"

    def get_package_modele_contenus(self):
        return self.GROUP_ID + "." + self.ARTIFACT_ID.replace("-", "") + ".modeles.typescontenus"

    def get_types(self):
        return self.TYPES

    def get_chemin_config_custom_fichier(self) -> str:
        """
        Methode permettant de récupérer le chemin vers le fichier "share-config-custom.xml" du projet.;
        :return: Le chemin vers le fichier "share-config-custom.xml" du projet.
        """
        print(self.CHEMIN)
        return self.CHEMIN + "/" + \
               self.ARTIFACT_ID + \
               "-share/src/main/resources/META-INF/share-config-custom.xml"
