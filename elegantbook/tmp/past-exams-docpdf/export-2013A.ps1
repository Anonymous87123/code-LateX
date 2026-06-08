$ErrorActionPreference = 'Stop'
$src = (Resolve-Path 'elegantbook2/试卷/2013级软件 工科数学分析下A.doc').Path
$dst = (Resolve-Path 'tmp/past-exams-docpdf').Path + '\2013-A.pdf'
$status = (Resolve-Path 'tmp/past-exams-docpdf').Path + '\2013-A.status.txt'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$word.AutomationSecurity = 3
try {
  $doc = $word.Documents.Open($src, $false, $true, $false, '', '', $false, '', '', 0, $false, $false, $false, $false, $true)
  try {
    $doc.ExportAsFixedFormat($dst, 17, $false, 0, 0, 1, 999, 0, $true, $true, 0, $true, $true, $false)
    'done' | Set-Content -Path $status -Encoding ASCII
  }
  finally { $doc.Close($false) }
}
catch {
  $_ | Out-String | Set-Content -Path $status -Encoding UTF8
  throw
}
finally { $word.Quit() }
