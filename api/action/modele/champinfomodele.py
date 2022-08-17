class ChampInfoModele:
    """
    Classe modèle pour un champ de classe.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'FieldInfoModele'.
        """
        self.NOM = None
        self.LABEL = None

    def maj_nom(self, nom: str):
        """
        Mise à jour du nom du champ. ;
        :param nom: La nouvelle valeur du nom du champ. ;
        """
        self.NOM = nom

    def maj_label(self, label: str):
        """
        Mise à jour du label du champ. ;
        :param label: La nouvelle valeur du label. ;
        """
        self.LABEL = label
