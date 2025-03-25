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
    requetes = list(curseur)
    res=''
    taille = 115
    ca_global = 0
    nb_global = 0
    nb_commande_livre = 0
    total = 0
    for i in range(len(requetes)-1):
        ligne = requetes[i]
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
        if i ==0:
            res +=f"Facture du {mois}/{annee}"
            res += f"Edition des factures du magasin {str(nommag)}\n"
            res += "-"*taille+"\n"   
            facture_editees = 0
            nb_livre = 0
        if i==len(requetes):
            res += str(facture_editees)+" factures éditées\n"
            res += str(nb_livre)+" livres vendus\n"
            res += "*"*taille+"\n"
            res +="Chiffre d'affaire global : "+str(ca_global)
            res +="Nombre livres vendus "+str(nb_global)







        if numcom != requetes[i+1]['numcom']:
            res += f"{requetes[i+1]['prenomcli']} {requetes[i+1]['nomcli']}\n{requetes[i+1]['adressecli']}\n{requetes[i+1]['codepostal']} {requetes[i+1]['villecli']}\n"
            res += f"commande n° {requetes[i+1]['numcom']} du {requetes[i+1]['datecom']}".center(taille)+"\n"
            res += "ISBN".rjust(12)+"Titre".rjust(20)+"qte".rjust(56)+"prix".rjust(16)+"total\n".rjust(11)
            res += str(nb_commande_livre).ljust(3)+str(isbn).ljust(15)+str(titre).ljust(68)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total)+"\n"
            total += Total
            facture_editees+=1
            res += "--------\n".rjust(taille)
            res += ("Total    "+str(total)+"\n").rjust(taille)
            res +="-"*taille+"\n"
            total = 0
            nb_livre += qte
            nb_commande_livre +=qte
            facture_editees+= 1
            if nommag != requetes[i+1]['nommag']:
                res += str(facture_editees)+" factures éditées\n"
                res += str(nb_livre)+" livres vendus\n"
                res += "*"*taille+"\n"
                res += "Edition des factures du magasin "+str(nommag)+"\n"
                res += "-"*taille+"\n"   
                facture_editees = 0
                nb_livre = 0
        else:
            res += str(nb_commande_livre).ljust(3)+str(isbn).ljust(15)+str(titre).ljust(68)+str(qte).ljust(14)+str(prix).ljust(9)+str(Total)+"\n"
            total += Total
            facture_editees+=1

        
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
    #passwd = getpass.getpass("mot de passe SQL:")
    passwd = "joubert"
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
