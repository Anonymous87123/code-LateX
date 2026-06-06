$ErrorActionPreference = "Stop"

$outDir = Join-Path (Get-Location) "_analysis_output\ocr_test"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null
$pdfSource = Join-Path (Get-Location) "2024年6月六级第一套原题.pdf"
$pdf = Join-Path $outDir "sample.pdf"
Copy-Item -LiteralPath $pdfSource -Destination $pdf -Force

$prefix = Join-Path $outDir "page"
$pdftoppm = "E:\Program Files\LateX\texlive\2025\bin\windows\pdftoppm.exe"
& $pdftoppm "-f" "4" "-l" "6" "-png" "-r" "200" $pdf $prefix

Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null

function Await($task) {
    $task.AsTask().GetAwaiter().GetResult()
}

$ocr = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
Get-ChildItem $outDir -Filter "*.png" | Sort-Object Name | ForEach-Object {
    $file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($_.FullName))
    $stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read))
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync())
    $result = Await ($ocr.RecognizeAsync($bitmap))
    $txtPath = [System.IO.Path]::ChangeExtension($_.FullName, ".txt")
    [System.IO.File]::WriteAllText($txtPath, $result.Text, [System.Text.Encoding]::UTF8)
    Write-Output ("OCR " + $_.Name)
}
