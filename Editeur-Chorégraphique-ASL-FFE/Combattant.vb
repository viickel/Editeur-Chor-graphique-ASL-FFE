Public Class Combattant
    Public Property ID As Integer
    Public Property Nom As String
    Public Property Prenom As String
    Public Property NumeroLicence As String

    ' Constructeur par défaut (AJOUTER CELUI-CI)
    Public Sub New()
        ' Initialisation par défaut si nécessaire
        Me.Nom = ""
        Me.Prenom = ""
        Me.NumeroLicence = ""
    End Sub

    ' Constructeur (optionnel mais utile pour l'initialisation)
    Public Sub New(id As Integer, nom As String, prenom As String, licence As String)
        Me.ID = id
        Me.Nom = nom
        Me.Prenom = prenom
        Me.NumeroLicence = licence
    End Sub

    Public Overrides Function ToString() As String
        Return $"{Prenom} {Nom} (Licence: {NumeroLicence})"
    End Function
End Class