from lmdeploy import pipeline
import re
import time
from things import captions, parse_csv


MODEL_PATH = "/scratch/gilbreth/park1361/models/internlm"
pipe = pipeline(MODEL_PATH, log_level = 'INFO')

llm_out_dict = parse_csv("/home/park1361/aif/rohan-buckets.csv")
#llm_out_dict = parse_csv("/home/park1361/aif/rohan-full-descriptive-prompting.csv")

with open(f'verification-log-{time.strftime("%Y%m%d-%H%M%S")}.txt', "a") as f:
    f.write("Full Description\n")

    for filename, og_cap in captions.items():
        if filename not in llm_out_dict:
            continue

        llm_res = llm_out_dict[filename]

        # prompt = f"""
        # Given the correct label, evaluate how well the description captured the essence of the label in scale of 1 - 10.

        # - Label: {og_cap}
        # - Description: {llm_res}
        # """
        prompt = f"""
        Given the correct label, evaluate how well the description captured the essence of the label in Yes or No.

        - Correct Label: {og_cap}
        - Description: {llm_res}
        """

        out = pipe(prompt)

        f.write(f"""
------------------------
Output for {filename}:
{out}
------------------------

        """)

