# Classe modèle pour un 'Type'
class Type:

    # Initialise une nouvelle instance de la classe 'Type'.
    # uri L'URI de type de contenu.
    # nom_complet Le nom complet du type.
    def __init__(self, uri: str, nom_complet):
        self.URI = uri
        self.PROPRIETES = []
        self.DESCRIPTION = None
        self.NOM_COMPLET = nom_complet
        self.PREFIX = nom_complet[0: nom_complet.rindex(":")]
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

    # Récupère le prefix l'aspect.
    # Retourne le prefix de l'aspect.
    def get_prefix(self):
        return self.PREFIX

    # Récupère La liste des propriétés.
    # Retourne La liste des propriétés.
    def get_proprietes(self):
        return self.PROPRIETES

    def get_uri(self):
        return self.URI
