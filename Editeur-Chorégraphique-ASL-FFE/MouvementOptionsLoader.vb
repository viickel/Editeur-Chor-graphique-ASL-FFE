Imports System.IO
Imports System.Collections.Generic
Imports System.Windows.Forms ' Pour Application.StartupPath
Imports System.Linq ' Ajout pour les méthodes LINQ comme Select

Public Class MouvementOptionsLoader

    Public Property Mains As New List(Of String)()
    Public Property Deplacements As New List(Of String)()
    Public Property Zones As New List(Of String)() ' <-- Nouvelle propriété pour les zones

    Private Const OptionsFileName As String = "OptionsMouvements.csv" ' Nom de ton fichier CSV
    Private Const CsvSeparator As Char = ";"c ' <-- Confirmation du séparateur point-virgule

    Public Sub New()
        LoadOptions()
    End Sub

    Private Sub LoadOptions()
        Mains.Clear()
        Deplacements.Clear()
        Zones.Clear() ' <-- Nettoyage de la nouvelle liste

        ' Chemin complet du fichier CSV (à côté de l'exécutable)
        Dim filePath As String = Path.Combine(Application.StartupPath, OptionsFileName)

        If File.Exists(filePath) Then
            Try
                ' Lire toutes les lignes du fichier
                Dim lines As String() = File.ReadAllLines(filePath, System.Text.Encoding.UTF8) ' Spécifier l'encodage pour la robustesse

                If lines.Length = 0 Then Throw New Exception("Le fichier CSV est vide.")

                ' Lire les en-têtes de la première ligne
                Dim headers As String() = lines(0).Split(CsvSeparator).Select(Function(h) h.Trim()).ToArray()

                ' Déterminer les indices des colonnes
                Dim mainIndex As Integer = Array.IndexOf(headers, "Main")
                Dim deplacementIndex As Integer = Array.IndexOf(headers, "Deplacement")
                Dim zoneIndex As Integer = Array.IndexOf(headers, "Zone") ' <-- Nouvel index pour la Zone

                ' Vérifier si les colonnes nécessaires existent
                If mainIndex = -1 OrElse deplacementIndex = -1 OrElse zoneIndex = -1 Then
                    Throw New Exception("Les en-têtes 'Main', 'Deplacement' ou 'Zone' sont manquants dans le fichier CSV.")
                End If

                ' Ignorer la première ligne (les en-têtes) et traiter les données
                For i As Integer = 1 To lines.Length - 1
                    Dim line As String = lines(i).Trim()
                    If Not String.IsNullOrEmpty(line) Then
                        Dim parts As String() = line.Split(CsvSeparator)

                        ' Extraire les valeurs et les ajouter aux listes si elles n'y sont pas déjà
                        If parts.Length > mainIndex Then
                            Dim value As String = parts(mainIndex).Trim()
                            If Not String.IsNullOrEmpty(value) AndAlso Not Mains.Contains(value) Then Mains.Add(value)
                        End If
                        If parts.Length > deplacementIndex Then
                            Dim value As String = parts(deplacementIndex).Trim()
                            If Not String.IsNullOrEmpty(value) AndAlso Not Deplacements.Contains(value) Then Deplacements.Add(value)
                        End If
                        If parts.Length > zoneIndex Then ' <-- Traitement de la nouvelle colonne Zone
                            Dim value As String = parts(zoneIndex).Trim()
                            If Not String.IsNullOrEmpty(value) AndAlso Not Zones.Contains(value) Then Zones.Add(value)
                        End If
                    End If
                Next
            Catch ex As Exception
                MessageBox.Show($"Erreur lors du chargement des options de mouvements : {ex.Message}{Environment.NewLine}Vérifiez le format du fichier '{OptionsFileName}'.", "Erreur de Chargement", MessageBoxButtons.OK, MessageBoxIcon.Error)
            End Try
        Else
            ' Si le fichier n'existe pas, créer un fichier par défaut
            MessageBox.Show($"Le fichier '{OptionsFileName}' est introuvable. Un fichier par défaut va être créé. Veuillez le modifier si nécessaire.", "Fichier Manquant", MessageBoxButtons.OK, MessageBoxIcon.Information)
            CreateDefaultOptionsFile(filePath)
            LoadOptions() ' Tenter de charger à nouveau après création
        End If
    End Sub

    Private Sub CreateDefaultOptionsFile(filePath As String)
        Dim defaultContent As New List(Of String)
        ' Mettre à jour les en-têtes et le contenu par défaut pour inclure "Zone"
        defaultContent.Add("Main;Deplacement;Zone") ' <-- Nouveaux en-têtes avec Zone
        defaultContent.Add("Aucun;Aucun;Aucune")     ' <-- Valeurs par défaut avec Zone
        defaultContent.Add("Poing;Pas simple;Tete")
        defaultContent.Add("Pied;Pas complexe;Tronc")
        defaultContent.Add("Garde;Esquive;Jambe")
        defaultContent.Add("Coup spécial;Saut;Bras")

        Try
            File.WriteAllLines(filePath, defaultContent, System.Text.Encoding.UTF8) ' Spécifier l'encodage
        Catch ex As Exception
            MessageBox.Show($"Erreur lors de la création du fichier par défaut '{OptionsFileName}' : {ex.Message}", "Erreur de Création", MessageBoxButtons.OK, MessageBoxIcon.Error)
        End Try
    End Sub

End Class