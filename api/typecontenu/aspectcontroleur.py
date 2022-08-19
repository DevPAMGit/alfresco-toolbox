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
