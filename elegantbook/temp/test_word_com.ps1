$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$base = (Get-Location).Path
$examName = [string]([char]0x8bd5) + [string]([char]0x5377)
$srcDir = Join-Path (Join-Path $base 'elegantbook2') $examName
$pattern = if ($args.Count -ge 1) { $args[0] } else { '2015*A.doc' }
$stem = if ($args.Count -ge 2) { $args[1] } else { '2015-A' }
$outDir = Join-Path (Join-Path (Join-Path $base 'tmp') 'past-exam-equations') $stem
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$src = Get-ChildItem -LiteralPath $srcDir -Filter '*.doc' |
  Where-Object { $_.Name -like $pattern } |
  Select-Object -First 1
if ($null -eq $src) {
  throw "Source DOC not found for pattern: $pattern"
}

$word = $null
$doc = $null
try {
  $word = New-Object -ComObject Word.Application
  $word.Visible = $false
  $word.DisplayAlerts = 0
  $doc = $word.Documents.Open($src.FullName, $false, $true)
  Write-Host "DOC $($src.Name)"
  Write-Host "TEXT_LENGTH $($doc.Content.Text.Length)"
  Write-Host "INLINESHAPES $($doc.InlineShapes.Count)"

  $manifest = New-Object System.Collections.Generic.List[string]
  $manifest.Add("index,type,class,start,end,context,file")

  for ($i = 1; $i -le $doc.InlineShapes.Count; $i++) {
    $shape = $doc.InlineShapes.Item($i)
    $range = $shape.Range
    $start = [int]$range.Start
    $beforeStart = [Math]::Max(0, $start - 36)
    $afterEnd = [Math]::Min($doc.Content.End, $range.End + 36)
    $ctxRange = $doc.Range($beforeStart, $afterEnd)
    $ctx = ($ctxRange.Text -replace "[`r`n`t]+", " " -replace '"', '""')
    $classType = ''
    try { $classType = $shape.OLEFormat.ClassType } catch {}

    $fileName = ('eq-{0:D3}.png' -f $i)
    $filePath = Join-Path $outDir $fileName
    $saved = $false
    try {
      [System.Windows.Forms.Clipboard]::Clear()
      $range.Select()
      $word.Selection.CopyAsPicture()
      Start-Sleep -Milliseconds 150
      $img = [System.Windows.Forms.Clipboard]::GetImage()
      if ($null -ne $img) {
        $img.Save($filePath, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
        $saved = $true
      }
    } catch {
      Write-Host "COPY_FAIL $i $($_.Exception.Message)"
    }

    if (-not $saved) {
      $fileName = ''
    }
    $manifest.Add(('{0},{1},"{2}",{3},{4},"{5}","{6}"' -f $i, $shape.Type, $classType, $range.Start, $range.End, $ctx, $fileName))
    Write-Host ("EQ {0} CLASS={1} SAVED={2} CTX={3}" -f $i, $classType, $saved, $ctx)
  }

  $manifestPath = Join-Path $outDir 'manifest.csv'
  [System.IO.File]::WriteAllLines($manifestPath, $manifest, [System.Text.Encoding]::UTF8)
  Write-Host "MANIFEST $manifestPath"
}
finally {
  if ($null -ne $doc) {
    try { $doc.Close($false) } catch {}
  }
  if ($null -ne $word) {
    try { $word.Quit() } catch {}
  }
}
