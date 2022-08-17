from api.action.modele.classeinfomodele import ClasseInfoModele


class ActionModele:
    """
    Classe définissant le modèle de données pour la gestion des actions d'un projet Alfresco.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'ActionModele'.
        """
        self.__GROUP_ID__ = None
        self.__ARTIFACT_ID__ = None
        self.__CHEMIN_PROJET__ = None
        self.__CHEMIN_DOSSIER_RESOURCE__ = None
        self.__ACTIONS__: list[ClasseInfoModele] = []

    def obt_actions(self):
        """
        Permet d'obtenir toutes les modèles de classes du projet. ;
        :return : La liste des modèles de classes du projet.
        """
        return self.__ACTIONS__

    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe __ARTIFACT_ID__. ;
        """
        self.__ARTIFACT_ID__ = artifact_id

    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe __CHEMIN_ID__. ;
        """
        self.__CHEMIN_PROJET__ = chemin_projet

    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe __GROUP_ID__. ;
        """
        self.__GROUP_ID__ = group_id

    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        self.__CHEMIN_DOSSIER_RESOURCE__ = chemin_dossier_ressource

    def obt_chemin_fichier_action_context(self) -> str:
        """
        Methode permettant de récupérer le chemin vers le fichier 'action-context.xml'.
        :return: Une chaîne de caractère représentant le chemin vers le fichier 'action-context.xml'.
        """
        return self.__CHEMIN_PROJET__ + "/" + self.__ARTIFACT_ID__ + "-platform/src/main/resources/alfresco/module/" + \
               self.__ARTIFACT_ID__ + "-platform/context/action-context.xml"

    def obt_chemin_dossier_classes_actions(self) -> str:
        """
        Méthode permettant de récupérer le chemin vers le dossier contenant les actions de classes. ;
        :return : Une chaîne de caractère représentant le chemin vers le dossier contenant les classes d'actions.
        """
        return self.__CHEMIN_PROJET__ + "/" + self.__ARTIFACT_ID__ + "-platform/src/main/java/" + \
               self.__GROUP_ID__.replace(".", "/") + "/" + self.__ARTIFACT_ID__.replace("-", "") + "/actions"

    def obt_chemin_fichier_modele(self):
        return self.__CHEMIN_DOSSIER_RESOURCE__ + "/alfrescoactions.xml.sauv"

    def ajt_classe_action(self, action: ClasseInfoModele):
        """
        Ajoute un modèle de classe dans le modèle de données. ;
        :param action : Le modèle de classe Action. ;
        """
        self.__ACTIONS__.append(action)

    def obt_chemin_fichier_module_context(self):
        return self.__CHEMIN_PROJET__ + "/" + self.__ARTIFACT_ID__ + "-platform/src/main/resources/alfresco/module/" + \
               self.__ARTIFACT_ID__ + "-platform/module-context.xml"
