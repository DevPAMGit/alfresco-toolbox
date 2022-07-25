# Classe pour gérer les interactions avec le client
class Vue:

    # Initialise une nouvelle instance de la classe Vue.
    # nom_application Le nom de l'application.
    def __init__(self,  nom_application):
        self.NOM_APPLICATION = nom_application

    # Ecrit un message de binvenue sur la sortie standard.
    def bienvenue(self):
        print("=== SCRIPT - " + self.NOM_APPLICATION + " ===")

    # Ecrit un message d'erreur sur la sortie standard.
    def print_erreur(self, param):
        print(param)

    #
    def demande_chemin_projet(self):
        print("Veuillez saisir le chemin vers votre dossier alfresco :", end='')
        return input()

    def information(self, param):
        print(param, end='')
