import re


class ClasseInfoModele:
    """
    Classe représentant les informations concernant une classe.
    """

    def __init__(self):
        self.NOM = None
        self.TITRE = None
        self.CHAMPS = None
        self.PACKAGE = None
        self.NOM_CLASSE = None
        self.DESCRIPTION = None
        self.REGISTRE_SERVICE_NOM = None
        self.UTILISE_SERVICE_REGISTRE: bool = False

    def maj_nom(self, nom: str):
        """
        Met à jour le paramètre de classe NOM. ;
        :param nom: La nouvelle valeur du nom de la classe.
        """
        self.NOM_CLASSE = nom
        self.NOM = re.sub("(\\w)([A-Z])", "\\1-\\2", nom)
        self.TITRE = re.sub("(\\w)([A-Z])", "\\1 \\2", nom)

    def maj_package(self, package: str):
        """
        Met à jour le package de la classe. ;
        :param package : La nouvelle valeur du package de la classe. ;
        """
        self.PACKAGE = package

    def maj_description(self, description: str):
        """
        Met à jour la description de la classe. ;
        :param description : La nouvelle valeur de la description de la classe. ;
        """
        self.DESCRIPTION = description

    def maj_utilisation_registre_service(self, utilisation: (bool, str)):
        """
        Met à jour la valeur indiquant si la classe utilise le registre de service Alfresco. ;
        :param utilisation : La valeur indiquant si la classe utilise le registre de service Alfresco. ;
        """
        t1, t2 = utilisation
        self.UTILISE_SERVICE_REGISTRE = t1
        self.REGISTRE_SERVICE_NOM = t2

    def maj_registre_service_nom(self, registre_service_nom):
        self.REGISTRE_SERVICE_NOM = registre_service_nom

    def maj_champs(self, champs):
        self.CHAMPS = champs
