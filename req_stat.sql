SELECT 
    COUNT(DISTINCT numcom) AS NbVentes,
    SUM(prixvente * qte) AS CA
FROM COMMANDE
NATURAL JOIN DETAILCOMMANDE
GROUP BY MONTH(datecom)