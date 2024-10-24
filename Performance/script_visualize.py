import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn

times_df = pd.read_csv("script_time.csv")
print(times_df.describe())

residual_df = pd.DataFrame()
residual_df["residual_pytest"] = [
    element - times_df["pytest"].mean()
    for element in pd.Series(times_df["pytest"]).to_list()
]
residual_df["residual_mnist"] = [
    element - times_df["mnist"].mean()
    for element in pd.Series(times_df["mnist"]).to_list()
]
residual_df["residual_functional"] = [
    element - times_df["functional"].mean()
    for element in pd.Series(times_df["functional"]).to_list()
]


def show_plot(plot_object, names):
    fig, axs = plt.subplots(1, len(names), sharey=False, sharex=True)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    ax_counter = 0
    colors = seaborn.palettes.color_palette("CMRmap", n_colors=len(names))
    fig.set_tight_layout(True)
    fig.supxlabel("Iteration")
    fig.supylabel("Time Per Run (s)")
    fig.suptitle("Residual Iteration Values")
    for name in names:
        seaborn.lineplot(
            x=plot_object.index,
            y=name,
            data=plot_object,
            ax=axs[ax_counter],
            errorbar=None,
            color=colors[ax_counter],
        )
        seaborn.regplot(
            x=plot_object.index,
            y=name,
            data=plot_object,
            ax=axs[ax_counter],
            ci=None,
            truncate=False,
            scatter=False,
        )
        axs[ax_counter].set_xlabel("")
        axs[ax_counter].legend([name, "Trend Line"])
        axs[ax_counter].set_ylabel("")
        ax_counter += 1
    plt.savefig("runtime_all")


show_plot(times_df, ["pytest", "mnist", "functional"])


def stem_plot(plot_object, info):
    fig, axs = plt.subplots(1, len(info), sharey=False, sharex=True)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    ax_counter = 0
    colors = seaborn.palettes.color_palette("CMRmap", n_colors=len(info))
    fig.set_tight_layout(True)
    fig.supxlabel("Iteration")
    fig.supylabel("Residuals")
    fig.suptitle("Residual Iteration Values")
    for name, mean in info:
        axs[ax_counter].stem(plot_object[name])

        axs[ax_counter].axhline(
            y=0,
            color=colors[ax_counter],
        )
        axs[ax_counter].axhline(
            y=mean * -0.1,
            color="r",
        )
        axs[ax_counter].axhline(
            y=mean * 0.1,
            color="r",
        )
        axs[ax_counter].set_title(name, color=colors[ax_counter])
        axs[ax_counter].set_ylabel("")
        ax_counter += 1
    plt.savefig("stem_all")


stem_plot(
    residual_df,
    [
        ("residual_pytest", times_df["pytest"].mean()),
        ("residual_mnist", times_df["mnist"].mean()),
        ("residual_functional", times_df["functional"].mean()),
    ],
)


def scaled_plot(plot_object, names, ax=None):
    plot_norm = (plot_object) / (plot_object.max())
    fig, ax = plt.subplots(sharey=True, sharex=True)
    fig.set_figheight(6)
    fig.set_figwidth(10)
    ax_counter = 0
    colors = seaborn.palettes.color_palette("CMRmap", n_colors=len(names))
    fig.set_tight_layout(True)
    fig.supxlabel("Iteration")
    fig.supylabel("Scaled Values [0-1]")
    fig.suptitle("Relative Runtime Behavior")
    for name in names:
        seaborn.lineplot(
            x=plot_norm.index,
            y=name,
            data=plot_norm,
            ax=ax,
            errorbar=None,
            label=name,
            color=colors[ax_counter],
        )
        ax_counter += 1
    plt.grid(which="minor")
    plt.autoscale(True)
    plt.savefig("relativ_all")


scaled_plot(times_df, ["pytest", "mnist", "functional"])


plt.show()
