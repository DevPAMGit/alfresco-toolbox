class Propriete:

    def __init__(self):
        self.TYPE = None
        self.TITRE = None
        self.MANDATORY = None
        self.NOM: str | None = None
        self.NOM_COMPLET: str | None = None

    def maj_nom(self, nom_complet: str):
        self.NOM_COMPLET = nom_complet
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    def maj_type(self, t: str):
        self.TYPE = t

    def set_mandatory(self, mandatory: bool):
        self.MANDATORY = mandatory

    def set_titre(self, titre):
        self.TITRE = titre

    def get_titre(self) -> str:
        return self.TITRE

    def get_nom(self) -> str:
        return self.NOM

    def get_nom_complet(self) -> str:
        return self.NOM_COMPLET

    def get_type(self) -> str:
        return self.TYPE

    def get_mandatory(self) -> str:
        return self.MANDATORY

    def to_string(self):
        return self.NOM + " " + self.NOM_COMPLET
