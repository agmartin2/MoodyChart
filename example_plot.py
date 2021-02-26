import matplotlib as mpl
mpl.use("pgf")

pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": r"\usepackage[utf8x]{inputenc} \usepackage[T1]{fontenc} \usepackage{times}"
}
mpl.rcParams.update(pgf_with_pdflatex)

# Output file basename
outputname = "example_plot"

import MoodyChart as MC

plt = MC.MoodyChart()
ax  = plt.gca()    # Only needed if something else is to be plotted

# Plotting ...
plt.savefig(outputname + '.pgf', bbox_inches = 'tight')
plt.savefig(outputname + '.pdf', bbox_inches = 'tight')
