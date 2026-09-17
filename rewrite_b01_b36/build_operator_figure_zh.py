#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from pathlib import Path
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

HERE = Path(__file__).resolve().parent
ASTRABUILD = HERE.parent
CATALOG = ASTRABUILD / 'release' / 'process_catalog.json'
DATA_DIR = HERE / 'data'
FIG_DIR = HERE / 'figures'

plt.rcParams.update({'font.family':'WenQuanYi Zen Hei','axes.unicode_minus':False})

ROWS = [
    ('拟合', lambda d: 'fit' in d['stages']),
    ('测量', lambda d: 'measure' in d['stages']),
    ('检查', lambda d: 'inspect' in d['stages']),
    ('规划', lambda d: 'plan' in d['stages']),
    ('细化', lambda d: 'refine' in d['stages']),
    ('审计', lambda d: 'audit' in d['stages']),
    ('交互式复核', lambda d: bool(d.get('review_page'))),
    ('发现 / 特征', lambda d: any(x in d['stages'] for x in ('discover','features'))),
    ('碰撞 / 干涉', lambda d: 'collision' in d['stages']),
]
BANDS = [(1,6,'局部拟合结构'),(7,19,'重复设备'),(20,30,'连接系统'),(31,36,'场站闭合')]


def load_batches():
    catalog=json.loads(CATALOG.read_text())
    batches=[]
    for d in catalog['dossiers']:
        bid=d.get('batch','')
        if re.fullmatch(r'B\d\d', bid) and 1 <= int(bid[1:]) <= 36:
            batches.append(d)
    batches.sort(key=lambda d:int(d['batch'][1:]))
    assert [d['batch'] for d in batches] == [f'B{i:02d}' for i in range(1,37)]
    return batches


def write_csv(batches,matrix):
    DATA_DIR.mkdir(parents=True,exist_ok=True)
    out=DATA_DIR/'operator_matrix_b01_b36_zh.csv'
    with out.open('w',newline='') as f:
        w=csv.writer(f); w.writerow(['算子',*[d['batch'] for d in batches]])
        for (label,_),row in zip(ROWS,matrix): w.writerow([label,*row.astype(int).tolist()])


def draw(batches,matrix):
    FIG_DIR.mkdir(parents=True,exist_ok=True)
    fig,ax=plt.subplots(figsize=(15.2,5.6))
    cmap=ListedColormap(['#f2f2f2','#222222'])
    ax.imshow(matrix,aspect='auto',interpolation='nearest',cmap=cmap,vmin=0,vmax=1)
    ax.set_yticks(range(len(ROWS))); ax.set_yticklabels([r[0] for r in ROWS],fontsize=9.5)
    ax.set_xticks(range(36)); ax.set_xticklabels([d['batch'] for d in batches],rotation=90,fontsize=7.4)
    ax.set_xlabel('连续重建批次',fontsize=10)
    ax.set_xticks(np.arange(-0.5,36,1),minor=True); ax.set_yticks(np.arange(-0.5,len(ROWS),1),minor=True)
    ax.grid(which='minor',linewidth=.25,alpha=.28); ax.tick_params(which='minor',bottom=False,left=False)
    for start,end,label in BANDS:
        x0=start-1; x1=end-1
        if start>1: ax.axvline(x0-.5,linewidth=1.15,color='black')
        ax.text((x0+x1)/2,-1.00,label,ha='center',va='bottom',fontsize=9.2,fontweight='bold',clip_on=False)
    ax.set_title('由保存工作流工件重建的 B01–B36 算子集合',fontsize=12.5,pad=34)
    fig.text(.5,.012,
             '深色单元格表示存在对应命名阶段或原始交互式 review 工件。Build 与 validate 构成全部 36 个批次共有的主干，因此未显示。该记录为描述性工作流证据，不是标准化动作遥测。',
             ha='center',va='bottom',fontsize=8.5)
    fig.subplots_adjust(left=.13,right=.99,top=.80,bottom=.24)
    png=FIG_DIR/'fig03_operator_portfolio_b01_b36_zh.png'
    fig.savefig(png,dpi=220,bbox_inches='tight')
    fig.savefig(FIG_DIR/'fig03_operator_portfolio_b01_b36_zh.svg',bbox_inches='tight')
    plt.close(fig)
    Image.open(png).convert('RGB').save(FIG_DIR/'fig03_operator_portfolio_b01_b36_zh.pdf','PDF',resolution=220.0)


def main():
    batches=load_batches(); matrix=np.array([[fn(d) for d in batches] for _,fn in ROWS],dtype=int)
    write_csv(batches,matrix); draw(batches,matrix)
    print(FIG_DIR/'fig03_operator_portfolio_b01_b36_zh.svg')

if __name__=='__main__': main()
