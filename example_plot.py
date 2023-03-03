import matplotlib as mpl
mpl.use("pgf")

pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "font.family": "serif",
    "pgf.preamble": \
         r"\usepackage[utf8x]{inputenc}" \
         r"\usepackage[T1]{fontenc}" \
         r"\usepackage{times}"
}
mpl.rcParams.update(pgf_with_pdflatex)

# Output file basename
outputname = "example_plot"

import MoodyChart as MC

# Create plot window
# Options can be passed as plt = MC.MoodyChart(lang="es",f_plotmax=1e-1,...)
plt = MC.MoodyChart()
ax  = plt.gca()    # Only needed if something else is to be plotted
# Plot data passed as two [x1,x2,...],[y1,y2,...] arrays
# ax.plot([],[],'ro')
# ax.plot([],[],'bo')

# Plotting ...
plt.savefig(outputname + '.pgf', bbox_inches = 'tight')
plt.savefig(outputname + '.pdf', bbox_inches = 'tight')
