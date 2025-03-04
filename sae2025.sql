-- Devoir 127
-- Nom: CHER , Prenom: Naick

-- Feuille SAE2.05 Exploitation d'une base de données: Livre Express
-- 
-- Veillez à bien répondre aux emplacements indiqués.
-- Seule la première requête est prise en compte.

-- +-----------------------+--
-- * Question 127156 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres qui ont été commandés le 1er décembre 2024 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | isbn          | titre                                      | nbpages | datepubli | prix  |
-- +---------------+--------------------------------------------+---------+-----------+-------+
-- | etc...
-- = Reponse question 127156.
\! echo "requete 1----------------------------------------------"
SELECT isbn, titre, nbpages, datepubli, prix 
FROM COMMANDE 
NATURAL JOIN DETAILCOMMANDE 
NATURAL JOIN LIVRE
WHERE datecom = str_to_date('01-12-2024','%d-%m-%Y');

--11--

-- +-----------------------+--
-- * Question 127202 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels clients ont commandé des livres de René Goscinny en 2021 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | idcli | nomcli  | prenomcli | adressecli                  | codepostal | villecli    |
-- +-------+---------+-----------+-----------------------------+------------+-------------+
-- | etc...
-- = Reponse question 127202.
\! echo "requete 2----------------------------------------------"
SELECT distinct(idcli),nomcli, prenomcli, adressecli, codepostal, villecli
FROM CLIENT 
NATURAL JOIN COMMANDE 
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN LIVRE
NATURAL JOIN ECRIRE
NATURAL JOIN AUTEUR
WHERE YEAR(datecom) = 2021 and nomauteur='René Goscinny';

--375--

-- +-----------------------+--
-- * Question 127235 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Quels sont les livres sans auteur et étant en stock dans au moins un magasin en quantité strictement supérieure à 8 ?

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +---------------+-----------------------------------+-------------------------+-----+
-- | isbn          | titre                             | nommag                  | qte |
-- +---------------+-----------------------------------+-------------------------+-----+
-- | etc...
-- = Reponse question 127235.
\! echo "requete 3----------------------------------------------"
SELECT isbn, titre, nommag, qte
FROM LIVRE
NATURAL LEFT JOIN ECRIRE
NATURAL JOIN POSSEDER
NATURAL JOIN MAGASIN
WHERE idauteur IS NULL AND qte > 8;

--13--

-- +-----------------------+--
-- * Question 127279 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut le nombre de clients qui habitent dans la ville de ce magasin (en affichant les 0)

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-------------------------+-------+
-- | idmag | nommag                  | nbcli |
-- +-------+-------------------------+-------+
-- | etc...
-- = Reponse question 127279.
\! echo "requete 4----------------------------------------------"
SELECT idmag, nommag, COUNT(idcli) AS nbcli
FROM MAGASIN
LEFT JOIN CLIENT ON MAGASIN.villemag = CLIENT.villecli
GROUP BY idmag, nommag; 

--7--

-- +-----------------------+--
-- * Question 127291 : 2pts --
-- +-----------------------+--
--  Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut la quantité de livres achetés le 15/09/2022 en affichant les 0.

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+------+
-- | nommag                  | nbex |
-- +-------------------------+------+
-- | etc...
-- = Reponse question 127291.
\! echo "requete 5----------------------------------------------"
SELECT nommag, IFNULL(SUM(qte), 0) AS nbex
FROM MAGASIN
NATURAL LEFT JOIN (
    SELECT idmag, numcom
    FROM COMMANDE
    WHERE datecom = str_to_date('15-09-2022','%d-%m-%Y')
) AS COMMANDE
NATURAL LEFT JOIN DETAILCOMMANDE
GROUP BY nommag;





-- +-----------------------+--
-- * Question 127314 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Instructions d'insertion dans la base de données
/* 
Indiquez les insertions à effectuer dans la base de données pour insérer le livre de numéro ISBN
9782844273765 dont le titre est SQL pour les Nuls publié en 2002 par First Interactive. 
compte 292 pages et a été écrit par Allen G. Taylor (d’identifiant OL246259A) et Reinhard Engel
(d’identifiant OL7670824A). Ce livre est stocké en 3 exemplaires dans le magasin Loire et Livres.
Son prix est de 33.5€

*/
-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------------+
-- | insertions |
-- +------------+
-- | etc...
-- = Reponse question 127314.

