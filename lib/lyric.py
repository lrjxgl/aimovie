import re
 
def lyricTimeList(lyric):
    lyric =  re.sub(r'\[(\d+)\]', lambda x:   x.group(1) + '.', lyric)
    lyric=re.sub(r'\n\s*\n', '\n', lyric).strip()
    data=lyric.split('\n')
    processed_data = []

    # 遍历每一行数据
    for i in range(len(data) - 1):
        line = data[i]
        next_line = data[i + 1]
        
        # 提取 start 和 content
        start = int(line.split('.')[0])
        content = line.split('.')[1]
        
        # 使用下一行的开始作为当前行的结束
        end = int(next_line.split('.')[0])
        
        processed_data.append({"start": start, "end": end, "content": content})

    # 处理最后一行
    last_line = data[-1]
    last_start = int(last_line.split('.')[0])
    last_content = last_line.split('.')[1]
    last_end = last_start + 20

    processed_data.append({"start": last_start, "end": last_end, "content": last_content})
    return processed_data
 