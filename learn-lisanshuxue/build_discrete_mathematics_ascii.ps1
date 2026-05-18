$ErrorActionPreference = 'Stop'

$root = 'D:\code LateX\elegantbook'
$src = Join-Path $root 'learn-lisanshuxue'
$out = Join-Path $root 'DiscreteMathematics.tex'
$chapters = @('chap1.tex', 'chap2.tex', 'chap3.tex', 'chap4.tex', 'chap5.tex')

function Convert-EnvSyntax {
    param([string]$Text)

    $blockEnvNames = 'definition|theorem|lemma|corollary|proposition|postulate|axiom'
    $inlineEnvNames = 'example|property'

    $Text = [regex]::Replace($Text, "\\begin\{($blockEnvNames)\}\{([^{}]*)\}\{([^{}]*)\}", {
        param($m)
        $env = $m.Groups[1].Value
        $title = $m.Groups[2].Value.Trim()
        if ([string]::IsNullOrWhiteSpace($title)) {
            return "\begin{$env}"
        }
        return "\begin{$env}{$title}"
    })

    $Text = [regex]::Replace($Text, "\\begin\{($inlineEnvNames)\}\{([^{}]*)\}\{([^{}]*)\}", {
        param($m)
        $env = $m.Groups[1].Value
        $title = $m.Groups[2].Value.Trim()
        if ([string]::IsNullOrWhiteSpace($title)) {
            return "\begin{$env}"
        }
        return "\begin{$env}[$title]"
    })

    $Text = $Text.Replace([string][char]0x200B, '')
    $Text = $Text -replace '\\pagestyle\{empty\}', ''
    return $Text
}

$mainLines = Get-Content -LiteralPath (Join-Path $src 'main.tex') -Encoding UTF8
$prefaceStart = -1
$prefaceEnd = -1

for ($i = 0; $i -lt $mainLines.Count; $i++) {
    if ($mainLines[$i] -match '^\\chapter\*') {
        $prefaceStart = $i
        break
    }
}

if ($prefaceStart -lt 0) {
    throw 'Failed to find preface start in main.tex.'
}

for ($i = $prefaceStart; $i -lt $mainLines.Count; $i++) {
    if ($mainLines[$i] -eq '\newpage') {
        $prefaceEnd = $i - 1
        break
    }
}

if ($prefaceEnd -lt $prefaceStart) {
    throw 'Failed to find preface end in main.tex.'
}

$prefaceText = ($mainLines[$prefaceStart..$prefaceEnd] -join "`r`n").Replace([string][char]0x200B, '')

$preamble = @'
\documentclass[lang=cn,11pt]{elegantbook}

\title{Discrete Mathematics}
\subtitle{Study Notes}

\author{Xia Tong}
\institute{South China University of Technology}
\date{\today}
\version{1.0}
\bioinfo{Course}{Discrete Mathematics}

\setcounter{tocdepth}{2}

\usepackage{amsmath,amssymb,bm,mathrsfs}
\allowdisplaybreaks
\usepackage{array}
\usepackage{enumitem}
\setlist{itemsep=-1pt}
\setlist[enumerate]{itemsep=-1pt, parsep=-1pt, topsep=0pt}
\usepackage{graphicx}
\usepackage{pgfplots}
\pgfplotsset{compat=1.18}
\usepackage{tikz}
\usepackage{circuitikz}
\usetikzlibrary{arrows,shapes.geometric,circuits.logic.US,positioning}
\usepackage{ulem}
\usepackage{caption}
\usepackage{cleveref}

\graphicspath{{./learn-lisanshuxue/flg/}{./learn-lisanshuxue/}{./figure/}{./image/}}

\newcommand{\R}{\mathbb{R}}
\newcommand{\C}{\mathbb{C}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\e}{\text{e}}
\newcommand{\dd}{\text{d}}
\newcommand{\nothing}{\ensuremath{\varnothing}}
\newcommand{\kt}{\kaishu}
\newcommand{\st}{\songti}
\newcommand{\htbf}{\heiti\bfseries}

\makeatletter
\@ifundefined{setCJKfamilyfont}{}{%
  \IfFontExistsTF{KaiTi}{%
    \setCJKfamilyfont{codexkaiti}[AutoFakeBold=2.5]{KaiTi}%
    \renewcommand{\kaishu}{\CJKfamily{codexkaiti}}%
  }{}%
  \IfFontExistsTF{FangSong}{%
    \setCJKfamilyfont{codexfangsong}[AutoFakeBold=2.5]{FangSong}%
    \renewcommand{\fangsong}{\CJKfamily{codexfangsong}}%
  }{}%
}
\makeatother

\sloppy

\begin{document}

\maketitle
\frontmatter
'@

$middle = @"
$prefaceText

\tableofcontents
\makeenvindex

\mainmatter
"@

$bodyParts = New-Object System.Collections.Generic.List[string]
foreach ($chapter in $chapters) {
    $path = Join-Path (Join-Path $src 'chapters') $chapter
    $content = Get-Content -LiteralPath $path -Raw -Encoding UTF8
    $content = Convert-EnvSyntax -Text $content
    $bodyParts.Add("`n% ===== Copied from learn-lisanshuxue/chapters/$chapter =====`n$content")
}

$ending = "`n\end{document}`n"
[System.IO.File]::WriteAllText($out, $preamble + $middle + ($bodyParts -join "`n") + $ending, [System.Text.UTF8Encoding]::new($false))
Write-Output "Created $out"
