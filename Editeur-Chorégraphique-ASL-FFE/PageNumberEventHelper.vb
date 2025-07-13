Imports iTextSharp.text
Imports iTextSharp.text.pdf

Public Class PageNumberEventHelper
    Inherits PdfPageEventHelper

    ' Police pour les numéros de page
    Private fontPageNumber As Font = FontFactory.GetFont(FontFactory.HELVETICA, 8, BaseColor.GRAY)

    ' Template pour le nombre total de pages
    Private totalPages As PdfTemplate

    Public Overrides Sub OnOpenDocument(writer As PdfWriter, document As Document)
        ' Créer le template pour le nombre total de pages
        totalPages = writer.DirectContent.CreateTemplate(30, 16)
    End Sub

    Public Overrides Sub OnCloseDocument(writer As PdfWriter, document As Document)
        ' Écrire le nombre total de pages dans le template quand le document est fermé
        totalPages.BeginText()
        totalPages.SetFontAndSize(BaseFont.CreateFont(BaseFont.HELVETICA, BaseFont.CP1252, BaseFont.NOT_EMBEDDED), 8)
        totalPages.ShowText(CStr(writer.PageNumber - 1)) ' writer.PageNumber est déjà incrémenté pour la prochaine page
        totalPages.EndText()
    End Sub

    Public Overrides Sub OnEndPage(writer As PdfWriter, document As Document)
        Dim currentPageNumber As Integer = writer.PageNumber

        ' Positionner le texte en bas à droite de la page
        Dim phrase As New Phrase(String.Format("Page {0} sur ", currentPageNumber), fontPageNumber)

        ' Créer un PdfContentByte pour écrire sur la page
        Dim cb As PdfContentByte = writer.DirectContent

        ' Calculer la position pour le numéro de page
        Dim pageSize As Rectangle = document.PageSize
        Dim textWidth As Single = fontPageNumber.GetCalculatedBaseFont(False).GetWidthPoint(phrase.Content, fontPageNumber.Size)
        Dim x As Single = pageSize.Width - document.RightMargin - textWidth
        Dim y As Single = document.BottomMargin - 10 ' 10 points sous la marge du bas

        ColumnText.ShowTextAligned(cb, Element.ALIGN_RIGHT, phrase, pageSize.Width - document.RightMargin, y, 0)

        ' Ajouter le template pour le nombre total de pages
        cb.AddTemplate(totalPages, pageSize.Width - document.RightMargin - fontPageNumber.GetCalculatedBaseFont(False).GetWidthPoint("000", fontPageNumber.Size), y)
    End Sub
End Class