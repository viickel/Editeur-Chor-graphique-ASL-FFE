<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()> _
Partial Class FormEditActions
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
        components = New ComponentModel.Container()
        btnCancelActions = New Button()
        btnMoveActionDown = New Button()
        btnValidateActions = New Button()
        btnMoveActionUp = New Button()
        btnDeleteAction = New Button()
        btnEditAction = New Button()
        btnAddAction = New Button()
        SplitContainer1 = New SplitContainer()
        lbxCombattants = New ListBox()
        dgvActions = New DataGridView()
        bsActionsLocal = New BindingSource(components)
        CType(SplitContainer1, ComponentModel.ISupportInitialize).BeginInit()
        SplitContainer1.Panel1.SuspendLayout()
        SplitContainer1.Panel2.SuspendLayout()
        SplitContainer1.SuspendLayout()
        CType(dgvActions, ComponentModel.ISupportInitialize).BeginInit()
        CType(bsActionsLocal, ComponentModel.ISupportInitialize).BeginInit()
        SuspendLayout()
        ' 
        ' btnCancelActions
        ' 
        btnCancelActions.Location = New Point(642, 87)
        btnCancelActions.Name = "btnCancelActions"
        btnCancelActions.Size = New Size(136, 29)
        btnCancelActions.TabIndex = 6
        btnCancelActions.Text = "Annuler et fermer"
        btnCancelActions.UseVisualStyleBackColor = True
        ' 
        ' btnMoveActionDown
        ' 
        btnMoveActionDown.Location = New Point(433, 87)
        btnMoveActionDown.Name = "btnMoveActionDown"
        btnMoveActionDown.Size = New Size(136, 29)
        btnMoveActionDown.TabIndex = 5
        btnMoveActionDown.Text = "Decendre action"
        btnMoveActionDown.UseVisualStyleBackColor = True
        ' 
        ' btnValidateActions
        ' 
        btnValidateActions.Location = New Point(642, 12)
        btnValidateActions.Name = "btnValidateActions"
        btnValidateActions.Size = New Size(136, 29)
        btnValidateActions.TabIndex = 4
        btnValidateActions.Text = "Valider et fermer"
        btnValidateActions.UseVisualStyleBackColor = True
        ' 
        ' btnMoveActionUp
        ' 
        btnMoveActionUp.Location = New Point(433, 12)
        btnMoveActionUp.Name = "btnMoveActionUp"
        btnMoveActionUp.Size = New Size(136, 29)
        btnMoveActionUp.TabIndex = 3
        btnMoveActionUp.Text = "monter Action"
        btnMoveActionUp.UseVisualStyleBackColor = True
        ' 
        ' btnDeleteAction
        ' 
        btnDeleteAction.Location = New Point(229, 87)
        btnDeleteAction.Name = "btnDeleteAction"
        btnDeleteAction.Size = New Size(136, 29)
        btnDeleteAction.TabIndex = 2
        btnDeleteAction.Text = "Supprimer Action"
        btnDeleteAction.UseVisualStyleBackColor = True
        ' 
        ' btnEditAction
        ' 
        btnEditAction.Location = New Point(229, 47)
        btnEditAction.Name = "btnEditAction"
        btnEditAction.Size = New Size(136, 29)
        btnEditAction.TabIndex = 1
        btnEditAction.Text = "Editer action"
        btnEditAction.UseVisualStyleBackColor = True
        ' 
        ' btnAddAction
        ' 
        btnAddAction.Location = New Point(229, 12)
        btnAddAction.Name = "btnAddAction"
        btnAddAction.Size = New Size(136, 29)
        btnAddAction.TabIndex = 0
        btnAddAction.Text = "Ajouter Action"
        btnAddAction.UseVisualStyleBackColor = True
        ' 
        ' SplitContainer1
        ' 
        SplitContainer1.Dock = DockStyle.Fill
        SplitContainer1.Location = New Point(0, 0)
        SplitContainer1.Name = "SplitContainer1"
        SplitContainer1.Orientation = Orientation.Horizontal
        ' 
        ' SplitContainer1.Panel1
        ' 
        SplitContainer1.Panel1.Controls.Add(btnCancelActions)
        SplitContainer1.Panel1.Controls.Add(lbxCombattants)
        SplitContainer1.Panel1.Controls.Add(btnValidateActions)
        SplitContainer1.Panel1.Controls.Add(btnMoveActionDown)
        SplitContainer1.Panel1.Controls.Add(btnAddAction)
        SplitContainer1.Panel1.Controls.Add(btnEditAction)
        SplitContainer1.Panel1.Controls.Add(btnMoveActionUp)
        SplitContainer1.Panel1.Controls.Add(btnDeleteAction)
        ' 
        ' SplitContainer1.Panel2
        ' 
        SplitContainer1.Panel2.Controls.Add(dgvActions)
        SplitContainer1.Size = New Size(800, 501)
        SplitContainer1.SplitterDistance = 138
        SplitContainer1.TabIndex = 1
        ' 
        ' lbxCombattants
        ' 
        lbxCombattants.FormattingEnabled = True
        lbxCombattants.Location = New Point(12, 12)
        lbxCombattants.Name = "lbxCombattants"
        lbxCombattants.Size = New Size(182, 104)
        lbxCombattants.TabIndex = 0
        ' 
        ' dgvActions
        ' 
        dgvActions.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize
        dgvActions.Dock = DockStyle.Fill
        dgvActions.Location = New Point(0, 0)
        dgvActions.Name = "dgvActions"
        dgvActions.RowHeadersWidth = 51
        dgvActions.Size = New Size(800, 359)
        dgvActions.TabIndex = 0
        ' 
        ' FormEditActions
        ' 
        AutoScaleDimensions = New SizeF(8F, 20F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 501)
        Controls.Add(SplitContainer1)
        Name = "FormEditActions"
        Text = "FormEditActions"
        SplitContainer1.Panel1.ResumeLayout(False)
        SplitContainer1.Panel2.ResumeLayout(False)
        CType(SplitContainer1, ComponentModel.ISupportInitialize).EndInit()
        SplitContainer1.ResumeLayout(False)
        CType(dgvActions, ComponentModel.ISupportInitialize).EndInit()
        CType(bsActionsLocal, ComponentModel.ISupportInitialize).EndInit()
        ResumeLayout(False)
    End Sub
    Friend WithEvents btnCancelActions As Button
    Friend WithEvents btnMoveActionDown As Button
    Friend WithEvents btnValidateActions As Button
    Friend WithEvents btnMoveActionUp As Button
    Friend WithEvents btnDeleteAction As Button
    Friend WithEvents btnEditAction As Button
    Friend WithEvents btnAddAction As Button
    Friend WithEvents SplitContainer1 As SplitContainer
    Friend WithEvents dgvActions As DataGridView
    Friend WithEvents bsActionsLocal As BindingSource
    Friend WithEvents lbxCombattants As ListBox
End Class
