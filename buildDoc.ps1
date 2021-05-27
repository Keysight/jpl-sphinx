Set-Location "docs"
Remove-Item "html" -Recurse -Force
Remove-Item "resources\scripts\modules.rst"
sphinx-apidoc -o "resources\scripts" "..\resources\scripts"
sphinx-build -b html . "html"
Set-Location ".."
