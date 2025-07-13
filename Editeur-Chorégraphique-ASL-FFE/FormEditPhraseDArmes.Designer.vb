<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FormEditPhraseDArmes
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
        lstPhraseDArmes = New ListBox()
        grpDetailsPhraseDArmes = New GroupBox()
        btnEditActions = New Button()
        btnDeletePhrase = New Button()
        btnUpdatePhrase = New Button()
        btnAddPhrase = New Button()
        rtbDescriptionSection = New RichTextBox()
        LabelDescription = New Label()
        txtNumero = New TextBox()
        LabelNum = New Label()
        btnMoveUp = New Button()
        btnMoveDown = New Button()
        btnCancel = New Button()
        btnSaveAndClose = New Button()
        grpDetailsPhraseDArmes.SuspendLayout()
        SuspendLayout()
        ' 
        ' lstPhraseDArmes
        ' 
        lstPhraseDArmes.Anchor = AnchorStyles.Top Or AnchorStyles.Bottom Or AnchorStyles.Left
        lstPhraseDArmes.FormattingEnabled = True
        lstPhraseDArmes.Location = New Point(30, 31)
        lstPhraseDArmes.Name = "lstPhraseDArmes"
        lstPhraseDArmes.Size = New Size(224, 384)
        lstPhraseDArmes.TabIndex = 0
        ' 
        ' grpDetailsPhraseDArmes
        ' 
        grpDetailsPhraseDArmes.Controls.Add(btnEditActions)
        grpDetailsPhraseDArmes.Controls.Add(btnDeletePhrase)
        grpDetailsPhraseDArmes.Controls.Add(btnUpdatePhrase)
        grpDetailsPhraseDArmes.Controls.Add(btnAddPhrase)
        grpDetailsPhraseDArmes.Controls.Add(rtbDescriptionSection)
        grpDetailsPhraseDArmes.Controls.Add(LabelDescription)
        grpDetailsPhraseDArmes.Controls.Add(txtNumero)
        grpDetailsPhraseDArmes.Controls.Add(LabelNum)
        grpDetailsPhraseDArmes.Location = New Point(376, 31)
        grpDetailsPhraseDArmes.Name = "grpDetailsPhraseDArmes"
        grpDetailsPhraseDArmes.Size = New Size(412, 355)
        grpDetailsPhraseDArmes.TabIndex = 1
        grpDetailsPhraseDArmes.TabStop = False
        grpDetailsPhraseDArmes.Text = "Details phrase d'armes"
        ' 
        ' btnEditActions
        ' 
        btnEditActions.Location = New Point(22, 284)
        btnEditActions.Name = "btnEditActions"
        btnEditActions.Size = New Size(145, 29)
        btnEditActions.TabIndex = 6
        btnEditActions.Text = "Editer Action"
        btnEditActions.UseVisualStyleBackColor = True
        ' 
        ' btnDeletePhrase
        ' 
        btnDeletePhrase.Location = New Point(315, 227)
        btnDeletePhrase.Name = "btnDeletePhrase"
        btnDeletePhrase.Size = New Size(94, 29)
        btnDeletePhrase.TabIndex = 5
        btnDeletePhrase.Text = "Supprimer"
        btnDeletePhrase.UseVisualStyleBackColor = True
        ' 
        ' btnUpdatePhrase
        ' 
        btnUpdatePhrase.Location = New Point(161, 227)
        btnUpdatePhrase.Name = "btnUpdatePhrase"
        btnUpdatePhrase.Size = New Size(117, 29)
        btnUpdatePhrase.TabIndex = 4
        btnUpdatePhrase.Text = "Mettre à jour"
        btnUpdatePhrase.UseVisualStyleBackColor = True
        ' 
        ' btnAddPhrase
        ' 
        btnAddPhrase.Location = New Point(22, 227)
        btnAddPhrase.Name = "btnAddPhrase"
        btnAddPhrase.Size = New Size(118, 29)
        btnAddPhrase.TabIndex = 3
        btnAddPhrase.Text = "Ajouter Phrase"
        btnAddPhrase.UseVisualStyleBackColor = True
        ' 
        ' rtbDescriptionSection
        ' 
        rtbDescriptionSection.Anchor = AnchorStyles.Top Or AnchorStyles.Left Or AnchorStyles.Right
        rtbDescriptionSection.Location = New Point(22, 110)
        rtbDescriptionSection.Name = "rtbDescriptionSection"
        rtbDescriptionSection.Size = New Size(375, 111)
        rtbDescriptionSection.TabIndex = 2
        rtbDescriptionSection.Text = ""
        ' 
        ' LabelDescription
        ' 
        LabelDescription.Anchor = AnchorStyles.Top Or AnchorStyles.Left Or AnchorStyles.Right
        LabelDescription.AutoSize = True
        LabelDescription.Location = New Point(22, 87)
        LabelDescription.Name = "LabelDescription"
        LabelDescription.Size = New Size(92, 20)
        LabelDescription.TabIndex = 1
        LabelDescription.Text = "Description :"
        ' 
        ' txtNumero
        ' 
        txtNumero.Anchor = AnchorStyles.Top Or AnchorStyles.Left Or AnchorStyles.Right
        txtNumero.Location = New Point(98, 31)
        txtNumero.Name = "txtNumero"
        txtNumero.ReadOnly = True
        txtNumero.Size = New Size(79, 27)
        txtNumero.TabIndex = 0
        ' 
        ' LabelNum
        ' 
        LabelNum.Anchor = AnchorStyles.Top Or AnchorStyles.Left Or AnchorStyles.Right
        LabelNum.AutoSize = True
        LabelNum.Location = New Point(22, 34)
        LabelNum.Name = "LabelNum"
        LabelNum.Size = New Size(70, 20)
        LabelNum.TabIndex = 0
        LabelNum.Text = "Numéro :"
        ' 
        ' btnMoveUp
        ' 
        btnMoveUp.Location = New Point(260, 118)
        btnMoveUp.Name = "btnMoveUp"
        btnMoveUp.Size = New Size(86, 29)
        btnMoveUp.TabIndex = 2
        btnMoveUp.Text = "Monter"
        btnMoveUp.UseVisualStyleBackColor = True
        ' 
        ' btnMoveDown
        ' 
        btnMoveDown.Location = New Point(260, 191)
        btnMoveDown.Name = "btnMoveDown"
        btnMoveDown.Size = New Size(86, 29)
        btnMoveDown.TabIndex = 3
        btnMoveDown.Text = "Decendre"
        btnMoveDown.UseVisualStyleBackColor = True
        ' 
        ' btnCancel
        ' 
        btnCancel.Location = New Point(537, 403)
        btnCancel.Name = "btnCancel"
        btnCancel.Size = New Size(110, 29)
        btnCancel.TabIndex = 4
        btnCancel.Text = "Annuler"
        btnCancel.UseVisualStyleBackColor = True
        ' 
        ' btnSaveAndClose
        ' 
        btnSaveAndClose.Location = New Point(653, 403)
        btnSaveAndClose.Name = "btnSaveAndClose"
        btnSaveAndClose.Size = New Size(132, 29)
        btnSaveAndClose.TabIndex = 5
        btnSaveAndClose.Text = "Valider et Fermer"
        btnSaveAndClose.UseVisualStyleBackColor = True
        ' 
        ' FormEditPhraseDArmes
        ' 
        AutoScaleDimensions = New SizeF(8F, 20F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 450)
        Controls.Add(btnSaveAndClose)
        Controls.Add(btnCancel)
        Controls.Add(btnMoveDown)
        Controls.Add(btnMoveUp)
        Controls.Add(grpDetailsPhraseDArmes)
        Controls.Add(lstPhraseDArmes)
        Name = "FormEditPhraseDArmes"
        Text = "FormEditPhraseDArmes"
        grpDetailsPhraseDArmes.ResumeLayout(False)
        grpDetailsPhraseDArmes.PerformLayout()
        ResumeLayout(False)
    End Sub

    Friend WithEvents lstPhraseDArmes As ListBox
    Friend WithEvents grpDetailsPhraseDArmes As GroupBox
    Friend WithEvents rtbDescriptionSection As RichTextBox
    Friend WithEvents LabelDescription As Label
    Friend WithEvents txtNumero As TextBox
    Friend WithEvents LabelNum As Label
    Friend WithEvents btnDeletePhrase As Button
    Friend WithEvents btnUpdatePhrase As Button
    Friend WithEvents btnAddPhrase As Button
    Friend WithEvents btnMoveUp As Button
    Friend WithEvents btnMoveDown As Button
    Friend WithEvents btnEditActions As Button
    Friend WithEvents btnCancel As Button
    Friend WithEvents btnSaveAndClose As Button
End Class
