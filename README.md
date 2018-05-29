# ReIPDog
用 Python 写的一个查询旁站的脚本

## 命令行参数
```
optional arguments:
  -h, --help  show this help message and exit (显示帮助信息并退出)
  -host HOST  ip/url/host host you want to search (输入你想搜索的 ip/host/url )
  --noutput   output all info (是否在搜索过程中输出详细信息)
  --set       Merge the results (输入多个 ip/host/url 时, 是否将结果合并在一起)
```
### 参数说明
1. `-h, --help` 就不废话了
2. `-host HOST`. 如果没指定这个参数, 默认是使用脚本目录下的`HostsList`作为输入. 可以放置多个目标
3. `--noutput` 也不废话了
4. `--set` 如果设置了多个目标, 目的一般有两种:

```
1. 要一次性搜索多个目标的旁站(利用上面提到的HostsList进行输入)
2. 要搜索一个目标具有多个 ip, 这些 ip 属于同一个目标, 所以需要聚合在一起

不聚合的时候, 每个目标分开储存; 聚合的时候, 存到一起的时候储存的文件名为 运行时刻

动手试一下就知道了
```
### 使用举例
`python ReIPDog.py`: 搜索`HostsList`中的目标, 且不进行聚合.

`python ReIPDog.py`: 搜索`HostsList`中的目标, 且进行聚合.

`python ReIPDog.py -host baidu.com`: 搜索`baidu.com`的旁站, 且输出详细信息

`python ReIPDog.py -host baidu.com --noutput`: 搜索`baidu.com`的旁站, 不输出详细信息

贴个结果吧:


## 隐形车
README 中有车, 打卡上车啦
