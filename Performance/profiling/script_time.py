import os, time, tqdm, seaborn, matplotlib.pyplot as plt, numpy as np, pandas as pd

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

pytest_time = time_system("pytest integration_tests/basic_full_flow.py --no-header --quiet -rN")
mnist_time = time_system("python3 examples/demo_mnist_convnet.py")
functional_time = time_system("python3 examples/demo_functional.py")

def print_stats(time_list, name):
    print(f"---{name}---")
    print(f"mean = {sum(time_list)/len(time_list)}")
    print(f"min = {min(time_list)}")
    print(f"max = {max(time_list)}")
    print(f"std = {np.std(time_list)}")

print_stats(pytest_time, "pytest")
print_stats(mnist_time, "mnist")
print_stats(functional_time, "functional")

def show_plot(time_list):
    times_df = pd.DataFrame({"TimePerRun": time_list, "x": range(ITERATIONS)})
    fig, ax = plt.subplots()
    seaborn.lineplot(x="x", y="TimePerRun", data=times_df, ax=ax, errorbar=None)
    seaborn.regplot(x="x", y="TimePerRun", data=times_df, ax=ax, ci=None,)
    ax.legend(["line", "Scatter Points", "Trend Line"], loc="best")
    ax.set_title("Run Time Behavior")
    ax.set_ylabel("TimePerRun (Sec)")
    ax.set_xlabel("Iteration")

show_plot(pytest_time)
show_plot(mnist_time)
show_plot(functional_time)

def scale_0_1(time_list):
    max_value = max(time_list)
    return [element / max_value for element in time_list]

scaled_pytest = scale_0_1(pytest_time)
scaled_mnist = scale_0_1(mnist_time)
scaled_functional = scale_0_1(functional_time)

times_df = pd.DataFrame({"pytest": scaled_pytest, "mnist": scaled_mnist, "functional": scaled_functional, "x": range(ITERATIONS)})

fig, ax = plt.subplots()
seaborn.lineplot(x="x", y="pytest", data=times_df, ax=ax, errorbar=None, label="basic_full_flow")
seaborn.lineplot(x="x", y="mnist", data=times_df, ax=ax, errorbar=None, label="mnist_covnvnet") 
seaborn.lineplot(x="x", y="functional", data=times_df, ax=ax, errorbar=None, label="functional")
ax.set_title("Relative Run time Behavior")
ax.set_ylabel("Scaled Time [0-1]")
ax.set_xlabel("Iteration")

plt.show()