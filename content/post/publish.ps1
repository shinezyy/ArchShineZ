# take arguments from command line as post name
param(
    [string]$postName
)

# goto the post directory
cd .\$postName
pandoc -f markdown index.md -t docx -o "$postName.docx"
cd ..

