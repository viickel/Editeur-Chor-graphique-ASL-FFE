Public Class Assistant
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

    Public Sub New(nom As String, prenom As String, Optional licence As String = "")
        Me.Nom = nom
        Me.Prenom = prenom
        Me.NumeroLicence = licence
    End Sub

    Public Overrides Function ToString() As String
        Return $"{Prenom} {Nom}" & If(String.IsNullOrWhiteSpace(NumeroLicence), "", $" (Licence: {NumeroLicence})")
    End Function
End Class