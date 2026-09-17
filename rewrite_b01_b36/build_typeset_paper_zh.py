from pathlib import Path
import re, subprocess

ROOT = Path(__file__).resolve().parent
MD = ROOT / '19_FULL_MANUSCRIPT_ZH_V1.md'
TEX = ROOT / 'paper_layout_zh.tex'
PDF = ROOT / 'paper_layout_zh.pdf'

raw = MD.read_text(encoding='utf-8')
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
yaml = m.group(1) if m else ''
title_m = re.search(r'^title:\s*"(.*)"\s*$', yaml, re.M)
title = title_m.group(1) if title_m else 'AstraBuild'
text = raw[m.end():] if m else raw

ma = re.search(r'# 摘要\n\n(.*?)\n\n---\n\n# 1 引言', text, re.S)
if not ma:
    raise SystemExit('Could not locate Chinese abstract/introduction boundary')
abstract_md = ma.group(1).strip()
body_md = '# 1 引言' + text[ma.end():]
body_md = re.sub(r'^---\s*$', '', body_md, flags=re.M)
body_md = re.sub(r'^(#{1,3})\s+\d+(?:\.\d+)*\s+', r'\1 ', body_md, flags=re.M)

figure_specs = {
    1: ('figures/fig01_problem_method_answer_b01_b36_zh.png', 0.285, 'fig:overview'),
    2: ('figures/fig02_longitudinal_map_b01_b36_zh.png', 0.255, 'fig:timeline'),
    3: ('figures/fig03_operator_portfolio_b01_b36_zh.png', 0.245, 'fig:operators'),
    4: ('figures/fig04_structural_transitions_b01_b36_zh.png', 0.335, 'fig:transitions'),
    5: ('figures/fig05_persistent_state_dependency_b01_b36_zh.png', 0.300, 'fig:persistence'),
}
for num, (path, maxh, label) in figure_specs.items():
    pat = re.compile(rf'!\[图 {num}\.[^\n]*\]\([^)]+\)\n\n\*图 {num}\. ([^\n]+)\*')
    mm = pat.search(body_md)
    if not mm:
        raise SystemExit(f'Chinese Figure {num} marker not found')
    cap = mm.group(1)
    cap_tex = (cap.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_'))
    fig_tex = rf'''\begin{{figure*}}[!t]
\centering
\includegraphics[width=\textwidth,height={maxh}\textheight,keepaspectratio]{{{path}}}
\caption{{{cap_tex}}}
\label{{{label}}}
\end{{figure*}}'''
    body_md = body_md[:mm.start()] + fig_tex + body_md[mm.end():]


def pandoc_fragment(md_text: str) -> str:
    p = subprocess.run(
        ['pandoc', '-f', 'markdown+raw_tex+tex_math_single_backslash', '-t', 'latex', '--natbib', '--bibliography=references.bib'],
        input=md_text, text=True, cwd=ROOT, capture_output=True, check=True)
    return p.stdout.strip()

abstract_tex = pandoc_fragment(abstract_md)
body_tex = pandoc_fragment(body_md)

preamble = r'''\documentclass[10pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont{TeX Gyre Termes}
\setsansfont{TeX Gyre Heros}
\setmonofont{Latin Modern Mono}
\setCJKmainfont{Noto Serif CJK SC}
\setCJKsansfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\usepackage[a4paper,top=15mm,bottom=16mm,left=15mm,right=15mm]{geometry}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{tabularx}
\usepackage{array}
\usepackage{amsmath,amssymb}
\usepackage{natbib}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{caption}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage{dblfloatfix}
\usepackage{balance}
\usepackage{url}

\definecolor{LinkBlue}{RGB}{45,87,140}
\hypersetup{unicode=true,colorlinks=true,linkcolor=LinkBlue,citecolor=LinkBlue,urlcolor=LinkBlue}
\setcitestyle{numbers,square,sort&compress}
\setlength{\columnsep}{5.2mm}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\setlength{\textfloatsep}{7pt plus 2pt minus 2pt}
\setlength{\floatsep}{6pt plus 1pt minus 1pt}
\setlength{\intextsep}{6pt plus 1pt minus 1pt}
\captionsetup{font=small,labelfont=bf,labelsep=period,skip=3pt}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\renewcommand{\abstractname}{摘要}
\renewcommand{\refname}{参考文献}
\titleformat{\section}{\large\bfseries\sffamily}{\thesection}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries\sffamily}{\thesubsection}{0.45em}{}
\titleformat{\subsubsection}{\normalsize\bfseries}{\thesubsubsection}{0.4em}{}
\titlespacing*{\section}{0pt}{1.3ex plus .4ex minus .2ex}{0.7ex}
\titlespacing*{\subsection}{0pt}{1.05ex plus .3ex minus .2ex}{0.45ex}
\titlespacing*{\subsubsection}{0pt}{0.9ex plus .2ex minus .2ex}{0.35ex}
\setlist{nosep,leftmargin=*}
\raggedbottom
\emergencystretch=1.0em
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
'''

safe_title = title.replace('&', r'\&').replace('_', r'\_')
front = rf'''\begin{{document}}
\makeatletter
\twocolumn[
\begin{{@twocolumnfalse}}
\vspace*{{-1.2em}}
\begin{{center}}
{{\LARGE\bfseries\sffamily {safe_title}\par}}
\vspace{{0.45em}}
{{\small 老师讨论稿 · B01--B36 clean-sheet 中文版\par}}
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
