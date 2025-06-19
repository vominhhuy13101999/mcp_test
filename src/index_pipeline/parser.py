from docling.document_converter import DocumentConverter

source = "C:\\Users\\Admin\\Work\\USProject\\ModelContextProtocol\\data\\20250523ThongkeGiaoDichTudoanh-OnePage.pdf"  # document per local path or URL

converter = DocumentConverter()

result = converter.convert(source)

print(result.document.export_to_html())

with open("data/output_ppt.html", "w", encoding="utf-8") as f:
    f.write(result.document.export_to_html())
