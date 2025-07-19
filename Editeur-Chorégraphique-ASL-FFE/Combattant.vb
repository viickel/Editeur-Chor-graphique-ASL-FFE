Imports System.Xml.Serialization ' Assurez-vous que cette importation est en haut si vous utilisez des attributs de sérialisation XML

<Serializable()>
Public Class Combattant
    Public Property ID As Integer
    Public Property Nom As String
    Public Property Prenom As String
    Public Property NumeroLicence As String
    Public Property Capitaine As Boolean

    ' Constructeur par défaut (AJOUTER CELUI-CI)
    Public Sub New()
        ' Initialisation par défaut si nécessaire
        Me.Nom = ""
        Me.Prenom = ""
        Me.NumeroLicence = ""
        Me.Capitaine = False
    End Sub

    ' Constructeur (optionnel mais utile pour l'initialisation)
    Public Sub New(id As Integer, nom As String, prenom As String, licence As String, capitaine As Boolean)
        Me.ID = id
        Me.Nom = nom
        Me.Prenom = prenom
        Me.NumeroLicence = licence
        Me.Capitaine = capitaine
    End Sub

    Public Overrides Function ToString() As String
        Return $"{Prenom} {Nom} (Licence: {NumeroLicence})"
    End Function
End Class