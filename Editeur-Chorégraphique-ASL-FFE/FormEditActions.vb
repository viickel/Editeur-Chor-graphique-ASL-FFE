Imports System.Data ' Nécessaire pour utiliser DataTable, DataRow, etc.
Imports System.Linq ' Nécessaire pour les méthodes Linq comme .Any(), .Max(), .OrderBy(), .FirstOrDefault()
Imports System.ComponentModel

Public Class FormEditActions


    Private ReadOnly MouvementOptions As MouvementOptionsLoader ' Nouvelle instance pour charger les options
    Private ReadOnly CommentOptions As List(Of String) ' Gardons les commentaires définis en dur pour l'instant

    Public Sub New()
        InitializeComponent()

        MouvementOptions = New MouvementOptionsLoader() ' Charge les options depuis le CSV
    End Sub


    ' Propriétés pour recevoir les données du formulaire parent (FormEditPhraseDArmes)
    ' ListeActionsDuProjet est une RÉFÉRENCE à la liste d'actions de la phrase sélectionnée.
    ' Donc les modifications ici affecteront directement l'objet PhraseDArmes.
    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property ListeActionsDuProjet As List(Of Action)

    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property ListeCombattants As List(Of Combattant)


    ' DataTable que le DataGridView va utiliser comme source de données
    Private actionsDataTable As DataTable

    ' *** NOUVELLE MÉTHODE : PopulateCombattantsListBox ***
    Private Sub PopulateCombattantsListBox()
        ' 1. Vider la ListBox avant de la remplir pour éviter les doublons si elle est appelée plusieurs fois
        lbxCombattants.Items.Clear()

        ' 2. Vérifier si la liste des combattants existe et contient des éléments
        If ListeCombattants IsNot Nothing AndAlso ListeCombattants.Any() Then
            ' 3. Trier les combattants par leur ID (ou Nom/Prénom) pour un affichage ordonné
            Dim sortedCombattants = ListeCombattants.OrderBy(Function(c) c.ID).ToList()

            ' 4. Parcourir chaque combattant trié et ajouter une chaîne formatée à la ListBox
            For Each c As Combattant In sortedCombattants
                ' Utilise l'interpolation de chaînes ($"...") pour un formatage facile
                lbxCombattants.Items.Add($"{c.Nom} {c.Prenom} (ID: {c.ID})")
            Next
        Else
            ' 5. Afficher un message si aucun combattant n'est trouvé
            lbxCombattants.Items.Add("Aucun combattant dans le projet.")
        End If
    End Sub
    ' ****************************************************


    ' --- Événement de Chargement du Formulaire ---
    Private Sub FormEditActions_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        ' S'assurer que les listes sont initialisées pour éviter les erreurs NullReferenceException
        If ListeActionsDuProjet Is Nothing Then
            ListeActionsDuProjet = New List(Of Action)()
        End If
        If ListeCombattants Is Nothing Then
            ListeCombattants = New List(Of Combattant)()
        End If

        ' Configurer les propriétés du DataGridView AVANT de construire les colonnes
        ' ou de lier la source de données, pour s'assurer que AutoGenerateColumns est False
        dgvActions.AutoGenerateColumns = False ' <--- TRÈS IMPORTANT : METS CELA À FALSE !!!
        dgvActions.AllowUserToAddRows = False
        dgvActions.AllowUserToDeleteRows = False
        dgvActions.ReadOnly = False ' C'est bien de le laisser à False ici.

        ' Construire la structure des colonnes du DataTable
        ' (Cela va ajouter les colonnes manuellement au dgvActions)
        BuildActionsDataTable()

        ' Remplir le DataTable avec les données existantes des actions
        PopulateActionsDataTable()


        PopulateCombattantsListBox()

        ' Lier le BindingSource au DataTable créé
        ' Note: Si PopulateActionsDataTable remplit directement le DGV et que vous n'utilisez pas
        ' actionsDataTable pour la liaison directe du DGV, cette ligne peut ne pas être nécessaire
        ' ou devrait lier dgvActions.DataSource directement si vous n'utilisez pas le BindingSource
        ' pour la liaison automatique de colonnes.
        ' Pour l'instant, laissons-la, mais le problème principal est AutoGenerateColumns.
        bsActionsLocal.DataSource = actionsDataTable ' Cette ligne doit être cohérente avec l'utilisation de actionsDataTable

        ' Désactiver les boutons d'édition/suppression/déplacement tant qu'aucune ligne n'est sélectionnée
        UpdateActionButtonsState()
    End Sub

    ' --- Méthode pour construire les colonnes du DataTable ---
    Private Sub BuildActionsDataTable()
        dgvActions.Columns.Clear()

        Dim showTargetColumns As Boolean = ListeCombattants.Count > 2

        ' Préparer les listes d'options avec l'option "vide" ou "Aucun"
        Dim mainOptions As New List(Of String)()
        mainOptions.Add("") ' Ou "Aucun" si tu préfères un texte
        mainOptions.AddRange(MouvementOptions.Mains.ToList())

        Dim zoneOptions As New List(Of String)()
        zoneOptions.Add("") ' Ou "Aucune"
        zoneOptions.AddRange(MouvementOptions.Zones.ToList())

        Dim deplacementOptions As New List(Of String)()
        deplacementOptions.Add("") ' Ou "Aucun"
        deplacementOptions.AddRange(MouvementOptions.Deplacements.ToList())

        ' Colonne pour le numéro d'action
        Dim colNumero As New DataGridViewTextBoxColumn()
        colNumero.Name = "NumeroAction"
        colNumero.HeaderText = "Numéro"
        colNumero.DataPropertyName = "NumeroAction"
        colNumero.SortMode = DataGridViewColumnSortMode.Automatic
        colNumero.ReadOnly = True
        dgvActions.Columns.Add(colNumero)

        For Each combatant As Combattant In ListeCombattants
            ' Colonne ComboBox pour Main droite
            Dim colMainDroite As New DataGridViewComboBoxColumn()
            colMainDroite.Name = $"Main droite ({combatant.ID})"
            colMainDroite.HeaderText = $"Main droite ({combatant.Nom} {combatant.Prenom})"
            colMainDroite.DataSource = mainOptions.Distinct().ToList() ' Utilise la liste préparée
            colMainDroite.AutoComplete = True
            colMainDroite.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
            dgvActions.Columns.Add(colMainDroite)

            ' Nouvelle Colonne ComboBox pour Zone Main Droite
            Dim colZoneMainDroite As New DataGridViewComboBoxColumn()
            colZoneMainDroite.Name = $"Zone MD ({combatant.ID})"
            colZoneMainDroite.HeaderText = $"Zone MD ({combatant.Nom} {combatant.Prenom})"
            colZoneMainDroite.DataSource = zoneOptions.Distinct().ToList() ' Utilise la liste préparée
            colZoneMainDroite.AutoComplete = True
            colZoneMainDroite.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
            dgvActions.Columns.Add(colZoneMainDroite)

            ' Colonne ComboBox pour Cible Main Droite (conditionnelle)
            If showTargetColumns Then
                Dim colCibleMainDroite As New DataGridViewComboBoxColumn()
                colCibleMainDroite.Name = $"Cible MD ({combatant.ID})"
                colCibleMainDroite.HeaderText = $"Cible MD ({combatant.Nom} {combatant.Prenom})"

                Dim cibleOptionsMD As New List(Of String)()
                cibleOptionsMD.Add("0") ' Pour "aucune cible"
                cibleOptionsMD.AddRange(ListeCombattants.Select(Function(c) CStr(c.ID)).ToList())
                colCibleMainDroite.DataSource = cibleOptionsMD.Distinct().ToList()

                colCibleMainDroite.AutoComplete = True
                colCibleMainDroite.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
                dgvActions.Columns.Add(colCibleMainDroite)
            End If

            ' Colonne ComboBox pour Main gauche
            Dim colMainGauche As New DataGridViewComboBoxColumn()
            colMainGauche.Name = $"Main gauche ({combatant.ID})"
            colMainGauche.HeaderText = $"Main gauche ({combatant.Nom} {combatant.Prenom})"
            colMainGauche.DataSource = mainOptions.Distinct().ToList() ' Utilise la liste préparée
            colMainGauche.AutoComplete = True
            colMainGauche.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
            dgvActions.Columns.Add(colMainGauche)

            ' Nouvelle Colonne ComboBox pour Zone Main Gauche
            Dim colZoneMainGauche As New DataGridViewComboBoxColumn()
            colZoneMainGauche.Name = $"Zone MG ({combatant.ID})"
            colZoneMainGauche.HeaderText = $"Zone MG ({combatant.Nom} {combatant.Prenom})"
            colZoneMainGauche.DataSource = zoneOptions.Distinct().ToList() ' Utilise la liste préparée
            colZoneMainGauche.AutoComplete = True
            colZoneMainGauche.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
            dgvActions.Columns.Add(colZoneMainGauche)

            ' Colonne ComboBox pour Cible Main Gauche (conditionnelle)
            If showTargetColumns Then
                Dim colCibleMainGauche As New DataGridViewComboBoxColumn()
                colCibleMainGauche.Name = $"Cible MG ({combatant.ID})"
                colCibleMainGauche.HeaderText = $"Cible MG ({combatant.Nom} {combatant.Prenom})"

                Dim cibleOptionsMG As New List(Of String)()
                cibleOptionsMG.Add("0")
                cibleOptionsMG.AddRange(ListeCombattants.Select(Function(c) CStr(c.ID)).ToList())
                colCibleMainGauche.DataSource = cibleOptionsMG.Distinct().ToList()

                colCibleMainGauche.AutoComplete = True
                colCibleMainGauche.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
                dgvActions.Columns.Add(colCibleMainGauche)
            End If

            ' Colonne ComboBox pour Déplacement
            Dim colDeplacement As New DataGridViewComboBoxColumn()
            colDeplacement.Name = $"Déplacement ({combatant.ID})"
            colDeplacement.HeaderText = $"Déplacement ({combatant.Nom} {combatant.Prenom})"
            colDeplacement.DataSource = deplacementOptions.Distinct().ToList() ' Utilise la liste préparée
            colDeplacement.AutoComplete = True
            colDeplacement.DisplayStyle = DataGridViewComboBoxDisplayStyle.DropDownButton
            dgvActions.Columns.Add(colDeplacement)

            ' Colonne de Texte simple pour les commentaires
            Dim colCommentaire As New DataGridViewTextBoxColumn()
            colCommentaire.Name = $"Commentaire ({combatant.ID})"
            colCommentaire.HeaderText = $"Commentaire ({combatant.Nom} {combatant.Prenom})"
            dgvActions.Columns.Add(colCommentaire)
        Next
    End Sub





    ' --- Méthode pour remplir le DataTable avec les données de ListeActionsDuProjet ---
    Private Sub PopulateActionsDataTable()
        dgvActions.Rows.Clear()

        ' Déterminer si nous avons plus de 2 combattants pour les colonnes Cible
        Dim showTargetColumns As Boolean = ListeCombattants.Count > 2

        For Each action As Action In ListeActionsDuProjet
            Dim rowValues As New List(Of Object)()
            rowValues.Add(action.NumeroAction)

            For Each projectCombatant As Combattant In ListeCombattants
                Dim mouvementForCombatant As Mouvement = action.Mouvements.FirstOrDefault(Function(m) m.CombattantID = projectCombatant.ID)

                If mouvementForCombatant IsNot Nothing Then
                    rowValues.Add(mouvementForCombatant.MainDroite)
                    rowValues.Add(mouvementForCombatant.ZoneMainDroite) ' Nouvelle Zone Main Droite
                    If showTargetColumns Then rowValues.Add(CStr(mouvementForCombatant.CibleMainDroiteID)) ' Nouvelle Cible Main Droite
                    rowValues.Add(mouvementForCombatant.MainGauche)
                    rowValues.Add(mouvementForCombatant.ZoneMainGauche) ' Nouvelle Zone Main Gauche
                    If showTargetColumns Then rowValues.Add(CStr(mouvementForCombatant.CibleMainGaucheID)) ' Nouvelle Cible Main Gauche
                    rowValues.Add(mouvementForCombatant.Deplacement)
                    rowValues.Add($"{mouvementForCombatant.Commentaire} {mouvementForCombatant.PouvoirForce}".Trim())
                Else
                    ' Si aucune donnée de mouvement, ajouter des chaînes vides ou valeurs par défaut
                    rowValues.Add("") ' MainDroite
                    rowValues.Add("") ' ZoneMainDroite
                    If showTargetColumns Then rowValues.Add("0") ' <--- MODIFICATION ICI : Mettre "0" comme valeur par défaut pour les cibles
                    rowValues.Add("") ' MainGauche
                    rowValues.Add("") ' ZoneMainGauche
                    If showTargetColumns Then rowValues.Add("0") ' <--- MODIFICATION ICI : Mettre "0" comme valeur par défaut pour les cibles
                    rowValues.Add("") ' Deplacement
                    rowValues.Add("") ' Commentaire
                End If
            Next
            dgvActions.Rows.Add(rowValues.ToArray())
        Next
    End Sub

    ' --- Méthode pour rafraîchir l'affichage du DataGridView ---
    Private Sub RefreshActionsDisplay()
        ' Reconstruire le DataTable pour refléter les changements dans ListeActionsDuProjet
        ' Cela inclut l'ordre et les valeurs des cellules.
        PopulateActionsDataTable()
        bsActionsLocal.ResetBindings(False) ' Force le BindingSource à relire le DataTable
        UpdateActionButtonsState() ' Mettre à jour l'état des boutons
    End Sub

    ' --- Méthode pour mettre à jour l'état des boutons (activer/désactiver) ---
    Private Sub UpdateActionButtonsState()
        Dim selectedRowCount As Integer = dgvActions.SelectedRows.Count
        If selectedRowCount = 1 Then
            btnEditAction.Enabled = True
            btnDeleteAction.Enabled = True

            Dim selectedIndex As Integer = dgvActions.SelectedRows(0).Index
            btnMoveActionUp.Enabled = (selectedIndex > 0)
            ' *** MODIFICATION ICI ***
            ' Utilisez dgvActions.Rows.Count au lieu de bsActionsLocal.Count
            btnMoveActionDown.Enabled = (selectedIndex < dgvActions.Rows.Count - 1)
        Else
            btnEditAction.Enabled = False
            btnDeleteAction.Enabled = False
            btnMoveActionUp.Enabled = False
            btnMoveActionDown.Enabled = False
        End If
    End Sub

    ' --- Événement quand la sélection du DataGridView change ---
    Private Sub dgvActions_SelectionChanged(sender As Object, e As EventArgs) Handles dgvActions.SelectionChanged
        UpdateActionButtonsState()
    End Sub

    ' --- Clic sur le bouton "Ajouter Action" ---
    Private Sub btnAddAction_Click(sender As Object, e As EventArgs) Handles btnAddAction.Click
        Dim newAction As New Action()
        ' Assigne un numéro unique, basé sur le numéro max existant + 1, ou 1 si c'est la première
        newAction.NumeroAction = If(ListeActionsDuProjet.Any(), ListeActionsDuProjet.Max(Function(a) a.NumeroAction) + 1, 1)

        ' Initialise un objet Mouvement vide pour CHAQUE combattant du projet, avec son ID
        For Each combattant As Combattant In ListeCombattants
            newAction.Mouvements.Add(New Mouvement With {.CombattantID = combattant.ID}) ' Utilise le constructeur par défaut de Mouvement, puis assigne l'ID
        Next

        ListeActionsDuProjet.Add(newAction)
        PopulateActionsDataTable() ' Rafraîchir l'affichage
        dgvActions.FirstDisplayedScrollingRowIndex = dgvActions.RowCount - 1 ' Aller à la nouvelle ligne
        MarkAsDirtyInMainForm()
    End Sub

    ' --- Clic sur le bouton "Supprimer Action" ---
    Private Sub btnDeleteAction_Click(sender As Object, e As EventArgs) Handles btnDeleteAction.Click
        If dgvActions.SelectedRows.Count > 0 Then
            Dim selectedRowIndex As Integer = dgvActions.SelectedRows(0).Index

            ' *** MODIFICATION ICI ***
            ' Accédez directement à la valeur de la cellule dans le DataGridView
            ' Supposons que "NumeroAction" est dans la première colonne (index 0).
            ' Si "NumeroAction" est dans une autre colonne, changez l'index (par exemple, 0 pour la 1ère colonne)
            Dim selectedActionNumero As Integer = CType(dgvActions.Rows(selectedRowIndex).Cells(0).Value, Integer)
            ' Si vous avez défini un nom pour la colonne dans dgvActions, vous pouvez aussi faire:
            ' Dim selectedActionNumero As Integer = CType(dgvActions.Rows(selectedRowIndex).Cells("NomDeLaColonneNumeroAction").Value, Integer)

            Dim actionToRemove As Action = ListeActionsDuProjet.FirstOrDefault(Function(a) a.NumeroAction = selectedActionNumero)
            If actionToRemove IsNot Nothing Then
                ListeActionsDuProjet.Remove(actionToRemove)

                ' Optionnel: re-numéroter les actions après suppression pour garder une séquence propre
                For i As Integer = 0 To ListeActionsDuProjet.Count - 1
                    ListeActionsDuProjet(i).NumeroAction = i + 1
                Next

                PopulateActionsDataTable() ' Rafraîchir l'affichage (qui va reconstruire les lignes de dgvActions)
                MarkAsDirtyInMainForm()
            End If
        Else
            MessageBox.Show("Veuillez sélectionner une ligne à supprimer.", "Suppression d'Action", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    ' --- Gestion de l'édition directe des cellules du DataGridView ---
    ' Quand la valeur d'une cellule change, mettez à jour l'objet Action sous-jacent.
    Private Sub dgvActions_CellValueChanged(sender As Object, e As DataGridViewCellEventArgs) Handles dgvActions.CellValueChanged
        If e.RowIndex >= 0 AndAlso e.ColumnIndex >= 0 Then
            Dim currentAction As Action = ListeActionsDuProjet(e.RowIndex)
            Dim columnName As String = dgvActions.Columns(e.ColumnIndex).Name

            Dim cellValue As Object = dgvActions.Rows(e.RowIndex).Cells(e.ColumnIndex).Value
            Dim newValue As String = If(cellValue Is DBNull.Value OrElse cellValue Is Nothing, "", CStr(cellValue))

            If columnName = "NumeroAction" Then
                If Integer.TryParse(newValue, currentAction.NumeroAction) Then
                    MarkAsDirtyInMainForm()
                Else
                    MessageBox.Show("Le numéro d'action doit être un nombre entier.", "Erreur de Saisie", MessageBoxButtons.OK, MessageBoxIcon.Error)
                    ' Optionnel: Annuler le changement ou restaurer l'ancienne valeur
                End If
            Else
                ' Extraire le type de mouvement/info et l'ID du combattant depuis le nom de la colonne
                Dim parts() As String = columnName.Split({"("c, ")"c}, StringSplitOptions.RemoveEmptyEntries)

                If parts.Length >= 2 Then
                    Dim infoType As String = parts(0).Trim() ' Ex: "Main droite", "Zone MD", "Cible MD", "Déplacement", "Commentaire"
                    Dim combatantIDStr As String = parts(1).Trim() ' L'ID du combattant
                    Dim targetCombatantID As Integer

                    If Not Integer.TryParse(combatantIDStr, targetCombatantID) Then
                        ' C'est une erreur, l'ID du combattant dans le nom de colonne n'est pas un nombre
                        Exit Sub
                    End If

                    Dim mouvementToUpdate As Mouvement = currentAction.Mouvements.FirstOrDefault(Function(m) m.CombattantID = targetCombatantID)

                    If mouvementToUpdate Is Nothing Then
                        mouvementToUpdate = New Mouvement With {.CombattantID = targetCombatantID}
                        currentAction.Mouvements.Add(mouvementToUpdate)
                    End If

                    Select Case infoType
                        Case "Main droite"
                            mouvementToUpdate.MainDroite = newValue
                        Case "Zone MD"
                            mouvementToUpdate.ZoneMainDroite = newValue
                        Case "Cible MD"
                            If Integer.TryParse(newValue, mouvementToUpdate.CibleMainDroiteID) Then
                                ' OK
                            Else
                                ' Gérer l'erreur si la cible n'est pas un ID valide
                                MessageBox.Show("La cible Main Droite doit être un ID de combattant valide.", "Erreur de Saisie", MessageBoxButtons.OK, MessageBoxIcon.Error)
                                ' Optionnel : Restaurer l'ancienne valeur ou vider la cellule
                                ' dgvActions.Rows(e.RowIndex).Cells(e.ColumnIndex).Value = mouvementToUpdate.CibleMainDroiteID.ToString()
                            End If
                        Case "Main gauche"
                            mouvementToUpdate.MainGauche = newValue
                        Case "Zone MG"
                            mouvementToUpdate.ZoneMainGauche = newValue
                        Case "Cible MG"
                            If Integer.TryParse(newValue, mouvementToUpdate.CibleMainGaucheID) Then
                                ' OK
                            Else
                                MessageBox.Show("La cible Main Gauche doit être un ID de combattant valide.", "Erreur de Saisie", MessageBoxButtons.OK, MessageBoxIcon.Error)
                            End If
                        Case "Déplacement"
                            mouvementToUpdate.Deplacement = newValue
                        Case "Commentaire"
                            ' Assurez-vous que le PouvoirForce est géré séparément si tu as de la logique pour ça
                            ' Ici, on combine juste commentaire et PouvoirForce lors de l'affichage.
                            ' Lors de l'enregistrement, tu devrais peut-être séparer.
                            mouvementToUpdate.Commentaire = newValue
                            mouvementToUpdate.PouvoirForce = "" ' Supposons que PouvoirForce est vide si le commentaire est saisi manuellement
                    End Select
                    MarkAsDirtyInMainForm()
                End If
            End If
        End If
    End Sub

    Private Sub dgvActions_CellValidating(sender As Object, e As DataGridViewCellValidatingEventArgs) Handles dgvActions.CellValidating
        Dim columnName As String = dgvActions.Columns(e.ColumnIndex).Name

        ' Vérifier si c'est une colonne ComboBox (Main droite, Main gauche, Déplacement)
        If columnName.StartsWith("Main droite (") OrElse
       columnName.StartsWith("Main gauche (") OrElse
       columnName.StartsWith("Déplacement (") Then

            Dim comboBoxColumn As DataGridViewComboBoxColumn = CType(dgvActions.Columns(e.ColumnIndex), DataGridViewComboBoxColumn)
            Dim currentValue As String = e.FormattedValue.ToString()

            ' Si la valeur saisie n'est pas dans la liste des options de la ComboBox
            ' et que vous voulez la forcer à être dans la liste, décommenter la ligne suivante.
            ' Sinon, la valeur saisie sera acceptée même si elle n'est pas dans la liste déroulante (ce qui est généralement souhaitable avec DropDownButton).
            ' If Not CType(comboBoxColumn.DataSource, List(Of String)).Contains(currentValue) Then
            '     e.Cancel = True
            '     dgvActions.Rows(e.RowIndex).Cells(e.ColumnIndex).ErrorText = "Veuillez sélectionner une option valide de la liste ou laisser vide."
            ' End If
        End If
        ' La colonne Commentaire n'est pas une ComboBox, donc elle n'est pas traitée ici.
    End Sub

    ' Méthode d'aide pour notifier le formulaire parent (FormEditPhraseDArmes) des changements
    Private Sub MarkAsDirtyInMainForm()
        If Me.Owner IsNot Nothing AndAlso TypeOf Me.Owner Is FormEditPhraseDArmes Then
            Dim parentForm As FormEditPhraseDArmes = CType(Me.Owner, FormEditPhraseDArmes)
            parentForm.MarkAsDirtyInMainForm() ' Appelle la méthode du parent pour marquer le projet comme modifié
        End If
    End Sub



    ' --- Méthode pour réassigner les numéros d'action et rafraîchir (similaire à ReassignPhraseNumbers) ---
    Private Sub ReassignActionNumbers()
        ' Créer une copie triée temporaire de la liste d'actions (basée sur les NumeroAction actuels)
        Dim sortedList As List(Of Action) = ListeActionsDuProjet.OrderBy(Function(a) a.NumeroAction).ToList()

        ' Vider la liste originale d'actions
        ListeActionsDuProjet.Clear()

        ' Remplir la liste originale avec les actions triées
        For Each action As Action In sortedList
            ListeActionsDuProjet.Add(action)
        Next

        ' Réassigner les numéros séquentiellement de 1 à N en fonction du nouvel ordre physique
        For i As Integer = 0 To ListeActionsDuProjet.Count - 1
            ListeActionsDuProjet(i).NumeroAction = i + 1
        Next

        ' Rafraîchir l'affichage du DataGridView (re-peuple le DataTable et réinitialise le BindingSource)
        RefreshActionsDisplay()
    End Sub

    ' --- Clic sur le bouton "Monter Action" ---
    Private Sub btnMoveActionUp_Click(sender As Object, e As EventArgs) Handles btnMoveActionUp.Click
        If dgvActions.SelectedRows.Count = 1 Then
            Dim selectedIndex As Integer = dgvActions.SelectedRows(0).Index ' Obtenir l'index de la ligne sélectionnée

            If selectedIndex > 0 Then ' Si ce n'est pas la première ligne
                Dim selectedAction As Action = ListeActionsDuProjet(selectedIndex)
                Dim actionAbove As Action = ListeActionsDuProjet(selectedIndex - 1)

                ' Échanger UNIQUEMENT les numéros des deux actions
                Dim tempNumero As Integer = actionAbove.NumeroAction
                actionAbove.NumeroAction = selectedAction.NumeroAction
                selectedAction.NumeroAction = tempNumero

                ' Appeler ReassignActionNumbers pour trier la liste, ré-numéroter et rafraîchir le DGV
                ReassignActionNumbers()

                ' Resélectionner la ligne déplacée
                dgvActions.ClearSelection()
                If selectedIndex - 1 >= 0 Then
                    dgvActions.Rows(selectedIndex - 1).Selected = True
                    dgvActions.FirstDisplayedScrollingRowIndex = selectedIndex - 1
                End If
            End If
        End If
    End Sub

    ' --- Clic sur le bouton "Descendre Action" ---
    Private Sub btnMoveActionDown_Click(sender As Object, e As EventArgs) Handles btnMoveActionDown.Click
        If dgvActions.SelectedRows.Count = 1 Then
            Dim selectedIndex As Integer = dgvActions.SelectedRows(0).Index

            If selectedIndex >= 0 AndAlso selectedIndex < ListeActionsDuProjet.Count - 1 Then ' Si ce n'est pas la dernière ligne
                Dim selectedAction As Action = ListeActionsDuProjet(selectedIndex)
                Dim actionBelow As Action = ListeActionsDuProjet(selectedIndex + 1)

                ' Échanger UNIQUEMENT les numéros des deux actions
                Dim tempNumero As Integer = actionBelow.NumeroAction
                actionBelow.NumeroAction = selectedAction.NumeroAction
                selectedAction.NumeroAction = tempNumero

                ' Appeler ReassignActionNumbers pour trier la liste, ré-numéroter et rafraîchir le DGV
                ReassignActionNumbers()

                ' Resélectionner la ligne déplacée
                dgvActions.ClearSelection()
                If selectedIndex + 1 < dgvActions.Rows.Count Then
                    dgvActions.Rows(selectedIndex + 1).Selected = True
                    dgvActions.FirstDisplayedScrollingRowIndex = selectedIndex + 1
                End If
            End If
        End If
    End Sub

    ' --- Clic sur le bouton "Valider" (Valider les modifications et fermer) ---
    Private Sub btnValidateActions_Click(sender As Object, e As EventArgs) Handles btnValidateActions.Click
        ' Les modifications sont déjà faites directement sur ListeActionsDuProjet
        ' car c'est une référence passée du formulaire parent.
        Me.DialogResult = DialogResult.OK
        Me.Close()
    End Sub

    ' --- Clic sur le bouton "Annuler" (Fermer sans sauvegarder les modifications) ---
    Private Sub btnCancelActions_Click(sender As Object, e As EventArgs) Handles btnCancelActions.Click
        ' Pour annuler réellement les modifications, il faudrait avoir fait une copie
        ' profonde de ListeActionsDuProjet lors du chargement du formulaire, et ne pas
        ' mettre à jour ListeActionsDuProjet avant de cliquer sur "Valider".
        ' Dans cette implémentation actuelle, les changements sont "live".
        Me.DialogResult = DialogResult.Cancel
        Me.Close()
    End Sub

    ' Gestionnaire d'événement pour le double-clic sur une cellule (optionnel, si vous voulez une pop-up d'édition)
    Private Sub dgvActions_CellDoubleClick(sender As Object, e As DataGridViewCellEventArgs) Handles dgvActions.CellDoubleClick
        If e.RowIndex >= 0 Then
            ' Optionnel : si vous voulez ouvrir un formulaire d'édition plus détaillé au double-clic
            ' Actuellement, l'édition se fait directement dans les cellules du DataGridView.
            ' Si vous décidez d'ajouter un formulaire d'édition, vous pouvez appeler btnEditAction_Click ici.
        End If
    End Sub





End Class