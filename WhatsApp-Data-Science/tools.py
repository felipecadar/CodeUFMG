import numpy as np
import pandas as pd
import string

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from scipy import stats
from scipy.stats import mode

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import itertools

from datetime import datetime, date

import matplotlib.pyplot as plt

from statsmodels.distributions.empirical_distribution import ECDF

# GREEN RED BLUE PURPLE #a65628

DIAS = [
    'SEGUNDA',
    'TERCA',
    'QUARTA',
    'QUINTA',
    'SEXTA',
    'SABADO',
    'DOMINGO'
]


def addWeekday(df):
    dia_da_semana = []
    for s_data in df['DATA']:
        d,m,y = list(map(int,s_data.split("/")))
        dia_da_semana.append(DIAS[date(year=y, day=d, month=m).weekday()])
    df['DIA'] = dia_da_semana

def histWeek(df):
    WORKDAY = ["TERCA", "QUARTA"]
    WEEKEND = DIAS[-2:]
    weekend_hist = []
    workday_hist = []
    fig, axiss = plt.subplots(ncols=2, sharey=True)

    for user in df['NOME'].unique():
        user_df = df[df["NOME"] == user]
        for day in WORKDAY:
            workday_hist.extend(user_df[user_df['DIA'] == day]["HORA"].values)
        for day in WEEKEND:
            weekend_hist.extend(user_df[user_df['DIA'] == day]["HORA"].values)

    axiss[0].hist(workday_hist, bins=range(25), density=False, color="#377eb8", alpha=0.6)
    axiss[1].hist(weekend_hist, bins=range(25), density=False, color="#ff7f00", alpha=0.6)
    
    hist1=np.histogram(workday_hist, bins=range(25))
    hist2=np.histogram(weekend_hist, bins=range(25))
        
    axiss[0].axvline(np.average(hist1[1][:-1], weights=hist1[0]) , label='Hora Média', color='#4daf4a', alpha=0.7)
    axiss[1].axvline(np.average(hist2[1][:-1], weights=hist2[0]) , label='Hora Média', color='#4daf4a', alpha=0.7)
    
    axiss[0].axhline(np.average(hist1[0]) , label='Média de Mensagens', color='#f781bf', alpha=0.7)
    axiss[1].axhline(np.average(hist2[0]) , label='Média de Mensagens', color='#f781bf', alpha=0.7)

    axiss[0].set_title("Terça-Quarta")
    axiss[1].set_title("Sábado-Domingo")

    for ax in axiss:
        ax.set_xlabel("Hora do Dia")
        ax.set_ylabel("#Mensagens Enviadas")
        ax.legend()
    plt.show()
    return (fig, axiss)


def genDatasetSequencia(df, op):
    users = df['NOME'].unique()
    data = {}
    for u in users:
        data[u] = {'x':[0], 'y':[0]}

    last_user = df.iloc[0].NOME
    message_sizes = []
    for idx, row in df.iterrows():
        if last_user == row.NOME:
            data[row.NOME]["x"][-1] += 1
            message_sizes.append(len(row.MSG))
            if idx == len(df)-1:
                data[row.NOME]["y"][-1] = op(message_sizes)           
        else:
            data[last_user]["y"][-1] = op(message_sizes)

            data[row.NOME]["x"].append(1)
            data[row.NOME]["y"].append(0)
            message_sizes = [len(row.MSG)]
            
            if idx == len(df)-1:
                data[row.NOME]["y"][-1] = len(row.MSG)

            last_user = row.NOME
    return data

def plotSequencia(data, op='Soma'):
    fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

    for i, key in enumerate(sorted(data.keys())):
        x = data[key]['x'] + np.random.rand(len(data[key]['x'])) - 0.5
        y = data[key]['y']
        axiss[i].scatter(x, y, alpha=0.1, color=colors[i%len(colors)])
        axiss[i].set_xlabel("#Mensagens")
        axiss[i].set_ylabel("{} do tamanho das mensagens".format(op))
        axiss[i].set_title("{} do tamanho das mensagens X Tamanho da sequência de mensagens - {}".format(op, key))
        
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return (fig, axiss)

def plotHistSequenciaOp(data, op="Media"):
    fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

    for i, key in enumerate(sorted(data.keys())):
        y = data[key]['y']
        axiss[i].hist(y, bins=range(0,150,5), alpha=0.6, color=colors[i%len(colors)])
        axiss[i].set_xlabel("{} do tamanho das mensagens".format(op))
        axiss[i].set_title("Distribuição da {} do tamanho das mensagens - ".format(op, key))
        
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return (fig, axiss)

