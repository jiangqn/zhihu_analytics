import requests
import re
import time
import jieba
from collections import Counter
from wordcloud import WordCloud

from src.utils.constants import headers, stopwords_path, font_path
from src.utils.load_stopwords import load_stopwords

def get_page(question_id: int, offset: int) -> dict:
    # 利用知乎API请求json数据
    # question_id: 知乎问题号
    # offset: 第几页
    # 知乎API
    url = "https://www.zhihu.com/api/v4/questions/{}/answers?include=content&limit=20&offset={}&platform=desktop&sort_by=default".format(
        question_id, offset)
    # https://www.zhihu.com/api/v4/questions/281789365/answers?include=content&limit=20&offset=20&platform=desktop&sort_by=default
    # https://www.zhihu.com/question/281789365
    res = requests.get(url, headers=headers)
    res.encoding = "utf-8"
    return res.json()

reg = re.compile("<[^>]*>")

def get_answers(question_id: int):
    answers = []
    offset = 0
    while True:
        page = get_page(question_id, offset)
        page_answers = page["data"]
        if len(page_answers) == 0 or len(answers) >= 1000:
            break

        for answer in page_answers:
            content = answer["content"]
            content = reg.sub("", content).replace("\n", "").replace(" ", "")
            answers.append(
                {
                    "question_id": question_id,
                    "author_id": answer["author"]["id"],
                    "author_name": answer["author"]["name"],
                    "answer_id": answer["id"],
                    "answer_content": content
                }
            )
        offset += 20
        # time.sleep(1)
    return answers

def normal_cut_sentence(text):
    text = re.sub('([。！？\?])([^’”])',r'\1\n\2',text)#普通断句符号且后面没有引号
    text = re.sub('(\.{6})([^’”])',r'\1\n\2',text)#英文省略号且后面没有引号
    text = re.sub('(\…{2})([^’”])',r'\1\n\2',text)#中文省略号且后面没有引号
    text = re.sub('([.。！？\?\.{6}\…{2}][’”])([^’”])',r'\1\n\2',text)#断句号+引号且后面没有引号
    return text.split("\n")

stopwords = load_stopwords(stopwords_path)

def create_wordcloud(question_id: int) -> None:
    answers = get_answers(question_id)

    words = []
    for answer in answers:
        document = answer["answer_content"]
        sentences = normal_cut_sentence(document)
        for sentence in sentences:
            words.extend(jieba.lcut(sentence))

    words = " ".join(words)

    wordcloud = WordCloud(
        font_path=font_path,
        background_color="white",
        width=1000,
        height=700,
        stopwords=stopwords,
        max_words=100
    ).generate(words)
    wordcloud.to_file("static/zhihu.png")