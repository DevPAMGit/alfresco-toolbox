

# Classe modele pour les aspects.
from mvc.modele.propriete_modele import ProprieteModele


class AspectModele:

    def __init__(self, aspect, xmlns, uri, prefix, group_id):
        self.URI = uri
        self.XMLNS = xmlns
        self.PREFIX = prefix
        self.PROPRIETES = {}
        self.GROUP_ID = group_id
        self.MANDATORY_ASPECTS = []
        self.NOM_COMPLET = aspect.tag["name"]
        self.NOM = aspect.tag["name"][aspect.tag["name"].rindex(':') + 1:len(aspect.tag["name"])]

        for propriete in aspect.find(self.XMLNS + "properties").findall(self.XMLNS + "property"):
            nom = propriete.tag["name"][propriete.tag["name"].rindex(':') + 1:len(propriete.tag["name"])]
            self.PROPRIETES[nom] = ProprieteModele(xmlns, propriete, nom)

        for mandatory_aspect in aspect.find(self.XMLNS + "mandatory-aspects").findall(self.XMLNS + "aspect"):
            self.MANDATORY_ASPECTS.put(mandatory_aspect)
