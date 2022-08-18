from abc import ABC

from api.aspect.aspectcontroleur import AspectControleur
from libs.pythonconsolevue.consolevue import ConsoleVue
from api.action.actioncontroleur import ActionControleur
from api.donnees.donneescontroleur import DonneesControleur
from api.principal.principalbuffercontroleur import PrincipalBufferControleur


class ControleurPrincipal(PrincipalBufferControleur, ABC):
    """
    Controleur principale de l'API
    """

    def __init__(self):
        super().__init__(ConsoleVue(100))

        self.CTRL_ASPECT = AspectControleur(100)
        self.CTRL_ACTIONS = ActionControleur(100)
        self.CTRL_DONNEES = DonneesControleur(self, 100)

    def formatter(self, argv: [str]):
        self.VUE.titre("FORMATAGE DU PROJET")

    def ajt_aspect(self, aspect):
        """
        Méthode permettant d'ajouter un nouvel aspect au modèle de données. ;
        :param aspect: L'aspect à ajouter. ;
        """
        self.CTRL_ASPECT.ajt_aspect(aspect)

    def obt_aspect(self, reference):
        pass