def plotHistTamanhoSequencia(data):
    fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

    for i, key in enumerate(sorted(data.keys())):
        x = data[key]['x']
        axiss[i].hist(x, bins=range(0,15,1), alpha=0.6, color=colors[i%len(colors)])
        axiss[i].set_xlabel("Tamanho da sequência de mensagens")
        axiss[i].set_title("Distribuição do tamanho da sequência de mensagens - {}".format(key))
        
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return (fig, axiss)

def plotHistRazaoSequencia(data):
    fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

    for i, key in enumerate(sorted(data.keys())):
        x = np.array(data[key]['x'])
        y = np.array(data[key]['y'])
        
        x[x == 0] = 1
        
        razoes = y/x
        IC = getIC(razoes)

        axiss[i].hist(razoes, bins=25, alpha=0.4, color=colors[i%len(colors)])
        axiss[i].axvline(IC[0], color="#4daf4a", label='IC inferior {:.3}'.format(IC[0]))
        axiss[i].axvline(IC[1], color="#a65628", label='IC superior {:.3}'.format(IC[1]))
        axiss[i].set_xlabel("Razão")
        axiss[i].set_title("Distribuição das Razões com Intervalo de Confiança de 95% - {}".format(key))
        axiss[i].legend()
        
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return (fig, axiss)

def getIC(data):    
    # data = []
    # for i in range(10000):
    #     medias = np.random.choice(data, 40).mean()
    #     data.append(medias)
    
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    se = std / np.sqrt(len(data))
    
    return (mean - 1.96 * se, mean + 1.96 * se)
    
#     fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
#     colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

#     for i, key in enumerate(sorted(data.keys())):
#         x = np.array(data[key]['x'])
#         y = np.array(data[key]['y'])
        
#         x[x == 0] = 1
        
#         razoes = y/x
#         ecdf = ECDF(razoes, side='left')

#         axiss[i].plot(ecdf.x, ecdf.y)
#         axiss[i].set_xlabel('Razao')
#         axiss[i].set_ylabel('P[X <= x]')
#         axiss[i].set_title(key)
#     plt.show()

def plotHistSequencia(data, op):
    fig, axiss = plt.subplots(nrows = 2, ncols=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']

    for i, key in enumerate(sorted(data.keys())):
        x = data[key]['x']
        axiss[1][i].hist(x, bins=range(0,15,1), alpha=0.6, color=colors[i%len(colors)])
        axiss[1][i].set_xlabel("Tamanho da sequência de mensagens")
        axiss[1][i].set_title("Distribuição do tamanho da sequência de mensagens - {}".format(key))
        
        y = data[key]['y']
        axiss[0][i].hist(y, bins=range(0,150,5), alpha=0.6, color=colors[i%len(colors)])
        axiss[0][i].set_xlabel("{} do tamanho das mensagens".format(op))
        axiss[0][i].set_title("Distribuição da {} do tamanho das mensagens - {}".format(op, key))
        
    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return (fig, axiss)

# from datetime import datetime
# def genDatasetRegressao(df):
#     dias = list(df["DATE"].unique())
#     x = [0]
#     y = []
#     last_user = df.iloc[0].NOME
#     for idx, row in df.iterrows():
#         if last_user == row.NOME:
#             x[-1] += 1
#         else:
#             last_user = row.NOME
#             # x[-1] += np.random.rand() - 0.5
#             x.append(0)
#             d,m,year = list(map(int,df.iloc[idx-1].DATE.split("/")))
#             hora = int(df.iloc[idx-1].DATA)
#             minuto = int(df.iloc[idx-1].MINUTES)
#             last_time = datetime(year, m, d, hora, minuto, 0)
#             d,m,year = list(map(int,df.iloc[idx].DATE.split("/")))
#             hora = int(df.iloc[idx].DATA)
#             minuto = int(df.iloc[idx].MINUTES)
#             ans_time = datetime(year, m, d, hora, minuto, 0)
#             diff = (ans_time - last_time).total_seconds()/60
#             y.append(min(max(diff, 0), 1000))
        
#     return (x[:-1], y)

def tempoResposta(df):
    y = {}
    for user in df['NOME'].unique():
        y[user] = []
        
    last_user = df.iloc[0].NOME
    for idx, row in df.iterrows():
        if last_user == row.NOME:
            pass
        else:
            last_user = row.NOME
            d,m,year = list(map(int,df.iloc[idx-1].DATA.split("/")))
            hora = int(df.iloc[idx-1].HORA)
            minuto = int(df.iloc[idx-1].MINUTO)
            last_time = datetime(year, m, d, hora, minuto)
            d,m,year = list(map(int,df.iloc[idx].DATA.split("/")))
            hora = int(df.iloc[idx].HORA)
            minuto = int(df.iloc[idx].MINUTO)
            ans_time = datetime(year, m, d, hora, minuto)
            diff = float((ans_time - last_time).total_seconds())
            if diff/60 < 200:
                y[row.NOME].append(diff/60)

    return y

def plotHistTempoResposta(data, join=False):
    if join:
        all_x = []
        for i, key in enumerate(data.keys()):
            x = data[key]
            all_x.extend(x)

        x = all_x
        bins = list(range(0, 40, 1)) + [200]
        hist = np.histogram(x, bins=bins, density=True)
        p = pd.DataFrame({'x':hist[1][1:],'UUUUUUUUUUU':hist[0]}).plot(x='x',kind='bar', alpha=0.6, color='#377eb8')

        p.axvline(np.average(list(range(0, 40, 1)), weights=hist[0]), color = "#4daf4a")
        p.axvline(np.median(x), color='#f781bf')
        p.axvline(mode(x)[0][0], color='#a65628')

        p.set_title("Distribuição do tempo de resposta em minutos")
        p.set_xlabel("Tempo de Resposta (Min)")
        p.set_ylabel("Prob")
        p.legend(["Média", "Mediana", "Moda", "Todos os Usuários"])

        plt.show()
        return p
    else:
        fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True)
        colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
        for i, key in enumerate(data.keys()):
            x = data[key]
            bins = list(range(0, 40, 1)) + [200]
            hist = np.histogram(x, bins=bins, density=True)
            p = pd.DataFrame({'x':hist[1][1:],'UUUUUUUUUUU':hist[0]}).plot(x='x',kind='bar', ax=axiss[i], alpha=0.6, color=colors[i%len(colors)])

            axiss[i].axvline(np.average(list(range(0, 40, 1)), weights=hist[0]), color = "#4daf4a")
            axiss[i].axvline(np.median(x), color='#f781bf')
            axiss[i].axvline(mode(x)[0][0], color='#a65628')

            axiss[i].set_title("Distribuição do tempo de resposta em minutos")
            axiss[i].set_xlabel("Tempo de Resposta (Min)")
            axiss[i].set_ylabel("Prob")
            axiss[i].legend(["Média", "Mediana", "Moda", key])

        plt.subplots_adjust(hspace=0.4)
        plt.show()
        return (fig, axiss)