--INSERT LIVRE (isbn, titre, nbpages, datepubli, prix)
--VALUES ('9782844273765', 'SQL pour les Nuls', 292, '2002-01-01', 33.5);
--INSERT EDITEUR VALUES ('First Interactive',240);
--INSERT EDITER VALUES ('9782844273765', 240);
--INSERT AUTEUR VALUES ('OL246259A', 'Allen G. Taylor');
--INSERT AUTEUR VALUES ('OL7670824A', 'Reinhard Engel');
--INSERT ECRIRE VALUES ('9782844273765', 'OL246259A');
--INSERT ECRIRE VALUES ('9782844273765', 'OL7670824A');
--INSERT POSSEDER VALUES ('Loire et Livres', '9782844273765', 3);


-- +-----------------------+--
-- * Question 127369 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 1 Nombre de livres vendus par magasin et par an

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+-------+-----+
-- | Magasin                 | Année | qte |
-- +-------------------------+-------+-----+
-- | etc...
-- = Reponse question 127369.
\! echo "requete 6----------------------------------------------"
SELECT nommag,YEAR(datecom) Année,sum(qte) qte FROM MAGASIN
NATURAL JOIN COMMANDE
NATURAL JOIN DETAILCOMMANDE
GROUP BY nommag,YEAR(datecom); 



-- +-----------------------+--
-- * Question 127370 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 2  Chiffre d'affaire par thème en 2024

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +--------------------------------------+---------+
-- | Theme                                | Montant |
-- +--------------------------------------+---------+
-- | etc...
\! echo "requete 7----------------------------------------------"
SELECT nomclass AS Theme, SUM(prixvente * qte) AS Montant
FROM DETAILCOMMANDE
NATURAL JOIN COMMANDE
NATURAL JOIN LIVRE
NATURAL JOIN THEMES
NATURAL JOIN CLASSIFICATION
WHERE YEAR(datecom) = 2024
GROUP BY LEFT(LPAD(iddewey, 3, '0'), 1)
ORDER BY nomclass;


-- +-----------------------+--
-- * Question 127381 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 3 Evolution chiffre d'affaire par magasin et par mois en 2024

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------+-------------------------+---------+
-- | mois | Magasin                 | CA      |
-- +------+-------------------------+---------+
-- | etc...
-- = Reponse question 127381.
\! echo "requete 8----------------------------------------------"
select MONTH(datecom) as mois, nommag as Magasin, sum(prixvente*qte) as CA
from COMMANDE
natural join DETAILCOMMANDE
natural join MAGASIN
where YEAR(datecom) = 2024
group by MONTH(datecom), nommag;


-- +-----------------------+--
-- * Question 127437 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 4 Comparaison ventes en ligne et ventes en magasin

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+------------+---------+
-- | annee | typevente  | montant |
-- +-------+------------+---------+
-- | etc...
-- = Reponse question 127437.



-- +-----------------------+--
-- * Question 127471 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 5

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------+-----------+
-- | Editeur           | nbauteurs |
-- +-------------------+-----------+
-- | etc...
-- = Reponse question 127471.



-- +-----------------------+--
-- * Question 127516 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 6 Origine des clients ayant acheter des livres de R. Goscinny

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------+-----+
-- | ville       | qte |
-- +-------------+-----+
-- | etc...
-- = Reponse question 127516.



-- +-----------------------+--
-- * Question 127527 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 7 Valeur du stock par magasin
--Requête Graphique 8 Statistiques sur l'évolution du chiffre d'affaire total par client 

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+---------+
-- | Magasin                 | total   |
-- +-------------------------+---------+
-- | etc...
-- = Reponse question 127527.



-- +-----------------------+--
-- * Question 127538 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Palmarès

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+---------+---------+
-- | annee | maximum | minimum | moyenne |
-- +-------+---------+---------+---------+
-- | etc...
-- = Reponse question 127538.



-- +-----------------------+--
-- * Question 127572 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête imprimer les commandes en considérant que l'on veut celles de février 2020

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-----------------------+-------+
-- | annee | nomauteur             | total |
-- +-------+-----------------------+-------+
-- | etc...
-- = Reponse question 127572.



