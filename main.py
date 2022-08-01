import sys

# C:\Users\mandrianaivo\IdeaProjects\affichage-des-actes
from modules.controleurs.controleur import Controleur

print("========== SCRIPT - INITIALISATION PROJET ==========")
print("[ERREUR] Veuillez saisir le chemin vers votre projet Alfresco.") \
    if len(sys.argv) != 2 else Controleur().generer_projet(sys.argv[1])
