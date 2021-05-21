Set-Location "doc"
Remove-Item "html" -Recurse -Force
Remove-Item "moduleRst\show_host_info.rst"
sphinx-apidoc -o "moduleRst" ..\resources\scripts
sphinx-build -b html . "html"
Set-Location ".."
