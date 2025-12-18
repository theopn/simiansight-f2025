# LMDeploy Guide

## Resources

- https://deepwiki.com/InternLM/lmdeploy/1.3-installation-and-setup
- https://lmdeploy.readthedocs.io/en/latest/api/pipeline.html
- https://github.com/InternLM/lmdeploy/blob/main/docs/en/get_started/get_started.md
- https://huggingface.co/docs/huggingface_hub/en/guides/cli

## Installation

```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
. "$HOME/.cargo/env"
pip install lmdeploy
pip install -U "huggingface_hub[cli]"
hf download OpenGVLab/InternVL2_5-8B --local-dir $RCAC_SCRATCH/models/internvl
pip install timm
```

## Verification

```py
import lmdeploy

print(lmdeploy.__version__)

# Check TurboMind availability
try:
    from lmdeploy.turbomind import TurboMind
    print("TurboMind backend available")
except ImportError:
    print("TurboMind backend not available")

# Check PyTorch backend
try:
    from lmdeploy.pytorch import Engine
    print("PyTorch backend available")
except ImportError:
    print("PyTorch backend not available")
```

Testing VLMs: https://lmdeploy.readthedocs.io/en/latest/multi_modal/vl_pipeline.html
```py
from lmdeploy import pipeline
from lmdeploy.vl import load_image

pipe = pipeline('/scratch/gilbreth/park1361/models/internvl')

#image = "./images/out1.png"
#response = pipe(('describe this image', image))

image_names = [ "out1.png", "out2.png", "out3.png", "out4.png", "out5.png", "out6.png", "out7.png" ]
images = [load_image("./images/" + name) for name in image_names]
response = pipe(('describe these images', images))

print(response)
```


## For Setting Up Gilbreth with Required Models and Python Modules

1. Execute the following:
    ```sh
    module load rcac conda
    conda create --prefix=$RCAC_SCRATCH/llm-script python=3.13 numpy matplotlib -y
    conda activate $RCAC_SCRATCH/llm-script

    . "$HOME/.cargo/env"
    pip install lmdeploy
    pip install -U "huggingface_hub[cli]"
    pip install timm
    hf download internlm/internlm3-8b-instruct --local-dir $RCAC_SCRATCH/models/internlm
    ```
2. testllm.py:
    ```py
    import lmdeploy

    MODEL_PATH = "/scratch/gilbreth/park1361/models/internlm"

    with lmdeploy.pipeline(MODEL_PATH) as pipe:
    response = pipe(["Hi, pls intro yourself", "Shanghai is"])
    print(response)
    ```
3. myjob.sub:
    ```sh
    #!/bin/bash
    # FILENAME:  myjob.sub

    #SBATCH -A csml
    #SBATCH -p a30
    #SBATCH --nodes=1 --gpus-per-node=1 --mem=60G
    #SBATCH --time=1:30:00
    #SBATCH --job-name ahhhh

    module load conda
    source activate $RCAC_SCRATCH/llm-script

    python testllm.py

    # followed by sbatch myjob.sub
    # maintain the status at:
    # https://gateway.gilbreth.rcac.purdue.edu/pun/sys/dashboard/activejobs
    ```

