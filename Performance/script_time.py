import os
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
import tqdm

ITERATIONS = 25


def time_system(system_call):
    time_list = [0] * ITERATIONS
    offset = -5
    for i in tqdm.tqdm(range((-offset) + ITERATIONS)):
        start_time = time.time()
        os.system(system_call)
        end_time = time.time()
        time_list[max(offset, 0)] = end_time - start_time
        offset += 1
    return time_list


pytest_time = time_system(
    "pytest integration_tests/basic_full_flow.py --no-header --quiet -rN"
)
mnist_time = time_system("python3 examples/demo_mnist_convnet.py")
functional_time = time_system("python3 examples/demo_functional.py")

times_df = pd.DataFrame(
    {
        "pytest": pytest_time,
        "mnist": mnist_time,
        "functional": functional_time,
    }
)

times_df.to_csv("script_time.csv")