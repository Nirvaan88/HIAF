import pypandoc

print("Downloading pandoc...")
pypandoc.download_pandoc()

print("Converting documentation.md to documentation.docx...")
pypandoc.convert_file('documentation.md', 'docx', outputfile='documentation.docx')
print("Done.")
