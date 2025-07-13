' Mouvement.vb

Public Class Mouvement
    Public Property CombattantID As Integer ' ID du combattant qui effectue le mouvement
    Public Property MainDroite As String
    Public Property ZoneMainDroite As String
    Public Property CibleMainDroiteID As Integer ' (ID du combattant cible)
    Public Property MainGauche As String
    Public Property ZoneMainGauche As String
    Public Property CibleMainGaucheID As Integer ' (ID du combattant cible)
    Public Property Deplacement As String
    Public Property PouvoirForce As String
    Public Property Commentaire As String

    ' Constructeur paramétré mis à jour
    Public Sub New(combattantId As Integer, mainDroite As String, zoneMainDroite As String, cibleMainDroiteID As Integer,
                   mainGauche As String, zoneMainGauche As String, cibleMainGaucheID As Integer,
                   deplacement As String, pouvoirForce As String, commentaire As String)
        Me.CombattantID = combattantId
        Me.MainDroite = mainDroite
        Me.ZoneMainDroite = zoneMainDroite
        Me.CibleMainDroiteID = cibleMainDroiteID
        Me.MainGauche = mainGauche
        Me.ZoneMainGauche = zoneMainGauche
        Me.CibleMainGaucheID = cibleMainGaucheID
        Me.Deplacement = deplacement
        Me.PouvoirForce = pouvoirForce
        Me.Commentaire = commentaire
    End Sub

    ' Constructeur par défaut mis à jour
    Public Sub New()
        ' Initialiser toutes les propriétés pour éviter les valeurs nulles
        Me.CombattantID = 0
        Me.MainDroite = ""
        Me.ZoneMainDroite = ""
        Me.CibleMainDroiteID = 0
        Me.MainGauche = ""
        Me.ZoneMainGauche = ""
        Me.CibleMainGaucheID = 0
        Me.Deplacement = ""
        Me.PouvoirForce = ""
        Me.Commentaire = ""
    End Sub
End Class