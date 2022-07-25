import sys
from mvc.controleur.controleur import Controleur

Controleur().run(sys.argv[1]) if len(sys.argv) == 2 else print("[ERREUR] Vous devez saisir le chemin vers votre projet (all-in-one) alfreso !")