def plotBootstrapMeans(data_list, label=None):
    if label == None:
        label = list(range(len(data_list)))
    fig1, [ax1, ax2] = plt.subplots(ncols=2, figsize=(22, 8))
    boot_iters = 10000
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
    styles = ['solid', 'dashed', 'dashdot', 'dotted']
    to_plot = pd.DataFrame()
    for idx, data in enumerate(data_list):
        means = []
        for key in data.keys():
            for i in range(boot_iters):
                means.append(sampleMean(data[key], samples=300))
        to_plot[label[idx]] = means
        IC = getIC(data[key])
        hist = np.histogram(means, bins = 50, density=True)
        ax1.plot(hist[1][:-1], hist[0],  linewidth=5.0 ,color=colors[idx%len(colors)], alpha = 0.6, label="Data {}".format(label[idx]))
        # ax1.plot(hist[1], np.insert(hist[0], 0, 0),  linewidth=5.0 ,color=colors[idx%len(colors)], alpha = 0.6, label="Data {}".format(label[idx]))
        # ax1.hist(means, bins=50, density=True, linewidth=5.0 ,color=colors[idx%len(colors)], alpha = 0.6, label="Data {}".format(label[idx]))
        ax1.axvline(IC[0], ls="solid", color=colors[idx%len(colors)], label="IC inicial {:.3} - {}".format(IC[0], label[idx]))
        ax1.axvline(IC[1], ls="dashdot", color=colors[idx%len(colors)], label="IC final {:.3} - {}".format(IC[1], label[idx]))
    
    ax1.set_title("Distribuição de médias com bootstrap e intervalos de confiaça")
    ax2.set_title("Plot dos quartis das médias do bootstrap")

    ax1.legend()

    to_plot.boxplot(grid=False, sym='', whis=[5, 95], showmeans=True, ax=ax2)

    plt.show()
def sampleMean(x, samples=40):
    return np.mean(np.random.choice(x, samples))
    

