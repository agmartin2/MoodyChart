MoodyChart.py
=============

### Purpose

MoodyChart.py is a python module to help creating and using Moody
charts for analysis of hydraulic head losses in pipes.

It is mostly intended to use TeX as underlying engine (with pgf
background), and for that reason strings and values are TeX formatted.

### Options

Some keyword options can be passed as arguments when calling the
MoodyChart function.

* `Re_plotmin`: Plot lower limit of Reynolds number.
* `Re_plotmax`: Plot upper limit of Reynolds number.
* `f_plotmin`:  Plot lower limit of friction coefficient.
* `f_plotmax`:  Plot upper limit of friction coefficient.
* `lang`:       Set language for strings (Only `en` and `es` are
  currently supported).
* `Debug`:      Enable debugging if set to `True`

### Example of usage

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

    plt = MC.MoodyChart()
    ax  = plt.gca()    # Only needed if something else is to be plotted
    ax.plot([11789],[4.01e-2],'ro')

    # Plotting ...
    plt.savefig(outputname + '.pgf', bbox_inches = 'tight')
    plt.savefig(outputname + '.pdf', bbox_inches = 'tight')

### More about this

This is my first python module, so there is surely room for
improvement. Suggestions and bug fixes are welcome.

This module currently provides output only in Spanish and English.
I prefer to keep everything on a single file, so I did not adapt it to
gettext. As said, I am very new to python and suggestions are welcome.

### License

MoodyChart is released under the the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

### Author

Agustín Martín Domingo `<agustin6martin@gmail.com>`
