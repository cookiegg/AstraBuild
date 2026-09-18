from pathlib import Path
import re, subprocess, tempfile

ROOT = Path(__file__).resolve().parent
MD = ROOT / '22_FULL_MANUSCRIPT_FIGURE_V24.md'
TEX = ROOT / 'paper_layout_v24.tex'
PDF = ROOT / 'paper_layout_v24.pdf'

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
Repeated equipment & B07--B19 & transformers, capacitor banks, 110/220 kV GIS & reusable components, variants, master/site boundaries \\
Connected systems & B20--B30 & busbars, insulators, jumpers, conductors & ports, routes, flexible paths, continuity, unexplained occupancy \\
Site closure & B31--B36 & buildings, cabins, ground, auxiliary facilities, bus racks & residual reconstruction under a large inherited state \\
\bottomrule
\end{tabularx}
\end{table*}
'''
body_md, ntable = table_re.subn(lambda _: table_tex, body_md, count=1)
if ntable not in (0, 1):
    raise SystemExit(f'Unexpected number of study tables replaced: {ntable}')

# Replace the two Findings markdown tables (caption line + table) with raw LaTeX table* floats.
failures_tex = r'''\begin{table*}[t]
\centering
\caption{Documented failure episodes in B01--B36, attributed by layer. Sources: preserved batch dossiers and validation chains.}
\label{tab:failures}
\small
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}{@{}p{0.055\textwidth}p{0.145\textwidth}XX@{}}
\toprule
\textbf{Episode} & \textbf{Failure layer} & \textbf{Observable evidence} & \textbf{Response} \\
\midrule
B01 & Evaluation protocol & Held-out cylindrical-domain RMS 4.84/7.32/5.10 cm violates the 5 cm screen; comparison domain mixed the target shaft with accessory geometry & B02 separates fitting and holdout regions; the revised metric is declared not directly comparable to B01 \\
B15 & Reusable-abstraction boundary & Local measurement contaminated by neighboring equipment; shared bus-spool master overlapped installations with different physical extents & Measurement method revised; finite site-specific geometry moved out of the shared master; obsolete supports archived, not overwritten \\
B23 & Representation class & Straight-lead hypothesis contradicted by a $\approx$0.5 m mid-span bow in the registered source & Reformulated as a constrained curved path; fixed-endpoint B-spline fitted by deterministic code; r1--r3 revision chain preserved \\
B25/B26 & Task selection & Structures absent from the model while their inventory entry appeared resolved & Coverage audit over selected high regions becomes a task-selection signal; $>$1 m unexplained-sample fraction 78.8\% $\rightarrow$ 14.6\% (B26) \\
B36 & Omission surfaced by review & Low bus racks missing; omission traced to an earlier decision that treated the structure as outside the transformer assembly & Audit-only history search, then a multi-revision rebuild including a 0.16 m displacement to avoid a fire riser \\
\bottomrule
\end{tabularx}
\end{table*}
'''
ledger_tex = r'''\begin{table*}[t]
\centering
\caption{Persistent-state ledger: what later batches consume, how it is checked, and what a wrong upstream state would propagate.}
\label{tab:ledger}
\small
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}{@{}p{0.055\textwidth}p{0.215\textwidth}XX@{}}
\toprule
\textbf{Batch} & \textbf{Inherited asset consumed} & \textbf{Validation check} & \textbf{Propagation surface if the asset were wrong} \\
\midrule
B23 & B08 transformer terminal interface & Endpoint/termination checks on the saved path & Every later neutral-lead connection would land on a wrong terminal \\
B29 & Previously modeled clamps and suspension/lead endpoints & Endpoint relations checked independently of coarse-surface agreement & Displaced clamps would detach strings and jumpers across intervals \\
B31 & More than 7,000 existing station transforms & State-preservation tests over inherited transforms & Transform drift would silently move already-accepted equipment \\
B36 & 36,615 previous objects, 7,114 prior station transforms, 2,798 protected files & Preservation checks plus explicit collision/interference checks & Inherited stubs or bushings that no longer match the site would misroute new busbars closing onto them \\
\bottomrule
\end{tabularx}
\end{table*}
'''
findings_tables = [
    (re.compile(r'\*\*Table 1\.\*\*[^\n]*\n\n\| Episode \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), failures_tex, 'failures'),
    (re.compile(r'\*\*Table 2\.\*\*[^\n]*\n\n\| Batch \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), ledger_tex, 'ledger'),
]
for pat, tex, name in findings_tables:
    body_md, n = pat.subn(lambda _: tex, body_md, count=1)
    if n != 1:
        raise SystemExit(f'Findings table {name} replaced {n} times (expected 1)')

figure_specs = {
    1: ('figure_v24/hybrid_pdf/fig01_overview_v24.pdf', 0.340, 'fig:overview'),
    2: ('figures/fig02_longitudinal_map_b01_b36.png', 0.340, 'fig:timeline'),
    3: ('figures/fig03_operator_portfolio_b01_b36.png', 0.285, 'fig:operators'),
    4: ('figure_v24/hybrid_pdf/fig04_transitions_v24.pdf', 0.560, 'fig:transitions'),
    5: ('figure_v24/hybrid_pdf/fig05_persistence_v24.pdf', 0.420, 'fig:persistence'),
    6: ('figure_v24/hybrid_pdf/fig06_findings_v24.pdf', 0.330, 'fig:findings'),
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
    page_break = ''
    fig_tex = page_break + rf'''\begin{{figure*}}[!t]
\centering
\includegraphics[width=\textwidth,height={maxh}\textheight,keepaspectratio]{{{path}}}
\caption{{{cap_tex}}}
\label{{{label}}}
\end{{figure*}}'''
    body_md = body_md[:mm.start()] + fig_tex + body_md[mm.end():]

# Render abstract to LaTeX as a fragment.
def pandoc_fragment(md_text: str) -> str:
    p = subprocess.run(
        ['pandoc', '-f', 'markdown+raw_tex+tex_math_single_backslash-latex_macros', '-t', 'latex', '--natbib', '--bibliography=references.bib'],
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
\renewcommand{\dbltopfraction}{0.92}
\renewcommand{\dblfloatpagefraction}{0.80}
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
{{\normalsize Walter Wang, hb.luo, pf.li, j.di, y.cao, y.kang\par}}
\vspace{{0.3em}}
{{\small Advisor-discussion draft · B01--B36 figure-v2.4 version\par}}
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
