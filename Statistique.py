import sqlalchemy
import argparse
import getpass
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt

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


def cov_ou_var(X,Y):
    moyX = np.mean(X)
    moyY = np.mean(Y)
    res = 0
    for i in range(len(X)):
        res += (X[i]-moyX)*(Y[i]-moyY)
    return res /len(X)

def corr(X,Y):
    return cov_ou_var(X,Y)/(sqrt(cov_ou_var(X,X))*sqrt(cov_ou_var(Y,Y)))

def regression_lineaire(X,Y):
    a = cov_ou_var(X,Y)/cov_ou_var(X,X)
    b = np.mean(Y)-a*np.mean(X)
    return a,b
    

def visualiser_points(requete:str, bd:MySQL):
    curseur = bd.execute(requete, [])
    nb_ventes = []
    ca = []
    
    for ligne in curseur:
        nb_ventes.append(ligne[0])  # NbVentes
        ca.append(round(ligne[1]))        # CA
    
    A = np.array(list(nb_ventes))
    B = np.array(list(ca))
    print(corr(A,B))
    a,b=regression_lineaire(A,B)
    print(a)
    print(b)
    
    plt.scatter(A,B, color='blue', marker='o', alpha=0.7)
    plt.plot([0,200],[0,(a*200)+b] , color='green')    
    curseur.close()
    plt.title("Relation entre NbVentes et CA")
    plt.xlabel("Nombre de ventes (NbVentes)")
    plt.ylabel("Chiffre d'affaires (CA)")
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