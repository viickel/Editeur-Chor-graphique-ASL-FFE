<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FormEditAssistants
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
        grpDetailsAssistant = New GroupBox()
        txtLicence = New TextBox()
        txtPrenom = New TextBox()
        txtNom = New TextBox()
        labelLicence = New Label()
        labelPrenom = New Label()
        labelNom = New Label()
        lstAssistants = New ListBox()
        btnSaveAndClose = New Button()
        btnCancel = New Button()
        btnDelete = New Button()
        btnUpdate = New Button()
        btnAdd = New Button()
        TxtRole = New TextBox()
        Label1 = New Label()
        grpDetailsAssistant.SuspendLayout()
        SuspendLayout()
        ' 
        ' grpDetailsAssistant
        ' 
        grpDetailsAssistant.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        grpDetailsAssistant.Controls.Add(TxtRole)
        grpDetailsAssistant.Controls.Add(Label1)
        grpDetailsAssistant.Controls.Add(txtLicence)
        grpDetailsAssistant.Controls.Add(txtPrenom)
        grpDetailsAssistant.Controls.Add(txtNom)
        grpDetailsAssistant.Controls.Add(labelLicence)
        grpDetailsAssistant.Controls.Add(labelPrenom)
        grpDetailsAssistant.Controls.Add(labelNom)
        grpDetailsAssistant.Location = New Point(371, 20)
        grpDetailsAssistant.Margin = New Padding(3, 2, 3, 2)
        grpDetailsAssistant.Name = "grpDetailsAssistant"
        grpDetailsAssistant.Padding = New Padding(3, 2, 3, 2)
        grpDetailsAssistant.Size = New Size(306, 138)
        grpDetailsAssistant.TabIndex = 8
        grpDetailsAssistant.TabStop = False
        grpDetailsAssistant.Text = "Détails de l'Assistant"
        ' 
        ' txtLicence
        ' 
        txtLicence.Location = New Point(94, 80)
        txtLicence.Margin = New Padding(3, 2, 3, 2)
        txtLicence.Name = "txtLicence"
        txtLicence.Size = New Size(208, 23)
        txtLicence.TabIndex = 7
        ' 
        ' txtPrenom
        ' 
        txtPrenom.Location = New Point(94, 54)
        txtPrenom.Margin = New Padding(3, 2, 3, 2)
        txtPrenom.Name = "txtPrenom"
        txtPrenom.Size = New Size(208, 23)
        txtPrenom.TabIndex = 6
        ' 
        ' txtNom
        ' 
        txtNom.Location = New Point(94, 27)
        txtNom.Margin = New Padding(3, 2, 3, 2)
        txtNom.Name = "txtNom"
        txtNom.Size = New Size(208, 23)
        txtNom.TabIndex = 5
        ' 
        ' labelLicence
        ' 
        labelLicence.AutoSize = True
        labelLicence.Location = New Point(34, 82)
        labelLicence.Name = "labelLicence"
        labelLicence.Size = New Size(47, 15)
        labelLicence.TabIndex = 3
        labelLicence.Text = "Licence"
        ' 
        ' labelPrenom
        ' 
        labelPrenom.AutoSize = True
        labelPrenom.Location = New Point(34, 56)
        labelPrenom.Name = "labelPrenom"
        labelPrenom.Size = New Size(49, 15)
        labelPrenom.TabIndex = 2
        labelPrenom.Text = "Prenom"
        ' 
        ' labelNom
        ' 
        labelNom.AutoSize = True
        labelNom.Location = New Point(34, 28)
        labelNom.Name = "labelNom"
        labelNom.Size = New Size(34, 15)
        labelNom.TabIndex = 1
        labelNom.Text = "Nom"
        ' 
        ' lstAssistants
        ' 
        lstAssistants.Anchor = AnchorStyles.Top Or AnchorStyles.Bottom Or AnchorStyles.Left
        lstAssistants.FormattingEnabled = True
        lstAssistants.Location = New Point(24, 20)
        lstAssistants.Margin = New Padding(3, 2, 3, 2)
        lstAssistants.Name = "lstAssistants"
        lstAssistants.Size = New Size(327, 139)
        lstAssistants.TabIndex = 7
        ' 
        ' btnSaveAndClose
        ' 
        btnSaveAndClose.Location = New Point(476, 192)
        btnSaveAndClose.Margin = New Padding(3, 2, 3, 2)
        btnSaveAndClose.Name = "btnSaveAndClose"
        btnSaveAndClose.Size = New Size(136, 22)
        btnSaveAndClose.TabIndex = 13
        btnSaveAndClose.Text = "Valider et fermer"
        btnSaveAndClose.UseVisualStyleBackColor = True
        ' 
        ' btnCancel
        ' 
        btnCancel.Location = New Point(371, 192)
        btnCancel.Margin = New Padding(3, 2, 3, 2)
        btnCancel.Name = "btnCancel"
        btnCancel.Size = New Size(82, 22)
        btnCancel.TabIndex = 12
        btnCancel.Text = "Annuler"
        btnCancel.UseVisualStyleBackColor = True
        ' 
        ' btnDelete
        ' 
        btnDelete.Location = New Point(277, 192)
        btnDelete.Margin = New Padding(3, 2, 3, 2)
        btnDelete.Name = "btnDelete"
        btnDelete.Size = New Size(82, 22)
        btnDelete.TabIndex = 11
        btnDelete.Text = "Supprimer"
        btnDelete.UseVisualStyleBackColor = True
        ' 
        ' btnUpdate
        ' 
        btnUpdate.Location = New Point(182, 192)
        btnUpdate.Margin = New Padding(3, 2, 3, 2)
        btnUpdate.Name = "btnUpdate"
        btnUpdate.Size = New Size(90, 22)
        btnUpdate.TabIndex = 10
        btnUpdate.Text = "Mis a jours"
        btnUpdate.UseVisualStyleBackColor = True
        ' 
        ' btnAdd
        ' 
        btnAdd.Location = New Point(37, 192)
        btnAdd.Margin = New Padding(3, 2, 3, 2)
        btnAdd.Name = "btnAdd"
        btnAdd.Size = New Size(140, 22)
        btnAdd.TabIndex = 9
        btnAdd.Text = "Ajouter Nouveau"
        btnAdd.UseVisualStyleBackColor = True
        ' 
        ' TxtRole
        ' 
        TxtRole.Location = New Point(95, 108)
        TxtRole.Margin = New Padding(3, 2, 3, 2)
        TxtRole.Name = "TxtRole"
        TxtRole.Size = New Size(208, 23)
        TxtRole.TabIndex = 9
        ' 
        ' Label1
        ' 
        Label1.AutoSize = True
        Label1.Location = New Point(35, 110)
        Label1.Name = "Label1"
        Label1.Size = New Size(30, 15)
        Label1.TabIndex = 8
        Label1.Text = "Rôle"
        ' 
        ' FormEditAssistants
        ' 
        AutoScaleDimensions = New SizeF(7F, 15F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(700, 268)
        Controls.Add(grpDetailsAssistant)
        Controls.Add(lstAssistants)
        Controls.Add(btnSaveAndClose)
        Controls.Add(btnCancel)
        Controls.Add(btnDelete)
        Controls.Add(btnUpdate)
        Controls.Add(btnAdd)
        Margin = New Padding(3, 2, 3, 2)
        Name = "FormEditAssistants"
        Text = "FormEditAssistants"
        grpDetailsAssistant.ResumeLayout(False)
        grpDetailsAssistant.PerformLayout()
        ResumeLayout(False)
    End Sub

    Friend WithEvents grpDetailsAssistant As GroupBox
    Friend WithEvents txtLicence As TextBox
    Friend WithEvents txtPrenom As TextBox
    Friend WithEvents txtNom As TextBox
    Friend WithEvents labelLicence As Label
    Friend WithEvents labelPrenom As Label
    Friend WithEvents labelNom As Label
    Friend WithEvents lstAssistants As ListBox
    Friend WithEvents btnSaveAndClose As Button
    Friend WithEvents btnCancel As Button
    Friend WithEvents btnDelete As Button
    Friend WithEvents btnUpdate As Button
    Friend WithEvents btnAdd As Button
    Friend WithEvents TxtRole As TextBox
    Friend WithEvents Label1 As Label
End Class
