from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdf2image import convert_from_path
import re
import unicodedata

filename = "22U1T.pdf"
# Store Pdf with convert_from_path function
images = convert_from_path(filename, poppler_path=r"poppler-23.11.0\Library\bin")

# for i in range(len(images)):
# print(images[i].size)
# Save pages as images in the pdf
# images[i].save("page" + str(i) + ".jpg", "JPEG")

fp = open(filename, "rb")
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)
current_page = 0
questions = []

for page in pages:
    # print("Processing next page...")
    # print(vars(page))
    interpreter.process_page(page)
    layout = device.get_result()
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            x, y, text = lobj.bbox[0], 792 - lobj.bbox[3], lobj.get_text()
            if re.match(r"^[0-9]+\.\s*\(\s*\)", text):
                questions.append([current_page, 0 if x < 306 else 1, y])
            elif text.startswith("答案："):
                questions[-1].extend(
                    [
                        current_page,
                        0 if x < 306 else 1,
                        y,
                        unicodedata.normalize("NFKC", text[4]),
                    ]
                )
            elif text.startswith("解析："):
                questions[-1].extend([current_page, 0 if x < 306 else 1, y])

    current_page += 1
    # print("At %r is text: %s" % ((x, y), text))

for q in questions:
    if q[0] == q[3] and q[1] == q[4]:
        images[q[0]].crop(
            (
                976 if q[1] else 264,
                q[2] * 2.77 - 5,
                1559 if q[1] else 847,
                q[5] * 2.77 - 31,
            )
        )  # .show()
        # print(q)
        # break
    # images[q[0]].crop((0, q[2], 595, q[5]))
