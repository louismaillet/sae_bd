-- Devoir 127
-- Nom: , Prenom: 

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
SELECT isbn, titre, nbpages, datepubli, prix 
FROM COMMANDE 
NATURAL JOIN DETAILCOMMANDE 
NATURAL JOIN LIVRE
WHERE datecom = str_to_date('01-12-2024','%d-%m-%Y');


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
SELECT distinct(idcli),nomcli, prenomcli, adressecli, codepostal, villecli
FROM CLIENT 
NATURAL JOIN COMMANDE 
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN LIVRE
NATURAL JOIN ECRIRE
NATURAL JOIN AUTEUR
WHERE YEAR(datecom) = 2021 and nomauteur='René Goscinny';


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
SELECT isbn, titre, nommag, qte
FROM LIVRE
NATURAL LEFT JOIN ECRIRE
NATURAL JOIN POSSEDER
NATURAL JOIN MAGASIN
WHERE idauteur IS NULL AND qte > 8;


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
SELECT idmag, nommag, COUNT(idcli) AS nbcli
FROM MAGASIN
LEFT JOIN CLIENT ON MAGASIN.villemag = CLIENT.villecli
GROUP BY idmag, nommag; 


-- +-----------------------+--
-- * Question 127291 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Pour chaque magasin, on veut la quantité de livres achetés le 15/09/2022 en affichant les 0.

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+------+
-- | nommag                  | nbex |
-- +-------------------------+------+
-- | etc...
-- = Reponse question 127291.
with Commandes_15092022 AS(
SELECT idmag, numcom
FROM COMMANDE
WHERE datecom = str_to_date('15-09-2022','%d-%m-%Y'))

SELECT nommag, IFNULL(SUM(qte), 0) AS nbex
FROM MAGASIN
NATURAL LEFT JOIN Commandes_15092022
NATURAL LEFT JOIN DETAILCOMMANDE
GROUP BY nommag;


-- +-----------------------+--
-- * Question 127314 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Instructions d'insertion dans la base de données

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +------------+
-- | insertions |
-- +------------+
-- | etc...
-- = Reponse question 127314.
INSERT LIVRE (isbn, titre, nbpages, datepubli, prix)
VALUES ('9782844273765', 'SQL pour les Nuls', 292, '2002-01-01', 33.5);
INSERT EDITEUR VALUES ('First Interactive',240);
INSERT EDITER VALUES ('9782844273765', 240);
INSERT AUTEUR VALUES ('OL246259A', 'Allen G. Taylor');
INSERT AUTEUR VALUES ('OL7670824A', 'Reinhard Engel');
INSERT ECRIRE VALUES ('9782844273765', 'OL246259A');
INSERT ECRIRE VALUES ('9782844273765', 'OL7670824A');
INSERT POSSEDER VALUES ('Loire et Livres', '9782844273765', 3);


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
-- = Reponse question 127370.
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
SELECT YEAR(datecom) as annee, 
    CASE 
        WHEN enligne = 'O' THEN 'en ligne' 
        ELSE 'en magasin' 
    END as typevente,
    sum(prixvente*qte) as montant
FROM COMMANDE
NATURAL JOIN DETAILCOMMANDE
GROUP BY YEAR(datecom), typevente;


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
select nomedit as Editeur, count(distinct idauteur) as nbauteurs
from EDITEUR
natural join EDITER
natural join LIVRE
natural join ECRIRE
group by nomedit
ORDER BY nbauteurs DESC
LIMIT 10;


-- +-----------------------+--
-- * Question 127516 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 6 Qté de livres de R. Goscinny achetés en fonction de l'orgine des clients

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------+-----+
-- | ville       | qte |
-- +-------------+-----+
-- | etc...
-- = Reponse question 127516.
SELECT villecli AS ville, SUM(qte) AS qte
FROM CLIENT
NATURAL JOIN COMMANDE
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN LIVRE
NATURAL JOIN ECRIRE
NATURAL JOIN AUTEUR
WHERE nomauteur = 'René Goscinny'
GROUP BY villecli;


-- +-----------------------+--
-- * Question 127527 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Graphique 7 Valeur du stock par magasin
-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------------------------+---------+
-- | Magasin                 | total   |
-- +-------------------------+---------+
-- | etc...
-- = Reponse question 127527.
select nommag as Magasin, sum(qte*prix) as total
from MAGASIN
natural join POSSEDER
natural join LIVRE
group by nommag;


-- +-----------------------+--
-- * Question 127538 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
-- Requête Graphique 8 Statistiques sur l'évolution du chiffre d'affaire total par client 
-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+---------+---------+---------+
-- | annee | maximum | minimum | moyenne |
-- +-------+---------+---------+---------+
-- | etc...
-- = Reponse question 127538.
with MoyenneClient(idcli,annee,CA) as (select idcli,YEAR(datecom) annee,SUM(qte*prixvente) CA from CLIENT
                       natural join COMMANDE natural join DETAILCOMMANDE
                       group by idcli,YEAR(datecom))
select annee,MAX(CA) maximum,MIN(CA) minimum,AVG(CA) moyenne from MoyenneClient
group by annee;


-- +-----------------------+--
-- * Question 127572 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête Palmarès

-- Voici le début de ce que vous devez obtenir.
-- ATTENTION à l'ordre des colonnes et leur nom!
-- +-------+-----------------------+-------+
-- | annee | nomauteur             | total |
-- +-------+-----------------------+-------+
-- | etc...
-- = Reponse question 127572.
WITH AuteurVentesAnnuel AS (
    SELECT YEAR(datecom) AS annee, idauteur, SUM(qte) AS total
    FROM ECRIRE
    NATURAL JOIN DETAILCOMMANDE
    NATURAL JOIN LIVRE
    NATURAL JOIN COMMANDE
    WHERE YEAR(datecom) < 2025
    GROUP BY YEAR(datecom), idauteur
    order by total DESC
)
SELECT annee, nomauteur, max(total) as total
FROM AUTEUR NATURAL RIGHT JOIN AuteurVentesAnnuel
Group BY annee;

-- +-----------------------+--
-- * Question 127574 : 2pts --
-- +-----------------------+--
-- Ecrire une requête qui renvoie les informations suivantes:
--  Requête imprimer les commandes en considérant que l'on veut celles de février 2020
-- = Reponse question 127574
SELECT nommag , numcom , datecom ,nomcli, prenomcli, adressecli, 
       codepostal, villecli, isbn, titre, qte, prixvente, 
       (prixvente * qte) AS Total
FROM COMMANDE
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN CLIENT
NATURAL JOIN LIVRE
NATURAL JOIN MAGASIN
WHERE MONTH(datecom) = 2 AND YEAR(datecom) = 2020
ORDER BY nommag, numcom, isbn;
