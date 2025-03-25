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

def faire_factures(requete:str, mois:int, annee:int, bd:MySQL):
    # exécute la requête en remplaçant le premier ? par le numéro du mois 
    # et le deuxième ? par l'année
    curseur=bd.execute(requete,(mois,annee))
    res=''
    # Initialisations du traitement
    res += f"Factures du {mois}/{annee}\n"
    taille_terminal = 115
    commande_prec = None
    magasin_prec = None
    ca_global = 0
    nb_global = 0
    nb_commande_livre = 0
    for ligne in curseur:
        nommag = ligne['nommag']
        numcom = ligne['numcom']
        datecom = ligne['datecom']
        nomcli = ligne['nomcli']
        prenomcli = ligne['prenomcli']
        adressecli = ligne['adressecli']
        codepostal = ligne['codepostal']
        villecli = ligne['villecli']
        isbn = ligne['isbn']
        titre = ligne['titre']
        qte = ligne['qte']
        prix = ligne['prixvente']
        Total = ligne['Total']

        if magasin_prec is None: #vérification pour le cas du début
            res += f"Edition des factures du magasin {nommag}\n"
            res += "-" * taille_terminal + "\n"
            nb_livre = 0
            facture_editees = 0
        elif nommag!= magasin_prec: #si je change de magasin
            nb_global+=nb_livre
            ca_global+=total
            res += "".ljust(111) + "---------\n"
            res += "".ljust(110) + "Total " + str(total) + "\n"
            res += "-" * taille_terminal + "\n"
            res += str(facture_editees) + " factures éditées\n"
            res += str(nb_livre) + " livres vendus\n"
            res += "*" * taille_terminal + "\n"
            print(f"Edition des factures du magasin {nommag}")
            print("-" * taille_terminal)
            nb_livre = 0
            facture_editees = 0
            total = 0

        if commande_prec is None: #vérification pour le cas du début
            nb_commande_livre +=1
            res += f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}\n"
            res += " " * (taille_terminal // 2 - 15) + "commande n°" + str(numcom) + " du " + str(datecom) + "\n"
            res += "".ljust(15) + "ISBN".ljust(40) + "Titre".ljust(35) + "qte".ljust(15) + "prix".ljust(10) + "total\n"
            res += "".ljust(5) + str(nb_commande_livre).ljust(5) + str(isbn).ljust(15) + str(titre).ljust(66) + str(qte).ljust(14) + str(prix).ljust(9) + str(Total) + "\n"
            total = 0
            total += Total
            nb_livre += qte
            facture_editees +=1

        elif commande_prec!=numcom: #si je change de commande
            if nommag == magasin_prec:
                res += "".ljust(111)+"---------"+"\n"
                res += "".ljust(110)+"Total "+str(total)+"\n"
                res += "-"*taille_terminal + "\n"
            ca_global+=total
            total = 0
            nb_commande_livre = 0
            nb_commande_livre +=1

            res += f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}"+"\n"
            res += " " * (taille_terminal//2-15) + "commande n°" + str(numcom) + " du "+str(datecom)+"\n"
            res += "".ljust(15)+"ISBN".ljust(40)+"Titre".ljust(35)+"qte".ljust(15)+"prix".ljust(10)+"total"+"\n"
            res += "".ljust(5)+str(nb_commande_livre).ljust(5)+str(isbn).ljust(15)+str(titre).ljust(66)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total)+"\n"

            total += Total
            nb_livre += qte
            facture_editees +=1
        else: #si je ne change pas de commande
            nb_commande_livre +=1

            res +="".ljust(5)+str(nb_commande_livre).ljust(5)+str(isbn).ljust(15)+str(titre).ljust(66)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total)+"\n"

            total += Total
            nb_livre += qte
            facture_editees +=1

        magasin_prec = nommag
        commande_prec = numcom

    nb_global += nb_livre
    ca_global+=total
    res += "".ljust(111) + "---------\n"
    res += "".ljust(110) + "Total " + str(total) + "\n"
    res += "-" * taille_terminal + "\n"
    res += str(facture_editees) + " factures éditées\n"
    res += str(nb_livre) + " livres vendus\n"
    res += "*" * taille_terminal + "\n"
    res += "Chiffre d'affaire global : " + str(ca_global) + "\n"
    res += "Nombre livres vendus " + str(nb_global) + "\n"


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
