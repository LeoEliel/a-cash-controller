import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

plt.rcParams["font.family"] = "DejaVu Sans"

fig, ax = plt.subplots(figsize=(13, 9), dpi=120)
ax.set_xlim(0, 13)
ax.set_ylim(0, 9)
ax.axis("off")
fig.patch.set_facecolor("#0F1B2D")
ax.set_facecolor("#0F1B2D")

HEADER = "#1D9E75"
HEADER2 = "#2E6FB7"
HEADER3 = "#C25E3A"
BODY = "#16263D"
TEXT = "#E8EEF6"
PK = "#D4A853"
LINE = "#5A7796"


def entity(ax, x, y, w, title, fields, header_color):
    rh = 0.44
    bh = rh * len(fields)
    total_h = 0.6 + bh
    ax.add_patch(
        FancyBboxPatch(
            (x, y - total_h),
            w,
            total_h,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            fc=BODY,
            ec=header_color,
            lw=2,
            zorder=2,
        )
    )
    ax.add_patch(
        FancyBboxPatch(
            (x, y - 0.6),
            w,
            0.6,
            boxstyle="round,pad=0.02,rounding_size=0.08",
            fc=header_color,
            ec=header_color,
            lw=2,
            zorder=3,
        )
    )
    ax.text(
        x + w / 2,
        y - 0.3,
        title,
        ha="center",
        va="center",
        color="white",
        fontsize=12,
        fontweight="bold",
        zorder=4,
    )
    for i, (name, kind) in enumerate(fields):
        fy = y - 0.6 - rh * (i + 0.5)
        col = PK if kind in ("PK", "FK") else TEXT
        wt = "bold" if kind in ("PK", "FK") else "normal"
        tag = f" [{kind}]" if kind in ("PK", "FK") else ""
        ax.text(
            x + 0.18,
            fy,
            f"{name}{tag}",
            ha="left",
            va="center",
            color=col,
            fontsize=8.8,
            fontweight=wt,
            zorder=4,
        )
        if i < len(fields) - 1:
            ax.plot(
                [x + 0.08, x + w - 0.08],
                [y - 0.6 - rh * (i + 1)] * 2,
                color="#2A3D57",
                lw=0.7,
                zorder=4,
            )
    return dict(x=x, y=y, w=w, h=total_h, cx=x + w / 2, bottom=y - total_h)


# Column 1 (left): User + Token
user = entity(
    ax,
    0.5,
    8.3,
    2.8,
    "User (auth)",
    [
        ("id", "PK"),
        ("username", ""),
        ("email", ""),
        ("password", ""),
        ("is_active", ""),
    ],
    HEADER2,
)

token = entity(
    ax,
    0.5,
    4.0,
    2.8,
    "Token (DRF)",
    [
        ("key", "PK"),
        ("user", "FK"),
        ("created", ""),
    ],
    HEADER3,
)

# Column 2 (middle): Transacao + Meta
trans = entity(
    ax,
    5.0,
    8.3,
    3.4,
    "Transacao",
    [
        ("id", "PK"),
        ("usuario", "FK"),
        ("categoria", "FK"),
        ("descricao", ""),
        ("valor", ""),
        ("data", ""),
        ("criado", ""),
    ],
    HEADER,
)

meta = entity(
    ax,
    5.0,
    3.4,
    3.4,
    "MetaEconomia",
    [
        ("id", "PK"),
        ("usuario", "FK"),
        ("titulo", ""),
        ("valor_alvo", ""),
        ("valor_atual", ""),
        ("prazo", ""),
        ("concluida", ""),
    ],
    HEADER,
)

# Column 3 (right): Categoria
cat = entity(
    ax,
    9.7,
    8.3,
    3.0,
    "Categoria",
    [
        ("id", "PK"),
        ("usuario", "FK"),
        ("nome", ""),
        ("tipo (E/S)", ""),
        ("cor", ""),
        ("icone", ""),
    ],
    HEADER,
)


def connect(ax, p1, p2, l1, l2, rad=0.0):
    arr = FancyArrowPatch(
        p1,
        p2,
        arrowstyle="-",
        color=LINE,
        lw=1.6,
        connectionstyle=f"arc3,rad={rad}",
        zorder=1,
    )
    ax.add_patch(arr)
    ax.text(p1[0], p1[1] + 0.16, l1, color=PK, fontsize=10, ha="center", zorder=5)
    ax.text(p2[0], p2[1] - 0.20, l2, color=PK, fontsize=10, ha="center", zorder=5)


# User(right) -> Transacao(left)  1:N
connect(ax, (3.3, 7.6), (5.0, 7.0), "1", "N")
# User(right) -> Meta(left)  1:N
connect(ax, (3.3, 6.6), (5.0, 2.6), "1", "N", rad=-0.15)
# User(right) -> Categoria(left)  1:N
connect(ax, (3.3, 8.0), (9.7, 7.4), "1", "N", rad=0.08)
# User(bottom) -> Token(top)  1:1
connect(ax, (1.9, 5.5), (1.9, 4.0), "1", "1")
# Categoria(left) -> Transacao(right)  1:N
connect(ax, (9.7, 6.6), (8.4, 6.4), "1", "N")

ax.text(
    6.5,
    8.78,
    "ACashController — Modelo de Dados (ER)",
    ha="center",
    va="center",
    color="white",
    fontsize=14,
    fontweight="bold",
)

legend = [
    Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor=HEADER,
        markersize=11,
        label="Apps do projeto",
        lw=0,
    ),
    Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor=HEADER2,
        markersize=11,
        label="Django auth (nativo)",
        lw=0,
    ),
    Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor=HEADER3,
        markersize=11,
        label="DRF (API token)",
        lw=0,
    ),
    Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor=PK,
        markersize=11,
        label="PK / FK",
        lw=0,
    ),
]
ax.legend(
    handles=legend,
    loc="lower right",
    fontsize=9,
    framealpha=0.15,
    facecolor=BODY,
    edgecolor=LINE,
    labelcolor=TEXT,
)

plt.tight_layout()
plt.savefig(
    "/home/user/financas-pessoais/docs/diagrama_er.png",
    facecolor=fig.get_facecolor(),
    bbox_inches="tight",
)
print("saved")
