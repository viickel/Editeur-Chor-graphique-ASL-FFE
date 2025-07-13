Imports System.Collections.Generic ' Pour utiliser List(Of T)
Imports System.ComponentModel
Public Class FormEditCombattants

    ' Propriété publique pour passer et récupérer la liste des combattants
    <DesignerSerializationVisibility(DesignerSerializationVisibility.Hidden)>
    Public Property ListeCombattantsDuProjet As List(Of Combattant)

    ' Pour le BindingSource, afin de lier la ListBox aux objets Combattant
    Private bsCombattants As New BindingSource()

    ' Pour stocker le combattant actuellement sélectionné pour modification
    Private currentSelectedCombattant As Combattant

    Private Sub FormEditCombattants_Load(sender As Object, e As EventArgs) Handles MyBase.Load
        ' Lier le BindingSource à la ListBox
        lstCombattants.DataSource = bsCombattants
        ' Indiquer quelle propriété de l'objet Combattant afficher dans la ListBox
        lstCombattants.DisplayMember = "ToString" ' Utilise la fonction ToString() de la classe Combattant

        ' Assigner la liste passée par le formulaire principal au BindingSource
        bsCombattants.DataSource = ListeCombattantsDuProjet
        bsCombattants.ResetBindings(False) ' Rafraîchir l'affichage

        ClearCombattantDetails() ' Réinitialise les champs de détails
    End Sub

    ' Méthode pour vider les champs de détails
    Private Sub ClearCombattantDetails()
        txtID.Text = ""
        txtNom.Text = ""
        txtPrenom.Text = ""
        txtLicence.Text = ""
        currentSelectedCombattant = Nothing ' Réinitialise le combattant sélectionné
        txtNom.Focus() ' Donne le focus au premier champ
        btnUpdate.Enabled = False
        btnDelete.Enabled = False
    End Sub

    ' Méthode pour afficher les détails du combattant sélectionné dans les TextBox
    Private Sub DisplayCombattantDetails(combattant As Combattant)
        If combattant IsNot Nothing Then
            txtID.Text = combattant.ID.ToString()
            txtNom.Text = combattant.Nom
            txtPrenom.Text = combattant.Prenom
            txtLicence.Text = combattant.NumeroLicence
            currentSelectedCombattant = combattant
            btnUpdate.Enabled = True
            btnDelete.Enabled = True
        Else
            ClearCombattantDetails()
        End If
    End Sub

    ' Événement de sélection dans la ListBox
    Private Sub lstCombattants_SelectedIndexChanged(sender As Object, e As EventArgs) Handles lstCombattants.SelectedIndexChanged
        If lstCombattants.SelectedItem IsNot Nothing Then
            DisplayCombattantDetails(CType(lstCombattants.SelectedItem, Combattant))
        Else
            ClearCombattantDetails()
        End If
    End Sub

    ' Bouton "Ajouter Nouveau"
    Private Sub btnAdd_Click(sender As Object, e As EventArgs) Handles btnAdd.Click
        ' Valider la saisie
        If String.IsNullOrWhiteSpace(txtNom.Text) OrElse String.IsNullOrWhiteSpace(txtPrenom.Text) Then
            MessageBox.Show("Le nom et le prénom du combattant sont obligatoires.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
            Return
        End If

        ' Générer un nouvel ID (simple incrément pour l'exemple)
        Dim newID As Integer = 1
        If ListeCombattantsDuProjet.Any() Then
            newID = ListeCombattantsDuProjet.Max(Function(c) c.ID) + 1
        End If

        Dim newCombattant As New Combattant(newID, txtNom.Text, txtPrenom.Text, txtLicence.Text)
        ListeCombattantsDuProjet.Add(newCombattant) ' Ajoute à la liste du projet
        bsCombattants.ResetBindings(False) ' Rafraîchit la ListBox
        ClearCombattantDetails() ' Prépare pour une nouvelle saisie
        MarkAsDirtyInMainForm() ' Notifier le formulaire principal
    End Sub

    ' Bouton "Mettre à jour"
    Private Sub btnUpdate_Click(sender As Object, e As EventArgs) Handles btnUpdate.Click
        If currentSelectedCombattant IsNot Nothing Then
            ' Valider la saisie
            If String.IsNullOrWhiteSpace(txtNom.Text) OrElse String.IsNullOrWhiteSpace(txtPrenom.Text) Then
                MessageBox.Show("Le nom et le prénom du combattant sont obligatoires.", "Saisie Incomplète", MessageBoxButtons.OK, MessageBoxIcon.Warning)
                Return
            End If

            currentSelectedCombattant.Nom = txtNom.Text
            currentSelectedCombattant.Prenom = txtPrenom.Text
            currentSelectedCombattant.NumeroLicence = txtLicence.Text

            bsCombattants.ResetBindings(False) ' Rafraîchit la ListBox pour afficher les changements
            ClearCombattantDetails()
            MarkAsDirtyInMainForm() ' Notifier le formulaire principal
        Else
            MessageBox.Show("Veuillez sélectionner un combattant à mettre à jour.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
        End If
    End Sub

    ' Bouton "Supprimer"
    Private Sub btnDelete_Click(sender As Object, e As EventArgs) Handles btnDelete.Click
        If currentSelectedCombattant IsNot Nothing Then
            Dim result As DialogResult = MessageBox.Show($"Êtes-vous sûr de vouloir supprimer {currentSelectedCombattant.Prenom} {currentSelectedCombattant.Nom} ?", "Confirmer la suppression", MessageBoxButtons.YesNo, MessageBoxIcon.Question)
            If result = DialogResult.Yes Then
                ListeCombattantsDuProjet.Remove(currentSelectedCombattant)
                bsCombattants.ResetBindings(False) ' Rafraîchit la ListBox
                ClearCombattantDetails()
                MarkAsDirtyInMainForm() ' Notifier le formulaire principal
            End If
        Else
            MessageBox.Show("Veuillez sélectionner un combattant à supprimer.", "Attention", MessageBoxButtons.OK, MessageBoxIcon.Information)
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
    ' C'est une méthode simple pour l'exemple. On pourrait aussi passer un booléen en paramètre
    ' du DialogResult si nécessaire.
    Private Sub MarkAsDirtyInMainForm()
        ' Nous allons appeler la méthode MarkAsDirty du Form1 directement depuis ici.
        ' Pour cela, Form1 doit être accessible.
        ' Une manière simple pour un dialogue est de le rendre modale et de vérifier les changements
        ' après qu'il soit fermé, mais pour simplifier l'exemple, nous allons le faire directement.
        ' C'est une simplification pour l'exercice. Dans une application plus complexe,
        ' on utiliserait des événements ou des interfaces.
        Dim mainForm As Form1 = CType(Me.Owner, Form1)
        If mainForm IsNot Nothing Then
            mainForm.MarkAsDirty()
        End If
    End Sub


End Class