# Guide on Purdue RACA Gilbreth Server Usage

- Gilbreth: https://gateway.gilbreth.rcac.purdue.edu/pun/sys/dashboard/batch_connect/sessions
  - Jupyter, A30 cluster, csml account, normal QoS, 48 wall time, 5 cores, 1 GPU
- Python environment: https://www.rcac.purdue.edu/knowledge/gilbreth/run/examples/apps/python/conda
    ```sh
    module load rcac
    module load conda
    conda create --prefix=$RCAC_SCRATCH/MyEnvName python=3.13 numpy -y
    conda env list
    conda install --prefix=$RCAC_SCRATCH/MyEnvName matplotlib -y
    source activate $RCAC_SCRATCH/MyEnvName
    ```
  - Also see : https://www.rcac.purdue.edu/knowledge/gilbreth/run/examples/apps/python/packages

- Job file:
    ```sh
    #!/bin/bash
    # FILENAME:  myjob.sub

    #SBATCH -A csml
    #SBATCH -p a30
    #SBATCH --nodes=1 --gpus-per-node=1 --mem=60G
    #SBATCH --time=1:30:00
    #SBATCH --job-name ahhhh

    module load conda
    source activate $RCAC_SCRATCH/MyEnvName

    python hello.py
    ```
  - For flags: https://www.rcac.purdue.edu/knowledge/gilbreth/run/slurm/queues
  - Test the environment creation & job with the following Python script
    ```py
    import string, sys
    import numpy as np
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    x = np.linspace(-np.pi, np.pi, 201)
    plt.plot(x, np.sin(x))
    plt.xlabel('Angle [rad]')
    plt.ylabel('sin(x)')
    plt.axis('tight')
    plt.savefig('sine.png')

    print('Sine image created!')
    ```
  - Call `sbatch myjob.sub`

- Quota: https://www.rcac.purdue.edu/knowledge/gilbreth/storage/quota
    ```sh
    myquota
    du -h --max-depth=1 $HOME >myfile
    du -h --max-depth=1 $RCAC_SCRATCH >myfile
    ```


