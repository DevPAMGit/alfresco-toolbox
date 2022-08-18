class ExceptionPersonnalisee(Exception):
    """
    Exception pour les erreurs personnalisées.
    """

    def __init__(self, message: str):
        """
        Initialise une nouvelle instance de la classe 'CustomException'.
        :param message: Le message de l'exception.
        """
        self.MESSAGE = message
