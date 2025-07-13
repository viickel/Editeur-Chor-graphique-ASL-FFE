<Global.Microsoft.VisualBasic.CompilerServices.DesignerGenerated()>
Partial Class Form1
    Inherits System.Windows.Forms.Form

    'Form overrides dispose to clean up the component list.
    <System.Diagnostics.DebuggerNonUserCode()>
    Protected Overrides Sub Dispose(disposing As Boolean)
        Try
            If disposing AndAlso components IsNot Nothing Then
                components.Dispose()
            End If
        Finally
            MyBase.Dispose(disposing)
        End Try
    End Sub

    'Required by the Windows Form Designer
    Private components As System.ComponentModel.IContainer

    'NOTE: The following procedure is required by the Windows Form Designer
    'It can be modified using the Windows Form Designer.  
    'Do not modify it using the code editor.
    <System.Diagnostics.DebuggerStepThrough()>
    Private Sub InitializeComponent()
        Bt_Open = New Button()
        Bt_Save = New Button()
        Bt_Save_As = New Button()
        Title_Box = New TextBox()
        Label_Titre = New Label()
        Rich_Intrigue = New RichTextBox()
        Label_Intrigue = New Label()
        Label1 = New Label()
        Label_Assistant = New Label()
        Bt_Edit_choregraphe = New Button()
        Bt_Edit_assistant = New Button()
        SplitContainer1 = New SplitContainer()
        lstCombattants = New ListBox()
        lstAssistantsDisplay = New ListBox()
        Bt_Editer_Chore = New Button()
        TextBox1 = New TextBox()
        Label2 = New Label()
        Bt_New = New Button()
        btnGeneratePdf = New Button()
        cboPageSize = New ComboBox()
        GroupBox1 = New GroupBox()
        CType(SplitContainer1, ComponentModel.ISupportInitialize).BeginInit()
        SplitContainer1.Panel1.SuspendLayout()
        SplitContainer1.Panel2.SuspendLayout()
        SplitContainer1.SuspendLayout()
        GroupBox1.SuspendLayout()
        SuspendLayout()
        ' 
        ' Bt_Open
        ' 
        Bt_Open.Location = New Point(119, 28)
        Bt_Open.Name = "Bt_Open"
        Bt_Open.Size = New Size(94, 29)
        Bt_Open.TabIndex = 0
        Bt_Open.Text = "Ouvrir"
        Bt_Open.UseVisualStyleBackColor = True
        ' 
        ' Bt_Save
        ' 
        Bt_Save.Location = New Point(219, 28)
        Bt_Save.Name = "Bt_Save"
        Bt_Save.Size = New Size(94, 29)
        Bt_Save.TabIndex = 1
        Bt_Save.Text = "Enregistrer"
        Bt_Save.UseVisualStyleBackColor = True
        ' 
        ' Bt_Save_As
        ' 
        Bt_Save_As.Location = New Point(319, 28)
        Bt_Save_As.Name = "Bt_Save_As"
        Bt_Save_As.Size = New Size(124, 29)
        Bt_Save_As.TabIndex = 2
        Bt_Save_As.Text = "Enregistrer Sous"
        Bt_Save_As.UseVisualStyleBackColor = True
        ' 
        ' Title_Box
        ' 
        Title_Box.Anchor = AnchorStyles.Top Or AnchorStyles.Left Or AnchorStyles.Right
        Title_Box.Location = New Point(27, 91)
        Title_Box.Name = "Title_Box"
        Title_Box.Size = New Size(416, 27)
        Title_Box.TabIndex = 3
        ' 
        ' Label_Titre
        ' 
        Label_Titre.AutoSize = True
        Label_Titre.Location = New Point(27, 68)
        Label_Titre.Name = "Label_Titre"
        Label_Titre.Size = New Size(39, 20)
        Label_Titre.TabIndex = 4
        Label_Titre.Text = "Titre"
        ' 
        ' Rich_Intrigue
        ' 
        Rich_Intrigue.Anchor = AnchorStyles.Top Or AnchorStyles.Bottom Or AnchorStyles.Left Or AnchorStyles.Right
        Rich_Intrigue.Location = New Point(27, 144)
        Rich_Intrigue.Name = "Rich_Intrigue"
        Rich_Intrigue.Size = New Size(752, 132)
        Rich_Intrigue.TabIndex = 5
        Rich_Intrigue.Text = ""
        ' 
        ' Label_Intrigue
        ' 
        Label_Intrigue.AutoSize = True
        Label_Intrigue.Location = New Point(27, 121)
        Label_Intrigue.Name = "Label_Intrigue"
        Label_Intrigue.Size = New Size(60, 20)
        Label_Intrigue.TabIndex = 6
        Label_Intrigue.Text = "Intrigue"
        ' 
        ' Label1
        ' 
        Label1.AutoSize = True
        Label1.Location = New Point(29, 24)
        Label1.Name = "Label1"
        Label1.Size = New Size(95, 20)
        Label1.TabIndex = 8
        Label1.Text = "Chorégraphe"
        ' 
        ' Label_Assistant
        ' 
        Label_Assistant.AutoSize = True
        Label_Assistant.Location = New Point(24, 19)
        Label_Assistant.Name = "Label_Assistant"
        Label_Assistant.Size = New Size(120, 20)
        Label_Assistant.TabIndex = 10
        Label_Assistant.Text = "Assistant Plateau"
        ' 
        ' Bt_Edit_choregraphe
        ' 
        Bt_Edit_choregraphe.Location = New Point(130, 20)
        Bt_Edit_choregraphe.Name = "Bt_Edit_choregraphe"
        Bt_Edit_choregraphe.Size = New Size(194, 29)
        Bt_Edit_choregraphe.TabIndex = 11
        Bt_Edit_choregraphe.Text = "Editer Chorégraphe"
        Bt_Edit_choregraphe.UseVisualStyleBackColor = True
        ' 
        ' Bt_Edit_assistant
        ' 
        Bt_Edit_assistant.Location = New Point(160, 15)
        Bt_Edit_assistant.Name = "Bt_Edit_assistant"
        Bt_Edit_assistant.Size = New Size(140, 29)
        Bt_Edit_assistant.TabIndex = 12
        Bt_Edit_assistant.Text = "Editer Assistant"
        Bt_Edit_assistant.UseVisualStyleBackColor = True
        ' 
        ' SplitContainer1
        ' 
        SplitContainer1.Anchor = AnchorStyles.Bottom Or AnchorStyles.Left Or AnchorStyles.Right
        SplitContainer1.Location = New Point(27, 299)
        SplitContainer1.Name = "SplitContainer1"
        ' 
        ' SplitContainer1.Panel1
        ' 
        SplitContainer1.Panel1.Controls.Add(lstCombattants)
        SplitContainer1.Panel1.Controls.Add(Bt_Edit_choregraphe)
        SplitContainer1.Panel1.Controls.Add(Label1)
        ' 
        ' SplitContainer1.Panel2
        ' 
        SplitContainer1.Panel2.Controls.Add(lstAssistantsDisplay)
        SplitContainer1.Panel2.Controls.Add(Bt_Edit_assistant)
        SplitContainer1.Panel2.Controls.Add(Label_Assistant)
        SplitContainer1.Size = New Size(752, 194)
        SplitContainer1.SplitterDistance = 387
        SplitContainer1.TabIndex = 13
        ' 
        ' lstCombattants
        ' 
        lstCombattants.FormattingEnabled = True
        lstCombattants.Location = New Point(29, 69)
        lstCombattants.Name = "lstCombattants"
        lstCombattants.Size = New Size(295, 104)
        lstCombattants.TabIndex = 14
        ' 
        ' lstAssistantsDisplay
        ' 
        lstAssistantsDisplay.FormattingEnabled = True
        lstAssistantsDisplay.Location = New Point(24, 69)
        lstAssistantsDisplay.Name = "lstAssistantsDisplay"
        lstAssistantsDisplay.Size = New Size(295, 104)
        lstAssistantsDisplay.TabIndex = 13
        ' 
        ' Bt_Editer_Chore
        ' 
        Bt_Editer_Chore.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        Bt_Editer_Chore.Location = New Point(626, 89)
        Bt_Editer_Chore.Name = "Bt_Editer_Chore"
        Bt_Editer_Chore.Size = New Size(162, 29)
        Bt_Editer_Chore.TabIndex = 14
        Bt_Editer_Chore.Text = "Editer Chorégraphie"
        Bt_Editer_Chore.UseVisualStyleBackColor = True
        ' 
        ' TextBox1
        ' 
        TextBox1.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        TextBox1.Location = New Point(474, 91)
        TextBox1.Name = "TextBox1"
        TextBox1.Size = New Size(146, 27)
        TextBox1.TabIndex = 15
        ' 
        ' Label2
        ' 
        Label2.Anchor = AnchorStyles.Top Or AnchorStyles.Right
        Label2.AutoSize = True
        Label2.Location = New Point(474, 68)
        Label2.Name = "Label2"
        Label2.Size = New Size(49, 20)
        Label2.TabIndex = 16
        Label2.Text = "Durée"
        ' 
        ' Bt_New
        ' 
        Bt_New.Location = New Point(27, 28)
        Bt_New.Name = "Bt_New"
        Bt_New.Size = New Size(86, 29)
        Bt_New.TabIndex = 17
        Bt_New.Text = "Nouveau"
        Bt_New.UseVisualStyleBackColor = True
        ' 
        ' btnGeneratePdf
        ' 
        btnGeneratePdf.Location = New Point(163, 22)
        btnGeneratePdf.Name = "btnGeneratePdf"
        btnGeneratePdf.Size = New Size(146, 29)
        btnGeneratePdf.TabIndex = 18
        btnGeneratePdf.Text = "Générer PDF"
        btnGeneratePdf.UseVisualStyleBackColor = True
        ' 
        ' cboPageSize
        ' 
        cboPageSize.DropDownStyle = ComboBoxStyle.DropDownList
        cboPageSize.FormattingEnabled = True
        cboPageSize.Items.AddRange(New Object() {"A4 Paysage", "A4 Portrait", "A3 Paysage", "A3 Portrait"})
        cboPageSize.Location = New Point(6, 22)
        cboPageSize.Name = "cboPageSize"
        cboPageSize.Size = New Size(151, 28)
        cboPageSize.TabIndex = 19
        ' 
        ' GroupBox1
        ' 
        GroupBox1.Controls.Add(btnGeneratePdf)
        GroupBox1.Controls.Add(cboPageSize)
        GroupBox1.Location = New Point(469, 8)
        GroupBox1.Name = "GroupBox1"
        GroupBox1.Size = New Size(319, 57)
        GroupBox1.TabIndex = 20
        GroupBox1.TabStop = False
        GroupBox1.Text = "Génération PDF"
        ' 
        ' Form1
        ' 
        AutoScaleDimensions = New SizeF(8F, 20F)
        AutoScaleMode = AutoScaleMode.Font
        ClientSize = New Size(800, 524)
        Controls.Add(GroupBox1)
        Controls.Add(Bt_New)
        Controls.Add(Label2)
        Controls.Add(TextBox1)
        Controls.Add(Bt_Editer_Chore)
        Controls.Add(SplitContainer1)
        Controls.Add(Label_Intrigue)
        Controls.Add(Rich_Intrigue)
        Controls.Add(Label_Titre)
        Controls.Add(Title_Box)
        Controls.Add(Bt_Save_As)
        Controls.Add(Bt_Save)
        Controls.Add(Bt_Open)
        Name = "Form1"
        Text = "Editeur Chorégraphique"
        SplitContainer1.Panel1.ResumeLayout(False)
        SplitContainer1.Panel1.PerformLayout()
        SplitContainer1.Panel2.ResumeLayout(False)
        SplitContainer1.Panel2.PerformLayout()
        CType(SplitContainer1, ComponentModel.ISupportInitialize).EndInit()
        SplitContainer1.ResumeLayout(False)
        GroupBox1.ResumeLayout(False)
        ResumeLayout(False)
        PerformLayout()
    End Sub

    Friend WithEvents Bt_Open As Button
    Friend WithEvents Bt_Save As Button
    Friend WithEvents Bt_Save_As As Button
    Friend WithEvents Title_Box As TextBox
    Friend WithEvents Label_Titre As Label
    Friend WithEvents Rich_Intrigue As RichTextBox
    Friend WithEvents Label_Intrigue As Label
    Friend WithEvents Rich_Choregraphe As RichTextBox
    Friend WithEvents Label1 As Label
    Friend WithEvents Label_Assistant As Label
    Friend WithEvents Rich_Assistant As RichTextBox
    Friend WithEvents Bt_Edit_choregraphe As Button
    Friend WithEvents Bt_Edit_assistant As Button
    Friend WithEvents SplitContainer1 As SplitContainer
    Friend WithEvents Bt_Editer_Chore As Button
    Friend WithEvents TextBox1 As TextBox
    Friend WithEvents Label2 As Label
    Friend WithEvents Bt_New As Button
    Friend WithEvents ListCombatant As ListBox
    Friend WithEvents lstAssistantsDisplay As ListBox
    Friend WithEvents lstCombattants As ListBox
    Friend WithEvents btnGeneratePdf As Button
    Friend WithEvents cboPageSize As ComboBox
    Friend WithEvents GroupBox1 As GroupBox

End Class
