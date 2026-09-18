"""Typeset the AstraBuild manuscript in single-column reference style.

Style follows the GPT-Policy reference front page: left-aligned bold title,
italic author/affiliation lines, plain full-width abstract without a heading,
and a shaded box with Code/Website links. Single column throughout.

Usage:
    python3 build_typeset_paper_v25.py        # English  -> paper_layout_v25.tex
    python3 build_typeset_paper_v25.py zh     # Chinese  -> paper_layout_v25_zh.tex
"""
from pathlib import Path
import re, subprocess, sys

ROOT = Path(__file__).resolve().parent
ZH = 'zh' in sys.argv[1:]

MD = ROOT / ('24_FULL_MANUSCRIPT_ZH_V24.md' if ZH else '22_FULL_MANUSCRIPT_FIGURE_V24.md')
TEX = ROOT / ('paper_layout_v25_zh.tex' if ZH else 'paper_layout_v25.tex')

raw = MD.read_text(encoding='utf-8')
m = re.match(r'^---\n(.*?)\n---\n', raw, re.S)
yaml = m.group(1) if m else ''
title_m = re.search(r'^title:\s*"(.*)"\s*$', yaml, re.M)
title = title_m.group(1) if title_m else 'AstraBuild'
text = raw[m.end():] if m else raw

if ZH:
    ma = re.search(r'# 摘要\n\n(.*?)\n\n---\n\n# 1 引言', text, re.S)
else:
    ma = re.search(r'# Abstract\n\n(.*?)\n\n---\n\n# 1 Introduction', text, re.S)
if not ma:
    raise SystemExit('Could not locate abstract/introduction boundary')
abstract_md = ma.group(1).strip()
body_md = text[ma.end():]
body_md = re.sub(r'^---\s*$', '', body_md, flags=re.M)
body_md = re.sub(r'^(#{1,3})\s+\d+(?:\.\d+)*\s+', r'\1 ', body_md, flags=re.M)

