Imports System.Xml.Serialization

<Serializable()>
<XmlInclude(GetType(Combattant))>
<XmlInclude(GetType(Assistant))>
<XmlInclude(GetType(PhraseDArmes))>
<XmlInclude(GetType(Action))>
<XmlInclude(GetType(Mouvement))>
Public Class ProjetChoregraphique
    Public Property Titre As String
    Public Property Intrigue As String
    Public Property Duree As String
    Public Property NomDuClub As String
    Public Property ListeCombattants As New List(Of Combattant)()
    Public Property ListeAssistants As New List(Of Assistant)
    Public Property ChoregraphieSections As New List(Of PhraseDArmes)

    Public Property Categorie As String ' Pour stocker "Duel", "Bataille", "Ensemble"
    Public Property IsMouvementEnsemble As Boolean ' Pour stocker l'état de la case à cocher




    Public Sub New()
        ' Initialise les listes pour éviter les NullReferenceException lors de la désérialisation
        ListeCombattants = New List(Of Combattant)()
        ListeAssistants = New List(Of Assistant)()
        ChoregraphieSections = New List(Of PhraseDArmes)()
        Me.Duree = "00m:00s" ' Initialiser avec une chaîne par défaut
        Me.NomDuClub = ""
    End Sub



End Class