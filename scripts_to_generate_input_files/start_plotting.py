from mass_balance_helper import calc_balance
from plotting_wb import read_and_convert, create_plot, calc_instant
import settings


mass_balance_check = input("Do you want to check mass balance of simulated data? (Y/N) \n").capitalize()
if mass_balance_check == "Y":
    calc_balance(settings.input_file_path_plots, settings.drain_spacing)

quit = False
while not quit:

    start = input("What time do you want to start your plot in month-day format?\n")
    end = input("What time do you want to end your plot in month-day format?\n")

    component = input("Which result would you like to plot? Press number:\n 0 - Total Water Balance, 6 - Snow-water equivalent, 7 - Ground water levels \n")

    df, precip_data, evap_data, discharge_to_open_ditch_data, drain_discharge_data, surface_runoff_data, snow_water_eq = read_and_convert(settings.input_file_path_plots, settings.year, settings.drain_spacing, start, end)

    precip_data_inst = calc_instant(precip_data, df["Date"])
    precip_data_inst_daily = precip_data_inst.resample('24H').sum()

    evap_data_inst = calc_instant(evap_data, df["Date"])
    evap_data_inst_daily = evap_data_inst.resample('24H').sum()

    discharge_to_open_ditch_data_inst = calc_instant(discharge_to_open_ditch_data, df["Date"])
    discharge_to_open_ditch_data_inst_daily = discharge_to_open_ditch_data_inst.resample('24H').sum()

    drain_discharge_data_inst = calc_instant(drain_discharge_data, df["Date"])
    drain_discharge_data_inst_daily = drain_discharge_data_inst.resample('24H').sum()

    surface_runoff_data_inst = calc_instant(surface_runoff_data, df["Date"])
    surface_runoff_data_inst_daily = surface_runoff_data_inst.resample('24H').sum()

    if component == "0":
        user_sel = input("Choose value: 1 - Cumulative, 2 - Instantaneous? \n")

        if user_sel == "1":
            create_plot(
                x = df['Date'],
                y_list = [precip_data, evap_data, discharge_to_open_ditch_data, drain_discharge_data, surface_runoff_data],
                label_list = ['Precipitation(oPrecSi)', 'Evapotranspiration(oEvap, sEtM, sEtF)', 'Open ditch(sDit_0,sDit_1)', 'Drains(sDra_0,sDra_1)', 'Surface runoff(oDit_0)'],
                save_name =settings.plots_folder + "total_wb_cumul",
                title = f"Water Balance Components, {settings.location}, {settings.year}, {settings.drain_spacing}"
            )

        elif user_sel == "2":

            create_plot(
                x = precip_data_inst_daily.index,
                y_list = [precip_data_inst_daily[0], evap_data_inst_daily[0], discharge_to_open_ditch_data_inst_daily[0], drain_discharge_data_inst_daily[0], surface_runoff_data_inst_daily[0]],
                label_list = ['Precipitation(oPrecSi)', 'Evapotranspiration(oEvap, sEtM, sEtF)', 'Open ditch(sDit_0,sDit_1)', 'Drains(sDra_0,sDra_1)', 'Surface runoff(oDit_0)'],
                save_name =settings.plots_folder + "total_wb_instant",
                title = f"Water Balance Components, {settings.location}, {settings.year}, {settings.drain_spacing} ",
                yaxis_title = "Instantaneous [mm]",
            )

    else:
        if component == "6":
            create_plot(
                x = df['Date'],
                y_list = [snow_water_eq],
                label_list = ["Snow water equivalent(oSnWaVo)"],
                yaxis_title = "Snow Water Equivalent [mm]",
                save_name =settings.plots_folder + "swe",
                title = f"Snow Water Equivalent, {settings.location}, {settings.year}"
            )

        elif component == "7":
            create_plot(
                x = df['Date'],
                y_list = [-df['sGw_1'], -df['sGw_0']],
                label_list = ["Groundwater level - macropores", "Groundwater level - soil matrix"],
                yaxis_title = "Depth [m]",
                save_name =settings.plots_folder + "ground_water_levels",
                title = f"Groundwater levels, {settings.location}, {settings.year}, {settings.drain_spacing}"
            )

        else:
            print("Error in selection has occurred! Please check your inputs.")


    user_quit = input("If you want to quit the program now press Q: \n").capitalize()
    if user_quit == "Q":
        quit = True



