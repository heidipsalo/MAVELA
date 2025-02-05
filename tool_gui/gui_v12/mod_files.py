from gridded_data import calc_swe


class ModFiles():
    def __init__(self, settings):
        # Create st_modnwsurfwater_01.txt
        content_surf_water = """00\t-\t# Settings for the ditch network model
01\t0\t# Model active (1=ON, 0=OFF)
02\t100\t# Maximum number of iterations [-]
03\t1.0E-08\t# Bisection, threshold depth (epsilon) [m]
04\t5.0\t# Bisection, max. water depth change [m]
05\t100\t# Bisection, max iterations [-]
06\t1.0E-05\t# Iteration stop pressure threshold [m]
07\t1.0\t# Implicity value [-] (DISABLED)
08\t0.0\t# Initial overland water depth [m]"""

        file_name = "st_modnwsurfwater_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_surf_water)

        # Create st_modsubcrack_01.txt
        content_sub_crack = """00\t-\t# Settings for the subsurface crack model
01\t0\t# Model active (1=ON, 0=OFF)"""

        file_name = "st_modsubcrack_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_sub_crack)

        # Create st_modsubheat_01.txt
        content_sub_heat = """00\t-\t# Settings for the subsurface heat transport model
01\t1\t# Model active (1=ON, 0=OFF)
02\t0.0001\t# Iteration stop temperature threshold [oC]
03\t100\t# Maximum number of iterations [-]
04\t1.0\t# Implicity value [-] (DISABLED)
05\t0.0001\t# Bisection, iteration threshold [oC]
06\t100\t# Bisection, max. number of iterations [-]
07\t-50.0\t# Bisection, left temperature limit [oC]
08\t50.0\t# Bisection, right temperature limit [oC]
09\t333.7\t# Latent heat of fusion [kJ kg-1]
10\t0.5\t# Freezing temperature [oC]
11\t1.5\t# Multiplier of the freezing curve [?] FIX THIS!
12\t1.25\t# Density of air [kg m-3]
13\t917.0\t# Density of ice [kg m-3]
14\t1000.0\t# Density of water [kg m-3]
15\t1.005\t# Heat capacity of air (Specific Heat of Moist Air) 1.013 [kJ kg-1 oC-1]
16\t2.09\t# Heat capacity of ice [kJ kg-1 oC-1]
17\t4.18\t# Heat capacity of water [kJ kg-1 oC-1]
18\t0.09\t# Conductivity of Air [kj h-1 m-1 oC-1]
19\t7.92\t# Conductivity of Ice [kj h-1 m-1 oC-1]
20\t2.052\t# Conductivity of Water [kj h-1 m-1 oC-1]
21\t1.0\t# Conductivity multiplier of air [-]
22\t1.0\t# Conductivity multiplier of ice [-]
23\t1.0\t# Conductivity multiplier of water [-]
24\t2.0\t# Soil initial temperature [oC]"""

        file_name = "st_modsubheat_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_sub_heat)

        # Create st_modsubsedim_01.txt
        content_sub_sedim = """00\t-\t# Settings for the subsurface sediment transport model
01\t0\t# Model active (1=ON, 0=OFF)
02\t1.0E-07\t# Iteration stop concentration change threshold [kg m-3]
03\t100\t# Maximum number of iterations [-]
04\t1.0\t# Implicity value [-] (disabled)
05\t1.0\t# Sediment transport depth [m]
06\t0.0\t# Initial sediment concentration [kg m-3]"""

        file_name = "st_modsubsedim_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_sub_sedim)

        # Create st_modsubsolute_01.txt
        content_sub_solut = """00\t-\t#Settings for the solute transport model
01\t0\t# Model active (1=ON, 0=OFF)
02\t1.0E-09\t# Iteration stop pressure threshold [kg m-3]
03\t200\t# Maximum number of iterations [-]
04\t1.0\t# Implicity value [-] (DISABLED)"""

        file_name = "st_modsubsolute_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_sub_solut)

        # Create st_modsubwaterbrute_01.txt
        content_sub_wat_brute = """00\t-\t# Settings for the subsurface water flow model
01\t0\t# Model active (1=ON, 0=OFF)
02\t100\t# Maximum number of iterations [-]
03\t1.0E-05\t# Iteration stop pressure threshold [m]
04\t1.0\t# Implicity value [-]
05\t-0.1\t# Evapotranspiration limit head, max. [m]
06\t-5.0\t# Evapotranspiration limit head, min. [m]
07\t-150.0\t# Evapotranspiration limit head, Wilting point [m]
08\t1.0101\t# Initial ground water depth from surface [m] (1.4)"""

        file_name = "st_modsubwaterbrute_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_sub_wat_brute)

        # Create st_modsubwaterpenta_01.txt
        content_mod_sub_wate_penta = """00\t-\t# Settings for the subsurface water flow model
01\t1\t# Model active (1=ON, 0=OFF)
02\t100\t# Maximum number of iterations [-]
03\t1.0E-05\t# Iteration stop pressure threshold [m]
04\t1.0\t# Implicity value [-] (DISABLED)
05\t-0.1\t# Evapotranspiration limit head, max. [m]
06\t-5.0\t# Evapotranspiration limit head, min. [m]
07\t-150.0\t# Evapotranspiration limit head, Wilting point [m]
08\t1.0\t# Initial ground water depth from surface [m] ()"""

        file_name = "st_modsubwaterpenta_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_mod_sub_wate_penta)

        # Create st_modsurfatmos_01.txt
        content_mod_surf_atm = f"""00\t-\t# Settings for the overland atmospheric model
01\t1\t# Model active (1=ON, 0=OFF)
02\t0.01\t# Iteration convergence threshold [oC]
03\t100\t# Maximum number of iterations [-]
04\t0.5\t# Implicity value [-] (DISABLED)
05\t-\t# Parameters
06\t0.85\t# Max albedo [-] (0.85-0.95)
07\t0.2\t# Min albedo [-] (0.2-0.3)
08\t0.002\t# Snow albedo parameter, precipitation limit [mm]
09\t2.0\t# Snow albedo parameter, time limit [h]
10\t1.0\t# Atmospheric stability weighing factor [-]
11\t10.0\t# Saturated hydraulic conductivity of wet snow [m h-1]
12\t0.0756\t# Snow thermal conductivity parameter [kJ h-1 m-1 oC-1] (0.0756)
13\t9.036\t# Snow thermal conductivity parameter [kJ h-1 m-1 oC-1] (9.036)
14\t0.0\t# Windless convection coefficient for latent heat flux [kJ m-2 h-1 Pa-1]
15\t7.2\t# Windless convection coefficient for sensible heat flux [kJ m-2 h-1 oC-1] (7.2)
16\t0.15\t# Density limit multiplier of snow (0.15 [g cm-3]) FIX THIS!
17\t500.0\t# Maximum density of snow [kg m-3]
18\t0.007\t# Snow surface roughness height [m] (0.003-0.005-0.007)
19\t0.99\t# Emissivity of snow [-]
20\t2.0\t# Reference height of measured temperature and relative humidity [m]
21\t2.0\t# Reference height of measured wind [m]
22\t0.16\t# Maximum limit of the estimated Richardson number [-]
23\t-10.0\t# Minimum limit of the estimated Richardson number [-]
24\t0.02\t# Maximum snow water equivalent of the upper snow layer [m]
25\t0.05\t# Liquid water holding capacity of snow [m3 m-3] (0.05-0.1)
26\t0.069\t# Snow metamorphism parameters C1 (0.01 -- 0.069 [cm-1 h-1])
27\t21.0\t# Snow metamorphism parameters C2 (cm3 g-1)
28\t0.01\t# Snow metamorphism parameters C3 (h-1)
29\t0.04\t# Snow metamorphism parameters C4 [K-1]
30\t2.0\t# Snow metamorphism parameters C5 [?] FIX THIS!
31\t0.0\t# Snow metamorphism parameters Tc [oC]
32\t5.0\t# Maximum temperature change of snow in an iteration round [oC]
33\t0.0\t# Snowfall/mixed-rain-snow temperature lower limit [oC]
34\t2.0\t# Snowfall/mixed-rain-snow temperature upper limit [oC]
35\t101.3\t# Base air pressure [kPa]
36\t10.0\t# Mean elevation of the area [m]
37\t1.1\t# Correction factors for rainfall [-]
38\t1.2\t# Correction factors for snowfall [-]
39\t150.0\t# Initial snow density [kg m-3]
40\t{calc_swe(settings)}\t# Initial snow water equivalent [m] (0.03)
41\t-150.0\t# Initial snow energy [kJ]
42\t-\t# Constants
43\t2.04E-7\t# Stefan-Boltzmann constant [kJ m-2 h oK-4]
44\t917.0\t# Density of ice [kg m-3]
45\t1000.0\t# Density of water [kg m-3]
46\t9.81\t# Acceleration of gravity [m s-2]
47\t1.005\t# Heat capacity of air  (Specific Heat of Moist Air) 1.013 [kJ kg-1 oC-1]
48\t2.09\t# Heat capacity of ice [kJ kg-1 oC-1]
49\t4.18\t# Heat capacity of water [kJ kg-1 oC-1]
50\t287.0\t# Ideal gas constant for dry air [J kg- 1 K-1]
51\t333.7\t# Latent heat of fusion [kJ kg-1]
52\t2834.0\t# Latent heat of sublimation [kJ kg-1]
53\t273.15\t# Degrees Kelvin at freezing point [oK]
54\t0.41\t# Von Karman constant"""

        file_name = "st_modsurfatmos_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_mod_surf_atm)

        # Create st_modsurfsedim_01.txt
        content_mod_surf_sed = """00\t-\t# Settings for the overland erosion model
01\t0\t# Model active (1=ON, 0=OFF)
02\t1.0E-10\t# Iteration stop concentration change threshold [kg m-3]
03\t100\t# Maximum number of iterations [-]
04\t1.0\t# Implicity value [-] (DISABLED)
05\t1000.0\t# Density of water [kg m-3]
06\t2650.0\t# Density of sediment [kg m-3]
07\t9.81\t# Gravitational accelaration [m s-2]
08\t1.0E-06\t# Kinematic viscosity [kg s-1 m-1]
09\t1.5E-06\t# Particle mean diameter [m]
10\t1.0E-07\t# Particle settling velocity [m s-1]
11\t5.0\t# Minimum sediment transport capacity [kg m-3]
12\t0.0\t# Initial overland sediment mass [kg m-2]"""

        file_name = "st_modsurfsedim_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_mod_surf_sed)

        # Create st_modsurfsolute_01.txt
        content_mod_surf_sol = """00\t-\t# Settings for the overland erosion model
01\t0\t# Model active (1=ON, 0=OFF)
02\t1.0E-10\t# Iteration stop concentration change threshold [kg m-3]
03\t100\t# Maximum number of iterations [-]
04\t1.0\t# Implicity value [-] (DISABLED)
05\t0.0\t# Initial overland solute mass [kg m-2]"""

        file_name = "st_modsurfsolute_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_mod_surf_sol)

        # Create st_modsurfwater_01.txt
        content_mod_surf_wat = """00\t-\t# Settings for the overland flow model
01\t1\t# Model active (1=ON, 0=OFF)
02\t100\t# Maximum number of iterations [-]
03\t1.0E-08\t# Bisection, threshold depth (epsilon) [m]
04\t5.0\t# Bisection, max. water depth change [m] (5.0)
05\t100\t# Bisection, max. number of iterations [-]
06\t1.0E-05\t# Iteration stop pressure threshold [m]
07\t1.0\t# Implicity value [-] (DISABLED)
08\t0.0\t# Initial overland water depth [m]"""

        file_name = "st_modsurfwater_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_mod_surf_wat)

        # Create dt_solutes_01.txt
        content_solutes = """ \tSolute\tAds.P.0\tAds.P.1\tAds.P.2\tMobile\tDec.r.0\tDec.t.0\tDec.r.1\tDec.t.1
0\tNitr.\t-1\t0\t1.0\t1\t0\t-1\t0\t-1
0\tNitr.\t-1\t0\t1.0\t1\t0\t-1\t0\t-1
0\tNitr.\t-1\t0\t1.0\t1\t0\t-1\t0\t-1"""

        file_name = "dt_solutes_01.txt"
        file_path = f"{settings.input_folder}/{file_name}"
        with open(file_path, 'w') as file:
            file.write(content_solutes)
