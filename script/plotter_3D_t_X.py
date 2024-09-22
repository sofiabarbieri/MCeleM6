#!/usr/bin/python
import sys, getopt
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, ticker
from scipy import optimize


def main(argv):
   inputfile = ''
   outputfile = ''
   data_profile = []
 
	
## LEGGERE FILES  
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print('test.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('test.py -i <inputfile> -o <outputfile>') 
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   print('Input file is "', inputfile)
   print('Output file is "', outputfile) 
   
   lines = [line.rstrip('\n') for line in open(inputfile)]
   vec_lines = [line.split('\t') for line in lines]
   
   

   matrix = np.array(vec_lines)
   matrix = np.delete(matrix, matrix.shape[1]-1, axis=1)
   matrix = np.asfarray(matrix,float)
   print(matrix[0])
   
   x = np.arange(len(matrix[0]))
   t = np.arange(matrix.shape[0])

   print(matrix.shape)
   print(x)
   print(t)
   
# PLOTS
   
   palette = plt.get_cmap('hsv')
   
  

   # Using set_dashes() to modify dashing of an existing line
#   line1, = ax.plot(x, vec_lines[0], label='Using set_dashes()')
   # Using plot(..., dashes=...) to set the dashing when creating a line
   # multiple line plot
   f = plt.figure(1)
   
   num=0
   for rows in range(0,matrix.shape[0]):
     num+=1
     plt.plot(x, matrix[rows,:], marker='', color=palette(num), linewidth=1, alpha=0.9, label=rows)
   #plt.legend(loc=2, ncol=2)   
   plt.xlabel('Embrio length ($\mathregular{\mu m}$)')
   plt.ylabel('velocity ($\mathregular{\mu}$m/s)')
   plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
   # ax.legend()
   f.show()
   
   num=0
   
   g = plt.figure(2)
   for columns in range(0,matrix.shape[1]):
     num+=1
     print(columns)
     print(matrix[:,0])
     #print matrix[:][columns]
     plt.plot(t, matrix[:,columns], marker='', color=palette(num), linewidth=1, alpha=0.9, label=columns)
   plt.xlabel('Embrio length ($\mathregular{\mu m}$)')
   plt.ylabel('velocity ($\mathregular{\mu}$m/s)')
   plt.ticklabel_format(axis="y", style="sci", scilimits=(0,0))
   g.show()
   ff = matrix.mean(1)

  
   #params, params_covariance = optimize.curve_fit(fit_func, t, ff, bounds=((-np.inf, -np.inf, 0), (np.inf,np.inf,np.inf)))
   #print params
   
   
  
   
   X_, Y_ = np.meshgrid(x, t)

   fig = plt.figure(3)
   ax = fig.gca(projection='3d')
   surf = ax.plot_surface(Y_, X_, matrix, cmap=cm.RdYlBu,
                       linewidth=0, antialiased=False)
   ax.set_zticks([])
   ax.set_xlabel('Time (frames)', fontsize=10, labelpad=10)
   ax.tick_params(axis='both', which='major', labelsize=10)
   ax.tick_params(axis='both', which='major', pad=5)
   ax.set_ylabel('Embryo length ($\mathregular{\mu m}$)', fontsize=10., labelpad=15)

   #surf.xlabel('t(s)',fontsize=16)
   #surf.ylabel('x',fontsize=16)
   
   fmt = ticker.ScalarFormatter(useMathText=True)
   fmt.set_powerlimits((0, 0))
   
   cbar = fig.colorbar(surf, shrink=0.5, aspect=5, format=fmt)
   cbar.ax.yaxis.get_offset_text().set(size=10)
   cbar.set_label('Concentration ($\mathregular{voxel^{-1}})$', rotation=270, fontsize=10., labelpad=15)

   cbar.ax.tick_params(labelsize=10) 
   fig.show()
   plt.show()
if __name__ == "__main__":
   main(sys.argv[1:])
