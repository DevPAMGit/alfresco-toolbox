from api.action.modele.classeinfomodele import ClasseInfoModele
from api.generale.modelegenerale import ModeleGenerale


class ActionModele(ModeleGenerale):
    """
    Classe définissant le modèle de données pour la gestion des actions d'un projet Alfresco.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'ActionModele'.
        """
        super().__init__()
        self.__ACTIONS__: list[ClasseInfoModele] = []

    def obt_actions(self):
        """
        Permet d'obtenir toutes les modèles de classes du projet. ;
        :return : La liste des modèles de classes du projet.
        """
        return self.__ACTIONS__

    def obt_chemin_fichier_action_context(self) -> str:
        """
        Methode permettant de récupérer le chemin vers le fichier 'action-context.xml'.
        :return: Une chaîne de caractère représentant le chemin vers le fichier 'action-context.xml'.
        """
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/src/main/resources/alfresco/module/" + \
               self.ARTIFACT_ID + "-platform/context/action-context.xml"

    def obt_chemin_dossier_classes_actions(self) -> str:
        """
        Méthode permettant de récupérer le chemin vers le dossier contenant les actions de classes. ;
        :return : Une chaîne de caractère représentant le chemin vers le dossier contenant les classes d'actions.
        """
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/src/main/java/" + \
               self.GROUP_ID.replace(".", "/") + "/" + self.ARTIFACT_ID.replace("-", "") + "/actions"

    def obt_chemin_fichier_modele(self):
        return self.CHEMIN_DOSSIER_RESOURCE + "/alfrescoactions.xml.sauv"

    def ajt_classe_action(self, action: ClasseInfoModele):
        """
        Ajoute un modèle de classe dans le modèle de données. ;
        :param action : Le modèle de classe Action. ;
        """
        self.__ACTIONS__.append(action)

    def obt_chemin_fichier_module_context(self):
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/src/main/resources/alfresco/module/" + \
               self.ARTIFACT_ID + "-platform/module-context.xml"
