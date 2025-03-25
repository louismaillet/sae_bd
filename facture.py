import sqlalchemy
import argparse
import getpass

#python3 facture.py --requete ./req_fac.sql --login joubert --serveur servinfo-maria --bd Librairie


class MySQL(object):
    def __init__(self, user, passwd, host, database,timeout=20):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.database = database
        #try:
        self.engine = sqlalchemy.create_engine(
                '://' + self.user + ':' + self.passwd + '@' + self.host + '/' + self.database,
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

def faire_factures(requete: str, mois: int, annee: int, bd: MySQL):
    curseur = bd.execute(requete, (mois, annee))
    print(f"Factures du {mois}/{annee}")
    requetes = list(curseur)
    res = ""  # Initialisation de res comme une chaîne de caractères
    taille = 115
    ca_global = 0
    nb_global = 0
    total = 0
    facture_editees = 0
    nb_livre = 0

    def ajouter_entete_facture(nommag, prenomcli, nomcli, adressecli, codepostal, villecli, numcom, datecom, res):
        res += f"Facture du {mois}/{annee}\n"
        res += f"Edition des factures du magasin {nommag}\n" + "-" * taille + "\n"
        res += f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}\n"
        res += f"commande n° {numcom} du {datecom}".center(taille) + "\n"
        res += "ISBN".rjust(12) + "Titre".rjust(20) + "qte".rjust(56) + "prix".rjust(16) + "total\n".rjust(11)
        return res

    for i, ligne in enumerate(requetes):
        if i == 0 or ligne['numcom'] != requetes[i - 1]['numcom']:
            if i != 0:
                res += "--------\n".rjust(taille)
                res += f"Total    {total}\n".rjust(taille) + "-" * taille + "\n"
                ca_global += total
                total = 0
                facture_editees += 1
                if ligne['nommag'] != requetes[i - 1]['nommag']:
                    res += f"{facture_editees} factures éditées\n{nb_livre} livres vendus\n" + "*" * taille + "\n"
                    nb_global += nb_livre
                    facture_editees = 0
                    nb_livre = 0
            res = ajouter_entete_facture(ligne['nommag'], ligne['prenomcli'], ligne['nomcli'], ligne['adressecli'], ligne['codepostal'], ligne['villecli'], ligne['numcom'], ligne['datecom'], res)
    
        res += f"{ligne['isbn'].ljust(15)}{ligne['titre'].ljust(68)}{str(ligne['qte']).rjust(14)}{str(ligne['prixvente']).rjust(9)}{str(ligne['Total']).rjust(9)}\n"
        total += ligne['Total']
        nb_livre += ligne['qte']  # Mise à jour du nombre de livres vendus

    # Finalisation après la dernière ligne
    res += "--------\n".rjust(taille)
    res += f"Total    {total}\n".rjust(taille) + "-" * taille + "\n"
    ca_global += total
    nb_global += nb_livre
    facture_editees += 1
    res += f"{facture_editees} factures éditées\n{nb_livre} livres vendus\n" + "*" * taille + "\n"
    res += f"Chiffre d'affaire global : {ca_global}\nNombre livres vendus : {nb_global}"

    curseur.close()
    return res
        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur",dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="127.0.0.1")
    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='limet')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str)    
    args = parser.parse_args()
    #passwd = getpass.getpass("mot de passe SQL:")
    passwd = "maillet"
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connection a échoué avec l'erreur suivante:", e)
        exit(0)
    #rep=input("Entrez le mois et l'année sous la forme mm/aaaa ")
    #mm,aaaa=rep.split('/')
    mois=int(2)
    annee=int(2020)
    with open(args.fichierRequete) as fic_req:
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))
