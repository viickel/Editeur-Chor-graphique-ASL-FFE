Imports System.Xml.Serialization

<Serializable()> _ ' Optionnel mais bonne pratique pour la sérialisation
<XmlInclude(GetType(Combattant))>
<XmlInclude(GetType(Assistant))>
<XmlInclude(GetType(PhraseDArmes))>
<XmlInclude(GetType(Action))>
<XmlInclude(GetType(Mouvement))>
Public Class ProjetChoregraphique
    Public Property Titre As String
    Public Property Intrigue As String
    Public Property Duree As String
    Public Property ListeCombattants As New List(Of Combattant)()
    Public Property ListeAssistants As New List(Of Assistant)
    Public Property ChoregraphieSections As New List(Of PhraseDArmes)



    Public Sub New()
        ' Initialise les listes pour éviter les NullReferenceException lors de la désérialisation
        ListeCombattants = New List(Of Combattant)()
        ListeAssistants = New List(Of Assistant)()
        ChoregraphieSections = New List(Of PhraseDArmes)()
        Me.Duree = "00m:00s" ' Initialiser avec une chaîne par défaut
    End Sub



End Class