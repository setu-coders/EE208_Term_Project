测试方法：
依赖库：pip install paddlepaddle
cd code

python server.py
访问http://localhost/（转发的）端口号/
输入搜索词(支持布尔和site:功能）和显示数目（默认50）
稍等片刻即显示结果

*注意：由于显示摘要功能依赖于读取html文件，所以上传的不带html文件的测试代码是没法显示摘要的，只能显示标题和超链接。
需要显示摘要需把html文件夹放在code上移两层的地方
（即
workspace
- /html
- /lab7
	- /code
		- server.py

html文件：
https://jbox.sjtu.edu.cn/l/T1XHXF