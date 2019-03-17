from io import BytesIO
from .get_username import get_username
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, inch

def _page_properties(title,buff, pagesizeConf, rightMarginConf, leftMarginConf, topMarginConf, bottomMarginConf):
    doc = SimpleDocTemplate(buff,
                            title=title,
                            pagesize=pagesizeConf,
                            rightMargin=rightMarginConf,
                            leftMargin=leftMarginConf,
                            topMargin=topMarginConf,
                            bottomMargin=bottomMarginConf,
                            )
    return doc

def _header_footer(canvas, doc):
    # Save the state of our canvas so we can draw on it
    canvas.saveState()
    styles = getSampleStyleSheet()

    # Header
    header = Paragraph('This is a multi-line header.  It goes on every page.   ' * 5, styles['Normal'])
    w, h = header.wrap(doc.width, doc.topMargin)
    header.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - h)

    # Footer
    footer = Paragraph('Usuario:' + str(get_username()), styles['Normal'])
    w, h = footer.wrap(doc.width, doc.bottomMargin)
    footer.drawOn(canvas, doc.leftMargin, h)

    # Release the canvas
    canvas.restoreState()
    
class NumberedCanvas(canvas.Canvas):

    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
 

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()
 

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
 
 
    def draw_page_number(self, page_count):
        # Change the position of this to wherever you want the page number to be
        self.drawRightString(50 * mm, 5,
                             "Pagina %d de %d" % (self._pageNumber, page_count)) 
    
