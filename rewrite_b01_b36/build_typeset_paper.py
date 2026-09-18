from pathlib import Path
import re, subprocess, tempfile

ROOT = Path(__file__).resolve().parent
MD = ROOT / '18_FULL_MANUSCRIPT_V1.md'
TEX = ROOT / 'paper_layout.tex'
PDF = ROOT / 'paper_layout.pdf'

raw = MD.read_text(encoding='utf-8')
# YAML title
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
yaml = m.group(1) if m else ''
title_m = re.search(r'^title:\s*"(.*)"\s*$', yaml, re.M)
title = title_m.group(1) if title_m else 'AstraBuild'
text = raw[m.end():] if m else raw

# Extract abstract and body.
ma = re.search(r'# Abstract\n\n(.*?)\n\n---\n\n# 1 Introduction', text, re.S)
if not ma:
    raise SystemExit('Could not locate abstract/introduction boundary')
abstract_md = ma.group(1).strip()
body_md = '# 1 Introduction' + text[ma.end():]
# Remove separator rules and manual numbering; LaTeX handles section numbering.
body_md = re.sub(r'^---\s*$', '', body_md, flags=re.M)
body_md = re.sub(r'^(#{1,3})\s+\d+(?:\.\d+)*\s+', r'\1 ', body_md, flags=re.M)

# Replace the four-band markdown table with a compact raw LaTeX table*.
table_re = re.compile(
    r'\| Descriptive band \| Batches \| Representative targets \| Structural issue introduced \|\n'
    r'\|---\|---\|---\|---\|\n'
    r'(?:\|.*\|\n){4}', re.M)
table_tex = r'''\begin{table*}[t]
\centering
\caption{Orientation to the B01--B36 sequential record. The bands summarize target structure; they are not a shared difficulty scale or discovered task regimes.}
\label{tab:study-bands}
\small
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}{@{}p{0.16\textwidth}p{0.09\textwidth}p{0.28\textwidth}X@{}}
\toprule
\textbf{Descriptive band} & \textbf{Batches} & \textbf{Representative targets} & \textbf{Structural issue introduced} \\
\midrule
Local fitted structures & B01--B06 & arresters, wall, gate & comparison domain, rigid pose, simple fitted geometry \\
Repeated equipment & B07--B19 & transformers, capacitor banks, two anonymized voltage classes GIS & reusable components, variants, master/site boundaries \\
Connected systems & B20--B30 & busbars, insulators, jumpers, conductors & ports, routes, flexible paths, continuity, unexplained occupancy \\
Site closure & B31--B36 & buildings, cabins, ground, auxiliary facilities, bus racks & residual reconstruction under a large inherited state \\
\bottomrule
\end{tabularx}
\end{table*}
'''
body_md, ntable = table_re.subn(lambda _: table_tex, body_md, count=1)
if ntable not in (0, 1):
    raise SystemExit(f'Unexpected number of study tables replaced: {ntable}')

figure_specs = {
    1: ('figures/fig01_problem_method_answer_b01_b36.png', 0.285, 'fig:overview'),
    2: ('figures/fig02_longitudinal_map_b01_b36.png', 0.255, 'fig:timeline'),
    3: ('figures/fig03_operator_portfolio_b01_b36.png', 0.245, 'fig:operators'),
    4: ('figures/fig04_structural_transitions_b01_b36.png', 0.335, 'fig:transitions'),
    5: ('figures/fig05_persistent_state_dependency_b01_b36.png', 0.300, 'fig:persistence'),
}
# Convert markdown figure + following prose caption into one full-width LaTeX float.
for num, (path, maxh, label) in figure_specs.items():
    pat = re.compile(rf'!\[Figure {num}\.[^\n]*\]\([^)]+\)\n\n\*Figure {num}\. ([^\n]+)\*')
    mm = pat.search(body_md)
    if not mm:
        raise SystemExit(f'Figure {num} marker not found')
    cap = mm.group(1)
    # Let pandoc escape the caption text separately by inserting only plain markdown caption into raw TeX later.
    # Escape a minimal safe subset needed by current captions.
    cap_tex = (cap.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_'))
    fig_tex = rf'''\begin{{figure*}}[!t]
\centering
\includegraphics[width=\textwidth,height={maxh}\textheight,keepaspectratio]{{{path}}}
\caption{{{cap_tex}}}
\label{{{label}}}
\end{{figure*}}'''
    body_md = body_md[:mm.start()] + fig_tex + body_md[mm.end():]

# Render abstract to LaTeX as a fragment.
def pandoc_fragment(md_text: str) -> str:
    p = subprocess.run(
        ['pandoc', '-f', 'markdown+raw_tex+tex_math_single_backslash', '-t', 'latex', '--natbib', '--bibliography=references.bib'],
        input=md_text, text=True, cwd=ROOT, capture_output=True, check=True)
    return p.stdout.strip()

abstract_tex = pandoc_fragment(abstract_md)
body_tex = pandoc_fragment(body_md)
# Remove Pandoc hyperlink wrapper noise around headings while keeping labels harmless.
# Section titles are already unnumbered in markdown; LaTeX will number them.

preamble = r'''\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,top=15mm,bottom=16mm,left=15mm,right=15mm]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{amsmath,amssymb}
\usepackage{natbib}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{dblfloatfix}
\usepackage{balance}
\usepackage{url}

\definecolor{LinkBlue}{RGB}{45,87,140}
\hypersetup{colorlinks=true,linkcolor=LinkBlue,citecolor=LinkBlue,urlcolor=LinkBlue}
\setcitestyle{numbers,square,sort&compress}
\setlength{\columnsep}{5.2mm}
\setlength{\parindent}{1em}
\setlength{\parskip}{0pt}
\setlength{\textfloatsep}{7pt plus 2pt minus 2pt}
\setlength{\floatsep}{6pt plus 1pt minus 1pt}
\setlength{\intextsep}{6pt plus 1pt minus 1pt}
\captionsetup{font=small,labelfont=bf,labelsep=period,skip=3pt}
\titleformat{\section}{\large\bfseries}{\thesection}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.45em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{0.4em}{}
\titlespacing*{\section}{0pt}{1.3ex plus .4ex minus .2ex}{0.7ex}
\titlespacing*{\subsection}{0pt}{1.05ex plus .3ex minus .2ex}{0.45ex}
\titlespacing*{\subsubsection}{0pt}{0.9ex plus .2ex minus .2ex}{0.35ex}
\setlist{nosep,leftmargin=*}
\raggedbottom
\emergencystretch=1.2em
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\renewcommand{\abstractname}{Abstract}
\renewcommand{\refname}{References}
'''

safe_title = title.replace('&', r'\&').replace('_', r'\_')
front = rf'''\begin{{document}}
\makeatletter
\twocolumn[
\begin{{@twocolumnfalse}}
\vspace*{{-1.2em}}
\begin{{center}}
{{\LARGE\bfseries {safe_title}\par}}
\vspace{{0.45em}}
{{\small Advisor-discussion draft · B01--B36 clean-sheet version\par}}
\end{{center}}
\vspace{{0.35em}}
\begin{{abstract}}
{abstract_tex}
\end{{abstract}}
\vspace{{0.6em}}
\end{{@twocolumnfalse}}
]
\makeatother
'''

ending = r'''\balance
\small
\bibliographystyle{unsrtnat}
\bibliography{references}
\end{document}
'''

TEX.write_text(preamble + '\n' + front + '\n' + body_tex + '\n' + ending, encoding='utf-8')
print(TEX)
