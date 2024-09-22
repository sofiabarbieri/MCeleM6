import matplotlib.pyplot as plt
import matplotlib.colors as mcolorson
from matplotlib import animation
import numpy as np
from scipy import optimize
import os
import ROOT

class Plot2D:
    def __init__(self, number, limits, limits_spheroid, plk1_to_mex_multiplicator, v_plk1, v_MEXp_slow, v_MEXp_fast, path):
        self.klast = 0.0
        self.profilelast = []
        self.x = [0] * number
        self.y = [0] * number
        self.limits = limits
        self.number = number
        self.kmultiplicator = plk1_to_mex_multiplicator
        self.v_plk1 = v_plk1
        self.v_MEXp_slow = v_MEXp_slow
        self.v_MEXp_fast = v_MEXp_fast
        self.center_y = (limits_spheroid[1][1] - limits_spheroid[0][1]) / 2
        self.list_m_fit_pre = []

        global fig3, fig4, fig5, fig_id1, fig_id_ratio
        fig3 = plt.figure()
        fig_id1 = plt.figure(figsize=[6, 10])
        fig_id_ratio = plt.figure(figsize=[9.6, 7.2])

        plt.grid(True)
        plt.subplots_adjust(hspace=1, wspace=0.6)

        self.ims_movie1 = []
        self.ims_movie2 = []
        self.data_movie_1 = []
        self.data_movie_2 = []

        self.counter = 0
        self.path = path

    def Update(self, particles, sliceD, slice_depth):
        self.x.clear()
        self.y.clear()

        if sliceD:
            for item in particles:
                if self.center_y - slice_depth / 2.0 < item.z < self.center_y + slice_depth / 2.0:
                    self.x.append(item.x)
                    self.y.append(item.y)
        else:
            for item in particles:
                self.x.append(item.x)
                self.y.append(item.y)

        self.plot()

    def UpdateCpp(self, x_list, y_list, z_list, sliceD, slice_depth):
        del self.x[:]
        del self.y[:]
        if (sliceD== True):
            for index, item in enumerate (x_list):
                if (z_list[index] > float(self.center_y)-float(slice_depth)/2. and z_list[index]  < float(self.center_y)+float(slice_depth)/2.):
                        self.x.append(x_list[index])
                        self.y.append(y_list[index])
        else:
            for index, item in enumerate (x_list):            
                self.x.append(x_list[index])
                self.y.append(y_list[index])

        self.plot()

    def plot(self):
        fig3.clf()
        
        self.ax1 = fig3.add_subplot(2, 1, 1)

        hist, xbins, ybins, im = self.ax1.hist2d(self.x, self.y, bins=self.limits[0][1], range=self.limits)
        self.ax1.set_title("2D distribution PLK-1")
        self.ax1.set_xlabel("Long axis (um)")
        self.ax1.set_ylabel("Short axis (um)")
        fig3.colorbar(im)

        oneD = []
        #density = self.limits[0][1] / self.limits[0][1]

        # defining line
        point1 = [5, 20]
        point2 = [45, 20]
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        self.ax1.plot(x_values, y_values)

        xbins_line = []
        for xbin in range(point1[0], point2[0]):
            oneD.append(hist[xbin][point2[1]])  # original statement int(point2[1] / density)
            xbins_line.append(float(xbin - point1[0]))

        #xbins = xbins[: xbins.shape[0] - 1]
        #xbins = xbins / np.max(xbins)
        xbins_line = xbins_line / np.max(xbins_line)
        xbins = xbins_line

        oneD = oneD / np.max(oneD)

        self.profilelast = oneD

        self.ax2 = fig3.add_subplot(2, 2, 3)
        self.ax2.plot(xbins, oneD)
        params, params_covariance = optimize.curve_fit(self.fit_func, xbins, oneD, bounds=((-np.inf, -np.inf), (np.inf, np.inf)))
        hist2 = self.ax2.plot(xbins, self.fit_func(xbins, params[0], params[1]), label='Fit')
        self.ax2.set_title(" PLK-1 gradient intensity")
        self.ax2.set_ylabel("Normal. intensity (a.u.)")
        self.ax2.set_xlabel("Normal. embryo length")
        self.list_m_fit_pre.append(params[0])

        self.klast = params[0]

        t_pre = np.arange(len(self.list_m_fit_pre))
        self.ax3 = fig3.add_subplot(2, 2, 4)
        self.ax3.plot(t_pre, self.list_m_fit_pre, marker='', linewidth=1, alpha=0.9)
        self.ax3.set_title("Slope vs time PLK-1")
        self.ax3.set_ylabel("Intensity gradient (dI/dx)")
        self.ax3.set_xlabel("Time (s)")

        #fig3.canvas.draw()

        #plt.show(block=False)
        #plt.pause(0.1)


    def conc_calcCpp(self, X_list, Y_list, Z_list, id_list):
        autosave = 10 # setting frequency of image saving
        self.counter += 1

        fig_id1.clf()
        fig_id_ratio.clf()

        id0_slice = []
        id1_slice = []
        id2_slice = []

        id0 = []
        id1 = []
        id2 = []

        xbins_line = []

        x1 = []
        y1 = []
        x2 = []
        y2 = []
        x3 = []
        y3 = []
        x4 = []
        y4 = []

        for index, item in enumerate(X_list):
            if id_list[index] == 0:
                x1.append(X_list[index])
                y1.append(Y_list[index])
            elif id_list[index] == 1:
                x2.append(X_list[index])
                y2.append(Y_list[index])
            elif id_list[index] == 2:
                x3.append(X_list[index])
                y3.append(Y_list[index])
            x4.append(X_list[index])
            y4.append(Y_list[index])


        
        ax_id3 = fig_id1.add_subplot(4, 1, 4)
        hist3, xbins3, ybins3, im3 = ax_id3.hist2d(x4, y4, bins=self.limits[0][1], range=self.limits)
        ax_id3.set(title="PLK-1", xlabel="Long axis (um)", ylabel="Short axis (um)", ylim=(0,30))
        fig_id1.colorbar(im3)

        #add normalisation with vmin and vmax from the total PLK-1 min and max value
        v_min=np.min(hist3)
        v_max=np.max(hist3)

        ax_id0 = fig_id1.add_subplot(4, 1, 1)
        hist, xbins, ybins, im = ax_id0.hist2d(x1, y1, bins=self.limits[0][1], range=self.limits, vmin=v_min, vmax=v_max)
        ax_id0.set(title="Unbound PLK-1", xlabel="Long axis (um)", ylabel="Short axis (um)", ylim=(0,30))
        fig_id1.colorbar(im)

        ax_id1 = fig_id1.add_subplot(4, 1, 2)
        hist1, xbins1, ybins1, im1 =ax_id1.hist2d(x2, y2, bins=self.limits[0][1], range=self.limits, vmin=v_min, vmax=0.8*v_max)
        ax_id1.set(title="PLK-1 to MEXps", xlabel="Long axis (um)", ylabel="Short axis (um)", ylim=(0,30))
        fig_id1.colorbar(im1)

        ax_id2 = fig_id1.add_subplot(4, 1, 3)
        hist2, xbins2, ybins2, im2 = ax_id2.hist2d(x3, y3, bins=self.limits[0][1], range=self.limits, vmin=v_min, vmax=0.8*v_max)
        ax_id2.set(title="PLK-1 to MEXpf", xlabel="Long axis (um)", ylabel="Short axis (um)", ylim=(0,30))
        fig_id1.colorbar(im2)
        fig_id1.tight_layout()
        fig_id1.canvas.draw()

        if self.counter % autosave == 0: 
            plt.imsave(os.path.join(self.path, f'Graphs/PLK-1-Embryo_t-{self.counter}.png'), np.array(fig_id1.canvas.renderer.buffer_rgba()))

        self.data_movie_1 = hist3
        density = self.limits[0][1] / self.limits[0][1]

        for xbin in range(0, len(xbins) - 1):
            id0_slice.append(hist[xbin][int(15 / density)])
            id1_slice.append(hist1[xbin][int(15 / density)])
            id2_slice.append(hist2[xbin][int(15 / density)])

            xbins_line.append(xbin)

        for xbin in range(0, len(xbins) - 1):
            id0.append(sum(hist[xbin][:]))
            id1.append(sum(hist1[xbin][:]))
            id2.append(sum(hist2[xbin][:]))

        self.ax_id_conc = fig_id_ratio.add_subplot(2, 2, 1)
        self.ax_id_conc.plot(xbins_line, id0, 'g', label="Unbound PLK-1")
        self.ax_id_conc.plot(xbins_line, id1, 'r', label="PLK-1 to MEXps")
        self.ax_id_conc.plot(xbins_line, id2, 'b', label="PLK-1 to MEXpf")
        self.ax_id_conc.set_title("# PLK-1 p.les, integrat. on Y and Z")
        self.ax_id_conc.set_ylabel("Number p.les PLK-1 species")
        self.ax_id_conc.set_xlabel("Embryo length (um)")
        self.ax_id_conc.legend(loc="upper right", frameon=False)

        self.ax_id_slice = fig_id_ratio.add_subplot(2, 2, 2)
        self.ax_id_slice.plot(xbins_line, id0_slice, 'g', label="Unbound PLK-1")
        self.ax_id_slice.plot(xbins_line, id1_slice, 'r', label="PLK-1 to MEXps")
        self.ax_id_slice.plot(xbins_line, id2_slice, 'b', label="PLK-1 to MEXpf")
        self.ax_id_slice.set_title("# PLK-1 p.les, integrat. on Z")
        self.ax_id_slice.set_ylabel("# p.les PLK-1 species")
        self.ax_id_slice.set_xlabel("Embryo length (um)")
        self.ax_id_slice.legend(loc="upper right", frameon=False)

        #root stuff
        self.histo3DSlow = ROOT.TH3F("plot3D-Slow", "plot3D-Slow", 50, 0, 50, 30, 0, 30, 30, 0, 30 )
        self.histo3DFast = ROOT.TH3F("plot3D-Fast", "plot3D-Fast", 50, 0, 50, 30 , 0, 30, 30, 0, 30 )
        self.histo3DUnbound = ROOT.TH3F("histo3DUnbound", "histo3DUnbound", 50, 0, 50, 30, 0, 30, 30, 0, 30 )


        x_3d = np.array(X_list)
        y_3d = np.array(Y_list)
        z_3d = np.array(Z_list)

        for xbin in range(0, len(x_3d)):
            if id_list[xbin] == 0:
                self.histo3DUnbound.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin])
            if id_list[xbin] == 1:
                self.histo3DSlow.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin])
            if id_list[xbin] == 2:
                self.histo3DFast.Fill(x_3d[xbin], y_3d[xbin], z_3d[xbin])

        slow_content = []
        fast_content = []
        unbound_content = []

        for x_bin in range(1, 51):
          slow_content.append(self.histo3DSlow.GetBinContent(x_bin, 15, 15))
          fast_content.append(self.histo3DFast.GetBinContent(x_bin, 15, 15))
          unbound_content.append(self.histo3DUnbound.GetBinContent(x_bin, 15, 15))

        max_arr = np.array(slow_content) + np.array(fast_content) + np.array(unbound_content)
        self.data_movie_2 = max_arr / np.max(max_arr)

        v_average = (np.array(slow_content) * self.v_MEXp_slow + np.array(fast_content) * self.v_MEXp_fast + np.array(
            unbound_content) * self.v_plk1) / (np.array(slow_content) + np.array(fast_content) + np.array(
            unbound_content))

        conc_root_MEXp_slow = np.array(slow_content) / self.number
        conc_root_MEXp_fast = np.array(fast_content) / self.number
        conc_root_plk1_unbound = np.array(unbound_content) / self.number

        self.ax_id_conc_root = fig_id_ratio.add_subplot(2, 2, 3)
        self.ax_id_conc_root.plot(xbins_line, conc_root_MEXp_slow, 'r', label="PLK-1 to MEXps")
        self.ax_id_conc_root.plot(xbins_line, conc_root_MEXp_fast, 'b', label="PLK-1 to MEXpf")
        self.ax_id_conc_root.plot(xbins_line, conc_root_plk1_unbound, 'g', label="Unbound PLK-1")
        self.ax_id_conc_root.set_title("PLK-1 concentr.,  Central voxel")
        self.ax_id_conc_root.set_ylabel("Concentr. of PLK-1 species")
        self.ax_id_conc_root.set_xlabel("Embryo length (um)")
        self.ax_id_conc_root.legend(loc="upper right", frameon=False)

        self.av_velocity = fig_id_ratio.add_subplot(2, 2, 4)
        self.av_velocity.plot(xbins_line, v_average)
        self.av_velocity.set_title("Mean PLK-1 velocity, Central Voxel")
        self.av_velocity.set_ylabel("Mean velocity of PLK-1 species")
        self.av_velocity.set_xlabel("Embryo length (um)")

        fig_id_ratio.tight_layout()
        fig_id_ratio.canvas.draw()

        if self.counter % autosave == 0: 
            plt.imsave(os.path.join(self.path, f'Graphs/PLK-1-PlotB_t-{self.counter}.png'), np.array(fig_id_ratio.canvas.renderer.buffer_rgba()))  

        #plt.show(block=False)
        #plt.pause(0.1)

        del self.histo3DSlow
        del self.histo3DFast
        del self.histo3DUnbound

        return conc_root_MEXp_slow, conc_root_MEXp_fast, conc_root_plk1_unbound, v_average

    def FillDrawMovie(self):
        self.ims_movie1.append(self.data_movie_1)
        self.ims_movie2.append(self.data_movie_2)

    def DrawMovie(self):
        fig, ax = plt.subplots()
        container = []

        for i in range(len(self.ims_movie1)):
            container.append([plt.imshow(self.ims_movie1[i])])
        im_ani = animation.ArtistAnimation(fig, container, interval=50, blit=False)
        im_ani.save(os.path.join(self.path, '2DPlk1.html'), writer='imagemagick', fps=10, dpi=50)

        fig2, a2x = plt.subplots()
        container2 = []

        for i in range(len(self.ims_movie2)):
            plotty, = a2x.plot(self.ims_movie2[i], color='blue')
            container2.append([plotty])
        im_ani2 = animation.ArtistAnimation(fig2, container2, interval=50, blit=False)
        #mywriter = animation.FFMpegWriter(fps=10) to try
        im_ani2.save(os.path.join(self.path, 'GradientPlk1.html'), writer='imagemagick', fps=10, dpi=50)
        print(os.path.join(self.path, 'GradientPlk1.html'))

        #plt.show(block=False)

    def fit_func(self, x, a, b):
        return a * x + b
