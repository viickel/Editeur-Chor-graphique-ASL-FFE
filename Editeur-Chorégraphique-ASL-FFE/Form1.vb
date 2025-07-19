Imports System.IO
Imports System.Xml.Serialization
Imports System.Windows.Forms ' Assure-toi que cette importation est présente pour les contrôles UI
Imports System.Globalization ' Pour TimeSpan.TryParseExact
Imports iTextSharp.text ' Pour les classes de base (Document, Paragraph, etc.)
Imports iTextSharp.text.pdf
Imports System.Drawing.Design ' Pour PdfWriter, PdfPTable, etc.

Public Class Form1

    ' Variable pour stocker le projet de chorégraphie actuellement chargé/créé
    Private currentProjet As ProjetChoregraphique

    ' Variable pour stocker le chemin du fichier du projet actuel
    Private currentFilePath As String = String.Empty

    ' Variable pour savoir si des modifications non enregistrées existent
    Private isDirty As Boolean = False
    Private bsCombattantsDisplay As New BindingSource()
    Private bsAssistantsDisplay As New BindingSource()

    ' Nous n'utiliserons pas de BindingSource directement avec RichTextBox,
    ' car RichTextBox est pour du texte formaté, pas une liste d'objets.
    ' La gestion des combattants et assistants sera manuelle pour l'instant
    ' jusqu'à ce que nous implémentions des dialogues d'édition dédiés.

    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load

        ' Lier la ListBox des combattants
        lstCombattants.DataSource = bsCombattantsDisplay
        lstCombattants.DisplayMember = "ToString" ' Utilise la fonction ToString() de Combattant

        ' Lier la ListBox des assistants
        lstAssistantsDisplay.DataSource = bsAssistantsDisplay
        lstAssistantsDisplay.DisplayMember = "ToString" ' Utilise la fonction ToString() de Assistant

        NewProject()

        DetermineAndSetCategorie() ' Détermine la catégorie au chargement/nouveau projet




    End Sub

    Private Sub NewProject()
        currentProjet = New ProjetChoregraphique()
        currentFilePath = String.Empty
        isDirty = False
        UpdateFormTitle()

        ' Réinitialiser tous les contrôles du formulaire avec les données du nouveau projet (vides)
        DisplayCurrentProjectData()
    End Sub

    ' Méthode pour mettre à jour le titre du formulaire
    Private Sub UpdateFormTitle()
        Dim title As String = "Editeur Chorégraphique"
        If Not String.IsNullOrEmpty(currentProjet.Titre) Then
            title &= $" - {currentProjet.Titre}"
        ElseIf Not String.IsNullOrEmpty(currentFilePath) Then
            title &= $" - {Path.GetFileNameWithoutExtension(currentFilePath)}"
        End If

        If isDirty Then
            title &= " *" ' Indique des modifications non enregistrées
        End If
        Me.Text = title
    End Sub

    ' Méthode à appeler chaque fois qu'une modification est faite sur les données du projet
    Public Sub MarkAsDirty()
        isDirty = True
        UpdateFormTitle()
    End Sub

    ' Gérer la fermeture du formulaire pour demander d'enregistrer
    Private Sub Form1_FormClosing(sender As Object, e As FormClosingEventArgs) Handles Me.FormClosing
        If isDirty Then
            Dim result As DialogResult = MessageBox.Show("Des modifications non enregistrées seront perdues. Voulez-vous enregistrer avant de quitter ?", "Enregistrer le projet", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Warning)
            If result = DialogResult.Yes Then
                If Not SaveProject() Then
                    e.Cancel = True ' Annule la fermeture si l'enregistrement échoue ou est annulé
                End If
            ElseIf result = DialogResult.Cancel Then
                e.Cancel = True ' Annule la fermeture
            End If
        End If
    End Sub

    ' Méthode générique pour sauvegarder le projet
    Private Function SaveProject(Optional saveAs As Boolean = False) As Boolean
        ' Avant de sauvegarder, assure-toi que les données de l'UI sont dans l'objet currentProjet
        UpdateCurrentProjectDataFromUI()

        If String.IsNullOrEmpty(currentFilePath) OrElse saveAs Then
            Using sfd As New SaveFileDialog()
                sfd.Filter = "Fichiers Chorégraphie (*.chore)|*.chore|Tous les fichiers (*.*)|*.*"
                sfd.Title = "Enregistrer le projet de chorégraphie"
                sfd.DefaultExt = "chore"
                sfd.FileName = If(Not String.IsNullOrEmpty(currentProjet.Titre), currentProjet.Titre, "NouveauProjet")

                If sfd.ShowDialog() = DialogResult.OK Then
                    currentFilePath = sfd.FileName
                Else
                    Return False ' L'utilisateur a annulé la boîte de dialogue
                End If
            End Using
        End If

        Try
            Using writer As New StreamWriter(currentFilePath)
                Dim serializer As New XmlSerializer(GetType(ProjetChoregraphique))
                serializer.Serialize(writer, currentProjet)
            End Using
            isDirty = False
            UpdateFormTitle()
            MessageBox.Show("Projet enregistré avec succès !", "Enregistrement", MessageBoxButtons.OK, MessageBoxIcon.Information)
            Return True
        Catch ex As Exception
            MessageBox.Show($"Erreur lors de l'enregistrement du projet : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
            Return False
        End Try
    End Function

    ' Méthode pour charger un projet
    Private Function LoadProject() As Boolean
        Using ofd As New OpenFileDialog()
            ofd.Filter = "Fichiers Chorégraphie (*.chore)|*.chore|Tous les fichiers (*.*)|*.*"
            ofd.Title = "Ouvrir un projet de chorégraphie"
            ofd.DefaultExt = "chore"

            If ofd.ShowDialog() = DialogResult.OK Then
                If isDirty Then
                    Dim result As DialogResult = MessageBox.Show("Des modifications non enregistrées seront perdues. Voulez-vous enregistrer avant d'ouvrir un nouveau projet ?", "Enregistrer le projet", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Warning)
                    If result = DialogResult.Yes Then
                        If Not SaveProject() Then
                            Return False ' Annule l'ouverture si l'enregistrement échoue ou est annulé
                        End If
                    ElseIf result = DialogResult.Cancel Then
                        Return False ' Annule l'ouverture
                    End If
                End If

                Try
                    Using reader As New StreamReader(ofd.FileName)
                        Dim serializer As New XmlSerializer(GetType(ProjetChoregraphique))
                        currentProjet = CType(serializer.Deserialize(reader), ProjetChoregraphique)
                    End Using
                    currentFilePath = ofd.FileName
                    isDirty = False
                    UpdateFormTitle()
                    MessageBox.Show("Projet chargé avec succès !", "Ouverture", MessageBoxButtons.OK, MessageBoxIcon.Information)

                    ' Mettre à jour tous les contrôles du formulaire avec les données du projet chargé
                    DisplayCurrentProjectData()

                    Return True
                Catch ex As Exception
                    MessageBox.Show($"Erreur lors du chargement du projet : {ex.Message}", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Error)
                    Return False
                End Try
            Else
                Return False ' L'utilisateur a annulé la boîte de dialogue
            End If
        End Using
    End Function

    ' --- Gestionnaires d'événements des boutons ---
    Private Sub Bt_Save_Click(sender As Object, e As EventArgs) Handles Bt_Save.Click
        SaveProject()
    End Sub

    Private Sub Bt_Save_As_Click(sender As Object, e As EventArgs) Handles Bt_Save_As.Click
        SaveProject(saveAs:=True)
    End Sub

    Private Sub Bt_Open_Click(sender As Object, e As EventArgs) Handles Bt_Open.Click
        LoadProject()
    End Sub

    Private Sub Bt_New_Click(sender As Object, e As EventArgs) Handles Bt_New.Click
        If isDirty Then
            Dim result As DialogResult = MessageBox.Show("Des modifications non enregistrées seront perdues. Voulez-vous enregistrer avant de créer un nouveau projet ?", "Nouveau Projet", MessageBoxButtons.YesNoCancel, MessageBoxIcon.Warning)
            If result = DialogResult.Yes Then
                If Not SaveProject() Then
                    Return ' Annule le nouveau projet si l'enregistrement échoue ou est annulé
                End If
            ElseIf result = DialogResult.Cancel Then
                Return ' Annule le nouveau projet
            End If
        End If
        NewProject()
    End Sub

    ' ====================================================================================
    ' MÉTHODES POUR GÉRER L'AFFICHAGE ET LA MISE À JOUR DES DONNÉES DE L'UI
    ' ====================================================================================

    ' Méthode pour afficher les données de currentProjet dans les contrôles de l'UI
    Private Sub DisplayCurrentProjectData()
        ' Section "Titre"
        Title_Box.Text = currentProjet.Titre

        ' Section "Intrigue"
        Rich_Intrigue.Text = currentProjet.Intrigue

        ' Section "Durée" (TextBox1 est le nom du contrôle pour la durée)
        TextBox1.Text = currentProjet.Duree

        'section Nom du club
        txtNomClub.Text = currentProjet.NomDuClub

        ' Section "Combattants" (avec la nouvelle ListBox)
        bsCombattantsDisplay.DataSource = currentProjet.ListeCombattants
        bsCombattantsDisplay.ResetBindings(False) ' Rafraîchit l'affichage

        ' Section "Assistants Plateau" (avec la nouvelle ListBox)
        bsAssistantsDisplay.DataSource = currentProjet.ListeAssistants
        bsAssistantsDisplay.ResetBindings(False) ' Rafraîchit l'affichage

        chkMouvementEnsemble.Checked = currentProjet.IsMouvementEnsemble ' Afficher l'état de la checkbox
        lblCategorie.Text = $"Catégorie : {currentProjet.Categorie}" ' Afficher la catégorie calculée 


        ' Pour les boutons d'édition des combattants/assistants, ils n'affichent pas de données,
        ' ils ouvriront des formulaires de gestion dédiés plus tard.
    End Sub

    ' Méthode pour prendre les données de l'UI et les mettre dans l'objet currentProjet
    Private Sub UpdateCurrentProjectDataFromUI()
        currentProjet.Titre = Title_Box.Text
        currentProjet.Intrigue = Rich_Intrigue.Text
        currentProjet.Duree = TextBox1.Text
        currentProjet.NomDuClub = txtNomClub.Text
        currentProjet.IsMouvementEnsemble = chkMouvementEnsemble.Checked
        ' Appel de la méthode pour déterminer et stocker la catégorie
        DetermineAndSetCategorie()


        ' Important : Pour les RichTextBox des combattants et assistants,
        ' nous ne pouvons pas les "lire" facilement pour recréer la liste d'objets Combattant/Assistant.
        ' Ces RichTextBox sont pour l'affichage uniquement dans cette version simplifiée.
        ' La gestion réelle des listes de combattants/assistants se fera via les boutons "Editer..."
        ' qui ouvriront de nouveaux formulaires dédiés à l'ajout/suppression/modification.
        ' Pour l'instant, currentProjet.ListeCombattants et currentProjet.ListeAssistants
        ' ne seront pas modifiés par la saisie directe dans ces RichTextBox.
        ' C'est pourquoi j'avais suggéré des ListBox plus tôt, car elles sont faites pour ça.
        ' On verra les dialogues d'édition plus tard.
    End Sub


    Private Sub DetermineAndSetCategorie()
        If currentProjet.ListeCombattants.Count > 2 Then
            chkMouvementEnsemble.Visible = True ' Rendre la CheckBox visible

        Else
            chkMouvementEnsemble.Visible = False

        End If



        If currentProjet.ListeCombattants.Count = 1 Then
            currentProjet.Categorie = "Kata"

        ElseIf currentProjet.ListeCombattants.Count = 2 Then
            currentProjet.Categorie = "Duel"

        ElseIf currentProjet.ListeCombattants.Count > 2 And Not currentProjet.IsMouvementEnsemble Then
            currentProjet.Categorie = "Bataille"

        ElseIf currentProjet.ListeCombattants.Count > 2 And currentProjet.IsMouvementEnsemble Then
            currentProjet.Categorie = "Ensemble"
        Else
            currentProjet.Categorie = "Non définie (Ajoutez des combattants)" ' Ou toute autre valeur par défaut
        End If

        ' Mettre à jour l'affichage de la catégorie sur le formulaire principal
        If lblCategorie IsNot Nothing AndAlso Not lblCategorie.IsDisposed Then
            lblCategorie.Text = $"Catégorie : {currentProjet.Categorie}"
        End If

        MarkAsDirty() ' La catégorie a changé, donc le projet est "dirty"
    End Sub


    ' ====================================================================================
    ' GESTION DES MODIFICATIONS DE L'UI POUR MARQUER LE PROJET COMME "Sale" (Dirty)
    ' ====================================================================================

    ' Marquer le projet comme modifié lorsque le titre change
    Private Sub Title_Box_TextChanged(sender As Object, e As EventArgs) Handles Title_Box.TextChanged
        MarkAsDirty()
    End Sub

    ' Marquer le projet comme modifié lorsque l'intrigue change
    Private Sub Rich_Intrigue_TextChanged(sender As Object, e As EventArgs) Handles Rich_Intrigue.TextChanged
        MarkAsDirty()
    End Sub

    ' Marquer le projet comme modifié lorsque la durée change
    Private Sub TextBox1_TextChanged(sender As Object, e As EventArgs) Handles TextBox1.TextChanged
        MarkAsDirty()
    End Sub

    'marquer le projet comme modifié lorsque le nom du club change
    Private Sub txtNomClub_TextChanged(sender As Object, e As EventArgs) Handles txtNomClub.TextChanged
        MarkAsDirty()
    End Sub

    ' TODO: Les RichTextBox pour Chorégraphe et Assistant n'ont pas de gestionnaire
    ' MarkAsDirty car ils ne seront pas la source principale des données pour l'enregistrement.
    ' Les données des listes de combattants et assistants seront gérées via des popups d'édition
    ' qui, eux, appelleront MarkAsDirty.



    Private Sub Bt_Edit_choregraphe_Click(sender As Object, e As EventArgs) Handles Bt_Edit_choregraphe.Click
        ' Créer une instance du nouveau formulaire d'édition des combattants
        Using formCombattants As New FormEditCombattants()
            ' Passer la liste actuelle des combattants du projet au formulaire d'édition
            formCombattants.ListeCombattantsDuProjet = currentProjet.ListeCombattants

            ' Afficher le formulaire en tant que boîte de dialogue modale
            Dim result As DialogResult = formCombattants.ShowDialog(Me) ' 'Me' définit Form1 comme propriétaire

            ' Si l'utilisateur a cliqué sur "Valider et Fermer" (DialogResult.OK)
            If result = DialogResult.OK Then
                ' La liste ListeCombattantsDuProjet dans formCombattants a déjà été modifiée en direct.
                ' Nous n'avons pas besoin de la réaffecter. Il suffit de rafraîchir l'affichage de Form1.
                ' Et marquer le projet comme "sale" si des changements ont eu lieu.

                ' La méthode DisplayCurrentProjectData rafraîchira le RichTextBox_Choregraphe
                DisplayCurrentProjectData()

                DetermineAndSetCategorie()
                MarkAsDirty() ' Indique qu'il y a des modifications à sauvegarder
            ElseIf result = DialogResult.Cancel Then
                ' Si l'utilisateur a annulé, il faut restaurer la liste originale si elle a été modifiée en direct.
                ' Dans cette implémentation simple, les modifications sont appliquées directement.
                ' Pour un "vrai" annuler, il faudrait cloner la liste avant de la passer au dialogue
                ' et ne la réaffecter que si DialogResult.OK.
                ' Pour l'instant, on assume que "Annuler" signifie simplement ne pas marquer comme dirty
                ' si aucune modification n'a été faite.
                ' Puisque les modifications sont directes, la seule chose à faire est de ne PAS appeler MarkAsDirty() ici.
                ' Cependant, si MarkAsDirtyInMainForm() a été appelée pendant l'édition, le Form1 est déjà marqué.
                ' Ce n'est pas idéal mais fonctionne pour l'exemple. Une meilleure gestion serait un clone.
            End If
        End Using
    End Sub

    Private Sub Bt_Edit_assistant_Click(sender As Object, e As EventArgs) Handles Bt_Edit_assistant.Click
        ' Créer une instance du nouveau formulaire d'édition des assistants
        Using formAssistants As New FormEditAssistants()
            ' Passer la liste actuelle des assistants du projet au formulaire d'édition
            formAssistants.ListeAssistantsDuProjet = currentProjet.ListeAssistants

            ' Afficher le formulaire en tant que boîte de dialogue modale
            Dim result As DialogResult = formAssistants.ShowDialog(Me) ' 'Me' définit Form1 comme propriétaire

            ' Si l'utilisateur a cliqué sur "Valider et Fermer" (DialogResult.OK)
            If result = DialogResult.OK Then
                ' La liste ListeAssistantsDuProjet dans formAssistants a déjà été modifiée en direct.
                ' Nous n'avons pas besoin de la réaffecter. Il suffit de rafraîchir l'affichage de Form1.
                DisplayCurrentProjectData()
                MarkAsDirty() ' Indique qu'il y a des modifications à sauvegarder
            ElseIf result = DialogResult.Cancel Then
                ' Gérer l'annulation si nécessaire (voir les notes précédentes sur le clonage)
            End If
        End Using
    End Sub

    Private Sub Bt_Editer_Chore_Click(sender As Object, e As EventArgs) Handles Bt_Editer_Chore.Click

        Using formPhraseDArmes As New FormEditPhraseDArmes()
            ' Passe la liste des phrases d'armes du projet au formulaire d'édition
            formPhraseDArmes.ListePhraseDArmesDuProjet = currentProjet.ChoregraphieSections

            ' >>> AJOUTEZ CETTE LIGNE <<<
            ' Passe l'objet ProjetChoregraphique complet au formulaire d'édition des phrases
            formPhraseDArmes.CurrentProjet = currentProjet

            ' Affiche le formulaire en tant que boîte de dialogue modale
            Dim result As DialogResult = formPhraseDArmes.ShowDialog(Me) ' 'Me' définit Form1 comme propriétaire

            ' Si l'utilisateur a cliqué sur "Valider et Fermer" (DialogResult.OK)
            If result = DialogResult.OK Then
                ' La liste ListePhraseDArmesDuProjet dans formPhraseDArmes a déjà été modifiée en direct.
                ' Il suffit de rafraîchir l'affichage de Form1.
                DisplayCurrentProjectData()
                MarkAsDirty() ' Indique qu'il y a des modifications à sauvegarder
            ElseIf result = DialogResult.Cancel Then
                ' L'utilisateur a annulé, aucune action particulière à faire car la liste n'a pas été modifiée.
            End If
        End Using
    End Sub




    ' Assure-toi que tu as accès à l'objet Projet global ici.
    ' Je suppose que tu as une propriété ou une variable de champ pour ton projet actuel.

    Private Sub btnGeneratePdf_Click(sender As Object, e As EventArgs) Handles btnGeneratePdf.Click
        If currentProjet Is Nothing Then
            MessageBox.Show("Aucun projet n'est chargé à éditer.", "Erreur", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        ' Assurez-vous que la ComboBox existe et a des éléments sélectionnés
        If cboPageSize.SelectedItem Is Nothing Then
            MessageBox.Show("Veuillez sélectionner un format de page (A4/A3, Portrait/Paysage).", "Format de page manquant", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        ' Définir le chemin de sauvegarde du PDF
        Dim saveFileDialog As New SaveFileDialog()
        saveFileDialog.Filter = "Fichiers PDF (*.pdf)|*.pdf"
        saveFileDialog.Title = "Enregistrer le Projet PDF"
        saveFileDialog.FileName = $"Projet Chorégraphique_{currentProjet.Titre.Replace(" ", "_")}.pdf" ' Nom de fichier par défaut

        If saveFileDialog.ShowDialog() = DialogResult.OK Then
            Dim filePath As String = saveFileDialog.FileName

            Try
                ' *** DÉBUT DES NOUVELLES MODIFICATIONS ***

                ' Récupérer la taille de page et l'orientation choisie par l'utilisateur
                Dim pageSize As iTextSharp.text.Rectangle
                Dim selectedPageSize As String = cboPageSize.SelectedItem.ToString() ' Récupère le texte sélectionné

                Select Case selectedPageSize
                    Case "A4 Portrait"
                        pageSize = iTextSharp.text.PageSize.A4
                    Case "A4 Paysage"
                        pageSize = iTextSharp.text.PageSize.A4.Rotate()
                    Case "A3 Portrait"
                        pageSize = iTextSharp.text.PageSize.A3
                    Case "A3 Paysage"
                        pageSize = iTextSharp.text.PageSize.A3.Rotate()
                    Case Else ' Fallback par sécurité, si rien n'est sélectionné ou valeur inattendue
                        pageSize = iTextSharp.text.PageSize.A4.Rotate() ' Défaut à A4 Paysage
                        MessageBox.Show("Format de page inconnu sélectionné, utilisant A4 Paysage par défaut.", "Avertissement", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                End Select

                ' 1. Créer un nouveau document PDF
                ' Document(taille_de_page_choisie, left, right, top, bottom) margins
                ' La marge du bas à 50 est bonne pour laisser de la place au numéro de page
                Dim doc As New Document(pageSize, 30, 30, 30, 50)

                ' *** FIN DES NOUVELLES MODIFICATIONS ***

                ' 2. Créer un PdfWriter pour écrire le document dans un fichier
                Dim writer As PdfWriter = PdfWriter.GetInstance(doc, New FileStream(filePath, FileMode.Create))

                ' Enregistrer l'événement de page pour la numérotation
                Dim pageEvent As New PageNumberEventHelper()
                writer.PageEvent = pageEvent

                ' 3. Ouvrir le document pour y ajouter du contenu
                doc.Open()

                ' --- Styles (Polices) ---
                Dim fontTitle As Font = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 24, BaseColor.BLACK)
                Dim fontSubtitle As Font = FontFactory.GetFont(FontFactory.HELVETICA_BOLD, 16, BaseColor.DARK_GRAY)
                Dim fontNormal As Font = FontFactory.GetFont(FontFactory.HELVETICA, 12, BaseColor.BLACK)
                Dim fontSmall As Font = FontFactory.GetFont(FontFactory.HELVETICA, 10, BaseColor.GRAY)
                Dim fontTiny As Font = FontFactory.GetFont(FontFactory.HELVETICA, 8, BaseColor.BLACK) ' Police pour les données de tableau
                Dim fontCapitaineBold As Font = New Font(fontNormal.Family, fontNormal.Size, Font.Bold, fontNormal.Color)


                ' --- Ajouter le titre, l'intrigue et le temps ---
                doc.Add(New Paragraph("Titre : " & currentProjet.Titre, fontTitle))
                doc.Add(New Paragraph("Intrigue : " & currentProjet.Intrigue, fontSubtitle))

                ' *** DÉBUT DE LA CORRECTION POUR LA DURÉE (STRING) ***
                Dim tempsFormatted As String = ""
                If Not String.IsNullOrEmpty(currentProjet.Duree) Then
                    tempsFormatted = $"Durée : {currentProjet.Duree}"
                Else
                    tempsFormatted = "Durée : Non spécifiée."
                End If
                doc.Add(New Paragraph(tempsFormatted, fontSubtitle)) ' Vous avez changé fontNormal en fontSubtitle ici, je le garde comme vous l'avez fait.
                doc.Add(New Paragraph(Environment.NewLine)) ' Ligne vide après le temps

                If Not currentProjet.NomDuClub Is Nothing Then
                    doc.Add(New Paragraph("Nom du Club : " & currentProjet.NomDuClub, fontSubtitle))
                End If

                doc.Add(New Paragraph("Catégorie : " & currentProjet.Categorie, fontSubtitle))
                doc.Add(New Paragraph(Environment.NewLine)) ' Ligne vide après le temps



                ' *** FIN DE LA CORRECTION POUR LA DURÉE (STRING) ***

                ' --- Tableau Combattants / Assistants ---
                doc.Add(New Paragraph("Participants :", fontSubtitle))
                Dim tableParticipants As New PdfPTable(2) ' 2 colonnes
                tableParticipants.WidthPercentage = 100 ' Prend 100% de la largeur disponible
                tableParticipants.SetWidths(New Single() {1, 1}) ' Largeur relative des colonnes

                doc.Add(New Paragraph(Environment.NewLine)) ' Ligne vide - (Note: cette ligne vide avant les en-têtes du tableau pourrait être déplacée après tableParticipants.AddCell(tableParticipants))

                ' En-têtes du tableau
                tableParticipants.AddCell(New PdfPCell(New Phrase("Combattant", fontNormal)))
                tableParticipants.AddCell(New PdfPCell(New Phrase("Assistant", fontNormal)))

                ' Contenu du tableau
                Dim maxParticipants As Integer = Math.Max(currentProjet.ListeCombattants.Count, currentProjet.ListeAssistants.Count)
                If maxParticipants = 0 Then maxParticipants = 1 ' Au moins une ligne pour afficher vide

                For i As Integer = 0 To maxParticipants - 1
                    Dim combattantCell As New PdfPCell()
                    If i < currentProjet.ListeCombattants.Count Then
                        Dim c As Combattant = currentProjet.ListeCombattants(i)
                        If c.Capitaine Then
                            combattantCell.AddElement(New Phrase($"Capitaine {c.Nom} {c.Prenom} (ID: {c.ID}) (Licence: {c.NumeroLicence})", fontCapitaineBold))
                        Else
                            combattantCell.AddElement(New Phrase($"{c.Nom} {c.Prenom} (ID: {c.ID}) (Licence: {c.NumeroLicence})", fontNormal))

                        End If
                    Else
                        combattantCell.AddElement(New Phrase("")) ' Cellule vide si pas de combattant
                    End If
                    tableParticipants.AddCell(combattantCell)

                    Dim assistantCell As New PdfPCell()
                    If i < currentProjet.ListeAssistants.Count Then
                        Dim a As Assistant = currentProjet.ListeAssistants(i)
                        assistantCell.AddElement(New Phrase($"{a.Nom} {a.Prenom} (Licence: {a.NumeroLicence})", fontNormal))
                    Else
                        assistantCell.AddElement(New Phrase("")) ' Cellule vide si pas d'assistant
                    End If
                    tableParticipants.AddCell(assistantCell)
                Next
                doc.Add(tableParticipants)
                doc.Add(New Paragraph(Environment.NewLine)) ' Ligne vide
                doc.NewPage() ' Nouvelle page après le tableau des participants

                ' --- Phrases d'armes et leurs actions (Structure de tableau inversée) ---
                Dim firstPhrase As Boolean = True
                For Each phrase As PhraseDArmes In currentProjet.ChoregraphieSections.OrderBy(Function(p) p.Numero) ' S'assurer de l'ordre
                    ' *** AJOUT : Saut de page pour chaque nouvelle phrase d'armes (sauf la toute première) ***
                    If Not firstPhrase Then
                        doc.NewPage()
                    Else
                        firstPhrase = False
                    End If

                    ' Ajouter le titre de la phrase
                    doc.Add(New Paragraph($"Phrase {phrase.Numero} : {phrase.DescriptionSection}", fontSubtitle))
                    doc.Add(New Paragraph(Environment.NewLine))

                    ' Déterminer le nombre d'actions dans cette phrase
                    Dim numActions As Integer = phrase.ListeActions.Count
                    If numActions = 0 Then
                        doc.Add(New Paragraph("Aucune action définie pour cette phrase.", fontSmall))
                        doc.Add(New Paragraph(Environment.NewLine))
                        Continue For ' Passer à la phrase suivante
                    End If

                    ' Le nombre de colonnes du tableau sera (1 fixe pour l'entête) + (nombre d'actions)
                    Dim totalColumnsTableActions As Integer = 1 + numActions
                    Dim tableActionsInverted As New PdfPTable(totalColumnsTableActions)
                    tableActionsInverted.WidthPercentage = 100

                    ' Définir les largeurs des colonnes (vous devrez ajuster ces valeurs)
                    Dim widths As New List(Of Single)()
                    widths.Add(2.0F) ' Largeur plus grande pour la colonne d'entête (ex: "Main D", "Zone MD")

                    ' Largeur pour chaque colonne d'action
                    Dim actionColumnWidth As Single = 1.0F ' Largeur par défaut pour une colonne d'action
                    If numActions > 10 Then ' Réduire la largeur si beaucoup d'actions
                        actionColumnWidth = 0.8F
                    ElseIf numActions > 20 Then ' Encore plus petite si très très nombreuses
                        actionColumnWidth = 0.5F
                    End If

                    For i As Integer = 0 To numActions - 1
                        widths.Add(actionColumnWidth)
                    Next
                    If widths.Count = totalColumnsTableActions Then
                        tableActionsInverted.SetWidths(widths.ToArray())
                    End If

                    ' --- Ligne d'en-tête du tableau (Numéros d'Action) ---
                    tableActionsInverted.AddCell(New PdfPCell(New Phrase("N° Action", fontSmall))) ' Entête fixe pour les numéros

                    Dim orderedActions As List(Of Action) = phrase.ListeActions.OrderBy(Function(a) a.NumeroAction).ToList()
                    For Each action As Action In orderedActions
                        tableActionsInverted.AddCell(New PdfPCell(New Phrase(CStr(action.NumeroAction), fontTiny)))
                    Next

                    ' --- Lignes pour chaque Combattant et leurs mouvements ---
                    For Each projectCombatant As Combattant In currentProjet.ListeCombattants.OrderBy(Function(c) c.ID)
                        ' Ligne pour le nom du Combattant (étend sur toutes les colonnes)
                        Dim cellCombatantName As New PdfPCell(New Phrase($"{projectCombatant.Nom} {projectCombatant.Prenom} (ID: {projectCombatant.ID})", fontSmall))
                        cellCombatantName.Colspan = totalColumnsTableActions
                        cellCombatantName.BackgroundColor = New BaseColor(240, 240, 240) ' Légère couleur de fond pour distinguer
                        cellCombatantName.HorizontalAlignment = Element.ALIGN_LEFT
                        tableActionsInverted.AddCell(cellCombatantName)

                        ' Liste des propriétés de mouvement à afficher
                        Dim mouvementProperties As New List(Of String) From {"MainDroite", "ZoneMainDroite", "CibleMainDroiteID",
                                                                             "MainGauche", "ZoneMainGauche", "CibleMainGaucheID",
                                                                             "Deplacement", "CommentaireEtPouvoirForce"}

                        ' Pour chaque propriété de mouvement (Main Droite, Zone MD, etc.)
                        For Each propName As String In mouvementProperties
                            Dim headerText As String = ""

                            Select Case propName
                                Case "MainDroite" : headerText = "Main D"
                                Case "ZoneMainDroite" : headerText = "Zone MD"
                                Case "CibleMainDroiteID" : headerText = "Cible MD"
                                Case "MainGauche" : headerText = "Main G"
                                Case "ZoneMainGauche" : headerText = "Zone MG"
                                Case "CibleMainGaucheID" : headerText = "Cible MG"
                                Case "Deplacement" : headerText = "Dépl."
                                Case "CommentaireEtPouvoirForce" : headerText = "Com."
                            End Select

                            tableActionsInverted.AddCell(New PdfPCell(New Phrase(headerText, fontTiny))) ' Entête de ligne fixe

                            ' Remplir les données pour cette propriété pour toutes les actions
                            For Each action As Action In orderedActions
                                Dim mouvementForCombatant As Mouvement = action.Mouvements.FirstOrDefault(Function(m) m.CombattantID = projectCombatant.ID)
                                Dim cellValue As String = ""

                                If mouvementForCombatant IsNot Nothing Then
                                    Select Case propName
                                        Case "MainDroite" : cellValue = mouvementForCombatant.MainDroite
                                        Case "ZoneMainDroite" : cellValue = mouvementForCombatant.ZoneMainDroite
                                        Case "CibleMainDroiteID" : cellValue = If(mouvementForCombatant.CibleMainDroiteID = 0, "", CStr(mouvementForCombatant.CibleMainDroiteID))
                                        Case "MainGauche" : cellValue = mouvementForCombatant.MainGauche
                                        Case "ZoneMainGauche" : cellValue = mouvementForCombatant.ZoneMainGauche
                                        Case "CibleMainGaucheID" : cellValue = If(mouvementForCombatant.CibleMainGaucheID = 0, "", CStr(mouvementForCombatant.CibleMainGaucheID))
                                        Case "Deplacement" : cellValue = mouvementForCombatant.Deplacement
                                        Case "CommentaireEtPouvoirForce" : cellValue = $"{mouvementForCombatant.Commentaire} {mouvementForCombatant.PouvoirForce}".Trim()
                                    End Select
                                End If
                                tableActionsInverted.AddCell(New PdfPCell(New Phrase(cellValue, fontTiny)))
                            Next
                        Next
                    Next

                    doc.Add(tableActionsInverted)
                    doc.Add(New Paragraph(Environment.NewLine)) ' Ligne vide après chaque tableau d'actions
                Next

                ' 4. Fermer le document
                doc.Close()

                MessageBox.Show($"Le rapport PDF a été généré avec succès à l'emplacement : {filePath}", "PDF Généré", MessageBoxButtons.OK, MessageBoxIcon.Information)

            Catch ex As Exception
                MessageBox.Show($"Une erreur est survenue lors de la génération du PDF : {ex.Message}", "Erreur PDF", MessageBoxButtons.OK, MessageBoxIcon.Error)
            End Try
        End If
    End Sub

    Private Sub SplitContainer1_Panel2_Paint(sender As Object, e As PaintEventArgs) Handles SplitContainer1.Panel2.Paint

    End Sub

    Private Sub chkMouvementEnsemble_CheckedChanged(sender As Object, e As EventArgs) Handles chkMouvementEnsemble.CheckedChanged
        DetermineAndSetCategorie() ' Recalcule la catégorie
    End Sub
End Class




