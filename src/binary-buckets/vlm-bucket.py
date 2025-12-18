import numpy as np
from lmdeploy import pipeline, GenerationConfig
from decord import VideoReader, cpu
from lmdeploy.vl.constants import IMAGE_TOKEN
from lmdeploy.vl.utils import encode_image_base64
from PIL import Image
import time
#pipe = pipeline('OpenGVLab/InternVL2-8B', log_level='INFO')
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

        question +="""Classify the animal behavior in this video by choosing one option for each category.

Categories:
    - Individual OR group
    - Aggressive OR Not aggressive
    - High energy OR low energy
    - Object OR no object
    - Adult OR Child
    - Feeding OR not feeding

Answer should only list the correct choice in bullet points.
       """
        # question += """ Describe the animal behavior in this video into one or more of the following buckets:

# * social_affiliative – bonding and cooperative behaviors (grooming, kissing, waiting for companion, friendly contact).
# * aggressive_dominance – threats, bristling, displays, attacks, throwing objects in aggression, dominance assertion.
# * submission_appeasement – appeasement gestures, submissive postures, pant-grunts, turning face away.
# * mating_reproductive – courtship, copulation, thrusting, covering nipple, sexual postures.
# * feeding_foraging – searching for, processing, or consuming food (wadging, fishing for ants, touching fruit, eating algae).
# * tool_use_object_manipulation – using or modifying objects/tools for functional or investigative purposes (hammering nuts, leaf-sponging, pushing objects, using sticks).
# * locomotion_travel – all forms of movement or travel (walking, running, sliding, wading, climbing).
# * resting_idle – stationary, low-energy states (sitting, lying, yawning, resting, idle watching).
# * vocal_communication – intentional or expressive vocal signals (wraa, waa bark, whimper, scream).
# * maternal_care – caregiving behaviors (carrying, nursing, covering nipple, transporting infant or corpse).
# * play – non-functional, social or object-based play (wrestling, tumbling, tickling, toying, sliding for fun).
        # """

        content = [{'type': 'text', 'text': question}]
        for img in imgs:
            content.append({'type': 'image_url', 'image_url': {'max_dynamic_patch': 1, 'url': f'data:image/jpeg;base64,{encode_image_base64(img)}'}})

        messages = [dict(role='user', content=content)]
        out = pipe(messages, gen_config=GenerationConfig(top_k=1))

        f.write(f"""

------------------------
Output for {video_path}:
{out}
------------------------

        """)

