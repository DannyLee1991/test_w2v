from gensim.models import word2vec
from pipeline import data_w2v_model, data_w2v_label
import matplotlib.pyplot as plt
import numpy as np
import os


def load_model():
    return word2vec.Word2Vec.load(data_w2v_model)


def similarity(word1, word2):
    return load_model().wv.similarity(word1, word2)


def most_similar(word_list_1, word_list_2):
    return load_model().wv.most_similar(word_list_1, word_list_2)


def view_tsne():
    visualizeVecs = []
    visualizeWords = []
    model = load_model()
    word_list = model.wv.index2word
    for word in word_list[:500]:
        vec = model[word]
        visualizeWords.append(word)
        visualizeVecs.append(vec)

    visualizeVecs = np.array(visualizeVecs).astype(np.float64)

    temp = (visualizeVecs - np.mean(visualizeVecs, axis=0))
    covariance = 1.0 / visualizeVecs.shape[0] * temp.T.dot(temp)
    U, S, V = np.linalg.svd(covariance)
    coord = temp.dot(U[:, 0:2])
    for i in range(len(visualizeWords)):
        color = 'red'
        plt.text(coord[i, 0], coord[i, 1], visualizeWords[i], bbox=dict(facecolor=color, alpha=0.1),
                 fontsize=22)  # fontproperties = ChineseFont1
    plt.xlim((np.min(coord[:, 0]), np.max(coord[:, 0])))
    plt.ylim((np.min(coord[:, 1]), np.max(coord[:, 1])))
    plt.show()


if __name__ == '__main__':
    # # 两个词的相关性
    # r = similarity('谷歌', '苹果')
    # print(r)
    # # 女人 + 国王 - 男人
    # r = most_similar(['女人', '国王'], ['男人'])
    # print(r)

    view_tsne()
