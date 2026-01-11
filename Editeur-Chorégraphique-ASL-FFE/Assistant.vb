Public Class Assistant
    Public Property Nom As String
    Public Property Prenom As String
    Public Property NumeroLicence As String

    Public Property Role As String ' Nouveau champ pour le rôle de l'assistant

    ' Constructeur par défaut (AJOUTER CELUI-CI)
    Public Sub New()
        ' Initialisation par défaut si nécessaire
        Me.Nom = ""
        Me.Prenom = ""
        Me.NumeroLicence = ""
        Me.Role = ""
    End Sub

    Public Sub New(nom As String, prenom As String, Optional licence As String = "", Optional Role As String = "")
        Me.Nom = nom
        Me.Prenom = prenom
        Me.NumeroLicence = licence
        Me.Role = Role
    End Sub

    Public Overrides Function ToString() As String
        Return $"{Prenom} {Nom}" & If(String.IsNullOrWhiteSpace(NumeroLicence), "", $" (Licence: {NumeroLicence})")
    End Function
End Class