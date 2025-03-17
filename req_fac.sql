SELECT nommag , numcom , datecom ,nomcli, prenomcli, adressecli, 
       codepostal, villecli, isbn, titre, qte, prixvente, 
       (prixvente * qte) AS Total
FROM COMMANDE
NATURAL JOIN DETAILCOMMANDE
NATURAL JOIN CLIENT
NATURAL JOIN LIVRE
NATURAL JOIN MAGASIN
WHERE MONTH(datecom) = ? AND YEAR(datecom) = ?
ORDER BY nommag, numcom, isbn