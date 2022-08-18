from api.modele.propriete import Propriete


class Modele:
    """
    Classe modèle pour des types de contenus.
    """

    def __init__(self, uri: str, nom_complet: str):
        """
        Initialise une nouvelle instance de la classe Modele. ;
        :param uri: L'URI du modèle. ;
        :param nom_complet : Le nom complet du modèle.
        """
        self.URI = None
        self.NOM = None
        self.TITRE = None
        self.PARENT = None
        self.PREFIX = None
        self.PROPRIETES = []
        self.DESCRIPTION = None
        self.NOM_COMPLET = None

    def maj_uri(self, uri: str):
        """
        Mise à jour de l'URI.
        :param uri: La nouvelle valeur de l'URI.
        """
        self.URI = uri

    def maj_nom(self, nom_complet: str):
        """
        Mise à jour du nom.
        :param nom_complet: Le nom complet.
        """
        self.NOM_COMPLET = nom_complet
        self.PREFIX = nom_complet[0: nom_complet.rindex(":")]
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    def ajt_proprietes(self, proprietes: list[Propriete]):
        """
        Méthode permettant d'ajouter une liste de propriétés.
        :param proprietes: La liste des propriétés.
        """
        self.PROPRIETES += proprietes