param(
  [Parameter(Mandatory=$true)][string]$Pattern,
  [Parameter(Mandatory=$true)][string]$OutName
)

$ErrorActionPreference = 'Stop'
$base = (Get-Location).Path
$examName = [string]([char]0x8bd5) + [string]([char]0x5377)
$srcDir = Join-Path (Join-Path $base 'elegantbook2') $examName
$outDir = Join-Path (Join-Path $base 'tmp') 'past-exams-docpdf'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$src = Get-ChildItem -LiteralPath $srcDir -Filter '*.doc' |
  Where-Object { $_.Name -like $Pattern } |
  Select-Object -First 1
if ($null -eq $src) {
  throw "Source DOC not found for pattern: $Pattern"
}

$pdf = Join-Path $outDir $OutName
$txt = [System.IO.Path]::ChangeExtension($pdf, '.word.txt')

$word = $null
$doc = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  Write-Host "OPEN $($src.Name)"
  $doc = $word.Documents.Open($src.FullName, $false, $true)
  [System.IO.File]::WriteAllText($txt, $doc.Content.Text, [System.Text.Encoding]::UTF8)
  Write-Host "SAVEAS $OutName"
  $doc.SaveAs2($pdf, 17)
  Write-Host "DONE $OutName"
}
finally {
  if ($null -ne $doc) {
    try { $doc.Close($false) } catch {}
  }
  if ($null -ne $word) {
    try { $word.Quit() } catch {}
  }
}
