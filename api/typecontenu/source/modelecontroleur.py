from api.typecontenu.source.modelemodele import ModeleModele
from api.generale.controleursecondaire import ControleurSecondaire
from api.modele.modele import Modele
from libs.pythonconsolevue.consolevue import ConsoleVue


class ModeleControleur(ControleurSecondaire):
    """
    Controleur pour gérer les aspects.
    """

    def __init__(self, maximum: int):
        """
        Initialise une nouvelle instance de la classe
        :param maximum: La largeur maximum de la vue en caractères.
        """
        super().__init__(ConsoleVue(maximum), ModeleModele())
        self.MODELE.__class__ = ModeleModele

    def ajt_modele(self, modele: Modele):
        """
        Ajoute un typecontenu dans le modèle de données.
        :param modele: L'type contenu à ajouter.
        """
        self.MODELE.ajt_modele(modele)

    def obt_modele(self, reference: str) -> (Modele | None):
        """
        Permet d'obtenir un type de contenu.
        :param reference: La référence au type de contenu (son nom).
        :return: Le type de contenu trouvé sinon None.
        """
        return self.MODELE.obt_modele(reference)

    def obt_modeles(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects de l'api.
        :return: Un dictionnaire des aspects de l'api.
        """
        return self.MODELE.obt_modeles()
