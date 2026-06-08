Add-Type -AssemblyName System.Drawing

$root = Split-Path -Parent $PSScriptRoot
$srcDir = Join-Path $PSScriptRoot "subagent-temp\b"
$outDir = Join-Path $root "image\pdf-exercises"

function Crop-Png($srcName, $destName, $x, $y, $w, $h) {
    $src = Join-Path $srcDir $srcName
    $dest = Join-Path $outDir $destName
    $bmp = [System.Drawing.Bitmap]::FromFile($src)
    try {
        $rect = New-Object System.Drawing.Rectangle($x, $y, $w, $h)
        $cropped = $bmp.Clone($rect, $bmp.PixelFormat)
        try {
            $cropped.Save($dest, [System.Drawing.Imaging.ImageFormat]::Png)
        } finally {
            $cropped.Dispose()
        }
    } finally {
        $bmp.Dispose()
    }
}

$page2 = "【包打听分享】2010大学物理_1_A卷试卷规范模版-2.png"
$page3 = "【包打听分享】2010大学物理_1_A卷试卷规范模版-3.png"
$page4 = "【包打听分享】2010大学物理_1_A卷试卷规范模版-4.png"

Crop-Png $page2 "pdf2010-q06-pv-paths.png" 545 300 250 175
Crop-Png $page2 "pdf2010-q07-carnot-cycles.png" 535 510 290 205
Crop-Png $page2 "pdf2010-q09-thin-film-phase.png" 665 890 175 170
Crop-Png $page3 "pdf2010-q15-shm-graph.png" 570 495 210 155
Crop-Png $page3 "pdf2010-q19-wedge-thickness.png" 555 970 285 175
Crop-Png $page4 "pdf2010-q21-rod-block.png" 575 260 240 215
Crop-Png $page4 "pdf2010-q23-wave-graph.png" 575 700 260 180
