import numpy as np
from lmdeploy import pipeline, GenerationConfig
from decord import VideoReader, cpu
from lmdeploy.vl.constants import IMAGE_TOKEN
from lmdeploy.vl.utils import encode_image_base64
from PIL import Image
import time
from things import generate_mcq

pipe = pipeline('/scratch/gilbreth/park1361/models/internvl/')


def get_index(bound, fps, max_frame, first_idx=0, num_segments=32):
    if bound:
        start, end = bound[0], bound[1]
    else:
        start, end = -100000, 100000
    start_idx = max(first_idx, round(start * fps))
    end_idx = min(round(end * fps), max_frame)
    seg_size = float(end_idx - start_idx) / num_segments
    frame_indices = np.array([
        int(start_idx + (seg_size / 2) + np.round(seg_size * idx))
        for idx in range(num_segments)
        ])
    return frame_indices


def load_video(video_path, bound=None, num_segments=32):
    vr = VideoReader(video_path, ctx=cpu(0), num_threads=1)
    max_frame = len(vr) - 1
    fps = float(vr.get_avg_fps())
    pixel_values_list, num_patches_list = [], []
    frame_indices = get_index(bound, fps, max_frame, first_idx=0, num_segments=num_segments)
    imgs = []
    for frame_index in frame_indices:
        img = Image.fromarray(vr[frame_index].asnumpy()).convert('RGB')
        imgs.append(img)
    return imgs


# Generate array of video paths
top_lv_path = '/home/park1361/aif/videos/clipped_book_videos/scene_'
video_paths = []
for i in range(144 + 1):
#for i in range(2):
    video_paths.append(f"{top_lv_path}{i:03d}.mp4")

with open(f'chimp-log-{time.strftime("%Y%m%d-%H%M%S")}.txt', "a") as f:
    # process
    for video_path in video_paths:
        imgs = load_video(video_path, num_segments=8)

        question = ''
        for i in range(len(imgs)):
            question = question + f'Frame{i+1}: {IMAGE_TOKEN}\n'

        mcq, ans = generate_mcq(video_path, 5)
        if not mcq or not ans:
            continue

        question += f"""Choose the number corresponding to the label that best represents the animal behavior in this video (simply report the number):

{mcq}
        """

        content = [{'type': 'text', 'text': question}]
        for img in imgs:
            content.append({'type': 'image_url', 'image_url': {'max_dynamic_patch': 1, 'url': f'data:image/jpeg;base64,{encode_image_base64(img)}'}})

        messages = [dict(role='user', content=content)]
        out = pipe(messages, gen_config=GenerationConfig(top_k=1))

        f.write(f"""

------------------------
Output for {video_path}:
- Choices:
{mcq}
- Correct: {ans}

{out}
------------------------

        """)

