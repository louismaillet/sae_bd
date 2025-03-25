import sqlalchemy
import argparse
import getpass
import numpy as np
import matplotlib.pyplot as plt

# python3 facture.py --requete ./req_fac.sql --login maillet --serveur servinfo-maria --bd Librairie

class MySQL(object):
    def __init__(self, user, passwd, host, database,timeout=20):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.database = database
        #try:
        self.engine = sqlalchemy.create_engine(
                'mariadb://' + self.user + ':' + self.passwd + '@' + self.host + '/' + self.database,
                )
        self.cnx = self.engine.connect()
        print("connexion réussie")

    def close(self):
        self.cnx.close()

    def execute(self, requete, liste_parametres):
        for param in liste_parametres:
            if type(param)==str:
                requete=requete.replace('?',"'"+param+"'",1)
            else:
                requete=requete.replace('?',str(param),1)
        return self.cnx.execute(requete)

def visualiser_points(requete:str, bd:MySQL):
    curseur = bd.execute(requete, [])
    nb_ventes = []
    ca = []
    
    for ligne in curseur:
        nb_ventes.append(ligne[0])  # NbVentes
        ca.append(ligne[1])        # CA
    
    curseur.close()
    
    # Tracer le nuage de points
    plt.scatter(nb_ventes, ca, color='blue', alpha=0.7)
    plt.title("Relation entre NbVentes et CA")
    plt.xlabel("Nombre de ventes (NbVentes)")
    plt.ylabel("Chiffre d'affaires (CA)")
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur",dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="127.0.0.1")
    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='maillet')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str)    
    args = parser.parse_args()
    passwd = getpass.getpass("mot de passe SQL:")
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connection a échoué avec l'erreur suivante:", e)
        exit(0)
    
    with open(args.fichierRequete) as fic_req:
        requete = fic_req.read()
    
    visualiser_points(requete, ms)