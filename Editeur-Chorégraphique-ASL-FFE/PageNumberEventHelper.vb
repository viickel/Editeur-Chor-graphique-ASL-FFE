Imports iTextSharp.text
Imports iTextSharp.text.pdf

Public Class PageNumberEventHelper
    Inherits PdfPageEventHelper

    ' Police pour les numéros de page
    ' Police définie à 8 points, couleur grise. C'est bien.
    Private fontPageNumber As Font = FontFactory.GetFont(FontFactory.HELVETICA, 8, BaseColor.GRAY)

    ' Template pour le nombre total de pages
    Private totalPages As PdfTemplate

    Public Overrides Sub OnOpenDocument(writer As PdfWriter, document As Document)
        ' Créer le template pour le nombre total de pages
        ' La taille (30, 16) est généralement suffisante.
        totalPages = writer.DirectContent.CreateTemplate(30, 16)
    End Sub

    ' Correction dans OnCloseDocument :
    ' Le template doit être rempli avec le nombre total de pages *réel*.
    ' writer.PageNumber donne le nombre de pages *déjà écrites*.
    ' Si vous voulez le total des pages, c'est bien writer.PageNumber à la fin.
    ' La ligne 'BaseFont.CreateFont(BaseFont.HELVETICA, BaseFont.CP1252, BaseFont.NOT_EMBEDDED)'
    ' devrait utiliser le même objet BaseFont que celui dérivé de fontPageNumber pour la cohérence.
    Public Overrides Sub OnCloseDocument(writer As PdfWriter, document As Document)
        ' Écrire le nombre total de pages dans le template quand le document est fermé
        totalPages.BeginText()
        ' Utiliser le même font que pour le reste du numéro de page
        totalPages.SetFontAndSize(fontPageNumber.GetCalculatedBaseFont(False), fontPageNumber.Size)
        totalPages.ShowText(writer.PageNumber.ToString()) ' Le nombre total de pages est writer.PageNumber à la fin du document
        totalPages.EndText()
    End Sub

    Public Overrides Sub OnEndPage(writer As PdfWriter, document As Document)
        Dim currentPageNumber As Integer = writer.PageNumber
        Dim cb As PdfContentByte = writer.DirectContent

        ' Texte de la première partie du numéro de page ("Page N / ")
        ' On utilise fontPageNumber pour obtenir la taille et la police.
        Dim textCurrentPage As String = String.Format("Page {0} / ", currentPageNumber)
        Dim phraseCurrentPage As New Phrase(textCurrentPage, fontPageNumber)

        ' Calculer la largeur de la première partie du texte
        Dim textCurrentPageWidth As Single = fontPageNumber.GetCalculatedBaseFont(False).GetWidthPoint(textCurrentPage, fontPageNumber.Size)

        ' Coordonnée Y (verticale) : Place le texte 20 points au-dessus de la marge inférieure du document.
        ' document.BottomMargin est généralement la marge que vous avez définie pour le document (par exemple 30 ou 50).
        ' Ajustez '-20' si le texte est trop bas ou trop haut.
        Dim yPosition As Single = document.BottomMargin - 20

        ' --- Calcul de la position X (horizontale) pour décaler vers la gauche ---
        ' document.PageSize.Width - document.RightMargin est le bord droit de la zone de contenu.
        ' Pour décaler l'ensemble du bloc "Page N / X" vers la gauche, on peut :
        ' 1. Estimer la largeur totale du texte "Page N / X" (pour un alignement précis à droite).
        ' 2. Définir un point de départ X pour ALIGN_LEFT et placer les éléments séquentiellement.

        ' Option 2 (Plus simple et plus robuste pour décaler à gauche) :
        ' Définir un point d'ancrage pour le début du texte "Page N / X".
        ' Par exemple, 100 points depuis le bord droit de la page.
        ' Vous devrez ajuster la valeur '100' pour obtenir le bon positionnement.
        Dim xOffsetFromRight As Single = 100 ' Distance du bord droit de la page

        ' La position X où le texte "Page N / " va COMMENCER (ALIGN_LEFT)
        Dim xStartPosition As Single = document.PageSize.Width - xOffsetFromRight - textCurrentPageWidth
        ' Pour que l'ensemble du bloc (Page N / X) soit à 100 points du bord droit de la page,
        ' la partie "Page N / " doit commencer à :
        ' (Largeur de la page - Marge droite - Décalage souhaité depuis la marge droite - Largeur estimée de 'X')
        ' Pour un placement simple et direct :

        ' Estimer la largeur maximale du nombre total de pages (ex: "999")
        Dim estimatedTotalPagesWidth As Single = fontPageNumber.GetCalculatedBaseFont(False).GetWidthPoint("999", fontPageNumber.Size)

        ' Calculer la largeur totale que prendra le texte "Page N / X"
        Dim totalTextWidth As Single = textCurrentPageWidth + estimatedTotalPagesWidth

        ' Calculer la position X où le bloc "Page N / X" DOIT COMMENCER pour être à 
        ' 'xOffsetFromRight' points du bord droit de la page.
        ' Par exemple, si vous voulez que le tout soit à 100 points du bord droit de la page:
        Dim xStartForFullBlock As Single = document.PageSize.Width - xOffsetFromRight - totalTextWidth

        ' --- Écriture du texte "Page N / " ---
        ' Utiliser ColumnText.ShowTextAligned pour la première partie du texte
        ' ALIGN_LEFT est utilisé pour que 'xStartForFullBlock' soit le point de départ du texte.
        ColumnText.ShowTextAligned(cb, Element.ALIGN_LEFT, phraseCurrentPage, xStartForFullBlock, yPosition, 0)

        ' --- Ajout du template pour le nombre total de pages ---
        ' Le template doit être positionné juste après la première partie du texte.
        ' Son point de départ X est le point de départ de la première partie plus la largeur de cette partie.
        cb.AddTemplate(totalPages, xStartForFullBlock + textCurrentPageWidth, yPosition)
    End Sub
End Class