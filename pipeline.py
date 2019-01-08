from tools import *
from string import punctuation
import os
from gensim.models import word2vec
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

data_dir = './data'
data_tar = os.path.join(data_dir, 'SogouCS.reduced.tar.gz')
data_original_dir = os.path.join(data_dir, 'original')
data_transcoding_dir = os.path.join(data_dir, 'transcoding')
data_clean_xml_dir = os.path.join(data_dir, 'clean_xml')
data_connect_txt = os.path.join(data_dir, 'connect.txt')
data_connect_clean_txt = os.path.join(data_dir, 'connect_clean.txt')
data_connect_cut_txt = os.path.join(data_dir, 'connect_cut.txt')
data_w2v_model = os.path.join(data_dir, 'w2v_model')
data_w2v_label = os.path.join(data_dir, 'w2v_label.txt')


def batch_transcoding(from_dir, to_dir):
    print("开始批量转码")
    os.makedirs(to_dir, exist_ok=True)
    for o_file_path in os.listdir(from_dir):
        from_path = os.path.join(from_dir, o_file_path)
        to_path = os.path.join(to_dir, o_file_path)
        transcoding(from_path, to_path, from_enc='gb18030')


def batch_clean_xml(from_dir, to_dir):
    print("开始批量清理xml标签")
    os.makedirs(to_dir, exist_ok=True)
    for o_file_path in os.listdir(from_dir):
        from_path = os.path.join(from_dir, o_file_path)
        to_path = os.path.join(to_dir, o_file_path)
        remove_xml(from_path, to_path)


def connect_all_txt(from_dir, to_txt):
    '''
    连接所有文本
    :param from_dir:
    :param to_txt:
    :return:
    '''
    print("开始连接所有文本")
    file_path_list = []
    for file in os.listdir(from_dir):
        file_path = os.path.join(from_dir, file)
        file_path_list.append(file_path)
    connect_txt(file_path_list, to_txt)


def clean_txt(from_txt, to_txt):
    print("开始清洗文本")
    add_punc = punctuation + '，。、【 】 “”：；（）《》‘’{}？！⑦()、%^>℃：.．”“^-——=&#@￥０１２３４５６７８９〔〕' \
                             '．－／㎡……［］＜＞→↖ ←↗＂×％　'
    to_file = open(to_txt, 'a+')
    with open(from_txt, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            line = str(line).replace(" ", "").strip()
            if line:
                for w in add_punc:
                    if w in line:
                        line = line.replace(w, ' ')
                while "  " in line:
                    line = line.replace("  ", " ")
                to_file.write(line + os.linesep)
            print("清洗进度 > {rate}%".format(rate=(index / len(lines)) * 100))
    to_file.close()


def train_w2c(from_txt, to_model_file):
    print("开始训练")
    sentences = word2vec.LineSentence(from_txt)
    model = word2vec.Word2Vec(sentences, size=200, window=5, min_count=5, workers=4)
    model.save(to_model_file)


def run():
    # remove_if_exist(data_original_dir)
    # untar(data_tar, data_original_dir)
    #
    # remove_if_exist(data_transcoding_dir)
    # batch_transcoding(data_original_dir, data_transcoding_dir)
    #
    # remove_if_exist(data_clean_xml_dir)
    # batch_clean_xml(data_transcoding_dir, data_clean_xml_dir)
    #
    # remove_if_exist(data_connect_txt)
    # connect_all_txt(data_clean_xml_dir, data_connect_txt)
    #
    # remove_if_exist(data_connect_clean_txt)
    # clean_txt(data_connect_txt, data_connect_clean_txt)
    #
    # remove_if_exist(data_connect_cut_txt)
    # cut_word(data_connect_clean_txt, data_connect_cut_txt)

    remove_if_exist(data_w2v_model)
    train_w2c(data_connect_cut_txt, data_w2v_model)


if __name__ == '__main__':
    run()
