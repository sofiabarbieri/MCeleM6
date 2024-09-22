import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import animation
import numpy as np
from scipy import optimize
import os
import ROOT

point1 = [5, 20]
point2 = [45, 20]
x_values = [point1[0], point2[0]]
y_values = [point1[1], point2[1]]


class Plot2D:
    def __init__(self, number, limits, limits_spheroid, v_MEXp_slow, v_MEXp_fast, path):
        self.klast = 0.0
        self.profilelast = []
        self.x = [0] * number
        self.y = [0] * number
        self.limits = limits
        self.list_m_fit_pre = []
        self.number = number
        self.center_y = (limits_spheroid[1][1] - limits_spheroid[0][1]) / 2
        self.counter = 0  # track the iteration it is on
        self.path = path

        os.mkdir(
            os.path.join(self.path, "Graphs")
        )  # creating the directory to store the graphs

        global fig, fig1, fig2, fig_id1, fig_id2, fig_id_ratio, fig_root_based, fig_movie
        fig = plt.figure()
        fig_id1 = plt.figure(figsize=[6, 8])
        fig_id_ratio = plt.figure(figsize=[9.6, 7.2])
        fig_root_based = plt.figure()

        plt.grid(True)
        plt.subplots_adjust(hspace=1, wspace=0.6)

        self.ims_movie1 = []
        self.ims_movie2 = []
        self.data_movie_1 = []
        self.data_movie_2 = []

        #   ROOT Stuff
        self.v_slow = v_MEXp_slow
        self.v_fast = v_MEXp_fast

    def Update(self, particles, sliceD, slice_depth):
        del self.x[:]
        del self.y[:]
        if sliceD == True:
            for index, item in enumerate(particles):
                if (
                    item.z > float(self.center_y) - float(slice_depth) / 2.0
                    and item.z < float(self.center_y) + float(slice_depth) / 2.0
                ):
                    self.x.append(item.x)
                    self.y.append(item.y)
        else:
            for index, item in enumerate(particles):
                self.x.append(item.x)
                self.y.append(item.y)
        self.Plot()
        print(len(self.x))

    def UpdateCpp(self, x_list, y_list, z_list, sliceD, slice_depth):
        del self.x[:]
        del self.y[:]
        if sliceD == True:
            for index, item in enumerate(x_list):
                if (
                    z_list[index] > float(self.center_y) - float(slice_depth) / 2.0
                    and z_list[index] < float(self.center_y) + float(slice_depth) / 2.0
                ):
                    self.x.append(x_list[index])
                    self.y.append(y_list[index])
        else:
            for index, item in enumerate(x_list):
                self.x.append(x_list[index])
                self.y.append(y_list[index])
        self.Plot()

    def Plot(self):
        fig.clf()

        self.ax1 = fig.add_subplot(2, 1, 1)
        hist, xbins, ybins, im = self.ax1.hist2d(
            self.x, self.y, bins=self.limits[0][1], range=self.limits
        )
        self.ax1.set_title("2D distribution MEXps")
        self.ax1.set_xlabel("Long axis (um)")
        self.ax1.set_ylabel("Short axis (um)")
        fig.colorbar(im)
        oneD = []

        # density = self.limits[0][1]/self.limits[0][1] to normalize on bin size if bin =/= 1um

        self.ax1.plot(x_values, y_values)

        xbins_line = []
        for xbin in range(point1[0], point2[0]):
            oneD.append(
                (hist[xbin][point2[1]])
            )  # original statement if playing with bins size: hist[xbin][int(point2[1]/density)
            xbins_line.append(float(xbin - point1[0]))

        # xbins = xbins[:xbins.shape[0]-1]
        # xbins = xbins/np.max(xbins)
        xbins_line = xbins_line / np.max(xbins_line)
        xbins = xbins_line

        oneD = oneD / np.max(oneD)

        self.profilelast = oneD

        self.ax2 = fig.add_subplot(2, 2, 3)
        self.ax2.plot(xbins, oneD)
        params, params_covariance = optimize.curve_fit(
            self.fit_func, xbins, oneD, bounds=((-np.inf, -np.inf), (np.inf, np.inf))
        )
        hist2 = self.ax2.plot(
            xbins, self.fit_func(xbins, params[0], params[1]), label="Fit"
        )
        self.ax2.set_title(" MEXp gradient intensity")
        self.ax2.set_ylabel("Normal. intensity (a.u.)")
        self.ax2.set_xlabel("Normal. embryo length")

        self.list_m_fit_pre.append(params[0])

        self.klast = params[0]

        t_pre = np.arange(len(self.list_m_fit_pre))
        self.ax3 = fig.add_subplot(2, 2, 4)
        self.ax3.plot(t_pre, self.list_m_fit_pre, marker="", linewidth=1, alpha=0.9)
        self.ax3.set_title("Slope vs time MEXp")
        self.ax3.set_ylabel("Intensity gradient (dI/dx)")
        self.ax3.set_xlabel("Time (s)")

        # fig.canvas.draw()

        # plt.show(block=False)
        # plt.pause(0.1)

    def conc_calcCpp(self, X_list, Y_list, Z_list, id_list):
        autosave = 100  # to save every N iterations, I advise to 10 for QC of production runs. 100 for exploratory work (only 21 images generated)
        self.counter += 1

        id0_slice = []
        id1_slice = []

        id0 = []
        id1 = []
        xbins_line = []

        x1 = []
        y1 = []
        x2 = []
        y2 = []
        x3 = []
        y3 = []

        fig_id_ratio.clf()

        for index, item in enumerate(X_list):
            if id_list[index] == 0:
                x1.append(X_list[index])
                y1.append(Y_list[index])
            elif id_list[index] == 1:
                x2.append(X_list[index])
                y2.append(Y_list[index])
            x3.append(X_list[index])
            y3.append(Y_list[index])

        fig_id1.clf()
        # Embryo plot with 3 subplots
        ax_id2 = fig_id1.add_subplot(3, 1, 3)
        hist2, xbins2, ybins2, im2 = ax_id2.hist2d(
            x3, y3, bins=self.limits[0][1], range=self.limits
        )
        ax_id2.set(
            title="2D concentration MEXp",
            xlabel="Long axis (um)",
            ylabel="Short axis (um)",
            ylim=(0, 30),
        )
        fig_id1.colorbar(im2)

        # normalisation of the plot colors intensities with vmin and vmax on the total MEXp
        v_min = np.min(hist2)
        v_max = np.max(hist2)

        ax_id0 = fig_id1.add_subplot(3, 1, 1)
        hist, xbins, ybins, im = ax_id0.hist2d(
            x1, y1, bins=self.limits[0][1], range=self.limits, vmin=v_min, vmax=v_max
        )
        ax_id0.set(
            title="2D concentration MEXps",
            xlabel="Long axis (um)",
            ylabel="Short axis (um)",
            ylim=(0, 30),
        )
        fig_id1.colorbar(im)

        ax_id1 = fig_id1.add_subplot(3, 1, 2)
        hist1, xbins1, ybins1, im1 = ax_id1.hist2d(
            x2,
            y2,
            bins=self.limits[0][1],
            range=self.limits,
            vmin=v_min,
            vmax=int(2 / 3 * v_max),
        )
        ax_id1.set(
            title="2D concentration MEXpf",
            xlabel="Long axis (um)",
            ylabel="Short axis (um)",
            ylim=(0, 30),
        )
        fig_id1.colorbar(im1)

        fig_id1.tight_layout()
        fig_id1.canvas.draw()

        # converting the canvas to a pixel matrix
        if self.counter % autosave == 0:
            plt.imsave(
                os.path.join(self.path, f"Graphs/MEXp-Embryo_t-{self.counter}.png"),
                np.array(fig_id1.canvas.renderer.buffer_rgba()),
            )

        density = self.limits[0][1] / self.limits[0][1]

        for xbin in range(0, len(xbins) - 1):
            id0_slice.append(
                (hist[xbin][int(15 / density)])
            )  # modified here to solve float issue of index?
            id1_slice.append((hist1[xbin][int(15 / density)]))
            xbins_line.append(xbin)

        for xbin in range(0, len(xbins) - 1):
            id0.append((sum(hist[xbin][:])))
            id1.append((sum(hist1[xbin][:])))

        ratio = np.divide(id0_slice, id1_slice)
        ratio2 = np.divide(id0, id1)

        ax_id_ratio = fig_id_ratio.add_subplot(3, 2, 1)
        ax_id_ratio.plot(xbins_line, ratio)
        ax_id_ratio.set(
            title="Ratio, integrat. on Z",
            ylabel="Ratio MEXps/MEXpf",
            xlabel="Embryo length (um)",
        )

        ax_id_ratio2 = fig_id_ratio.add_subplot(3, 2, 2)
        ax_id_ratio2.plot(xbins_line, ratio2)
        ax_id_ratio2.set(
            title="Ratio, integrat. on Y and Z",
            ylabel="Ratio MEXps/MEXpf",
            xlabel="Embryo length (um)",
        )

        ax_id_conc = fig_id_ratio.add_subplot(3, 2, 3)
        ax_id_conc.plot(xbins_line, id0, "r", label="MEXps")
        ax_id_conc.plot(xbins_line, id1, "b", label="MEXpf")
        ax_id_conc.set(
            title="# MEXp p.les, integrat. on Y and Z",
            ylabel="# p.les MEXps , MEXpf",
            xlabel="Embryo length (um)",
        )
        ax_id_conc.legend(loc="upper right", frameon=False)

        ax_id_slice = fig_id_ratio.add_subplot(3, 2, 4)
        ax_id_slice.plot(xbins_line, id0_slice, "r", label="MEXps")
        ax_id_slice.plot(xbins_line, id1_slice, "b", label="MEXpf")
        ax_id_slice.set(
            title="# MEXp p.les, integrat. on Z",
            ylabel="# p.les MEXps , MEXpf",
            xlabel="Embryo length (um)",
        )
        ax_id_slice.legend(loc="upper right", frameon=False)

        MEXp_slow = np.array(id0_slice) / self.number
        MEXp_fast = np.array(id1_slice) / self.number
        MEXp_tot = MEXp_slow + MEXp_fast

        ax_id_slice_conc = fig_id_ratio.add_subplot(3, 2, 5)
        ax_id_slice_conc.plot(xbins_line, MEXp_tot, "g", label="Tot. concentr.")
        ax_id_slice_conc.plot(xbins_line, MEXp_slow, "r", label="MEXps")
        ax_id_slice_conc.plot(xbins_line, MEXp_fast, "b", label="MEXp5f")
        ax_id_slice_conc.set(
            title="MEXp concentrat., integrat. on Z",
            ylabel="Conc. MEXps + MEXpf",
            xlabel="Embryo length (um)",
        )
        ax_id_slice_conc.legend(loc="upper right", frameon=False)

        fig_id_ratio.tight_layout()
        fig_id_ratio.canvas.draw()

        if self.counter % autosave == 0:
            plt.imsave(
                os.path.join(self.path, f"Graphs/MEXp-PlotA_t-{self.counter}.png"),
                np.array(fig_id_ratio.canvas.renderer.buffer_rgba()),
            )

            # root stuff
        histo3DSlow = ROOT.TH3F(
            "plot3D-Slow", "plot3D-Slow", 50, 0, 50, 30, 0, 30, 30, 0, 30
        )
        histo3DFast = ROOT.TH3F(
            "plot3D-Fast", "plot3D-Fast", 50, 0, 50, 30, 0, 30, 30, 0, 30
        )

        x_3d = np.array(X_list)
        y_3d = np.array(Y_list)
        z_3d = np.array(Z_list)
        for xbin in range(0, len(x_3d)):
            if id_list[xbin] == 0:
                histo3DSlow.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin])
            else:
                histo3DFast.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin])

        slow_content = []
        fast_content = []
        for x_bin in range(1, 51):
            slow_content.append(histo3DSlow.GetBinContent(x_bin, 15, 15))
            fast_content.append(histo3DFast.GetBinContent(x_bin, 15, 15))

        max_arr = np.array(slow_content) + np.array(fast_content)

        self.data_movie_2 = max_arr / np.max(max_arr)

        fig_root_based.clf()

        ratio3 = np.divide(slow_content, fast_content)

        ax_id_ratio3 = fig_root_based.add_subplot(2, 2, 1)
        ax_id_ratio3.plot(xbins_line, ratio3)
        ax_id_ratio3.set(
            title="Ratio, Central Voxel",
            ylabel="Ratio MEXps/MEXpf",
            xlabel="Embryo length (um)",
        )
        ax_id_ratio3.set_ylabel("Ratio MEXps/MEXpf")
        ax_id_ratio3.set_xlabel("Embryo length (um)")

        v_average = (
            np.array(slow_content) * self.v_slow + np.array(fast_content) * self.v_fast
        ) / (np.array(slow_content) + np.array(fast_content))

        conc_root_MEXp_slow = np.array(slow_content) / self.number
        conc_root_MEXp_fast = np.array(fast_content) / self.number

        # For ax_id_conc_root
        ax_id_conc_root = fig_root_based.add_subplot(2, 2, 2)
        ax_id_conc_root.plot(xbins_line, conc_root_MEXp_slow, "r", label="MEXp slow")
        ax_id_conc_root.plot(xbins_line, conc_root_MEXp_fast, "b", label="MEXp fast")
        ax_id_conc_root.set(
            title="MEXp concentr.,  Central voxel",
            ylabel="Concentr. MEXps , MEXpf",
            xlabel="Embryo length (um)",
        )
        ax_id_conc_root.legend(loc="upper right", frameon=False)

        # For av_velocity
        av_velocity = fig_root_based.add_subplot(2, 2, 3)
        av_velocity.plot(xbins_line, v_average)
        av_velocity.set(
            title="Mean MEXp velocity, Central Voxel",
            ylabel="Mean velocity MEXps, MEXpf",
            xlabel="Embryo length (um)",
        )

        fig_root_based.tight_layout()
        fig_root_based.canvas.draw()

        # if self.counter % autosave == 0:
        #  plt.imsave(os.path.join(self.path, f'Graphs/MEXp-PlotB_t-{self.counter}.png'), np.array(fig_root_based.canvas.renderer.buffer_rgba()))
        # plt.show(block=False)
        # plt.pause(0.1)
        del histo3DSlow
        del histo3DFast

        return (
            ratio2.tolist(),
            conc_root_MEXp_slow.tolist(),
            conc_root_MEXp_fast.tolist(),
            v_average.tolist(),
        )

    def FillDrawMovie(self):
        self.ims_movie1.append(self.data_movie_1)
        self.ims_movie2.append(self.data_movie_2)

    def DrawMovie(self):
        fig, ax = plt.subplots()
        container = []

        for i in range(len(self.ims_movie1)):
            container.append([plt.imshow(self.ims_movie1[i])])
        im_ani = animation.ArtistAnimation(fig, container, interval=50, blit=False)
        im_ani.save(
            os.path.join(self.path, "2DMEXp.html"), writer="imagemagick", fps=10, dpi=50
        )

        fig2, a2x = plt.subplots()
        container2 = []

        for i in range(len(self.ims_movie2)):
            (plotty,) = a2x.plot(self.ims_movie2[i], color="blue")
            container2.append([plotty])
        im_ani2 = animation.ArtistAnimation(fig2, container2, interval=50, blit=False)
        im_ani2.save(
            os.path.join(self.path, "Gradient.html"),
            writer="imagemagick",
            fps=10,
            dpi=50,
        )
        print("done")

        # plt.show(block=False)

    def fit_func(self, x, a, b):
        return a * x + b
