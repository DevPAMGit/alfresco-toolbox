from api.typecontenu.source.modelecontroleur import ModeleControleur


class AspectControleur(ModeleControleur):
    """
    Classe permettant de gérer les aspects du projet.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe 'AspectControleur'.
        :param maximum: La largeur de l'affichage de la vue en caractères.
        """
        super().__init__(maximum)

    def generer_aspects(self):
        """
        Méthode permettant de générer les fichiers de gestion des aspects et leur prise en compte.
        """
        self.VUE.titre("PRISE EN COMPTE DES ASPECTS")
        self.creer_fichiers_java("aspect")
        self.maj_fichier_share_config_custom("aspect")