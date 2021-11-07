from PyPDF2 import PdfFileReader, PdfFileWriter
import os

def Make_Booklet(pdf_path,output_path):
    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()
    pdf_writer.appendPagesFromReader(pdf_reader)

    Num_addPages = 4 - (pdf_reader.numPages % 4)

    if Num_addPages != 4:
        for i in range(int(Num_addPages)):
            pdf_writer.addBlankPage()
    
    Num_Pages = pdf_writer.getNumPages() 
    booklet = PdfFileWriter()   
    for i in range(Num_Pages // 4):        
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 1)))
        booklet.addPage(pdf_writer.getPage(int(2 * i)))
        booklet.addPage(pdf_writer.getPage(int(2 * i + 1)))
        booklet.addPage(pdf_writer.getPage(int(Num_Pages - 2 * i - 2)))

    if(os.path.isfile(output_path)):
        os.remove(output_path)


    with open(output_path, 'wb') as fh:
        booklet.write(fh)

def Make_Thumb(pdf_path,Thumb_path):
    pdf_reader = PdfFileReader(pdf_path)
    pdf_writer = PdfFileWriter()

    pdf_writer.addPage(pdf_reader.getPage(0))

    with open(Thumb_path,'wb') as fh:
        pdf_writer.write(fh)