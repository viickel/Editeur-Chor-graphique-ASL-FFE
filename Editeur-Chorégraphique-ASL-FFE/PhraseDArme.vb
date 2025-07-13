Public Class PhraseDArmes
    Public Property Numero As Integer
    Public Property DescriptionSection As String
    Public Property ListeActions As New List(Of Action)()


    Public Sub New()
        ' Constructeur par défaut
        Me.ListeActions = New List(Of Action)()
        ' Le numéro sera assigné dynamiquement, donc pas besoin de l'initialiser ici
        ' La description peut être vide par défaut
    End Sub
    Public Overrides Function ToString() As String
        ' Affiche le numéro et le début de la description
        Return $"Phrase {Numero}: {DescriptionSection.Substring(0, Math.Min(DescriptionSection.Length, 30))}..."
    End Function

End Class