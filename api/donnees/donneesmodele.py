from api.generale.modelegenerale import ModeleGenerale


class DonneesModele(ModeleGenerale):
    """
    Classe modèle pour le gestionnaire de données.
    """

    def __init__(self):
        super().__init__()
        self.PLATFORM_ARTIFACT_ID = None
        self.CHEMIN_FICHIER_BOOTSTRAP = None

    def obt_chemin_pom_platform(self):
        """
        Méthode permettant de récupérer le chemin vers le fichier 'pom' du sous-projet platform. ;
        :return : Le chemin vers le fichier 'pom' du sous-projet platform.
        """
        return self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID + "-platform/pom.xml"

    def maj_platform_artifact_id(self, platform_artifact_id: str):
        """
        Méthode permettant de mettre à jour la valeur de l'artifact id du sous-projet platform. ;
        :param platform_artifact_id : La nouvelle valeur de l'artifact id du sous-projet platform. ;
        """
        self.PLATFORM_ARTIFACT_ID = platform_artifact_id
        self.CHEMIN_FICHIER_BOOTSTRAP = self.CHEMIN_PROJET + "/" + self.ARTIFACT_ID \
                                        + "-platform/src/main/resources/alfresco/module/" + self.PLATFORM_ARTIFACT_ID \
                                        + "/context/bootstrap-context.xml"
