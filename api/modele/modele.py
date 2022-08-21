from api.modele.propriete import Propriete


class Modele:
    """
    Classe modèle pour des types de contenus.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe Modele.
        """
        self.URI = None
        self.TITRE = None
        self.PARENT = None
        self.DESCRIPTION = None
        self.NOM_COMPLET = None
        self.NOM: str | None = None
        self.PREFIX: str | None = None
        self.PROPRIETES: list[Propriete] = []

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

    def obt_proprietes(self):
        """
        Méthode permettant de récupérer la liste des propriétés.
        :return: La liste des propriétés.
        """
        return self.PROPRIETES

    def maj_parent(self, parent: (str | None)):
        """
        Met à jour le parent du modèle.
        :param parent: La nouvelle valeur du parent.
        """
        self.PARENT = parent

    def maj_description(self, description: str):
        """
        Méthode permettant d'ajouter une description fichier.
        :param description:
        :return:
        """
        self.DESCRIPTION = description
