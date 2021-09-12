from pytube import YouTube

# pprint-pretty print 不必要，仅仅为了让输出更好看，每个视频文件占一行
from pprint import pprint

yt = YouTube("https://www.youtube.com/watch?v=Ul_aLx_sH1c")

# 显示所有可以下载的视频文件
pprint(yt.get_videos())

# 显示视频文件名
print(yt.filename)

# # 设置视频文件名
# yt.set_filename('myFirstVideo')

# # 根据文件类型过滤视频文件
# pprint(yt.filter('flv'))

# # 由于排序是按清晰度从低到高，所以可以用 -1 索引到最高清版本
# print(yt.filter('.mp4')[-1])

# # 根据清晰度过滤文件
# pprint(yt.filter(resolution='480p'))

# # 通过文件类型和清晰度指定下载的视频
# video = yt.get('mp4','720p')

# # 如果有多个相同类型，或者相同清晰度的文件，则不能仅指定一种格式来下载视频，例如下面一行可能会报错：
# video = yt.get('mp4')

# # 其实，上面的 video 完全可以用过滤+索引的方式获得，不一定非得用 get 方法
# video = yt.filter('.mp4')[-1]

# # 下载到指定路径
# video.download('/home/Desktop')