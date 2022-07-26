class ProprieteModele:

    def __init__(self, xmlns, propriete, nom):
        self.NOM = nom
        self.XMLNS = xmlns
        self.NOM_COMPLET = propriete.tag["name"]
        self.MANDATORY = self.est_obligatoire(propriete)
        self.DESCRIPTION = self.get_description(propriete)

    def est_obligatoire(self, propriete):
        mandatory = propriete.find(self.XMLNS + "mandatory")
        if mandatory is None:
            return False
        mandatory_valeur = mandatory.text.lower()
        if mandatory_valeur == "true":
            return True
        else:
            return False

    def get_description(self, propriete):
        description = propriete.find(self.XMLNS + "description")
        if description is None:
            return None
        else:
            return description.text



