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
        grpDetailsAssistant.SuspendLayout()
        SuspendLayout()
        ' 
        ' grpDetailsAssistant
        ' 
        grpDetailsAssistant.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        grpDetailsAssistant.Controls.Add(txtLicence)
        grpDetailsAssistant.Controls.Add(txtPrenom)
        grpDetailsAssistant.Controls.Add(txtNom)
        grpDetailsAssistant.Controls.Add(labelLicence)
        grpDetailsAssistant.Controls.Add(labelPrenom)
        grpDetailsAssistant.Controls.Add(labelNom)
        grpDetailsAssistant.Location = New Point(424, 27)
        grpDetailsAssistant.Name = "grpDetailsAssistant"
        grpDetailsAssistant.Size = New Size(350, 184)
        grpDetailsAssistant.TabIndex = 8
        grpDetailsAssistant.TabStop = False
        grpDetailsAssistant.Text = "Détails de l'Assistant"
        ' 
        ' txtLicence
        ' 
        txtLicence.Location = New Point(107, 107)
        txtLicence.Name = "txtLicence"
        txtLicence.Size = New Size(237, 27)
        txtLicence.TabIndex = 7
        ' 
        ' txtPrenom
        ' 
        txtPrenom.Location = New Point(107, 72)
        txtPrenom.Name = "txtPrenom"
        txtPrenom.Size = New Size(237, 27)
        txtPrenom.TabIndex = 6
        ' 
        ' txtNom
        ' 
        txtNom.Location = New Point(107, 36)
        txtNom.Name = "txtNom"
        txtNom.Size = New Size(237, 27)
        txtNom.TabIndex = 5
        ' 
        ' labelLicence
        ' 
        labelLicence.AutoSize = True
        labelLicence.Location = New Point(39, 109)
        labelLicence.Name = "labelLicence"
        labelLicence.Size = New Size(58, 20)
        labelLicence.TabIndex = 3
        labelLicence.Text = "Licence"
        ' 
        ' labelPrenom
        ' 
        labelPrenom.AutoSize = True
        labelPrenom.Location = New Point(39, 74)
        labelPrenom.Name = "labelPrenom"
        labelPrenom.Size = New Size(60, 20)
        labelPrenom.TabIndex = 2
        labelPrenom.Text = "Prenom"
        ' 
        ' labelNom
        ' 
        labelNom.AutoSize = True
        labelNom.Location = New Point(39, 38)
        labelNom.Name = "labelNom"
        labelNom.Size = New Size(42, 20)
        labelNom.TabIndex = 1
        labelNom.Text = "Nom"
        ' 
        ' lstAssistants
        ' 
        lstAssistants.Anchor = AnchorStyles.Top Or AnchorStyles.Bottom Or AnchorStyles.Left
        lstAssistants.FormattingEnabled = True
        lstAssistants.Location = New Point(27, 27)
        lstAssistants.Name = "lstAssistants"
        lstAssistants.Size = New Size(373, 184)
        lstAssistants.TabIndex = 7
        ' 
        ' btnSaveAndClose
        ' 
        btnSaveAndClose.Location = New Point(544, 256)
        btnSaveAndClose.Name = "btnSaveAndClose"
        btnSaveAndClose.Size = New Size(155, 29)
        btnSaveAndClose.TabIndex = 13
        btnSaveAndClose.Text = "Valider et fermer"
        btnSaveAndClose.UseVisualStyleBackColor = True
        ' 
        ' btnCancel
        ' 
        btnCancel.Location = New Point(424, 256)
        btnCancel.Name = "btnCancel"
        btnCancel.Size = New Size(94, 29)
        btnCancel.TabIndex = 12
        btnCancel.Text = "Annuler"
        btnCancel.UseVisualStyleBackColor = True
        ' 
        ' btnDelete
        ' 
        btnDelete.Location = New Point(317, 256)
        btnDelete.Name = "btnDelete"
        btnDelete.Size = New Size(94, 29)
        btnDelete.TabIndex = 11
        btnDelete.Text = "Supprimer"
        btnDelete.UseVisualStyleBackColor = True
        ' 
        ' btnUpdate
        ' 
        btnUpdate.Location = New Point(208, 256)
        btnUpdate.Name = "btnUpdate"
        btnUpdate.Size = New Size(103, 29)
        btnUpdate.TabIndex = 10
        btnUpdate.Text = "Mis a jours"
        btnUpdate.UseVisualStyleBackColor = True
        ' 
        ' btnAdd
        ' 
        btnAdd.Location = New Point(42, 256)
        btnAdd.Name = "btnAdd"
        btnAdd.Size = New Size(160, 29)
        btnAdd.TabIndex = 9
        btnAdd.Text = "Ajouter Nouveau"
        btnAdd.UseVisualStyleBackColor = True
        ' 
        ' FormEditAssistants
        ' 
        AutoScaleDimensions = New SizeF(8F, 20F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 358)
        Controls.Add(grpDetailsAssistant)
        Controls.Add(lstAssistants)
        Controls.Add(btnSaveAndClose)
        Controls.Add(btnCancel)
        Controls.Add(btnDelete)
        Controls.Add(btnUpdate)
        Controls.Add(btnAdd)
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
End Class
