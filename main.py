import pandas as pd
import matplotlib.pyplot as plt
import ezodf
from pandas_ods_reader import read_ods
import math
import numpy as np


def read_odsmy(filename, microsecond, sheet_no=0, header=0):
    # tab = ezodf.opendoc(filename=filename).sheets[sheet_no]
    df = read_ods(filename, sheet_no)

    # df = pd.DataFrame({col[header].value: [x.value for x in col[header + 1:]]
    #                  for col in tab.columns()})
    for col in list(df.columns):
        if isinstance(df[col][0], str):
            df[col] = (df[col].str.replace(r' ms', '000'))
            df[col] = (df[col].str.replace(r'\D', '')).astype('int64')
            if not microsecond:
                df[col] = df[col] / 1000
    return df


def save_Bbox(sheet_no, table_name, rowNum, oneRow, microsecond, explainationRow):
    data = read_odsmy('testResultRaw.ods', microsecond, sheet_no)
    print(table_name)

    data.columns = data.columns.str.replace('Picnic', 'P')
    fig, axs = plt.subplots(rowNum, oneRow)
    plt.setp(axs.flat, ylabel=explainationRow)  # xlabel='X-label',
    # plt.ylabel(u"\u03bcs")
    # plt.xlabel("Signature Schemes with Key Blinding")
    row = 0
    coll = 0
    colors = ['#73020C', '#229954', '#D94D1A', '#FFC300', '#A3E4D7', '#D7BDE2', '#82E0AA', '#2C3E50', '#AF7AC5',
              '#AED6F1', '#E74C3C', '#CCD1D1', '#633974', '#2874A6']
    # axs[0][0].annotate(explainationRow, xy=(0, 0.5), xytext=(-axs[0][0].yaxis.labelpad - 5, 0),
    #            xycoords=axs[0][0].yaxis.label, textcoords='offset points',
    #            size='large', ha='right', va='center')
    description = ''
    for col in list(data.columns):
        print(data[col].describe())
        latexName = (col.replace('_', '\_'))
        description = description + latexName.replace('P', 'Picnic') + ' & ' + str(data[col].min()) + ' & ' + \
                      str(data[col].mean()) + ' & ' + str(data[col].max()) + '\\\\ \n'

        colorNum = colors[(row) * oneRow + coll]
        color = dict(color=colors[(row) * oneRow + coll])
        box = axs[row, coll].boxplot(data[col], patch_artist=True, flierprops=dict(markeredgecolor=colorNum))
        # boxprops=color, medianprops=color, whiskerprops=color, capprops=color, flierprops=dict(markeredgecolor=colorNum) ,labels=[col]
        axs[row, coll].set_title(col, color=colorNum)

        box['boxes'][0].set_facecolor(colorNum)
        coll = 1 + coll
        if coll % oneRow == 0:
            row = row + 1
            coll = 0
    print(description)
    for index in range(len(data.columns), rowNum * oneRow):
        row = math.floor(len(data.columns) / oneRow)
        col = len(data.columns) % oneRow
        axs[row, col].axis('off')
    fig.subplots_adjust(left=0.08, right=0.98, bottom=0.05, top=0.9,
                        hspace=0.7, wspace=1.8)
    # data.boxplot(grid='True', column=list(data.columns), color='black')
    # boxplot = data.boxplot(figsize = (5,5), rot = 90, fontsize= '8', grid = False)

    # data.boxplot(grid='True',column =[data.columns.values] ,color='red')

    plt.savefig(table_name + '.png', dpi=150, bbox_inches="tight")
    plt.clf()


def save_BboxAllTogether(sheet_no, table_name, rowNum, oneRow, microsecond, explainationRow):
    data = read_odsmy('testResultRaw.ods', microsecond, sheet_no)
    print(table_name)

    data.columns = data.columns.str.replace('Picnic', 'P')
    colors = ['#73020C', '#229954', '#D94D1A', '#FFC300', '#A3E4D7', '#D7BDE2', '#82E0AA', '#2C3E50', '#AF7AC5',
              '#AED6F1', '#E74C3C', '#CCD1D1', '#633974', '#2874A6']

    data.boxplot(labels=list(data.columns))

    plt.ylabel(explainationRow)
    plt.xticks(rotation=90)
    plt.xlabel("Signature Schemes with Key Blinding")
    plt.savefig(table_name + '_All.png', dpi=150, bbox_inches="tight")
    plt.clf()


