# get-from-lofter
从lofter的“归档”批量下载文章

# 第一步：打开想要下载的lofter的归档页面
![第一步](/demo_img/1.png)
# 第二步：打开开发者工具（有的浏览器里叫做“审查元素”）
![第二步](/demo_img/2.png)
# 第三步：在右侧的Console里输入如下代码：
```sh
for(var a of document.getElementsByTagName('a')){
console.log(a.href)
}
```
# 第四步：把console输出的内容全选贴回目录下的“links.txt”
![第三步](/demo_img/3.png)
# 第五步：执行目录下的python程序
![第四步](/demo_img/4.png)

