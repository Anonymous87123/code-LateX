$ErrorActionPreference = 'Stop'
$base = (Get-Location).Path
$examName = [string]([char]0x8bd5) + [string]([char]0x5377)
$srcDir = Join-Path (Join-Path $base 'elegantbook2') $examName
$outDir = Join-Path (Join-Path $base 'tmp') 'past-exams-docpdf'
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$targets = @(
  @{ Pattern = '2009*A.doc'; Out = '2009-A.pdf' },
  @{ Pattern = '2009*B.doc'; Out = '2009-B.pdf' },
  @{ Pattern = '2012*A*.doc'; Out = '2012-A.pdf' },
  @{ Pattern = '2012*B*.doc'; Out = '2012-B.pdf' },
  @{ Pattern = '2014*A.doc'; Out = '2014-A.pdf' },
  @{ Pattern = '2014*B.doc'; Out = '2014-B.pdf' },
  @{ Pattern = '2015*A.doc'; Out = '2015-A.pdf' },
  @{ Pattern = '2015*B.doc'; Out = '2015-B.pdf' }
)

$word = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0

  foreach ($t in $targets) {
    $src = Get-ChildItem -LiteralPath $srcDir -Filter '*.doc' |
      Where-Object { $_.Name -like $t.Pattern } |
      Select-Object -First 1
    if ($null -eq $src) {
      Write-Host "MISS $($t.Pattern)"
      continue
    }

    $pdf = Join-Path $outDir $t.Out
    Write-Host "EXPORT $($src.Name) -> $($t.Out)"
    $doc = $null
    try {
      $doc = $word.Documents.Open($src.FullName, $false, $true)
      $doc.ExportAsFixedFormat($pdf, 17)
      $txt = [System.IO.Path]::ChangeExtension($pdf, '.word.txt')
      [System.IO.File]::WriteAllText($txt, $doc.Content.Text, [System.Text.Encoding]::UTF8)
    }
    finally {
      if ($null -ne $doc) {
        try { $doc.Close($false) } catch {}
      }
    }
  }
}
finally {
  if ($null -ne $word) {
    try { $word.Quit() } catch {}
  }
}
