Cloned from https://github.com/MadCreeper/crawler_course.git

Currently working on term project. 
# Updating in /TermProject.

Previously done labs included for reference.



# git 简单教程
提交新代码流程：
1. git pull 保证本地仓库与远程同步。 可能会显示冲突，这时候需要进到vscode里把冲突的代码修改。一般本地服从远程修改，特殊情况请沟通好
2. 添加、修改、删除、重命名代码
3. git add xxx.py   或者  git add /somefolder/something/ 添加代码或者文件夹。
**慎用**git add -A， 使用前请**务必保证**.gitignore里排除了你不想提交的文件。 不要提交一大堆html文件、巨大的二进制文件、巨大的zip等等。github最大支持100MB，而且文件大了以后上传下载非常缓慢。
4. git commit -m "blahblahblah" ，引号里简单描述你这次提交改了什么
5. ** git pull** 防止你写代码的这段时间远程被其他人改了造成不同步。 同1，如果提示冲突解决之
6. git push 出现...done代表大功告成！

## 总结: pull -> 写代码 -> （如果创建了新文件）add -> commit -> push 