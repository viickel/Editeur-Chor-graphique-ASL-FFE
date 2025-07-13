Imports System.Collections.Generic
Public Class Action
    Public Property NumeroAction As Integer

    Public Property Mouvements As New List(Of Mouvement)()


    ' Constructeur par défaut (nécessaire pour la désérialisation XML)
    Public Sub New()
        Me.NumeroAction = 0
    End Sub

    ' Pour un affichage plus lisible si besoin (ex: dans une ListBox de débogage)

End Class