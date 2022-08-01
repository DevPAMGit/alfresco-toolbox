class Propriete:

    def __init__(self, nom_complet):
        self.TYPE = None
        self.TITRE = None
        self.MANDATORY = None
        self.NOM_COMPLET = nom_complet
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    def set_type(self, t):
        self.TYPE = t

    def set_mandatory(self, mandatory):
        self.MANDATORY = mandatory

    def set_titre(self, titre):
        self.TITRE = titre

    def get_nom(self):
        return self.NOM

    def get_nom_complet(self):
        return self.NOM_COMPLET
