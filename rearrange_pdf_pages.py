import PyPDF2 as pdf
import os

class PdfFile:

    def __init__(self):
        self.pdf_reader = None
        self.pdf_writer = pdf.PdfWriter()
        self.cwd = os.path.dirname(os.path.abspath(__file__))
        self.pages = 0
        self.file_name = ""

    def modify_writer(self, order):
        for idx in range(4):
            if order[idx] is None:
                self.pdf_writer.add_blank_page()
            elif idx == 2 or idx == 3:
                page = self.pdf_reader.pages[order[idx]]
                page.rotate(180)
                self.pdf_writer.add_page(page)
            else:
                self.pdf_writer.add_page(self.pdf_reader.pages[order[idx]])

    def rearrange(self, iteration, **kwargs):
        first = iteration*4
        order = [ first+1, first+2, first, first+3 ]
        if kwargs.get("redundant_iteration"):
            extras = kwargs.get("extra_pages")
            for i in range(4):
                if extras and order[i] >= self.pages:
                    order[i] = None
                    extras-=1
        self.modify_writer(order)


    def initial_calc(self):
        self.file_name = input("Enter file name: ")
        file_path = os.path.join(self.cwd, f"{self.file_name}.pdf")
        with open(file_path, 'rb') as input_pdf_file:
            self.pdf_reader = pdf.PdfReader(input_pdf_file)

            self.pages = len(self.pdf_reader.pages)
            pages_to_add = 4 - (temp if (temp:=(self.pages%4)) else 4)
            iterations = (self.pages//4)

            for i in range(iterations):
                self.rearrange(i)

            if pages_to_add:
                self.rearrange(iterations, redundant_iteration=True, extra_pages = pages_to_add)



    def write_file(self):
        output_path = os.path.join(self.cwd, f"{self.file_name}_rearranged.pdf")
        with open(output_path, 'wb') as output_pdf_file:
            self.pdf_writer.write(output_pdf_file)
        
        print(f"PDF pages have been rearranged and saved to {output_path}")

pdf_file = PdfFile()
pdf_file.initial_calc()
pdf_file.write_file()