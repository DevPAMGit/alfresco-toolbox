from xml.etree import ElementTree

from mvc.modele.aspect_modele import AspectModele


class ExtracteurModele:

    def __init__(self, chemin_fichier_contenu, group_id):
        self.GROUP_ID = group_id
        self.RACINE = ElementTree.parse(chemin_fichier_contenu).getroot()
        self.XMLNS = "{" + self.RACINE.tag[1:self.RACINE.tag.rindex('}')] + "}"
        self.URI = self.RACINE.find(".//" + self.XMLNS + "namespaces/namespace").attrib["uri"]
        self.PREFIX = self.RACINE.find(".//" + self.XMLNS + "namespaces/namespace").attrib["prefix"]

    def charger_aspects(self):
        aspects = {}
        for aspect in self.RACINE.find(".//" + self.XMLNS + "aspects").findall(self.XMLNS + "aspect"):
            aspects[aspect.attrib["name"]] = AspectModele(aspect, self.XMLNS, self.URI, self.PREFIX, self.GROUP_ID)
        return aspects

    def charger_type(self):
        types = {}
        for typ in self.RACINE.find(".//" + self.XMLNS + "types").findall(self.XMLNS + "type"):
            types[typ.attrib["name"]] = AspectModele(type, self.XMLNS, self.URI, self.PREFIX, self.GROUP_ID)
        return types
