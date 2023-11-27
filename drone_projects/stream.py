import ffmpeg

# 创建一个ffmpeg实例
ffmpeg_instance = ffmpeg.input('input_file')

# 设置输入文件
input_file = ffmpeg.input('input_file')

# 设置输出文件
output_file = ffmpeg.output(input_file, 'output_file')

# 设置推流参数
stream = ffmpeg.output(input_file, 'output_file', f='flv', r=25)

# 开始推流
ffmpeg.run(stream)

# 停止推流
ffmpeg.stop()
