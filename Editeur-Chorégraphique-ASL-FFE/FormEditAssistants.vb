Imports System.Collections.Generic
Imports System.ComponentModel ' Pour DesignerSerializationVisibility

Public Class FormEditAssistants

    ' Propriété publique pour passer et récupérer la liste des assistants
    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property ListeAssistantsDuProjet As List(Of Assistant)

    ' Pour le BindingSource, afin de lier la ListBox aux objets Assistant
    Private bsAssistants As New BindingSource()

    ' Pour stocker l'assistant actuellement sélectionné pour modification
    Private currentSelectedAssistant As Assistant

    Private Sub FormEditAssistants_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        ' Lier le BindingSource à la ListBox
        lstAssistants.DataSource = bsAssistants
        ' Indiquer quelle propriété de l'objet Assistant afficher dans la ListBox
        lstAssistants.DisplayMember = "ToString" ' Utilise la fonction ToString() de la classe Assistant

        ' Assigner la liste passée par le formulaire principal au BindingSource
        bsAssistants.DataSource = ListeAssistantsDuProjet
        bsAssistants.ResetBindings(False) ' Rafraîchir l'affichage

        ClearAssistantDetails() ' Réinitialise les champs de détails
    End Sub

    ' Méthode pour vider les champs de détails
    Private Sub ClearAssistantDetails()
        txtNom.Text = ""
        txtPrenom.Text = ""
        txtLicence.Text = ""
        currentSelectedAssistant = Nothing ' Réinitialise l'assistant sélectionné
        txtNom.Focus() ' Donne le focus au premier champ
        btnUpdate.Enabled = False
        btnDelete.Enabled = False
    End Sub

    ' Méthode pour afficher les détails de l'assistant sélectionné dans les TextBox
    Private Sub DisplayAssistantDetails(assistant As Assistant)
        If assistant IsNot Nothing Then
            txtNom.Text = assistant.Nom
            txtPrenom.Text = assistant.Prenom
            txtLicence.Text = assistant.NumeroLicence
            currentSelectedAssistant = assistant
            btnUpdate.Enabled = True
            btnDelete.Enabled = True
        Else
            ClearAssistantDetails()
        End If
    End Sub

    ' Événement de sélection dans la ListBox
    Private Sub lstAssistants_SelectedIndexChanged(sender As Object, e As EventArgs) Handles lstAssistants.SelectedIndexChanged
        If lstAssistants.SelectedItem IsNot Nothing Then
            DisplayAssistantDetails(CType(lstAssistants.SelectedItem, Assistant))
        Else
            ClearAssistantDetails()
        End If
    End Sub

    ' Bouton "Ajouter Nouveau"
    Private Sub btnAdd_Click(sender As Object, e As EventArgs) Handles btnAdd.Click
        ' Valider la saisie
        If String.IsNullOrWhiteSpace(txtNom.Text) OrElse String.IsNullOrWhiteSpace(txtPrenom.Text) Then
            MessageBox.Show("Le nom et le prénom de l'assistant sont obligatoires.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        Dim newAssistant As New Assistant(txtNom.Text, txtPrenom.Text, txtLicence.Text)
        ListeAssistantsDuProjet.Add(newAssistant) ' Ajoute à la liste du projet
        bsAssistants.ResetBindings(False) ' Rafraîchit la ListBox
        ClearAssistantDetails() ' Prépare pour une nouvelle saisie
        MarkAsDirtyInMainForm() ' Notifier le formulaire principal
    End Sub

    ' Bouton "Mettre à jour"
    Private Sub btnUpdate_Click(sender As Object, e As EventArgs) Handles btnUpdate.Click
        If currentSelectedAssistant IsNot Nothing Then
            ' Valider la saisie
            If String.IsNullOrWhiteSpace(txtNom.Text) OrElse String.IsNullOrWhiteSpace(txtPrenom.Text) Then
                MessageBox.Show("Le nom et le prénom de l'assistant sont obligatoires.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                Return
            End If

            currentSelectedAssistant.Nom = txtNom.Text
            currentSelectedAssistant.Prenom = txtPrenom.Text
            currentSelectedAssistant.NumeroLicence = txtLicence.Text

            bsAssistants.ResetBindings(False) ' Rafraîchit la ListBox pour afficher les changements
            DisplayAssistantDetails(currentSelectedAssistant) ' Réafficher les détails mis à jour
            MarkAsDirtyInMainForm()
        Else
            MessageBox.Show("Veuillez sélectionner un assistant à mettre à jour.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    ' Bouton "Supprimer"
    Private Sub btnDelete_Click(sender As Object, e As EventArgs) Handles btnDelete.Click
        If currentSelectedAssistant IsNot Nothing Then
            Dim result As DialogResult = MessageBox.Show($"Êtes-vous sûr de vouloir supprimer {currentSelectedAssistant.Prenom} {currentSelectedAssistant.Nom} ?", "Confirmer la suppression", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
            If result = DialogResult.Yes Then
                ListeAssistantsDuProjet.Remove(currentSelectedAssistant)
                bsAssistants.ResetBindings(False) ' Rafraîchit la ListBox
                ClearAssistantDetails()
                MarkAsDirtyInMainForm() ' Notifier le formulaire principal
            End If
        Else
            MessageBox.Show("Veuillez sélectionner un assistant à supprimer.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    ' Bouton "Annuler" (ferme le dialogue sans sauvegarder les changements)
    Private Sub btnCancel_Click(sender As Object, e As EventArgs) Handles btnCancel.Click
        Me.DialogResult = DialogResult.Cancel ' Indique que le dialogue a été annulé
        Me.Close()
    End Sub

    ' Bouton "Valider et Fermer" (sauvegarde les changements et ferme le dialogue)
    Private Sub btnSaveAndClose_Click(sender As Object, e As EventArgs) Handles btnSaveAndClose.Click
        Me.DialogResult = DialogResult.OK ' Indique que les changements sont à prendre en compte
        Me.Close()
    End Sub

    ' Propriété pour indiquer au formulaire principal si des modifications ont été faites
    Private Sub MarkAsDirtyInMainForm()
        Dim mainForm As Form1 = CType(Me.Owner, Form1)
        If mainForm IsNot Nothing Then
            mainForm.MarkAsDirty()
        End If
    End Sub

End Class