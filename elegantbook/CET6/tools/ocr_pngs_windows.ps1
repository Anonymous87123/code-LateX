param(
    [string]$Pattern = "ocr_page-*.png"
)

$ErrorActionPreference = "Stop"

Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] | Out-Null

function Await($op) {
    if ($op -is [System.Threading.Tasks.Task]) {
        return $op.GetAwaiter().GetResult()
    }
    return $op.AsTask().GetAwaiter().GetResult()
}

$ocr = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()

Get-ChildItem -Filter $Pattern | Sort-Object Name | ForEach-Object {
    $file = Await([Windows.Storage.StorageFile]::GetFileFromPathAsync($_.FullName))
    $stream = Await($file.OpenAsync([Windows.Storage.FileAccessMode]::Read))
    $decoder = Await([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
    $bitmap = Await($decoder.GetSoftwareBitmapAsync())
    $result = Await($ocr.RecognizeAsync($bitmap))
    Write-Output ("===== " + $_.Name + " =====")
    Write-Output $result.Text
}
