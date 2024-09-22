#!/usr/bin/python
import sys, getopt
import numpy as np

from scipy import optimize
import os
import matplotlib.pyplot as plt

import module_2Dplotter as plotter2D
import module_2Dplotter_PLK1 as plotter2DPLK1
from datetime import datetime


class eloG:
    def __init__(self, filename):
        self.log_open(filename)
        self.name = filename

    def log_open(self, name):
        self.file = open(name, "w+")

    def log_open_append(self):
        self.file = open(self.name, "a+")

    def writeLine(self, string):
        self.file.write(string)
        self.file.write("\n")

    def writeListRow(self, lista):
        for item in lista:
            self.file.write(str(item))
            self.file.write("\t")
        self.file.write("\n")

    def writeListCol(self, lista):
        for item in lista:
            self.file.write(str(item))
            self.file.write("\n")

    def closeFile(self):
        self.file.close()


# Start here
def main(argv):
    print("Starting...")

    # define vel and k param
    v_MEXp_fast = 0.0
    v_MEXp_slow = 0.0
    v_plk1 = 0.0
    plk1_to_MEXp = 0.0

    if not os.path.exists("logs"):
        os.makedirs("logs")

    now = datetime.now()
    date_time = now.strftime("%d_%m_%Y_%H_%M_%S")
    print("Start time: ", date_time)

    if not os.path.exists("logs/" + date_time):
        os.makedirs("logs/" + date_time)

    file_log_name = "logs/" + date_time + "/summary_parameter.txt"
    file_log_name_k_plk1 = "logs/" + date_time + "/log_k_plk1.txt"
    file_log_name_k_MEXp = "logs/" + date_time + "/log_k_MEXp.txt"
    file_log_name_profile_MEXp = "logs/" + date_time + "/log_profileAP_MEXp.txt"
    file_log_name_profile_plk1 = "logs/" + date_time + "/log_profileAP_plk1.txt"
    file_log_name_MEXp_ratio_slow_fast = (
        "logs/" + date_time + "/log_MEXp_ratio_slow_fast.txt"
    )
    file_log_v_MEXp = "logs/" + date_time + "/log_v_MEXp.txt"
    file_log_v_plk1 = "logs/" + date_time + "/log_v_plk1.txt"
    file_log_conc_id0_MEXp = "logs/" + date_time + "/conc_id0_MEXp.txt"
    file_log_conc_id1_MEXp = "logs/" + date_time + "/conc_id1_MEXp.txt"

    file_log_conc_id0_plk1 = "logs/" + date_time + "/conc_id0_plk1.txt"
    file_log_conc_id1_plk1 = "logs/" + date_time + "/conc_id1_plk1.txt"
    file_log_conc_id2_plk1 = "logs/" + date_time + "/conc_id2_plk1.txt"

    log = eloG(file_log_name)

    #  plt.ion()
    particles = 0
    particles_list = []
    particles_list_plk1 = []
    settings = ""
    multi = False
    bound = False
    plk1 = False
    threeD = False
    sliced = True
    drawMovie = False

    slice_depth = 0.0
    initial_slow = 0.0
    initial_fast = 0.0
    k_fast_slow = 0.1
    k_slow_fast_low = 0.02
    k_slow_fast_high = 0.11

    k_plk1_attach_to_free = 0.0
    plk1_attach_to_mex_fast = 0
    plk1_attach_to_mex_slow = 1
    plk1_to_mex_multiplicator = 1
    plk1_detached_when_MEXp_changes = 0

    plk1_delay_start_time = 0.0
    plk1_delay_end_time = 100.0

    try:
        opts, args = getopt.getopt(
            argv,
            "hp:bfmds:",
            [
                "particles=",
                "bound",
                "plk1",
                "threeD",
                "slice",
                "drawMovie",
                "settings=",
            ],
        )
    except getopt.GetoptError:
        print("test.py -p <particles>")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print("test.py -p <particles> ")
            sys.exit()
        elif opt in ("-p", "--particles"):
            particles = int(arg)
        elif opt in ("-b", "--bound"):
            bound = True
        elif opt in ("--plk1"):
            plk1 = True
        elif opt in ("--threeD"):
            threeD = True
        elif opt in ("--drawMovie"):
            drawMovie = True
        elif opt in ("s", "--settings"):
            settings = str(arg)
        elif opt in ("f", "--slice"):
            sliced = True

    multi = True
    assert settings != "", "A settings file is needed!"
    if sliced == True:
        assert threeD == True, "Impossible to use slice option without threeD set"

    f_sett = open(settings)
    lines = f_sett.readlines()
    temp_sett = []
    assert len(lines) == 17, "10 lines are expected"
    for line in lines:
        temp_sett.append(float(line.replace("\n", "").split("\t")[1]))
    f_sett.close()
    print(temp_sett)
    v_MEXp_fast = temp_sett[0]
    v_MEXp_slow = temp_sett[1]
    v_plk1 = temp_sett[2]
    plk1_to_MEXp = temp_sett[3]
    slice_depth = temp_sett[4]
    initial_slow = temp_sett[5]
    initial_fast = temp_sett[6]
    k_fast_slow = temp_sett[7]
    k_slow_fast_low = temp_sett[8]
    k_slow_fast_high = temp_sett[9]

    k_plk1_attach_to_free = temp_sett[10]
    plk1_attach_to_mex_slow = temp_sett[11]
    plk1_attach_to_mex_fast = temp_sett[12]
    plk1_to_mex_multiplicator = temp_sett[13]
    plk1_detached_when_MEXp_changes = temp_sett[14]

    plk1_delay_start_time = temp_sett[15]
    plk1_delay_end_time = temp_sett[16]

    assert (
        v_MEXp_fast != 0.0
        and v_MEXp_slow != 0.0
        and v_plk1 != 0.0
        and plk1_to_MEXp != 0.0
    ), "something went wrong in reading the setting file"

    log.writeLine("Starting simulation ")
    log.writeLine("N. particles " + str(particles))
    log.writeLine("bound " + str(bound))
    log.writeLine("plk1 " + str(plk1))
    log.writeLine("threeD " + str(threeD))
    log.writeLine("slice " + str(sliced))
    log.writeLine("sliceDepth " + str(slice_depth))
    log.writeLine("setting file " + str(settings))
    log.writeLine("setting file " + str(settings))
    log.writeLine("v fast MEXp " + str(v_MEXp_fast))
    log.writeLine("v slow MEXp " + str(v_MEXp_slow))
    log.writeLine("v plk1 " + str(v_plk1))
    log.writeLine("plk1_to_MEXp " + str(plk1_to_MEXp))
    log.writeLine("initial_slow " + str(initial_slow))
    log.writeLine("initial_fast " + str(initial_fast))
    log.writeLine("k_fast_slow " + str(k_fast_slow))
    log.writeLine("k_slow_fast_low " + str(k_slow_fast_low))
    log.writeLine("k_slow_fast_high " + str(k_slow_fast_high))
    log.writeLine("k_plk1_attach_to_free " + str(k_plk1_attach_to_free))
    log.writeLine("plk1_attach_to_mex_fast " + str(plk1_attach_to_mex_fast))
    log.writeLine("plk1_attach_to_mex_slow " + str(plk1_attach_to_mex_slow))
    log.writeLine("plk1_to_mex_multiplicator " + str(plk1_to_mex_multiplicator))
    log.writeLine(
        "plk1_detached_when_MEXp_changes " + str(plk1_detached_when_MEXp_changes)
    )

    log.writeLine("plk1_delay_start_time " + str(plk1_delay_start_time))
    log.writeLine("plk1_delay_end_time " + str(plk1_delay_end_time))

    log.writeLine("log k MEXp " + str(file_log_name_k_MEXp))
    log.writeLine("log k plk1 " + str(file_log_name_k_plk1))
    log.writeLine("log profile MEXp " + str(file_log_name_profile_MEXp))
    log.writeLine("log profile plk1 " + str(file_log_name_profile_plk1))
    log.writeLine(
        "log profile ratio slow/fast " + str(file_log_name_MEXp_ratio_slow_fast)
    )

    log.writeLine("log v MEXp " + str(file_log_v_MEXp))
    log.writeLine("log v plk1 " + str(file_log_v_plk1))

    log.writeLine("log conc id0 MEXp " + str(file_log_conc_id0_MEXp))
    log.writeLine("log conc id1 MEXp " + str(file_log_conc_id1_MEXp))
    log.writeLine("log conc id0 plk1 " + str(file_log_conc_id0_plk1))
    log.writeLine("log conc id1 plk1 " + str(file_log_conc_id1_plk1))
    log.writeLine("log conc id2 plk1" + str(file_log_conc_id2_plk1))

    log.closeFile()
    limits_particle = []
    limits = [[0, 0], [50, 30]]
    limits2 = [[0, 0], [50, 30]]
    limits3 = [[0, 50], [0, 50]]
    limits3D = [[0, 0, 0], [50, 30, 30]]
    if threeD:
        import particle3D_manager as pm
        import particle3D_managerPLK1 as pm_plk1

        limits_particle = [0, 0, 0, 50, 30, 30]

    else:
        import module_particle as particle_m
        import module_particle_plk1 as particle_plk1_m

        limits_particle = limits2

    log_k_MEXp = eloG(file_log_name_k_MEXp)
    log_profile_MEXp = eloG(file_log_name_profile_MEXp)
    log_MEXp_ratio_slow_fast = eloG(file_log_name_MEXp_ratio_slow_fast)
    log_v_MEXp = eloG(file_log_v_MEXp)
    log_conc_id0_MEXp = eloG(file_log_conc_id0_MEXp)
    log_conc_id1_MEXp = eloG(file_log_conc_id1_MEXp)

    log_k_MEXp.closeFile()
    log_profile_MEXp.closeFile()
    log_MEXp_ratio_slow_fast.closeFile()
    log_v_MEXp.closeFile()
    log_conc_id0_MEXp.closeFile()
    log_conc_id1_MEXp.closeFile()

    if plk1:
        log_profile_plk1 = eloG(file_log_name_profile_plk1)
        log_k_plk1 = eloG(file_log_name_k_plk1)
        log_v_plk1 = eloG(file_log_v_plk1)
        log_conc_id0_plk1 = eloG(file_log_conc_id0_plk1)
        log_conc_id1_plk1 = eloG(file_log_conc_id1_plk1)
        log_conc_id2_plk1 = eloG(file_log_conc_id2_plk1)

        log_profile_plk1.closeFile()
        log_k_plk1.closeFile()
        log_v_plk1.closeFile()
        log_conc_id0_plk1.closeFile()
        log_conc_id1_plk1.closeFile()
        log_conc_id2_plk1.closeFile()

    # Fill the particle list
    particle_family = pm.particle3D_manager(particles)

    if plk1:
        particle_family_plk1 = pm_plk1.particle3D_managerPLK1(particles)

    particle_family.SetSettings(
        initial_slow, initial_fast, k_fast_slow, k_slow_fast_low, k_slow_fast_high
    )

    particle_family.Shuffle(limits_particle)

    if plk1:
        particle_family_plk1.SetSettings(
            plk1_attach_to_mex_slow,
            plk1_attach_to_mex_fast,
            k_plk1_attach_to_free,
            plk1_detached_when_MEXp_changes,
            plk1_delay_start_time,
            plk1_delay_end_time,
        )
        particle_family_plk1.Shuffle(limits_particle)
        particle_family_plk1.MEXpSetSettings(
            k_fast_slow, k_slow_fast_low, k_slow_fast_high
        )

    plots = plotter2D.Plot2D(
        particles, limits3, limits, v_MEXp_slow, v_MEXp_fast, "logs/" + date_time
    )

    if plk1:
        plots_plk1 = plotter2DPLK1.Plot2D(
            particles,
            limits3,
            limits,
            plk1_to_mex_multiplicator,
            v_plk1,
            v_MEXp_slow,
            v_MEXp_fast,
            "logs/" + date_time,
        )

    # Get info from cpp libraries
    X_list = list(particle_family.GetXpos())
    Y_list = list(particle_family.GetYpos())
    Z_list = list(particle_family.GetZpos())

    plots.UpdateCpp(X_list, Y_list, Z_list, sliced, slice_depth)

    if plk1:
        X_list = list(particle_family.GetXpos())
        Y_list = list(particle_family.GetYpos())
        Z_list = list(particle_family.GetZpos())
        plots_plk1.UpdateCpp(X_list, Y_list, Z_list, sliced, slice_depth)

    for i in range(0, 1500):
        print("starting evt" + str(datetime.now().time()))  # time object

        particle_family.Move(v_MEXp_slow, v_MEXp_fast, 1, limits_particle, bound, i)

        X_list = list(particle_family.GetXpos())
        Y_list = list(particle_family.GetYpos())
        Z_list = list(particle_family.GetZpos())
        ID_list = list(particle_family.GetID())
        ratio, concid0, concid1, vel = plots.conc_calcCpp(
            X_list, Y_list, Z_list, ID_list
        )

        concid0 = (np.array(concid0) * plk1_to_mex_multiplicator).tolist()
        concid1 = (np.array(concid1) * plk1_to_mex_multiplicator).tolist()

        if plk1:
            particle_family_plk1.Move(
                v_plk1,
                v_MEXp_slow,
                v_MEXp_fast,
                1,
                ratio,
                concid0,
                concid1,
                limits_particle,
                bound,
                i,
            )

            # it is defined as follow: v standard, v_fast, v_slow, k_probability, dt, limits, nobound

            X_list_plk1 = list(particle_family_plk1.GetXpos())
            Y_list_plk1 = list(particle_family_plk1.GetYpos())
            Z_list_plk1 = list(particle_family_plk1.GetZpos())

            ID_list_plk1 = list(particle_family_plk1.GetID())
            conc1, conc2, conc3, v_plk1_average = plots_plk1.conc_calcCpp(
                X_list_plk1, Y_list_plk1, Z_list_plk1, ID_list_plk1
            )

        if i != 0 and i % 10 == 0:
            X_list = list(particle_family.GetXpos())
            Y_list = list(particle_family.GetYpos())
            Z_list = list(particle_family.GetZpos())
            plots.UpdateCpp(X_list, Y_list, Z_list, sliced, slice_depth)

            if drawMovie:
                plots.FillDrawMovie()

            log_k_MEXp.log_open_append()
            log_profile_MEXp.log_open_append()
            log_MEXp_ratio_slow_fast.log_open_append()
            log_v_MEXp.log_open_append()
            log_conc_id0_MEXp.log_open_append()
            log_conc_id1_MEXp.log_open_append()

            log_k_MEXp.writeLine(str(plots.klast))
            log_profile_MEXp.writeListRow(plots.profilelast)
            log_MEXp_ratio_slow_fast.writeListRow(ratio)
            log_v_MEXp.writeListRow(vel)

            log_conc_id0_MEXp.writeListRow(concid0)
            log_conc_id1_MEXp.writeListRow(concid1)

            log_k_MEXp.closeFile()
            log_profile_MEXp.closeFile()
            log_MEXp_ratio_slow_fast.closeFile()
            log_v_MEXp.closeFile()

            log_conc_id0_MEXp.closeFile()
            log_conc_id1_MEXp.closeFile()

            if plk1:
                log_k_plk1.log_open_append()
                log_profile_plk1.log_open_append()
                log_v_plk1.log_open_append()
                log_conc_id0_plk1.log_open_append()
                log_conc_id1_plk1.log_open_append()
                log_conc_id2_plk1.log_open_append()

                plots_plk1.UpdateCpp(
                    X_list_plk1, Y_list_plk1, Z_list_plk1, sliced, slice_depth
                )

                log_conc_id0_plk1.writeListRow(conc3)
                log_conc_id1_plk1.writeListRow(conc1)
                log_conc_id2_plk1.writeListRow(conc2)

                log_k_plk1.writeLine(str(plots_plk1.klast))
                log_profile_plk1.writeListRow(plots_plk1.profilelast)
                log_v_plk1.writeListRow(v_plk1_average)

                log_k_plk1.closeFile()
                log_profile_plk1.closeFile()
                log_v_plk1.closeFile()

                log_conc_id0_plk1.closeFile()
                log_conc_id1_plk1.closeFile()
                log_conc_id2_plk1.closeFile()

                if drawMovie:
                    plots_plk1.FillDrawMovie()

    if drawMovie:
        plots.DrawMovie()
        if plk1:
            plots_plk1.DrawMovie()

    end_time = datetime.now()
    end_date_time = end_time.strftime("%d_%m_%Y_%H_%M_%S")
    print("Ending time: ", end_date_time)
    print("Finished!")


if __name__ == "__main__":
    main(sys.argv[1:])
