# Classe modèle pour un 'Type'
class Type:

    # Initialise une nouvelle instance de la classe 'Type'.
    # nom_complet Le nom complet du type.
    def __init__(self, nom_complet):
        self.PROPRIETES = []
        self.DESCRIPTION = None
        self.NOM_COMPLET = nom_complet
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    # Récupère le nom du type.
    # Retourne le nom du type.
    def get_nom(self):
        return self.NOM

    # Récupère le nom complet du type.
    # Retourne le nom complet du type.
    def get_nom_complet(self):
        return self.NOM_COMPLET

    def add_propriete(self, propriete):
        self.PROPRIETES.append(propriete)

    def add_proprietes(self, propriete):
        self.PROPRIETES += propriete

    # Modifie de la valeur de la description du type.
    # description La valeur de la description du type.
    def set_description(self, description: str):
        self.DESCRIPTION = description

