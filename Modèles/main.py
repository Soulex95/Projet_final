# Importer les bibliothèques necessaires
from flask import Flask, render_template
from flask_paginate import Pagination, get_page_args
import pandas as pd
import pickle as pkl

app = Flask(__name__,template_folder='templates')

Modele1 = "Model1.py"
content = open(Modele1).read()
exec(content)

Modele2 = "Model2.py"
content = open(Modele2).read()
exec(content)
# Telecharger les modèles
Model1 = pkl.load(open("model1.pickle", "rb"))
matrix = pkl.load(open("matrix.pickle", "rb"))
Model2 = pkl.load(open("model2.pickle", "rb"))
matrix2 = pkl.load(open("matrix2.pickle", "rb"))
df1 = pkl.load(open("df1.pickle", "rb"))
df = pkl.load(open("df.pickle", "rb"))
df_likes = pkl.load(open("df_likes.pickle", "rb"))

def get_data(dt,offset=0, per_page=10):
    return dt[offset: offset + per_page]

def index(dt):
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(dt)
    pagination_dt = get_data(dt,offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('index.html',
                           users=pagination_dt,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )
# créer les liens de connexions
def getrecom(iduser,ch="all"): # une fonction getrecom pour recommander a un utilisateur
    estim=Model1.loc[iduser,:]
    donne=matrix.loc[iduser,matrix.loc[iduser,:] > 0]
    if ch=="discover":
        res=estim
    else:
        res=estim.append(donne)
    res=res.sort_values(ascending=False)[0:len(df_likes)]
    result=pd.DataFrame(res)
    #liste.append(result.index)
    liste = pd.DataFrame(result.index, columns=['user'])
    data = []
    for k in df['user_id']:
        if k in liste['user']:
            data.append(df.loc[k])

    dt= pd.DataFrame(data)
    #dt.drop_duplicates(keep = 'first', inplace=True)
    dt=dt.reset_index(drop=True)

    #userid=10
    verif = []
    for i in range(len(df_likes)):#['user_id']:
        if iduser == df_likes['user_id'][i]:
            verif.append(df_likes['post_id'][i])
    #verif
    for k in verif:
        for l in range(len(dt)):#['id']:
            if k == dt['id'][l]:
                dt['i_liked'][l] = 1
    blankIndex = [''] * len(dt)
    dt.index = blankIndex
    #dt = HTML(dt.to_html(index=False))
    #dt = dt.set_index(inplace = True)
    return index(dt)

def recommand(iduser,ch="all"): # une fonction getrecom pour recommander a un utilisateur
    estim=Model2.loc[iduser,:]
    donne=matrix2.loc[iduser,matrix2.loc[iduser,:] > 0]
    if ch=="discover":
        res=estim
    else:
        res=estim.append(donne)
    res=res.sort_values( ascending=False)[0:len(df1)]
    result=pd.DataFrame(res)
    #liste.append(result.index)
    liste = pd.DataFrame(result.index, columns=['user'])
    data = []
    for k in df['user_id']:
        if k in liste['user']:
            data.append(df.loc[k])

    dt= pd.DataFrame(data)
    #dt.drop_duplicates(keep = 'first', inplace=True)
    dt=dt.reset_index(drop=True)

    #userid=10
    verif = []
    for i in range(len(df_likes)):#['user_id']:
        if iduser == df_likes['user_id'][i]:
            verif.append(df_likes['post_id'][i])
    #verif
    for k in verif:
        for l in range(len(dt)):#['id']:
            if k == dt['id'][l]:
                dt['i_liked'][l] = 1
    blankIndex = [''] * len(dt)
    dt.index = blankIndex
    #dt = HTML(dt.to_html(index=False))
    return index(dt)

def recom_pop(iduser):
    counter = df_likes['post_id'].value_counts()
    counter = counter.to_frame(name='counter').reset_index()
    df_count = []
    for i in range(len(counter)):
        if counter['counter'][i] > 10:
            df_count.append(counter['index'][i])
    for i in range(len(df_likes)):
        if (df_likes['post_id'][i] in df_count and df_likes['user_id'][i] == iduser):
            df_count.remove(df_likes['post_id'][i])
    data = []
    for k in df['user_id']:
        if k in df_count:
            data.append(df.loc[k])
    dt = pd.DataFrame(data)
    dt = dt.reset_index(drop=True)

    verif = []
    for i in range(len(df_likes)):
        if iduser == df_likes['user_id'][i]:
            verif.append(df_likes['post_id'][i])

    for k in verif:
        for l in range(len(dt)):
            if k == dt['id'][l]:
                dt['i_liked'][l] = 1
    blankIndex = [''] * len(dt)
    dt.index = blankIndex
    # dt = HTML(dt.to_html(index=False))
    return index(dt)

@app.route('/final_recom', methods=['GET'])
def final_recom(iduser=10):
    if iduser not in df_likes['user_id']:
        return recommand(iduser,ch="all")
    else:
        return getrecom(iduser,ch="discover")

if __name__ == '__main__':
    app.run(debug=True)