def plotTamanhoMensagem(df, keys=None):
    if keys is None:
        keys = df["NOME"].unique()
    
    dict_lens = {}
    fig, axiss = plt.subplots(nrows=len(keys), sharey=True)
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
    for i, user in enumerate(keys):
        user_df = df[df["NOME"] == user]
        dict_lens[user] = user_df["MSG"].str.len().tolist()
        axiss[i].hist(dict_lens[user], bins = list(range(0,200,3))+[201], alpha=0.6, color=colors[i%len(colors)])
        axiss[i].set_xlabel("Tamanho da Mensagem")
        axiss[i].set_ylabel("#Mensagens")
        axiss[i].set_title("Distribuição do tamnho das mensagens - User {}".format(user))
        axiss[i].axvline(np.average(dict_lens[user]), label="Tamanho Médio")
        axiss[i].legend()

    plt.subplots_adjust(hspace=0.4)
    plt.show()
    return dict_lens

def Regressao(data):
    fig, axiss = plt.subplots(nrows=len(data.keys()), sharey=True, figsize=(15,12))
    colors = ['#377eb8', '#ff7f00', '#4daf4a','#f781bf', '#a65628', '#984ea3','#999999', '#e41a1c', '#dede00']
    print("-------------------------")
    for i, key in enumerate(sorted(data.keys())):
        x = (np.array(data[key]['x']) +  np.random.rand(len(data[key]['x'])) - 0.5).reshape(-1,1)
        y = np.array(data[key]['y'])
        lin_reg = LinearRegression()
        lin_reg.fit(x, y)

        r_sq = lin_reg.score(x, y)
        print('coefficient of determination:', r_sq)

        print('intercept:', lin_reg.intercept_)
        print('slope:', lin_reg.coef_)
        print("-------------------------")

        axiss[i].scatter(x, y, alpha=0.6, color=colors[i%len(colors)])
        axiss[i].plot(sorted(x), lin_reg.predict(sorted(x)), color = "#a65628", label='Regression')
        axiss[i].set_xlabel("#Mensagens")
        axiss[i].set_ylabel("Soma do tamanho das mensagens")
        axiss[i].legend()
    plt.show()
    
    ##############################################
    



def Preprocess(tex):
    nopunct=[char for char in tex if char not in string.punctuation]
    nopunct=''.join(nopunct)
    filtered = [word.lower() for word in nopunct.split() if word.lower() not in stopwords.words('portuguese')]
    return filtered
#     return [word if list(np.unique(list(word))) == ["K"] else "K" for word in filtered ] #substituir risadas de tamanhos diferentes por apenas "K"

def Encoder(df):
    y = df['NOME']
    X = df['MSG']
    labelencoder = LabelEncoder()
    y = labelencoder.fit_transform(y)
    return (X,y)

def GenDataset(df):
    X,y = Encoder(df)
    X_train, X_test, y_train, y_test = train_test_split(X, y
                                      ,test_size=0.2, random_state=1234)
    bow_transformer=CountVectorizer(analyzer=Preprocess).fit(X_train)
    # transforming into Bag-of-Words and hence textual data to numeric..
    text_bow_train=bow_transformer.transform(X_train)#ONLY TRAINING DATA
    # transforming into Bag-of-Words and hence textual data to numeric..
    text_bow_test=bow_transformer.transform(X_test)#TEST DATA
    
    return (X_train, X_test, y_train, y_test, text_bow_train, text_bow_test)

def TrainTest(dataset, df):
    X_train, X_test, y_train, y_test, text_bow_train, text_bow_test = dataset
    model = MultinomialNB()
    model = model.fit(text_bow_train, y_train)
    print("Treino: ", model.score(text_bow_train, y_train))
    print("Teste: ",model.score(text_bow_test, y_test))
    
    predictions = model.predict(text_bow_test)
    print(classification_report(y_test,predictions))

    cm = confusion_matrix(y_test,predictions)
    plt.figure()
    plot_confusion_matrix(cm, classes=np.unique(df["NOME"]), normalize=True, title='Confusion Matrix')
    return model

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(cm)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0])
                                  , range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    
    
################################################

def Vocabulario(df):
    vocabulario = {}
    for i, user in enumerate(df["NOME"].unique()):
        user_df = df[df["NOME"] == user]
        vocab = []
        for idx, row in user_df.iterrows():
            vocab.extend(Preprocess(row.MSG))
         
        vocabulario[user] = set(np.unique(vocab))
        
    return vocabulario

from collections import Counter
def histPalavras(df):
#     vocab = Vocabulario(df)
    for i, user in enumerate(df["NOME"].unique()):
#         v = vocab[user]
        user_df = df[df["NOME"] == user]
        all_words = []
        for idx, row in user_df.iterrows():
            msg = row.MSG
            if list(np.unique(list(msg.lower()))) != ["k"] and len(msg) < 100:
                all_words.extend(Preprocess(row.MSG))

        hist = Counter(all_words)
        print(hist)
#         print('Ready')
#         pd.Series(all_words).value_counts().plot('bar')
#         plt.show()
#         print('DOne')