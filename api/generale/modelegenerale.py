class ModeleGenerale:
    """
    Classe modèle général pour tous les modèles de l'api.
    """

    def __init__(self):
        self.GROUP_ID = None
        self.GROUP_ID = None
        self.ARTIFACT_ID = None
        self.CHEMIN_PROJET = None
        self.CHEMIN_DOSSIER_RESOURCE = None

    def maj_chemin_projet(self, chemin_projet: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_ID__. ;
        :param chemin_projet : La nouvelle valeur du paramètre de classe __CHEMIN_ID__. ;
        """
        self.CHEMIN_PROJET = chemin_projet

    def maj_artifact_id(self, artifact_id: str):
        """
        Met à jour la valeur du paramètre de classe __ARTIFACT_ID__.;
        :param artifact_id : La nouvelle valeur du paramètre de classe __ARTIFACT_ID__. ;
        """
        self.ARTIFACT_ID = artifact_id

    def maj_group_id(self, group_id: str):
        """
        Met à jour la valeur du paramètre de classe __GROUP_ID__. ;
        :param group_id : La nouvelle valeur du paramètre de classe __GROUP_ID__. ;
        """
        self.GROUP_ID = group_id

    def maj_chemin_dossier_ressources(self, chemin_dossier_ressource: str):
        """
        Met à jour la valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        :param chemin_dossier_ressource : La nouvelle valeur du paramètre de classe __CHEMIN_DOSSIER_RESOURCE__. ;
        """
        self.CHEMIN_DOSSIER_RESOURCE = chemin_dossier_ressource

    def get_artifact_id(self) -> str:
        """
        Récupère l'artifact id du modèle de donnée.
        :return: La valeur de l'artifact id du modèle de donnée.
        """
        return self.ARTIFACT_ID