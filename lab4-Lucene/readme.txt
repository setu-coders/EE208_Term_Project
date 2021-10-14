测试方法
0.安装docker环境中缺少的库
pip install paddlepaddle
cd code_u


1.索引
python IndexFiles_zhCN.py
*由于html文件过多，上传的只选了很小一部分供验证功能,运行也会保存在/index_zhCN_small中
搜索时检索的索引文件是由完整的的7000多个html文件索引得到的，存储在/index_zhCN中

2.搜索
python SearchFiles_zhCN.py
输入查询词（支持布尔查询）即可得到搜索结果(文件名，存储地址（相对），URL，标题）