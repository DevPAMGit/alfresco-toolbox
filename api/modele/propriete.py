class Propriete:

    def __init__(self):
        self.NOM = None
        self.TYPE = None
        self.TITRE = None
        self.MANDATORY = None
        self.NOM_COMPLET = None

    def maj_nom(self, nom_complet: str):
        self.NOM_COMPLET = nom_complet
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    def maj_type(self, t):
        self.TYPE = t

    def set_mandatory(self, mandatory):
        self.MANDATORY = mandatory

    def set_titre(self, titre):
        self.TITRE = titre

    # Récupère la valeur du titre.
    # Retourne Le titre de la propriété.
    def get_titre(self):
        return self.TITRE

    def get_nom(self):
        return self.NOM

    def get_nom_complet(self):
        return self.NOM_COMPLET

    def get_type(self):
        return self.TYPE

    def get_mandatory(self):
        return self.MANDATORY
