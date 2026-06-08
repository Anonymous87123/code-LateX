$ErrorActionPreference = 'Continue'
$base = (Get-Location).Path
$examName = [string]([char]0x8bd5) + [string]([char]0x5377)
$srcDir = Join-Path (Join-Path $base 'elegantbook2') $examName
$rawDir = Join-Path $base 'word\past-exams\raw'
New-Item -ItemType Directory -Force -Path $rawDir | Out-Null
function SafeName($name) {
  $stem = [System.IO.Path]::GetFileNameWithoutExtension($name)
  $s = [regex]::Replace($stem, '[^0-9A-Za-z\p{IsCJKUnifiedIdeographs}]+', '_').Trim('_')
  if ($s.Length -gt 90) { $s = $s.Substring(0,90) }
  if ($s.Length -eq 0) { $s = 'file' }
  return $s
}
$result = @()
$files = Get-ChildItem -LiteralPath $srcDir -Filter *.doc | Sort-Object Name
foreach ($f in $files) {
  Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue
  $safe = SafeName $f.Name
  $txtPath = Join-Path $rawDir ($safe + '.txt')
  $word = $null
  $doc = $null
  try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $doc = $word.Documents.Open($f.FullName, $false, $true, $false)
    $text = $doc.Content.Text
    Set-Content -LiteralPath $txtPath -Value $text -Encoding UTF8
    $chars = (($text) -replace '\s+', '').Length
    $result += [pscustomobject]@{ Name=$f.Name; Status='converted-text'; Chars=$chars; Text=$txtPath }
    Write-Output ("OK`t{0}`t{1}" -f $chars,$f.Name)
  } catch {
    $result += [pscustomobject]@{ Name=$f.Name; Status=('failed: ' + $_.Exception.Message); Chars=0; Text=$txtPath }
    Write-Output ("FAIL`t{0}`t{1}" -f $_.Exception.Message,$f.Name)
  } finally {
    if ($doc -ne $null) { try { $doc.Close($false) } catch {} }
    if ($word -ne $null) { try { $word.Quit() } catch {} }
    Stop-Process -Name WINWORD -Force -ErrorAction SilentlyContinue
  }
}
$result | ConvertTo-Json -Depth 3 | Set-Content -LiteralPath (Join-Path $base 'word\past-exams\doc-conversion.json') -Encoding UTF8
