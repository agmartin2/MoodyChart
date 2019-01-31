#!/usr/bin/python

# dfr_diagrama-Moody.py - A Python-based Moody chart
# Copyright (C) 2018-2019 Agustin Martin Domingo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import numpy as np
# import texfig first to configure Matplotlib's backend
import texfig
# then, import PyPlot
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.ticker as ticker


# matplotlib.use('pgf')
# import matplotlib as mpl
# mpl.use("pgf")
#
# pgf_with_pdflatex = {
#     "pgf.texsystem": "pdflatex",
#     "pgf.preamble": [
#          r"\usepackage[utf8x]{inputenc}",
#          r"\usepackage[T1]{fontenc}",
#          r"\usepackage{cmbright}",
#          ]
# }
# mpl.rcParams.update(pgf_with_pdflatex)

def Colebrook_getf_iterate (Re,rr):
    f_seed = 0.04
    f = np.empty(len(Re))
    f.fill(f_seed)
    for i in range(10):
        f = ( 2*np.log10(rr/3.7 + 2.51/Re/np.sqrt(f)) )**(-2)
    return f

# ---------------------------------------------------
# Some limit values
# ---------------------------------------------------

# Re limits in plot
Re_plotmin = 500
Re_plotmax = 1e8
f_plotmin  = 0.008
f_plotmax  = 0.1


# Re limits for laminar zone plot
Re_lam_low  = Re_plotmin
Re_lam_high = 2300

# Re limits for critical zone plot
Re_cri_low  = 2e3
Re_cri_high = 4e3

# Re limits for turbulent flow plot
Re_trb_min  = 3000
Re_trb_max  = Re_plotmax

Re = np.logspace(np.log10(Re_plotmin), np.log10(Re_plotmax), num=200)
rr = [
    [0, 1],
    [1e-6, 2e3],
    [5e-6, 0.7e3],
    [1e-5, 1.5e2],
    [5e-5, 6e1],
    [1e-4, 3e1],
    [2e-4, 1],
    [4e-4, 1],
    [6e-4, 1],
    [8e-4, 1],
    [1e-3, 1],
    [2e-3, 1],
    [4e-3, 1],
    [6e-3, 1],
    [8e-3, 1],
    [1e-2, 1],
    [1.5e-2, 1],
    [2e-2, 1],
    [3e-2, 1],
    [4e-2, 1],
    [5e-2, 1],
    [6e-2, 1],
    [7e-2, 1],
    [8e-2, 1]
]

# ======== Now the figure object handling ==================

# Creating the figure object
fig = texfig.figure()

# Set size
fig.set_size_inches(11.69,8.27)
fig.set_size_inches(9.35,6.62)

# Get a reference to the coordinate axes object. Important.
# Some commands need it (can also be done by declaring a single subplot)
ax = plt.gca()

plt.xscale('log')
plt.yscale('log')

# Set plot limits
plt.xlim(Re_plotmin,Re_plotmax)
plt.ylim(f_plotmin,f_plotmax)

ax.set_xlabel("Reynolds number ($\\textsl{Re}$)")
ax.set_ylabel("Friction coefficient ($f$)")
ax.text(2*Re_plotmax,np.sqrt(f_plotmin*f_plotmax),
        "Relative roughness ($rr = e/D$)",
        fontsize=10,
        VerticalAlignment="center",
        rotation=90)

# Plot f(Re) Moody lines for laminar flow
laminar_Re = Re[ Re <= Re_lam_high ]
laminar_Re = np.concatenate([laminar_Re,[Re_lam_high]])
line, = plt.plot(laminar_Re, 64/laminar_Re, lw=1)

# Plot f(Re) Moody lines as for laminar flow in transition zone
transition_Re = Re[ (Re >= Re_lam_high)  & (Re <= Re_cri_high) ]
transition_Re = np.concatenate([[Re_lam_high],transition_Re,[Re_cri_high]])
line, = plt.plot(transition_Re, 64/transition_Re, lw=1)

# Plot f(Re,rr) Moody lines for turbulent flow
turbulent_Re = Re[ Re >= Re_trb_min ]
turbulent_Re = np.concatenate([[Re_trb_min],turbulent_Re])
for thisrr in rr:
    my_rr = thisrr[0]
    if thisrr[1] == 1:
        my_Re = turbulent_Re
    else:
        my_Re = turbulent_Re[ turbulent_Re >= Re_trb_min*thisrr[1] ]

    if my_Re.size > 0:
        Moody_line = Colebrook_getf_iterate(my_Re,my_rr)
        line, = plt.plot(my_Re, Moody_line, lw=1)
        Moody_line_min = Moody_line[-1]
        if Moody_line_min > f_plotmin:
            ax.text(1.1*Re_plotmax,Moody_line.min(),my_rr,fontsize=6)
    else:
        print "Skipping relative roughness: ", my_rr

# Boundary between turbulence and completely developed turbulence
Turb_Boundary = (1.14-2*np.log10(3500/turbulent_Re))**-2
line, = ax.plot(turbulent_Re, Turb_Boundary, lw=1)

# Draw a rectangle above critical zone
ax.add_patch(
    patches.Rectangle(
        (Re_cri_low, f_plotmin),   # (x,y)
        Re_cri_high - Re_cri_low,  # width
        f_plotmax - f_plotmin,     # height
        facecolor="lightgray",
        linewidth=0.3,
        edgecolor="black"
    )
)

# Draw minor ticks smaller
ax.tick_params(which='minor',labelsize=6)

