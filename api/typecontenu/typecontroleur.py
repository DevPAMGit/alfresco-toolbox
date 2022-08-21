from api.typecontenu.source.modelecontroleur import ModeleControleur


class TypeControleur(ModeleControleur):
    """
    Classe permettant de gérer les types du projet.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe 'TypeControleur'.
        :param maximum: La largeur de l'affichage de la vue en caractères.
        """
        super().__init__(maximum)

    def generer_type(self):
        """
        Méthode permettant de générer les fichiers de gestion des aspects et leur prise en compte.
        """
        self.VUE.titre("PRISE EN COMPTE DES TYPES")
        self.creer_fichiers_java("type")
        self.maj_fichier_share_config_custom("type")