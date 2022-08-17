from libs.pythonconsolevue.consolevue import ConsoleVue


class ActionConsoleVue(ConsoleVue):
    """
    Classe permettant de gérer la vue de la sous api gérant les actions.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe 'ActionConsoleVue'. ;
        :param maximum: La largeur maximale (en caractères) de l'affichage.
        """
        super().__init__(maximum)
