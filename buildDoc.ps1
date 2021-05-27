Set-Location "docs"
Remove-Item "html" -Recurse -Force
Remove-Item "resources\scripts" -Recurse
sphinx-apidoc -o "resources\scripts" "..\resources\scripts"
sphinx-build -b html . "html"
Set-Location ".."
