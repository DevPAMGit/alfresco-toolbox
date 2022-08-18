from api.aspect.aspectmodele import AspectModele
from api.generale.controleursecondaire import ControleurSecondaire
from api.modele.modele import Modele
from libs.pythonconsolevue.consolevue import ConsoleVue


class AspectControleur(ControleurSecondaire):

    def __init__(self, maximum: int):
        super().__init__(ConsoleVue(maximum), AspectModele())
        self.MODELE.__class__ = AspectModele

    def ajt_aspect(self, aspect: Modele):
        self.MODELE.ajt_modele(aspect)
