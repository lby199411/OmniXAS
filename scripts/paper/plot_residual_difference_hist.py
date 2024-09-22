# %%

from scipy.stats import gaussian_kde
from src.data.ml_data import DataQuery, load_xas_ml_data
from src.models.trained_models import Trained_FCModel
import numpy as np
import matplotlib.pyplot as plt
from config.defaults import cfg

# %%


fig = plt.figure(figsize=(9, 12))
plt.style.use(["default", "science"])
gs = fig.add_gridspec(5, 2, hspace=0.05, wspace=0.02)
axs = gs.subplots(sharex=True, sharey=True)
i = 0
iterator = list(zip(cfg.compounds, ["FEFF"] * len(cfg.compounds)))
iterator.append(("Ti", "VASP"))
iterator.append(("Cu", "VASP"))
FONTSIZE = 22
win_rate_dict = {}
for ax, (compound, simulation_type) in zip(axs.flatten(), iterator):
    model_expert = Trained_FCModel(
        # DataQuery(compound=compound, simulation_type="FEFF"),
        DataQuery(compound=compound, simulation_type=simulation_type),
        name="per_compound_tl",
    )
    residues_expert = model_expert.predictions - model_expert.data.test.y
    model_tuned = Trained_FCModel(
        # DataQuery(compound=compound, simulation_type="FEFF"),
        DataQuery(compound=compound, simulation_type=simulation_type),
        name="ft_tl",
    )
    residues_tuned = model_tuned.predictions - model_tuned.data.test.y
    residues_expert, residues_tuned = np.abs(residues_expert), np.abs(residues_tuned)

    data = residues_expert - residues_tuned
    data = data.flatten()
    good = data[data > 0]
    bad = data[data < 0]
    good = np.log10(good)
    bad = np.log10(-bad)

    bins = 40

    bins = np.linspace(-5, 0, bins)

    scale_factor = 1

    bars = np.histogram(good, bins=bins)[0]
    count = model_expert.data.test.y.size
    # count = 1

    bars = (bars / count) * 100

    ax.bar(
        bins[:-1],
        bars,
        width=np.diff(bins),
        color=plt.get_cmap("tab10")(i),
        # label=r"$\varepsilon^{\text{tuned}}_{i,j} < \varepsilon^{\text{expert}}_{i,j}$",
        label=r"$\Delta > 0$",
        edgecolor="black",
        linewidth=0.5,
    )

    bars = np.histogram(bad, bins=bins)[0]
    bars = (bars / count) * 100
    ax.bar(
        bins[:-1],
        bars,
        width=np.diff(bins),
        alpha=0.7,
        # label=r"$\varepsilon^{\text{tuned}}_{i,j} > \varepsilon^{\text{expert}}_{i,j}$",
        label=r"$\Delta < 0$",
        edgecolor="black",
        linewidth=0.5,
        color="white",
    )

    ax.set_xticks(np.arange(-4, 0, 1))
    ax.set_xticklabels(
        ax.get_xticks(),
        fontsize=FONTSIZE * 0.8,
    )

    ax.set_yticks([])

    ax.set_yticks(np.arange(1, 7, 2))
    ax.set_yticklabels(
        [f"{y:.0f}%" for y in ax.get_yticks()],
        fontsize=FONTSIZE * 0.8,
    )

    ax.text(
        0.95,
        0.9,
        compound,
        horizontalalignment="right",
        verticalalignment="top",
        transform=ax.transAxes,
        fontsize=FONTSIZE,
        # color=plt.get_cmap("tab10")(i),
        fontweight="bold",
        bbox=dict(
            facecolor=plt.get_cmap("tab10")(i),
            alpha=0.5,
            edgecolor=plt.get_cmap("tab10")(i),
        ),
    )

    if simulation_type == "VASP":
        ax.text(
            0.97,
            0.65,
            "VASP",
            horizontalalignment="right",
            verticalalignment="top",
            transform=ax.transAxes,
            fontsize=FONTSIZE * 0.6,
            # color=plt.get_cmap("tab10")(i),
            # fontweight="bold",
        )

    # no ticks top top and make ticks come outside
    ax.tick_params(axis="x", which="both", top=False, direction="out")
    ax.tick_params(axis="y", which="both", right=False, direction="in")

    # # a text that show the wincount of the tuned model
    # win_rate = np.sum(model_expert.mse_per_spectra > model_tuned.mse_per_spectra)
    # win_rate = win_rate / len(model_expert.mse_per_spectra) * 100
    # win_rate = np.round(win_rate, 2)
    # win_rate_dict[f"{compound}_{simulation_type}"] = win_rate
    # # top left win rate
    # ax.text(
    #     0.05,
    #     0.9,
    #     r"$\text{Win}: " + f"{win_rate:.2f}\%$",
    #     horizontalalignment="left",
    #     verticalalignment="top",
    #     transform=ax.transAxes,
    #     fontsize=FONTSIZE * 0.8,
    #     color=plt.get_cmap("tab10")(i),
    #     fontweight="bold",
    #     bbox=dict(
    #         facecolor="white",
    #         alpha=0.5,
    #         edgecolor=plt.get_cmap("tab10")(i),
    #     ),
    # )

    ax.minorticks_off()

    # ax.set_xlim(-5, 0)
    i += 1

# # add legend at bottom left axes
# axs[0, 0].legend(
#     fontsize=FONTSIZE * 0.8,
#     # loc="upper left",
#     bbox_to_anchor=(0.05, 0.9),
#     # bbox_transform=fig.transFigure,
# )


# add legend above all axes
handles, labels = axs[0, 0].get_legend_handles_labels()
from matplotlib.patches import Patch

handles = [
    Patch(
        facecolor="black",
        edgecolor="black",
        # label=r"$\varepsilon^{\text{tuned}}_{i,j} < \varepsilon^{\text{expert}}_{i,j}$",
        label=r"$\Delta>0$",
    ),
    Patch(
        facecolor="lightgray",
        edgecolor="black",
        alpha=0.7,
        # label=r"$\varepsilon^{\text{tuned}}_{i,j} > \varepsilon^{\text{expert}}_{i,j}$",
        label=r"$\Delta<0$",
    ),
]
fig.legend(
    handles=handles,
    labels=labels,
    loc="upper center",
    fontsize=FONTSIZE,
    ncol=2,
    bbox_to_anchor=(0.5, 0.95),
    bbox_transform=fig.transFigure,
)

# add log10
# xlabel = r"$\log_{10}(|\varepsilon^{\text{tuned}}_{i,j} - \varepsilon^{\text{expert}}_{i,j}|)$"
xlabel = r"$\log_{10}( |\Delta| )$"
axs[-1, 0].set_xlabel(xlabel, fontsize=FONTSIZE)
axs[-1, 1].set_xlabel(xlabel, fontsize=FONTSIZE)


fig.text(
    0.06,
    0.5,
    r"Number of Spectra Points (\%)",
    va="center",
    rotation="vertical",
    fontsize=FONTSIZE,
)

fig.tight_layout()
plt.savefig("residual_difference_histograms.pdf", bbox_inches="tight", dpi=300)


# %%
