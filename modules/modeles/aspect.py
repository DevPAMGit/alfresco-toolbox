# Classe modèle pour un aspect.
class Aspect:

    # Initialise une nouvelle instance de la classe 'Aspect'.
    # nom_complet Le nom complet de l'aspect.
    def __init__(self, nom_complet):
        self.TITRE = None
        self.PROPRIETES = []
        self.DESCRIPTION = None
        self.NOM_COMPLET = nom_complet
        self.NOM = nom_complet[nom_complet.rindex(":") + 1:len(nom_complet)]

    # Récupère le nom de l'aspect.
    # Retourne le nom de l'aspect.
    def get_nom(self):
        return self.NOM

    # Récupère le nom complet de l'aspect.
    # Retourne le nom complet de l'aspect.
    def get_nom_complet(self):
        return self.NOM_COMPLET

    # Modifie de la valeur de la description de l'aspect.
    # description La valeur de la description de l'aspect.
    def set_description(self, description):
        self.DESCRIPTION = description

    # Ajoute une propriété à l'aspect.
    # propriete La propriété à ajouter.
    def add_propriete(self, propriete):
        self.PROPRIETES.append(propriete)

    # Ajoute une liste de propriétés aux propriétés de l'aspect.
    # proprietes Les propriétés à ajouter.
    def add_proprietes(self, proprietes):
        self.PROPRIETES += proprietes

    # Modifie la valeur du titre de l'aspect.
    # Retourne la valeur du titre de l'aspect.
    def set_titre(self, titre):
        self.TITRE = titre

    # Récupère La liste des propriétés.
    # Retourne La liste des propriétés.
    def get_proprietes(self):
        return self.PROPRIETES