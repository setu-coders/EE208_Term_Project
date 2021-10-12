import paddle
import jieba
paddle.enable_static()

contents = "在新世纪福音战士中，我试图将一个四年间破碎又无能为力的我，全部都放进去。逃避了四年，仅仅是没死而已的我，仅仅因为一个念头“不能逃避！”而开始制作这部作品。我的意图是在电影中留下深刻印象。"
jieba.enable_paddle()
cut_words = jieba.cut(contents,cut_all=True)    # requires paddlepaddle. -> pip install paddlepaddle
print(" ".join(cut_words))