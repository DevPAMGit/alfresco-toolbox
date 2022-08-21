import os
import sys

# C:\Users\mandrianaivo\IdeaProjects\affichage-des-actes
# from modules.controleurs.controleur import Controleur
#
# print("========== SCRIPT - INITIALISATION PROJET ==========")
# print("[ERREUR] Veuillez saisir le chemin vers votre projet Alfresco.") \
#     if len(sys.argv) != 2 else Controleur().generer_projet(sys.argv[1])

#from api.action.actioncontroleur import ActionControleur

#ctrl: ActionControleur = ActionControleur(90)

#ctrl.maj_group_id("org.cd59")
#ctrl.maj_artifact_id("affichage-des-actes")
#ctrl.maj_chemin_projet("C:\personnels\\developpements\\affichage-des-actes")
#ctrl.maj_chemin_dossier_ressources(os.getcwd() + "/ressources")

#ctrl.controler()

from api.principal.principalcontroleur import ControleurPrincipal

ctrl: ControleurPrincipal = ControleurPrincipal()
print(sys.argv)
ctrl.formatter(sys.argv[1])
