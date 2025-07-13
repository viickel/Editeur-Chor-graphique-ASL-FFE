<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FormEditCombattants
    Inherits System.Windows.Forms.Form

    'Form remplace la méthode Dispose pour nettoyer la liste des composants.
    <System.Diagnostics.DebuggerNonUserCode()> _
    Protected Overrides Sub Dispose(ByVal disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Requise par le Concepteur Windows Form
    Private components As System.ComponentModel.IContainer

    'REMARQUE : la procédure suivante est requise par le Concepteur Windows Form
    'Elle peut être modifiée à l'aide du Concepteur Windows Form.  
    'Ne la modifiez pas à l'aide de l'éditeur de code.
    <System.Diagnostics.DebuggerStepThrough()> _
    Private Sub InitializeComponent()
        lstCombattants = New ListBox()
        GroupBox1 = New GroupBox()
        txtLicence = New TextBox()
        txtPrenom = New TextBox()
        txtNom = New TextBox()
        txtID = New TextBox()
        labelLicence = New Label()
        labelPrenom = New Label()
        labelNom = New Label()
        labelID = New Label()
        btnAdd = New Button()
        btnUpdate = New Button()
        btnDelete = New Button()
        btnCancel = New Button()
        btnSaveAndClose = New Button()
        GroupBox1.SuspendLayout()
        SuspendLayout()
        ' 
        ' lstCombattants
        ' 
        lstCombattants.Anchor = AnchorStyles.Top Or AnchorStyles.Bottom Or AnchorStyles.Left
        lstCombattants.FormattingEnabled = True
        lstCombattants.Location = New Point(41, 12)
        lstCombattants.Name = "lstCombattants"
        lstCombattants.Size = New Size(373, 184)
        lstCombattants.TabIndex = 0
        ' 
        ' GroupBox1
        ' 
        GroupBox1.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        GroupBox1.Controls.Add(txtLicence)
        GroupBox1.Controls.Add(txtPrenom)
        GroupBox1.Controls.Add(txtNom)
        GroupBox1.Controls.Add(txtID)
        GroupBox1.Controls.Add(labelLicence)
        GroupBox1.Controls.Add(labelPrenom)
        GroupBox1.Controls.Add(labelNom)
        GroupBox1.Controls.Add(labelID)
        GroupBox1.Location = New Point(438, 12)
        GroupBox1.Name = "GroupBox1"
        GroupBox1.Size = New Size(350, 184)
        GroupBox1.TabIndex = 1
        GroupBox1.TabStop = False
        GroupBox1.Text = "Détails du Combattant"
        ' 
        ' txtLicence
        ' 
        txtLicence.Location = New Point(107, 142)
        txtLicence.Name = "txtLicence"
        txtLicence.Size = New Size(237, 27)
        txtLicence.TabIndex = 7
        ' 
        ' txtPrenom
        ' 
        txtPrenom.Location = New Point(107, 107)
        txtPrenom.Name = "txtPrenom"
        txtPrenom.Size = New Size(237, 27)
        txtPrenom.TabIndex = 6
        ' 
        ' txtNom
        ' 
        txtNom.Location = New Point(107, 71)
        txtNom.Name = "txtNom"
        txtNom.Size = New Size(237, 27)
        txtNom.TabIndex = 5
        ' 
        ' txtID
        ' 
        txtID.Location = New Point(107, 35)
        txtID.Name = "txtID"
        txtID.Size = New Size(237, 27)
        txtID.TabIndex = 4
        ' 
        ' labelLicence
        ' 
        labelLicence.AutoSize = True
        labelLicence.Location = New Point(39, 144)
        labelLicence.Name = "labelLicence"
        labelLicence.Size = New Size(58, 20)
        labelLicence.TabIndex = 3
        labelLicence.Text = "Licence"
        ' 
        ' labelPrenom
        ' 
        labelPrenom.AutoSize = True
        labelPrenom.Location = New Point(39, 109)
        labelPrenom.Name = "labelPrenom"
        labelPrenom.Size = New Size(60, 20)
        labelPrenom.TabIndex = 2
        labelPrenom.Text = "Prenom"
        ' 
        ' labelNom
        ' 
        labelNom.AutoSize = True
        labelNom.Location = New Point(39, 73)
        labelNom.Name = "labelNom"
        labelNom.Size = New Size(42, 20)
        labelNom.TabIndex = 1
        labelNom.Text = "Nom"
        ' 
        ' labelID
        ' 
        labelID.AutoSize = True
        labelID.Location = New Point(39, 37)
        labelID.Name = "labelID"
        labelID.Size = New Size(24, 20)
        labelID.TabIndex = 0
        labelID.Text = "ID"
        ' 
        ' btnAdd
        ' 
        btnAdd.Location = New Point(56, 241)
        btnAdd.Name = "btnAdd"
        btnAdd.Size = New Size(160, 29)
        btnAdd.TabIndex = 2
        btnAdd.Text = "Ajouter Nouveau"
        btnAdd.UseVisualStyleBackColor = True
        ' 
        ' btnUpdate
        ' 
        btnUpdate.Location = New Point(222, 241)
        btnUpdate.Name = "btnUpdate"
        btnUpdate.Size = New Size(103, 29)
        btnUpdate.TabIndex = 3
        btnUpdate.Text = "Mis a jours"
        btnUpdate.UseVisualStyleBackColor = True
        ' 
        ' btnDelete
        ' 
        btnDelete.Location = New Point(331, 241)
        btnDelete.Name = "btnDelete"
        btnDelete.Size = New Size(94, 29)
        btnDelete.TabIndex = 4
        btnDelete.Text = "Supprimer"
        btnDelete.UseVisualStyleBackColor = True
        ' 
        ' btnCancel
        ' 
        btnCancel.Location = New Point(438, 241)
        btnCancel.Name = "btnCancel"
        btnCancel.Size = New Size(94, 29)
        btnCancel.TabIndex = 5
        btnCancel.Text = "Annuler"
        btnCancel.UseVisualStyleBackColor = True
        ' 
        ' btnSaveAndClose
        ' 
        btnSaveAndClose.Location = New Point(558, 241)
        btnSaveAndClose.Name = "btnSaveAndClose"
        btnSaveAndClose.Size = New Size(155, 29)
        btnSaveAndClose.TabIndex = 6
        btnSaveAndClose.Text = "Valider et fermer"
        btnSaveAndClose.UseVisualStyleBackColor = True
        ' 
        ' FormEditCombattants
        ' 
        AutoScaleDimensions = New SizeF(8F, 20F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 450)
        Controls.Add(btnSaveAndClose)
        Controls.Add(btnCancel)
        Controls.Add(btnDelete)
        Controls.Add(btnUpdate)
        Controls.Add(btnAdd)
        Controls.Add(GroupBox1)
        Controls.Add(lstCombattants)
        Name = "FormEditCombattants"
        Text = "FormEditCombattants"
        GroupBox1.ResumeLayout(False)
        GroupBox1.PerformLayout()
        ResumeLayout(False)
    End Sub

    Friend WithEvents lstCombattants As ListBox
    Friend WithEvents GroupBox1 As GroupBox
    Friend WithEvents labelLicence As Label
    Friend WithEvents labelPrenom As Label
    Friend WithEvents labelNom As Label
    Friend WithEvents labelID As Label
    Friend WithEvents btnAdd As Button
    Friend WithEvents btnUpdate As Button
    Friend WithEvents btnDelete As Button
    Friend WithEvents btnCancel As Button
    Friend WithEvents btnSaveAndClose As Button
    Friend WithEvents txtID As TextBox
    Friend WithEvents txtLicence As TextBox
    Friend WithEvents txtPrenom As TextBox
    Friend WithEvents txtNom As TextBox
End Class
