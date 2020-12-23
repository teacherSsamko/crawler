import os
import subprocess
import datetime

import ffmpeg

today = datetime.date.today()
video_dir_path = f'crawler/hmall/videos/src/{today}'
dir_list = [x for x in os.listdir(video_dir_path) if '.' not in x]

for directory in dir_list:
    prod_id = directory
    files = os.listdir(f'{video_dir_path}/{directory}')
    print(files)
    for f in files:
        if 'chunklist' in f:
            chunk = f
    print(chunk)
    target_path = os.path.join(f'{video_dir_path}/{directory}', f'{prod_id}.mp4')
    print(target_path)
    # in_file = ffmpeg.input(f'crawler/hmall/videos/{prod_id}/{chunk}')
    # (
    #     ffmpeg
    #     .input(in_file)
        
    #     # .output(f'crawler/hmall/videos/{prod_id}/{prod_id}.mp4', c='copy', bsf='a acc_adtstoasc')
    #     .output(target_path, c='copy', bsf='a aac_adtstoasc')
    #     .run()
    # )
    # ffmpeg -i {m3u8} -bsf:a aac_adtstoasc -c copy {target_path}

    # result = subprocess.Popen(['ffmpeg', '-i', f'crawler/hmall/videos/{prod_id}/{chunk}', '-bsf:a', 'acc_adtstoasc', '-c', 'copy', f'crawler/hmall/videos/{prod_id}/{prod_id}.mp4'])
    cmd = f'ffmpeg -i {video_dir_path}/{prod_id}/{chunk} -bsf:a aac_adtstoasc -c copy crawler/hmall/videos/{today}/{prod_id}.mp4'
    result = os.system(cmd)
    print(result)
        

