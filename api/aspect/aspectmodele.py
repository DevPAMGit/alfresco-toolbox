from api.generale.modelegenerale import ModeleGenerale
from api.modele.modele import Modele


class AspectModele(ModeleGenerale):
    """
    Modèle de données pour l'api gérant les aspects du projet.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'AspectModele'.
        """
        super().__init__()
        self.MODELES: list[Modele] = []

    def ajt_modele(self, modele: Modele):


