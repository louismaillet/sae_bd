WITH CA_ParCommande AS (
    SELECT 
        numcom AS Vente, 
        SUM(prixvente * qte) AS CA
    FROM DETAILCOMMANDE
    NATURAL JOIN COMMANDE
    GROUP BY numcom
),
CA_Cumulé AS (
    SELECT 
        C1.Vente, 
        COALESCE(SUM(C2.CA), 0) AS ChiffreAffaireCumulé
    FROM CA_ParCommande C1
    LEFT JOIN CA_ParCommande C2 ON C2.Vente <= C1.Vente
    GROUP BY C1.Vente
)
SELECT *
FROM CA_Cumulé
ORDER BY Vente ;