from weasyprint import HTML

def export2pdf2(filename):
    HTML('templates/apply.html').write_pdf('static/export_pdf/'+filename)

export2pdf2('Exp1.pdf')