if ZH:
    failures_tex = r'''\begin{table}[t]
\centering
\caption{B01--B36 中有据可查的失败事件，按层归因。来源：保存的批次档案与验证链。}
\label{tab:failures}
\small
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}{@{}p{0.055\textwidth}p{0.145\textwidth}XX@{}}
\toprule
\textbf{事件} & \textbf{失败层} & \textbf{可观测证据} & \textbf{应对} \\
\midrule
B01 & 评估协议 & 留出的圆柱区域 RMS 4.84/7.32/5.10 cm 违反 5 cm 筛查；比较域混入了目标柱体与附件几何 & B02 分离拟合区域与留出区域；修订后的指标被声明为与 B01 不可直接比较 \\
B15 & 可复用抽象边界 & 局部测量被相邻设备污染；共享母线管段主组件在实际长度不同的安装之间产生重叠 & 修订测量方法；有限的现场专用几何移出共享主组件；废弃支架归档而非覆盖 \\
B23 & 表示类别 & 直线引线假设被配准源中 $\approx$0.5 m 的跨中弓形偏移否定 & 重新组织为受约束曲线路径；由确定性代码拟合端点固定的 B 样条；保留 r1--r3 修订链 \\
B25/B26 & 任务选择 & 结构在模型中缺失，而其台账条目显示已解决 & 对选定高处区域的覆盖率 audit 成为任务选择信号；$>$1 m 未解释样本比例 78.8\% $\rightarrow$ 14.6\%（B26） \\
B36 & 由 review 发现的遗漏 & 低压侧母线构架缺失；遗漏追溯到此前将该结构划在变压器组件之外的决定 & 先进行仅检索的历史追查，再经多次修订重建，包括为避开消防立管的 0.16 m 位移 \\
\bottomrule
\end{tabularx}
\end{table}
'''
    ledger_tex = r'''\begin{table}[t]
\centering
\caption{持续状态台账：后续批次消费什么、如何检查、上游状态出错会传播什么。}
\label{tab:ledger}
\small
\setlength{\tabcolsep}{5pt}
\renewcommand{\arraystretch}{1.12}
\begin{tabularx}{\textwidth}{@{}p{0.055\textwidth}p{0.215\textwidth}XX@{}}
\toprule
\textbf{批次} & \textbf{消费的继承资产} & \textbf{验证检查} & \textbf{若资产出错时的传播面} \\
\midrule
B23 & B08 变压器端子接口 & 对保存路径的端点/端接检查 & 此后每一处中性点引线连接都会落到错误的端子上 \\
B29 & 此前建模的线夹与悬挂/引线端点 & 独立于粗模表面一致性检查端点关系 & 线夹移位会使多个间隔的耐张串与跳线脱开 \\
B31 & 七千余个既有站变换 & 对继承变换做状态保持测试 & 变换漂移会无声地移动已被接受的设备 \\
B36 & 36,615 个既有对象、7,114 个既有站变换、2,798 个受保护文件 & 保持检查加显式碰撞/干涉检查 & 过时的端头或套管会使闭合其上的新母线走错路由 \\
\bottomrule
\end{tabularx}
\end{table}
'''
    findings_tables = [
        (re.compile(r'\*\*表 1\.\*\*[^\n]*\n\n\| 事件 \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), failures_tex, 'failures'),
        (re.compile(r'\*\*表 2\.\*\*[^\n]*\n\n\| 批次 \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), ledger_tex, 'ledger'),
    ]
else:
    failures_tex = r'''\begin{table}[t]
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
\end{table}
'''
    ledger_tex = r'''\begin{table}[t]
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
\end{table}
'''
    findings_tables = [
        (re.compile(r'\*\*Table 1\.\*\*[^\n]*\n\n\| Episode \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), failures_tex, 'failures'),
        (re.compile(r'\*\*Table 2\.\*\*[^\n]*\n\n\| Batch \|[^\n]*\n\|---\|---\|---\|---\|\n(?:\|.*\|\n)+', re.M), ledger_tex, 'ledger'),
    ]
for pat, tex, name in findings_tables:
    body_md, n = pat.subn(lambda _: tex, body_md, count=1)
    if n != 1:
        raise SystemExit(f'Findings table {name} replaced {n} times (expected 1)')

if ZH:
    figure_specs = {
        1: ('figure_v24/hybrid_pdf/fig01_overview_v24.pdf', 0.300, 'fig:overview'),
        2: ('figures/fig02_longitudinal_map_b01_b36.png', 0.330, 'fig:timeline'),
        3: ('figures/fig03_operator_portfolio_b01_b36.png', 0.270, 'fig:operators'),
        4: ('figure_v24/hybrid_pdf/fig04_transitions_v24.pdf', 0.430, 'fig:transitions'),
        5: ('figure_v24/hybrid_pdf/fig05_persistence_v24.pdf', 0.380, 'fig:persistence'),
        6: ('figure_v24/hybrid_pdf/fig06_findings_v24_zh.pdf', 0.300, 'fig:findings'),
        7: ('figure_v24/hybrid_pdf/fig07_session_anatomy_v24_zh.pdf', 0.330, 'fig:session'),
    }
else:
    figure_specs = {
        1: ('figure_v24/hybrid_pdf/fig01_overview_v24.pdf', 0.300, 'fig:overview'),
        2: ('figures/fig02_longitudinal_map_b01_b36.png', 0.330, 'fig:timeline'),
        3: ('figures/fig03_operator_portfolio_b01_b36.png', 0.270, 'fig:operators'),
        4: ('figure_v24/hybrid_pdf/fig04_transitions_v24.pdf', 0.430, 'fig:transitions'),
        5: ('figure_v24/hybrid_pdf/fig05_persistence_v24.pdf', 0.380, 'fig:persistence'),
        6: ('figure_v24/hybrid_pdf/fig06_findings_v24.pdf', 0.300, 'fig:findings'),
        7: ('figure_v24/hybrid_pdf/fig07_session_anatomy_v24.pdf', 0.330, 'fig:session'),
    }
for num, (path, maxh, label) in figure_specs.items():
    if ZH:
        pat = re.compile(rf'!\[Figure {num}\.[^\n]*\]\([^)]+\)\n\n\*图 {num}\. ([^\n]+)\*')
    else:
        pat = re.compile(rf'!\[Figure {num}\.[^\n]*\]\([^)]+\)\n\n\*Figure {num}\. ([^\n]+)\*')
    mm = pat.search(body_md)
    if not mm:
        raise SystemExit(f'Figure {num} marker not found')
    cap = mm.group(1)
    cap_tex = (cap.replace('&', r'\&').replace('%', r'\%').replace('_', r'\_'))
    fig_tex = rf'''\begin{{figure}}[!t]
\centering
\includegraphics[width=\textwidth,height={maxh}\textheight,keepaspectratio]{{{path}}}
\caption{{{cap_tex}}}
\label{{{label}}}
\end{{figure}}'''
    body_md = body_md[:mm.start()] + fig_tex + body_md[mm.end():]

def pandoc_fragment(md_text: str) -> str:
    p = subprocess.run(
        ['pandoc', '-f', 'markdown+raw_tex+tex_math_single_backslash-latex_macros', '-t', 'latex', '--natbib', '--bibliography=references.bib'],
        input=md_text, text=True, cwd=ROOT, capture_output=True, check=True)
    return p.stdout.strip()

abstract_tex = pandoc_fragment(abstract_md)
body_tex = pandoc_fragment(body_md)

if ZH:
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
\usepackage[a4paper,top=19mm,bottom=20mm,left=19mm,right=19mm]{geometry}
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
\usepackage{url}

\definecolor{LinkBlue}{RGB}{45,87,140}
\hypersetup{unicode=true,colorlinks=true,linkcolor=LinkBlue,citecolor=LinkBlue,urlcolor=LinkBlue}
\setcitestyle{numbers,square,sort&compress}
\setlength{\parindent}{2em}
\setlength{\parskip}{0pt}
\setlength{\textfloatsep}{8pt plus 2pt minus 2pt}
\setlength{\floatsep}{7pt plus 1pt minus 1pt}
\setlength{\intextsep}{7pt plus 1pt minus 1pt}
\captionsetup{font=small,labelfont=bf,labelsep=period,skip=3pt}
\renewcommand{\figurename}{图}
\renewcommand{\tablename}{表}
\renewcommand{\refname}{参考文献}
\titleformat{\section}{\large\bfseries}{\thesection}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.45em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{0.4em}{}
\titlespacing*{\section}{0pt}{1.6ex plus .4ex minus .2ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{1.2ex plus .3ex minus .2ex}{0.5ex}
\titlespacing*{\subsubsection}{0pt}{1.0ex plus .2ex minus .2ex}{0.4ex}
\setlist{nosep,leftmargin=*}
\raggedbottom
\emergencystretch=1.2em
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
'''
else:
    preamble = r'''\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage[a4paper,top=19mm,bottom=20mm,left=19mm,right=19mm]{geometry}
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
\usepackage{url}

\definecolor{LinkBlue}{RGB}{45,87,140}
\hypersetup{colorlinks=true,linkcolor=LinkBlue,citecolor=LinkBlue,urlcolor=LinkBlue}
\setcitestyle{numbers,square,sort&compress}
\setlength{\parindent}{1em}
\setlength{\parskip}{0pt}
\setlength{\textfloatsep}{8pt plus 2pt minus 2pt}
\setlength{\floatsep}{7pt plus 1pt minus 1pt}
\setlength{\intextsep}{7pt plus 1pt minus 1pt}
\captionsetup{font=small,labelfont=bf,labelsep=period,skip=3pt}
\titleformat{\section}{\large\bfseries}{\thesection}{0.5em}{}
\titleformat{\subsection}{\normalsize\bfseries}{\thesubsection}{0.45em}{}
\titleformat{\subsubsection}{\normalsize\itshape}{\thesubsubsection}{0.4em}{}
\titlespacing*{\section}{0pt}{1.6ex plus .4ex minus .2ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{1.2ex plus .3ex minus .2ex}{0.5ex}
\titlespacing*{\subsubsection}{0pt}{1.0ex plus .2ex minus .2ex}{0.4ex}
\setlist{nosep,leftmargin=*}
\raggedbottom
\emergencystretch=1.2em
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\providecommand{\tightlist}{\setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
'''

safe_title = title.replace('&', r'\&').replace('_', r'\_')
if ZH:
    authors_line = r'Walter Wang, P. Li, J. Di, H. Luo$^{*}$'
    affil_line = '中国科学技术大学'
    corr_line = '$^{*}$通讯作者'
    code_label = '代码'
    site_label = '项目网页'
else:
    authors_line = r'Walter Wang, P. Li, J. Di, H. Luo$^{*}$'
    affil_line = 'University of Science and Technology of China'
    corr_line = '$^{*}$Corresponding author'
    code_label = 'Code'
    site_label = 'Website'

front = rf'''\begin{{document}}
\noindent{{\LARGE\bfseries {safe_title}\par}}
\vspace{{0.9em}}

\noindent{{\small\itshape {authors_line}\par}}
\vspace{{0.15em}}
\noindent{{\small\itshape {affil_line}\par}}
\vspace{{0.15em}}
\noindent{{\small\itshape {corr_line}\par}}
\vspace{{1.0em}}

{{\small {abstract_tex}\par}}
\vspace{{0.8em}}

\noindent\colorbox{{black!6}}{{\parbox{{\dimexpr\linewidth-2\fboxsep\relax}}{{\small\textbf{{{code_label}:}} \url{{https://github.com/cookiegg/AstraBuild}}\\[2pt]\textbf{{{site_label}:}} \url{{https://cookiegg.github.io/AstraBuild/}}}}}}
\vspace{{0.8em}}
'''

ending = r'''\small
\bibliographystyle{unsrtnat}
\bibliography{references}
\end{document}
'''

TEX.write_text(preamble + '\n' + front + '\n' + body_tex + '\n' + ending, encoding='utf-8')
print(TEX)
