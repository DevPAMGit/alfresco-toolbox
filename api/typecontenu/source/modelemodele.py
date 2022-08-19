from api.generale.modelegenerale import ModeleGenerale
from api.modele.modele import Modele


class ModeleModele(ModeleGenerale):
    """
    Modèle de données pour l'api gérant les aspects du projet.
    """

    def __init__(self):
        """
        Initialise une nouvelle instance de la classe 'AspectModele'.
        """
        super().__init__()
        self.MODELES: dict[str, Modele] = {}

    def ajt_modele(self, modele: Modele):
        """
        Ajoute un modèle dans le modèle de données.
        :param modele: Le modèle à ajouter.
        """
        self.MODELES[modele.NOM_COMPLET] = modele

    def obt_modele(self, reference: str) -> (Modele | None):
        """
        Méthode permettant d'obtenir un modèle par son nom.
        :param reference: Le nom du modèle à récupérer.
        :return: Le modèle référencé par le nom.
        """
        if reference in self.MODELES.keys():
            resultat: (Modele | None) = self.MODELES[reference]
        else:
            resultat = None

        return resultat

    def obt_modeles(self) -> dict[str, Modele]:
        """
        Méthode permettant de récupérer les aspects du modèle.
        :return: Un dictionnaire des aspects du modèle.
        """
        return self.MODELES