# Ploting vertical grid and Re labels
xmajor_list = range(int(np.floor(np.log10(Re_plotmin))),int(np.ceil(np.log10(Re_plotmax)))+1)
ax.xaxis.set_major_locator(ticker.FixedLocator(map(lambda x: 10**x, xmajor_list)))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(map(lambda x: format("$10^{%s}$" % x), xmajor_list)))
# xmajor_list = np.array([])
xminor_list = []
xminor_tags = []
for i in xmajor_list:
    xpower = 10**i
    # xmajor_list.append(xpower)
    if xpower >= Re_plotmin:
        line, = ax.plot([xpower,xpower],[f_plotmin,f_plotmax],linewidth=0.8)

    for j in [2,3,4,5,6,7,8,9]:
        xminor = j*xpower;
        xminor_list.append(xminor)
        if j < 8:
            xminor_tags.append(j)
        else:
            xminor_tags.append("")
        if ( (xminor >= Re_plotmin) & (xminor <= Re_plotmax) ):
            line, = ax.plot([xminor,xminor],[f_plotmin,f_plotmax],linewidth=0.3)

    for j in [1.2,1.4,1.6,1.8,2.2,2.4,2.6,2.8,3.5,4.5,5.5,6.5]:
        xminor = j*xpower;
        if ( (xminor >= Re_plotmin) & (xminor <= Re_plotmax) ):
            line, = ax.plot([xminor,xminor],[f_plotmin,f_plotmax],linewidth=0.1)

ax.xaxis.set_minor_locator(ticker.FixedLocator(np.asarray(xminor_list)))
ax.xaxis.set_minor_formatter(ticker.FixedFormatter(xminor_tags))

# Ploting horizontal grid and f labels
ymajor_list = range(int(np.floor(np.log10(f_plotmin))),int(np.ceil(np.log10(f_plotmax)))+1)
ax.yaxis.set_major_locator(ticker.FixedLocator(map(lambda x: 10**x, ymajor_list)))
ax.yaxis.set_major_formatter(ticker.FixedFormatter(map(lambda x: format("$10^{%s}$" % x), ymajor_list)))
yminor_list = []
yminor_tags = []
for i in range(int(np.floor(np.log10(f_plotmin))),int(np.ceil(np.log10(f_plotmax)))+1):
    ymajor = 10**i
    if ymajor >= f_plotmin:
        line, = ax.plot([Re_plotmin,Re_plotmax],[ymajor,ymajor],linewidth=0.8)

    for j in [1.5,2,3,4,5,6,7,8,9]:
        yminor = j*ymajor
        yminor_list.append(yminor)
        yminor_tags.append(j)
        if ( (yminor >= f_plotmin) & (yminor <= f_plotmax) ):
            line, = ax.plot([Re_plotmin,Re_plotmax],[yminor,yminor],linewidth=0.3)

    for j in [1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,
              2.9,3.1,3.2,3.3,3.4,3.5,3.6,3.7,3.8,3.9,4.1,4.2,4.3,4.4,4.5,4.6,4.7,
              4.8,4.9,5.2,5.4,5.6,5.8,6.2,6.4,6.6,6.8,7.2,7.4,7.6,7.8,8.5,9.5]:
        yminor = j*ymajor;
        if ( (yminor >= f_plotmin) & (yminor <= f_plotmax) ):
            line, = ax.plot([Re_plotmin,Re_plotmax],[yminor,yminor],linewidth=0.1)

ax.yaxis.set_minor_locator(ticker.FixedLocator(np.asarray(yminor_list)))
ax.yaxis.set_minor_formatter(ticker.FixedFormatter(yminor_tags))

# Zona de regimen laminar
ax.annotate("",
            xy = (Re_lam_low,9e-3),
            xytext=(Re_cri_low,9e-3),
            arrowprops=dict(facecolor='black',
                            arrowstyle="<->",
                            linewidth=0.3))
ax.annotate("Laminar",
            xy = (Re_lam_low,9e-3),
            xytext=(np.sqrt(Re_lam_low*Re_cri_low),9e-3),
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=8,
)

# Zona critica de transicion de laminar a turbulento
ax.annotate("",
            xy = (Re_cri_low,9e-3),
            xytext=(Re_cri_high,9e-3),
            arrowprops=dict(facecolor='black',
                            arrowstyle="<->",
                            linewidth=0.3))
ax.annotate("Critico",
            xy = (Re_lam_low,9e-3),
            xytext=(np.sqrt(Re_cri_low*Re_cri_high),9e-3),
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=8,
)

# Zona turbulenta
ax.annotate("Turbulento",
            xy = (Re_cri_high,9e-3),
            xytext=(np.sqrt(Re_cri_high*Re_trb_max),9e-3),
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=8,
            arrowprops=dict(facecolor='black',
                            arrowstyle="->",
                            linewidth=0.3)
)

# Zona de turbulencia completa
ax.annotate("",
            xy = (1e5,6e-2),
            xytext=(Re_plotmax,6e-2),
            arrowprops=dict(facecolor='black',
                            arrowstyle="<->",
                            linewidth=0.3))
ax.annotate("Turbulencia completa",
            xy = (1e5,6e-2),
            xytext=(np.sqrt(1e5*Re_plotmax),6e-2),
            horizontalalignment='center',
            verticalalignment='bottom',
            fontsize=8,
)

# Ploteando ...
plt.show()
texfig.savefig("example_plot", bbox_inches = 'tight')

# plt.show()
# plt.savefig("kk.pdf", bbox_inches='tight')
#plt.margins(0.1,0.5)
