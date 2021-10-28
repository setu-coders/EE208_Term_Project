测试方法：
依赖库：pip install paddlepaddle
cd code

Index:
python IndexFiles_zhCN_sim.py -sim SIM_TYPE -o DIR
(-sim为similarity函数，-1为lucene默认，0 和 1 为2种不同的相似度函数，实现见CustomSimilarity.py; -o 为存储路径)
例：
python python IndexFiles_zhCN_sim.py -sim -1 -o index_sim_-1
python python IndexFiles_zhCN_sim.py -sim 0 -o index_sim_0
python python IndexFiles_zhCN_sim.py -sim 1 -o index_sim_1
(比较耗时，对应的index已附）

Search:
python SearchFiles_zhCN_sim.py -res NUM_OF_RESULTS -i DIR -sim SIM_TYPE
（-res为显示条目数；-i 为存储路径；-sim为similarity函数，同index）
例：
python SearchFiles_zhCN_sim.py -res 10 -i index_sim_-1 -sim -1
python SearchFiles_zhCN_sim.py -res 10 -i index_sim_0 -sim 0
python SearchFiles_zhCN_sim.py -res 10 -i index_sim_1 -sim 1

* 索引程序未包含html文件，如需测试请注意代码中相对路径位置和文件夹名