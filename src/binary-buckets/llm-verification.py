from lmdeploy import pipeline
import re
import time

captions = {
        "scene_000.mp4":'groom&pant',
        "scene_001.mp4":'yawn',
        "scene_002.mp4":'yawn',
        "scene_002.mp4":'yawn',
        "scene_002.mp4":'yawn',
        "scene_003.mp4":'wriggle',
        "scene_004.mp4":'wrestle with fingers',
        "scene_005.mp4":'tilt head',
        "scene_005.mp4":'wrestle bipedal',
        "scene_006.mp4":'"wrestle, handicap self"',
        "scene_007.mp4":'wraa',
        "scene_008.mp4":'wraa',
        "scene_009.mp4":'wraa',
        "scene_009.mp4":'wraa& scream',
        "scene_010.mp4":'wraa&scream',
        "scene_011.mp4":'wraa&scream',
        "scene_012.mp4":'wraa & scream',
        "scene_013.mp4":'wipe with detached obiect',
        "scene_014.mp4":'walk quadrupedal on palms',
        "scene_015.mp4":'wadge',
        "scene_016.mp4":'whisk fly with arm',
        "scene_017.mp4":'whimper-scream',
        "scene_018.mp4":'whimper',
        "scene_019.mp4":'copulate',
        "scene_020.mp4":'"wean, cover nipple"',
        "scene_021.mp4":'watch',
        "scene_022.mp4":'walk tripedal',
        "scene_023.mp4":'walk tripedal',
        "scene_025.mp4":'walk quadrupedal on backs of hands',
        "scene_025.mp4":'slide down boulder',
        "scene_025.mp4":'walk quadrupedal on palms',
        "scene_025.mp4":'slide down bouider',
        "scene_026.mp4":'walk quadrupedal on knuckles',
        "scene_027.mp4":'walk quadrupedal on backs of hands',
        "scene_027.mp4":'slide down boulder',
        "scene_027.mp4":'walk quadrupedal on palms',
        "scene_027.mp4":'slide down bouider',
        "scene_028.mp4":'walk in sloth position',
        "scene_033.mp4":'walk bipedal',
        "scene_034.mp4":'walk bipedal',
        "scene_035.mp4":'walkbipedal',
        "scene_036.mp4":'walk bipedal',
        "scene_041.mp4":'fish for carpenter ant',
        "scene_042.mp4":'wait for companion',
        "scene_043.mp4":'Wadge without adding leaf',
        "scene_044.mp4":'wadge by addingleaf',
        "scene_045.mp4":'wadge',
        "scene_046.mp4":'use tool & fish for carpenter ant',
        "scene_047.mp4":'scoop algae & eat algae',
        # why are there like million captions for this
        "scene_048.mp4":'leaf-sponge',
# "scene_048.mp4":'push object into',
# "scene_048.mp4":'leaf-sponge',
# "scene_048.mp4":'drink from hole in tree',
# "scene_048.mp4":'leaf-sponge',
# "scene_048.mp4":'push object into',
# "scene_048.mp4":'push obiect into',
# "scene_048.mp4":'leaf-sponge',
# "scene_048.mp4":'drink from hole in tree',
"scene_049.mp4":'usetool & toolset (GoualougoTriangle',
"scene_051.mp4":'travel',
"scene_052.mp4":'travel',
"scene_053.mp4":'Travel',
"scene_053.mp4":'travel',
"scene_054.mp4":'wade',
"scene_055.mp4":'waa bark',
"scene_056.mp4":'vomit',
"scene_057.mp4":'vacate',
"scene_058.mp4":'hammer nut with stone & use tool',
"scene_059.mp4":'"urinate,sitting"',
"scene_060.mp4":'urinate quadrupedal',
"scene_061.mp4":'urinate quadrupedal',
"scene_062.mp4":'"urinate,prone"',
"scene_063.mp4":'urinate & play with urine',
"scene_064.mp4":'twist(red colobus)',
"scene_065.mp4":'twist(red colobus)',
"scene_065.mp4":'twist(red colobus)',
"scene_066.mp4":'turn up lip',
"scene_067.mp4":'turn face away',
"scene_069.mp4":'approach',
"scene_069.mp4":'turn around',
"scene_070.mp4":'tumble',
"scene_073.mp4":'trifle with',
"scene_074.mp4":'travel and play',
"scene_075.mp4":'travel and play',
"scene_076.mp4":'travel and.play',
"scene_077.mp4":'travel and play',
"scene_078.mp4":'travel',
"scene_079.mp4":'transport in mouth',
"scene_079.mp4":'transport in mouth',
"scene_080.mp4":'transportin mouth',
"scene_081.mp4":'transportin mouth',
"scene_082.mp4":'transport with hand support',
"scene_083.mp4":'transport two offspring',
"scene_085.mp4":'transport on shoulder',
"scene_087.mp4":'transport on head or nape',
"scene_088.mp4":'transport on back',
"scene_089.mp4":'transporton back',
"scene_090.mp4":'transportonback',
"scene_091.mp4":'transporton back',
"scene_092.mp4":'transporton back',
"scene_093.mp4":'transport in neck pocket',
"scene_094.mp4":'transport in mouth',
"scene_095.mp4":'transport food & transport in hand',
"scene_096.mp4":'transport in groin pocket',
"scene_096.mp4":'drop',
"scene_097.mp4":'transport in foot',
"scene_098.mp4":'transport food',
"scene_099.mp4":'transport corpse of infant',
"scene_100.mp4":'transport bipedal',
"scene_101.mp4":'transport',
"scene_102.mp4":'transfer',
"scene_103.mp4":'trample',
"scene_103.mp4":'stamp other',
"scene_104.mp4":'toy',
"scene_105.mp4":'use tool &tool set (GoualougoTriangle',
"scene_106.mp4":'heave to protest & throw temper tantrum',
"scene_106.mp4":'leave to protest & throwtemper tantrurn',
"scene_107.mp4":'leave to protest & throw temper tantrum',
"scene_107.mp4":'throw splash',
"scene_108.mp4":'touch with foot',
"scene_109.mp4":'touch scrotum',
"scene_110.mp4":'touch fruit & inspect fruit',
"scene_111.mp4":'touch fruit & inspect fruit',
"scene_112.mp4":'touch fruit & inspect fruit',
"scene_113.mp4":'touch fruit & inspect fruit',
"scene_114.mp4":'scratch self',
"scene_114.mp4":'pant-grunt with bent elbow',
"scene_114.mp4":'"extend hand, palmupward"',
"scene_114.mp4":'scratch self',
"scene_116.mp4":'tilt head',
"scene_116.mp4":'wrestle bipedal',
"scene_117.mp4":'tickle',
"scene_118.mp4":'grin-full-open',
"scene_118.mp4":'thrust misdirected',
"scene_118.mp4":'grin-fuli-open',
"scene_119.mp4":'thrust in vacuum',
"scene_120.mp4":'thrust bipedal',
"scene_121.mp4":'thrust',
"scene_123.mp4":'throw temper tantrum',
"scene_127.mp4":'throw stone or rock',
"scene_128.mp4":'throw splash',
"scene_129.mp4":'throw sand',
"scene_130.mp4":'throw dry leaves',
"scene_131.mp4":'bristle',
"scene_131.mp4":'bristle & throw branch',
"scene_131.mp4":'bristle',
"scene_132.mp4":'bristle',
"scene_133.mp4":'bristle',
"scene_134.mp4":'fish for carpenter ant',
"scene_134.mp4":'fish for carpenter ant & take tool',
"scene_134.mp4":'fish for carpenter ant',
"scene_135.mp4":'sway woody vegetation & rake',
"scene_136.mp4":'sway woody vegetation & rake',
"scene_137.mp4":'throw at inanimate object',
"scene_140.mp4":'throw at animate obiect',
"scene_141.mp4":'throw at animate obiect',
"scene_142.mp4":'throw & kill another species',
"scene_143.mp4":'threaten',
"scene_143.mp4":'kiss with open mouth',
"scene_144.mp4":'tease',
        }