def save_BboxAllTogetherLog(sheet_no, table_name, rowNum, oneRow, microsecond, explainationRow):
    data = read_odsmy('testResultRaw.ods', microsecond, sheet_no)
    data.columns = data.columns.str.replace('Picnic', 'P')
    colors = ['#73020C', '#229954', '#D94D1A', '#FFC300', '#A3E4D7', '#D7BDE2', '#82E0AA', '#2C3E50', '#AF7AC5',
              '#AED6F1', '#E74C3C', '#CCD1D1', '#633974', '#2874A6']
    print(data.columns)
    data.boxplot(labels=list(data.columns))
    plt.ylabel(explainationRow)
    plt.yscale('log')
    plt.xticks(rotation=90)
    plt.xlabel("Signature Schemes with Key Blinding")
    plt.savefig(table_name + '_All_Log.png', dpi=150, bbox_inches="tight")
    plt.clf()


def saveSizeVSDur():
    dataSize = pd.Series(read_odsmy('testResultRaw.ods', False, 2).mean(), name= 'Sig_Size(avg)').to_frame()
    dataDur = pd.Series(read_odsmy('testResultRaw.ods', False, 3).mean(), name= 'Sig_Dur(avg)').to_frame()

    df = pd.concat([dataSize, dataDur], axis=1, join="inner")
    print(df)
    colors = ['#73020C', '#229954', '#D94D1A', '#FFC300', '#A3E4D7', '#D7BDE2', '#82E0AA', '#2C3E50', '#AF7AC5',
              '#AED6F1', '#E74C3C', '#CCD1D1']
    l = 0
    zipped= zip(colors,list(df.index.values))

    # m=df.plot(style='.-', x='Signing Duration', y='Signature Size (Avg)',  color=colors[l])

    fig, ax = plt.subplots()
    for color, scheme in  list(zipped):
        ax.scatter(x=df.loc[[scheme],['Sig_Size(avg)']], y=df.loc[[scheme],['Sig_Dur(avg)']],  c=color, label = scheme)
    ax.legend(bbox_to_anchor=(1.1, 1.05))
    ax.set_ylabel('Signing Duration(Avg)')
    ax.set_xlabel('Signature Size(Avg)')
    plt.grid(True)
    plt.savefig('sizeVSdur.png', dpi=150, bbox_inches="tight")


def main():
    save_Bbox(1, "veryDur", 3, 5, False, 'Run Time[ms]')
    save_Bbox(2, "SignSize", 3, 4, False, 'Size[byte]')
    save_Bbox(3, "signDur", 3, 5, False, 'Run Time[ms]')
    save_Bbox(4, "keyblindDur", 3, 5, True, 'Run Time[\u03bcs]')
    save_Bbox(5, "keygenDur", 3, 5, True, 'Run Time[\u03bcs]')

    save_BboxAllTogether(1, "veryDur", 3, 5, False, 'Run Time[ms]')
    save_BboxAllTogether(2, "SignSize", 3, 4, False, 'Size[byte]')
    save_BboxAllTogether(3, "signDur", 3, 5, False, 'Run Time[ms]')
    save_BboxAllTogether(4, "keyblindDur", 3, 5, True, 'Run Time[\u03bcs]')
    save_BboxAllTogether(5, "keygenDur", 3, 5, True, 'Run Time[\u03bcs]')

    save_BboxAllTogetherLog(1, "veryDur", 3, 5, False, 'Run Time[ms]')
    save_BboxAllTogetherLog(2, "SignSize", 3, 4, False, 'Size[byte]')
    save_BboxAllTogetherLog(3, "signDur", 3, 5, False, 'Run Time[ms]')
    save_BboxAllTogetherLog(4, "keyblindDur", 3, 5, True, 'Run Time[\u03bcs]')
    save_BboxAllTogetherLog(5, "keygenDur", 3, 5, True, 'Run Time[\u03bcs]')


saveSizeVSDur()
