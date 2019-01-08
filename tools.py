import tarfile
import os
import re
import shutil
import jieba


def untar(fname, dirs):
    '''
    解压缩
    :param fname:
    :param dirs:
    :return:
    '''
    print("开始解压")
    t = tarfile.open(fname)
    t.extractall(path=dirs)


def remove_if_exist(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            print("清空 > {path}".format(path=path))
            shutil.rmtree(path)
        else:
            print("删除 > {path}".format(path=path))
            os.remove(path)


def transcoding(from_file, to_file, from_enc, to_enc='utf-8'):
    '''
    转码
    :param from_file:
    :param to_file:
    :param from_enc:
    :param to_enc:
    :return:
    '''
    cmd = "cat {from_file} | iconv -f {from_enc} -t {to_enc} | grep \"<content>\" > {to_file}".format(
        from_file=from_file, to_file=to_file, from_enc=from_enc, to_enc=to_enc)
    os.system(cmd)


def remove_xml(from_file, to_file):
    '''
    提出标签
    :param from_file:
    :param to_file:
    :return:
    '''
    pat = re.compile('<[^>]+>', re.S)
    with open(from_file, 'r') as ff:
        c = pat.sub('', ff.read())
        with open(to_file, 'w') as tf:
            tf.write(c)


def connect_txt(input_txt_list, output_txt):
    '''
    合并文本
    :param input_txt_list:
    :param output_txt:
    :return:
    '''
    with open(output_txt, 'w') as of:
        for index, input_file in enumerate(input_txt_list):
            print("connect > {crt}/{total}".format(crt=index + 1, total=len(input_txt_list)))
            with open(input_file, 'r') as inf:
                in_txt = inf.read()
                of.write(in_txt)
    print("connect finish!")


def cut_word(from_txt, to_txt):
    '''
    分词
    :param from_txt:
    :param to_txt:
    :return:
    '''
    print("开始分词")
    to_file = open(to_txt, 'a+')
    with open(from_txt, 'r') as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            new_line = " ".join(jieba.cut(line))
            while "  " in new_line:
                new_line = new_line.replace("  ", " ")
                to_file.write(new_line)
            print("分词进度 > {rate}%".format(rate=(index / len(lines)) * 100))
    to_file.close()


if __name__ == '__main__':
    for txt in os.listdir('./data'):
        print(txt)