all_captions = list(set(captions.values()))


def generate_mcq(filename):
    correct_caption = captions[video_name]

    distractors = random.sample(
        [c for c in all_captions if c != correct_caption],
        k=min(num_choices - 1, len(all_captions) - 1)
    )

    options = distractors + [correct_caption]
    random.shuffle(options)

    # find correct answer index
    correct_idx = options.index(correct_caption) + 1

    # format question string
    question = "\n".join([f"{i+1}. {opt}" for i, opt in enumerate(options)])

    return question, correct_idx


def parse_log(log_path: str):
    # Read the entire file
    with open(log_path, "r") as f:
        content = f.read()

    # Split into blocks separated by dashed lines
    blocks = re.split(r"-{10,}", content)
    dic = {}

    for block in blocks:
        # Extract video path
        match_path = re.search(r"Output for (.*?):", block)
        # Extract text
        match_text = re.search(r"text=(.*)", block)
        if match_path and match_text:
            video_path = match_path.group(1).strip()
            text = match_text.group(1).strip()
            dic[video_path] = text

    return dic



top_lv_path = '/home/park1361/aif/videos/clipped_book_videos/'

log_dic = parse_log('/home/park1361/chimp-log-full-desc-20251028-125436.txt')

MODEL_PATH = "/scratch/gilbreth/park1361/models/internlm"
pipe = pipeline(MODEL_PATH, log_level = 'INFO')

with open(f'verification-log-{time.strftime("%Y%m%d-%H%M%S")}.txt', "a") as f:
    for filename, og_cap in captions.items():
        # Make it the full path
        filename = top_lv_path + filename

        llm_res = log_dic[filename]

        # prompt = f"""
        # Given the correct label, evaluate how well the description captured the essence of the label in scale of 1 - 10.

        # - Label: {og_cap}
        # - Description: {llm_res}
        # """
        #prompt = f"""
        #Given the correct label, evaluate how well the description captured the essence of the label in Yes or No.

        #- Label: {og_cap}
        #- Description: {llm_res}
        #"""
        prompt = f"""Classify the animal behavior given by the caption by choosing one option for each category.

- Caption: {og_cap}

Categories:
    - Individual OR group
    - Aggressive OR Not aggressive
    - High energy OR low energy
    - Object OR no object
    - Adult OR Child
    - Feeding OR not feeding

Answer should only list the correct choice in bullet points.
        """


        out = pipe(prompt)

        f.write(f"""
------------------------
Output for {filename}:
{out}
------------------------

        """)

