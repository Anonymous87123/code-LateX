
$ErrorActionPreference = 'Stop'
$base = (Get-Location).Path
$examName = [string]([char]0x8bd5) + [string]([char]0x5377)
$srcDir = Join-Path (Join-Path $base 'elegantbook2') $examName
$outDir = Join-Path $base 'word\past-exams\converted'
$rawDir = Join-Path $base 'word\past-exams\raw'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$wdFormatPDF = 17
function SafeName($name) {
  $stem = [System.IO.Path]::GetFileNameWithoutExtension($name)
  $s = [regex]::Replace($stem, '[^0-9A-Za-z\p{IsCJKUnifiedIdeographs}]+', '_').Trim('_')
  if ($s.Length -gt 90) { $s = $s.Substring(0,90) }
  if ($s.Length -eq 0) { $s = 'file' }
  return $s
}
$result = @()
try {
  Get-ChildItem -LiteralPath $srcDir -Filter *.doc | Sort-Object Name | ForEach-Object {
    $safe = SafeName $_.Name
    $txtPath = Join-Path $rawDir ($safe + '.txt')
    $pdfPath = Join-Path $outDir ($safe + '.pdf')
    $doc = $null
    try {
      $doc = $word.Documents.Open($_.FullName, $false, $true)
      $text = $doc.Content.Text
      Set-Content -LiteralPath $txtPath -Value $text -Encoding UTF8
      try { $doc.ExportAsFixedFormat($pdfPath, $wdFormatPDF) } catch {}
      $chars = (($text) -replace '\s+', '').Length
      $result += [pscustomobject]@{ Name=$_.Name; Status='converted-text'; Text=$txtPath; Pdf=$pdfPath; Chars=$chars }
    } catch {
      $result += [pscustomobject]@{ Name=$_.Name; Status=('failed: ' + $_.Exception.Message); Text=$txtPath; Pdf=$pdfPath; Chars=0 }
    } finally {
      if ($doc -ne $null) { $doc.Close($false) }
    }
  }
} finally {
  $word.Quit()
}
$result | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $base 'word\past-exams\doc-conversion.json') -Encoding UTF8
$result | Format-Table -AutoSize
