Imports System.Collections.Generic ' Pour List(Of T)
Imports System.ComponentModel    ' Pour DesignerSerializationVisibility
Imports System.Linq              ' Pour les méthodes Linq comme OrderBy, ToList, etc.


Public Class FormEditPhraseDArmes

    ' Dans la classe FormEditPhraseDArmes
    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property CurrentProjet As ProjetChoregraphique ' Pour passer l'objet projet principal


    ' Propriété publique pour passer et récupérer la liste des phrases d'armes du projet
    ' DesignerSerializationVisibility.Hidden empêche le designer de tenter de sérialiser cette propriété,
    ' ce qui est important car elle est passée de Form1.
    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property ListePhraseDArmesDuProjet As List(Of PhraseDArmes)

    ' Pour le BindingSource, afin de lier la ListBox aux objets PhraseDArmes
    Private bsPhraseDArmes As New BindingSource()

    ' Pour stocker la phrase d'armes actuellement sélectionnée pour modification
    Private currentSelectedPhraseDArmes As PhraseDArmes

    ' --- Gestionnaire d'événements au chargement du formulaire ---
    Private Sub FormEditPhraseDArmes_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        lstPhraseDArmes.DataSource = bsPhraseDArmes
        lstPhraseDArmes.DisplayMember = "ToString"

        ' Assurez-vous que la liste passée par le formulaire principal n'est pas Nothing
        If ListePhraseDArmesDuProjet Is Nothing Then
            ListePhraseDArmesDuProjet = New List(Of PhraseDArmes)()
        End If

        ' IMPORTANT: Assigner la source de données au BindingSource une seule fois au début.
        ' Le BindingSource doit pointer vers l'instance de liste que nous allons modifier.
        bsPhraseDArmes.DataSource = ListePhraseDArmesDuProjet

        ' Appeler ReassignPhraseNumbers pour trier et numéroter initialement la liste.
        ' Cette méthode va modifier la ListePhraseDArmesDuProjet en place et appeler ResetBindings(False).
        ReassignPhraseNumbers()

        ClearPhraseDArmesDetails()   ' Réinitialise les champs de détails au démarrage
        UpdateMoveButtonsState()     ' Met à jour l'état des boutons de déplacement
    End Sub

    ' --- Méthodes de gestion des détails de la phrase d'armes ---

    ' Méthode pour vider les champs de détails (utilisée pour "nouvelle saisie" ou "aucune sélection")
    Private Sub ClearPhraseDArmesDetails()
        txtNumero.Text = ""                  ' Vider le champ du numéro
        rtbDescriptionSection.Text = ""      ' Vider le champ de la description
        currentSelectedPhraseDArmes = Nothing ' Réinitialiser l'objet sélectionné
        txtNumero.Focus()                    ' Donne le focus au premier champ (ici, le numéro non éditable)
        btnUpdatePhrase.Enabled = False      ' Désactiver le bouton de mise à jour
        btnDeletePhrase.Enabled = False      ' Désactiver le bouton de suppression
        btnEditActions.Enabled = False       ' Désactiver le bouton d'édition des actions
        UpdateMoveButtonsState()             ' Met à jour l'état des boutons de déplacement
    End Sub

    ' Méthode pour afficher les détails de la phrase d'armes sélectionnée dans les contrôles
    Private Sub DisplayPhraseDArmesDetails(phrase As PhraseDArmes)
        If phrase IsNot Nothing Then
            txtNumero.Text = phrase.Numero.ToString() ' Afficher le numéro (ReadOnly)
            rtbDescriptionSection.Text = phrase.DescriptionSection ' Afficher la description
            currentSelectedPhraseDArmes = phrase   ' Mettre à jour l'objet sélectionné
            btnUpdatePhrase.Enabled = True         ' Activer le bouton de mise à jour
            btnDeletePhrase.Enabled = True         ' Activer le bouton de suppression
            btnEditActions.Enabled = True          ' Activer le bouton d'édition des actions
        Else
            ClearPhraseDArmesDetails() ' Si aucune phrase, vider les détails
        End If
        UpdateMoveButtonsState() ' Met à jour l'état des boutons de déplacement
    End Sub

    ' --- Gestionnaire d'événements pour la sélection dans la ListBox ---
    Private Sub lstPhraseDArmes_SelectedIndexChanged(sender As Object, e As EventArgs) Handles lstPhraseDArmes.SelectedIndexChanged
        If lstPhraseDArmes.SelectedItem IsNot Nothing Then
            DisplayPhraseDArmesDetails(CType(lstPhraseDArmes.SelectedItem, PhraseDArmes))
        Else
            ClearPhraseDArmesDetails()
        End If
    End Sub

    ' --- Méthode d'aide pour recalculer et réaffecter les numéros des phrases ---
    Private Sub ReassignPhraseNumbers()
        ' 1. Créer une copie TEMPORAIRE triée de la liste actuelle, basée sur les numéros ACTUELS.
        Dim sortedList As List(Of PhraseDArmes) = ListePhraseDArmesDuProjet.OrderBy(Function(p) p.Numero).ToList()

        ' 2. Vider la liste ORIGINALE (celle à laquelle le BindingSource est lié et qui est partagée avec Form1).
        ListePhraseDArmesDuProjet.Clear()

        ' 3. Ajouter les éléments de la copie triée à la liste ORIGINALE.
        ' C'est cette étape qui réorganise physiquement la liste.
        For Each phrase As PhraseDArmes In sortedList
            ListePhraseDArmesDuProjet.Add(phrase)
        Next

        ' 4. Réassigner les numéros séquentiellement de 1 à N en fonction du NOUVEL ordre.
        For i As Integer = 0 To ListePhraseDArmesDuProjet.Count - 1
            ListePhraseDArmesDuProjet(i).Numero = i + 1 ' Les numéros commencent à 1
        Next

        ' 5. Informer le BindingSource que la liste sous-jacente a été modifiée.
        ' Cela force la ListBox à se rafraîchir et à afficher les éléments dans le nouvel ordre.
        bsPhraseDArmes.ResetBindings(False)
    End Sub

    ' --- Méthode d'aide pour gérer l'état des boutons de déplacement ---
    Private Sub UpdateMoveButtonsState()
        Dim selectedIndex As Integer = lstPhraseDArmes.SelectedIndex
        Dim itemCount As Integer = ListePhraseDArmesDuProjet.Count

        ' Le bouton "Monter" est activé si un élément est sélectionné et qu'il n'est pas le premier
        btnMoveUp.Enabled = selectedIndex > 0

        ' Le bouton "Descendre" est activé si un élément est sélectionné et qu'il n'est pas le dernier
        btnMoveDown.Enabled = selectedIndex < (itemCount - 1) AndAlso selectedIndex >= 0
    End Sub

    ' --- Gestionnaires d'événements pour les boutons d'action ---

    Private Sub btnAddPhrase_Click(sender As Object, e As EventArgs) Handles btnAddPhrase.Click
        ' Validation minimale : la description est obligatoire
        If String.IsNullOrWhiteSpace(rtbDescriptionSection.Text) Then
            MessageBox.Show("La description de la phrase d'armes est obligatoire.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        Dim newPhrase As New PhraseDArmes()
        newPhrase.DescriptionSection = rtbDescriptionSection.Text

        ' Calculer le prochain numéro disponible pour la nouvelle phrase
        ' Si la liste est vide, le premier numéro est 1. Sinon, c'est le numéro maximum actuel + 1.
        Dim nextNumero As Integer = 0
        If ListePhraseDArmesDuProjet.Any() Then ' Vérifie si la liste contient des éléments
            nextNumero = ListePhraseDArmesDuProjet.Max(Function(p) p.Numero) + 1
        Else
            nextNumero = 1 ' C'est la première phrase d'armes
        End If
        newPhrase.Numero = nextNumero ' Assigner le numéro à la nouvelle phrase


        ListePhraseDArmesDuProjet.Add(newPhrase)
        ReassignPhraseNumbers()
        bsPhraseDArmes.ResetBindings(False)

        ' Après l'ajout, videz les champs pour permettre une nouvelle saisie
        ClearPhraseDArmesDetails() ' Appelez cette méthode pour réinitialiser les champs et l'état

        MarkAsDirtyInMainForm()
    End Sub

    Private Sub btnUpdatePhrase_Click(sender As Object, e As EventArgs) Handles btnUpdatePhrase.Click
        If currentSelectedPhraseDArmes IsNot Nothing Then
            ' Validation minimale : la description est obligatoire
            If String.IsNullOrWhiteSpace(rtbDescriptionSection.Text) Then
                MessageBox.Show("La description de la phrase d'armes est obligatoire.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                Return
            End If

            ' Mise à jour de la description de la phrase sélectionnée
            currentSelectedPhraseDArmes.DescriptionSection = rtbDescriptionSection.Text

            bsPhraseDArmes.ResetBindings(False) ' Rafraîchit la ListBox pour refléter les changements (notamment le ToString())
            DisplayPhraseDArmesDetails(currentSelectedPhraseDArmes) ' Réaffiche les détails pour confirmer la mise à jour
            MarkAsDirtyInMainForm()
        Else
            MessageBox.Show("Veuillez sélectionner une phrase d'armes à mettre à jour.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If

        ClearPhraseDArmesDetails() ' Appelez cette méthode pour réinitialiser les champs et l'état

    End Sub

    Private Sub btnDeletePhrase_Click(sender As Object, e As EventArgs) Handles btnDeletePhrase.Click
        If currentSelectedPhraseDArmes IsNot Nothing Then
            Dim result As DialogResult = MessageBox.Show(
                $"Êtes-vous sûr de vouloir supprimer la phrase '{currentSelectedPhraseDArmes.ToString()}' et toutes ses actions/mouvements associés ?",
                "Confirmer la suppression",
                MessageBoxButtons.YesNo,
                MessageBoxIcon.Question)

            If result = DialogResult.Yes Then
                Dim selectedIndex As Integer = lstPhraseDArmes.SelectedIndex ' Garder l'index avant suppression
                ListePhraseDArmesDuProjet.Remove(currentSelectedPhraseDArmes) ' Supprimer la phrase
                ReassignPhraseNumbers()                                     ' Réassigner les numéros des phrases restantes

                If ListePhraseDArmesDuProjet.Count > 0 Then
                    ' Tenter de sélectionner l'élément voisin (précédent ou premier)
                    If selectedIndex > 0 Then
                        lstPhraseDArmes.SelectedIndex = selectedIndex - 1
                    Else
                        lstPhraseDArmes.SelectedIndex = 0
                    End If
                Else
                    ClearPhraseDArmesDetails() ' Si la liste est vide, tout effacer
                End If

                MarkAsDirtyInMainForm()
            End If
        Else
            MessageBox.Show("Veuillez sélectionner une phrase d'armes à supprimer.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    Private Sub btnMoveUp_Click(sender As Object, e As EventArgs) Handles btnMoveUp.Click
        ' Récupérer l'index de la phrase actuellement sélectionnée
        Dim selectedIndex As Integer = lstPhraseDArmes.SelectedIndex

        ' Vérifier qu'une phrase est sélectionnée et qu'elle n'est pas la première de la liste
        If selectedIndex > 0 AndAlso selectedIndex < ListePhraseDArmesDuProjet.Count Then
            ' Obtenir les références aux deux phrases concernées
            Dim selectedPhrase As PhraseDArmes = ListePhraseDArmesDuProjet(selectedIndex)
            Dim phraseAbove As PhraseDArmes = ListePhraseDArmesDuProjet(selectedIndex - 1)

            ' --- LOGIQUE CLÉ : Échanger UNIQUEMENT les numéros des deux phrases ---
            ' Nous stockons temporairement le numéro de la phrase du dessus
            Dim tempNumero As Integer = phraseAbove.Numero

            ' La phrase du dessus prend le numéro de la phrase sélectionnée
            phraseAbove.Numero = selectedPhrase.Numero

            ' La phrase sélectionnée prend l'ancien numéro de la phrase du dessus
            selectedPhrase.Numero = tempNumero
            ' --- FIN LOGIQUE CLÉ ---

            ' Maintenant, nous appelons ReassignPhraseNumbers() qui va :
            ' 1. Trier la liste complète en mémoire selon les NOUVEAUX numéros (qui viennent d'être échangés).
            ' 2. Réaffecter tous les numéros de manière séquentielle (1, 2, 3...) après le tri.
            ' 3. Forcer le rafraîchissement de la ListBox.
            ReassignPhraseNumbers()

            ' Resélectionner la phrase déplacée à sa nouvelle position
            lstPhraseDArmes.SelectedIndex = selectedIndex - 1

            ' Indiquer que le projet a été modifié pour la sauvegarde
            MarkAsDirtyInMainForm()
        End If
    End Sub

    Private Sub btnMoveDown_Click(sender As Object, e As EventArgs) Handles btnMoveDown.Click
        ' Récupérer l'index de la phrase actuellement sélectionnée
        Dim selectedIndex As Integer = lstPhraseDArmes.SelectedIndex

        ' Vérifier qu'une phrase est sélectionnée et qu'elle n'est pas la dernière de la liste
        If selectedIndex >= 0 AndAlso selectedIndex < ListePhraseDArmesDuProjet.Count - 1 Then
            ' Obtenir les références aux deux phrases concernées
            Dim selectedPhrase As PhraseDArmes = ListePhraseDArmesDuProjet(selectedIndex)
            Dim phraseBelow As PhraseDArmes = ListePhraseDArmesDuProjet(selectedIndex + 1)

            ' --- LOGIQUE CLÉ : Échanger UNIQUEMENT les numéros des deux phrases ---
            ' Nous stockons temporairement le numéro de la phrase du dessous
            Dim tempNumero As Integer = phraseBelow.Numero

            ' La phrase du dessous prend le numéro de la phrase sélectionnée
            phraseBelow.Numero = selectedPhrase.Numero

            ' La phrase sélectionnée prend l'ancien numéro de la phrase du dessous
            selectedPhrase.Numero = tempNumero
            ' --- FIN LOGIQUE CLÉ ---

            ' Appeler ReassignPhraseNumbers() pour trier, réassigner les numéros et rafraîchir
            ReassignPhraseNumbers()

            ' Resélectionner la phrase déplacée à sa nouvelle position
            lstPhraseDArmes.SelectedIndex = selectedIndex + 1

            ' Indiquer que le projet a été modifié pour la sauvegarde
            MarkAsDirtyInMainForm()
        End If
    End Sub





    ' --- Boutons de contrôle du formulaire (Annuler / Valider et Fermer) ---

    Private Sub btnCancel_Click(sender As Object, e As EventArgs) Handles btnCancel.Click
        Me.DialogResult = DialogResult.Cancel ' Indique que le dialogue a été annulé
        Me.Close()
    End Sub

    Private Sub btnSaveAndClose_Click(sender As Object, e As EventArgs) Handles btnSaveAndClose.Click
        Me.DialogResult = DialogResult.OK ' Indique que les changements sont à prendre en compte par le formulaire appelant
        Me.Close()
    End Sub

    ' --- Méthode pour notifier le formulaire principal d'une modification ---
    Public Sub MarkAsDirtyInMainForm()
        ' Tente de caster le propriétaire de ce formulaire (qui devrait être Form1) en Form1
        Dim mainForm As Form1 = CType(Me.Owner, Form1)
        If mainForm IsNot Nothing Then
            mainForm.MarkAsDirty() ' Appelle la méthode MarkAsDirty de Form1
        End If
    End Sub

    Private Sub btnEditActions_Click(sender As Object, e As EventArgs) Handles btnEditActions.Click
        If currentSelectedPhraseDArmes IsNot Nothing Then
            Using formActions As New FormEditActions()
                formActions.ListeActionsDuProjet = currentSelectedPhraseDArmes.ListeActions
                ' Passe la liste complète des objets Combattant, pas seulement les noms ou une sélection
                formActions.ListeCombattants = Me.CurrentProjet.ListeCombattants ' <-- PLUS de .Select(Function(c) c.Nom).ToList() ici !

                If formActions.ShowDialog(Me) = DialogResult.OK Then ' Passer 'Me' comme propriétaire
                    MarkAsDirtyInMainForm()
                End If
            End Using
        Else
            MessageBox.Show("Veuillez sélectionner une phrase d'armes pour éditer ses actions.", "Aucune Phrase Sélectionnée", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub
End Class