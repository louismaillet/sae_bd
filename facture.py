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

def faire_factures(requete: str, mois: int, annee: int, bd: MySQL):
    def ajouter_ligne_facture(res, nb_commande_livre, isbn, titre, qte, prix, total):
        if len(titre)<66: 
            return res + f"{'':<5}{nb_commande_livre:<5}{isbn:<15}{titre:<66}{qte:<14}{prix:<10}{total}\n"
        else:
            return res + f"{'':<5}{nb_commande_livre:<5}{isbn:<15}{(titre[:60]+"..."):<66}{qte:<14}{prix:<9}{total}\n"

    def ajouter_total_facture(res, total):
        return res + f"{'':<111}---------\n{'':<110}Total {total}\n" + "-" * taille_terminal + "\n"

    curseur = bd.execute(requete, (mois, annee))
    res = f"Factures du {mois}/{annee}\n"
    taille_terminal = 122
    
    magasin_prec, commande_prec = None, None
    ca_global, nb_global = 0, 0
    nb_livre_magasin, nb_livre_commande, total_commande = 0, 0, 0
    facture_editees_magasin, facture_editees_global = 0, 0
    
    for ligne in curseur:
        nommag, numcom, datecom = ligne['nommag'], ligne['numcom'], ligne['datecom']
        nomcli, prenomcli, adressecli = ligne['nomcli'], ligne['prenomcli'], ligne['adressecli']
        codepostal, villecli = ligne['codepostal'], ligne['villecli']
        isbn, titre, qte, prix, Total = ligne['isbn'], ligne['titre'], ligne['qte'], ligne['prixvente'], ligne['Total']
        
        if magasin_prec is None or nommag != magasin_prec:
            if magasin_prec is not None:
                res = ajouter_total_facture(res, total_commande)
                nb_global += nb_livre_magasin
                res += f"{facture_editees_magasin} factures éditées\n{nb_livre_magasin} livres vendus\n" + "*" * taille_terminal + "\n"
            res += f"Edition des factures du magasin {nommag}\n" + "-" * taille_terminal + "\n"
            nb_livre_magasin, facture_editees_magasin = 0, 0
            total_commande, nb_livre_commande = 0, 0
        
        if commande_prec is None or numcom != commande_prec:
            if commande_prec is not None and magasin_prec == nommag:
                res = ajouter_total_facture(res, total_commande)
            nb_livre_commande = 0
            res += f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}\n"
            res += f"{' ' * (taille_terminal // 2 - 15)}commande n°{numcom} du {datecom}\n"
            res += f"{'':<15}{'ISBN':<40}{'Titre':<35}{'qte':<15}{'prix':<10}total\n"
            facture_editees_magasin += 1
            facture_editees_global += 1
            total_commande = 0
        nb_livre_commande += qte
        nb_livre_magasin += qte
        total_commande += Total
        ca_global += Total
        res = ajouter_ligne_facture(res, nb_livre_commande, isbn, titre, qte, prix, Total)
        
        magasin_prec, commande_prec = nommag, numcom
    
    # Ajouter le dernier total de commande et magasin
    res = ajouter_total_facture(res, total_commande)
    nb_global += nb_livre_magasin
    res += f"{facture_editees_magasin} factures éditées\n{nb_livre_magasin} livres vendus\n" + "*" * taille_terminal + "\n"
    res += f"Chiffre d'affaire global : {ca_global}\nNombre livres vendus {nb_global}\n"
    
    curseur.close()
    return res

        


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--serveur",dest="nomServeur", help="Nom ou adresse du serveur de base de données", type=str, default="127.0.0.1")
    parser.add_argument("--bd",dest="nomBaseDeDonnees", help="Nom de la base de données", type=str,default='Librairie')
    parser.add_argument("--login",dest="nomLogin", help="Nom de login sur le serveur de base de donnée", type=str, default='limet')
    parser.add_argument("--requete", dest="fichierRequete", help="Fichier contenant la requete des commandes", type=str)    
    args = parser.parse_args()
    passwd = getpass.getpass("mot de passe SQL:")
    try:
        ms = MySQL(args.nomLogin, passwd, args.nomServeur, args.nomBaseDeDonnees)
    except Exception as e:
        print("La connection a échoué avec l'erreur suivante:", e)
        exit(0)
    rep=input("Entrez un mois et une année sous la forme mois/année : 00/0000 ")
    mm,aaaa=rep.split('/')
    mois=int(mm)
    annee=int(aaaa)
    with open(args.fichierRequete) as fic_req:
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))
