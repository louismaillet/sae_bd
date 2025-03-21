import shutil
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
    # Initialisations du traitement
    print(f"Factures du {mois}/{annee}")
    taille_terminal = shutil.get_terminal_size().columns
    res=''
    livres_vendu = 0
    commande_prec = None
    magasin_prec = None
    ca_global = 0
    nb_global = 0
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
        
        if magasin_prec is None:
            print(f"Edition des factures du magasin {nommag}")
            print("-" * taille_terminal)
            nb_livre = 0
            facture_editees = 0
        elif nommag!= magasin_prec:
            print(str(facture_editees) +" factures éditées")
            print(str(nb_livre)+" livres vendus")
            print("*"*taille_terminal)
            print(f"Edition des factures du magasin {nommag}")
            print("-" * taille_terminal)
            nb_livre = 0
            facture_editees = 0


        if commande_prec is None:
            total = 0
            print(f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}")
            print(" " * (taille_terminal//2-15) + "commande n°" + str(numcom) + " du "+str(datecom))
            print("".ljust(15)+"ISBN".ljust(40)+"Titre".ljust(35)+"qte".ljust(15)+"prix".ljust(10)+"total")
            print("".ljust(5)+str(nb_livre+1).ljust(5)+str(isbn).ljust(15)+str(titre).ljust(66)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total))
            total += Total
            nb_livre += qte
            facture_editees +=1
        elif commande_prec!=numcom:
            print("".ljust(111)+"---------")
            print("".ljust(110)+"Total "+str(total))
            print("-"*taille_terminal)
            ca_global+=total
            total = 0
            print(f"{prenomcli} {nomcli}\n{adressecli}\n{codepostal} {villecli}")
            print(" " * (taille_terminal//2-15) + "commande n°" + str(numcom) + " du "+str(datecom))
            print("".ljust(15)+"ISBN".ljust(40)+"Titre".ljust(35)+"qte".ljust(15)+"prix".ljust(10)+"total")
            print("".ljust(5)+str(nb_livre).ljust(5)+str(isbn).ljust(15)+str(titre).ljust(66)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total))
            total += Total
            nb_livre += qte
            facture_editees +=1
        else:
            print("".ljust(5)+str(nb_livre).ljust(5)+str(isbn).ljust(15)+str(titre).ljust(66)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total))
            total += Total
            nb_livre += qte
            facture_editees +=1
            
        magasin_prec = nommag
        commande_prec = numcom
    print("".ljust(111)+"---------")
    print("".ljust(110)+"Total "+str(total))
    print("-"*taille_terminal)
    print(str(facture_editees) +" factures éditées")
    print(str(nb_livre)+" livres vendus")
    print("*"*taille_terminal)
    print(f"Edition des factures du magasin {nommag}")
    print("-" * taille_terminal)
    print("Chiffre d'affaire global : "+ca_global)
    print("Nombre livres vendus "+nb_global)


        
    #ici fin du traitement
    # fermeture de la requête
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
    rep=input("Entrez le mois et l'année sous la forme mm/aaaa ")
    mm,aaaa=rep.split('/')
    mois=int(mm)
    annee=int(aaaa)
    with open(args.fichierRequete) as fic_req:
        requete=fic_req.read()
    print(faire_factures(requete,mois,annee,ms))
