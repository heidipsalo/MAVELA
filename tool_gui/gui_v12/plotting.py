from plotting_helper import read_and_convert, create_plot, calc_instant


class PlotResults():
    def __init__(self, settings):

        df, precip_data, evap_data, discharge_to_open_ditch_data, drain_discharge_data, surface_runoff_data, snow_water_eq = read_and_convert(settings.flush_results_file, settings.year, settings.drain_spacing)

        if settings.plot == 0 and settings.plot_type == 0:
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

            create_plot(
                x = precip_data_inst_daily.index,
                y_list = [precip_data_inst_daily[0], evap_data_inst_daily[0], discharge_to_open_ditch_data_inst_daily[0], drain_discharge_data_inst_daily[0], surface_runoff_data_inst_daily[0]],
                label_list = ['Precipitation(oPrecSi)', 'Evapotranspiration(oEvap, sEtM, sEtF)', 'Open ditch(sDit_0,sDit_1)', 'Drains(sDra_0,sDra_1)', 'Surface runoff(oDit_0)'],
                save_name = settings.plots_folder + "total_wb_instant",
                title = f"Water Balance Components, {settings.location_name}, {settings.year}, {settings.drain_spacing} ",
                yaxis_title = "Instantaneous [mm]",
            )

        if settings.plot == 0 and settings.plot_type == 1:
            create_plot(
                x = df['Date'],
                y_list = [precip_data, evap_data, discharge_to_open_ditch_data, drain_discharge_data, surface_runoff_data],
                label_list = ['Precipitation(oPrecSi)', 'Evapotranspiration(oEvap, sEtM, sEtF)', 'Open ditch(sDit_0,sDit_1)', 'Drains(sDra_0,sDra_1)', 'Surface runoff(oDit_0)'],
                save_name = settings.plots_folder + "total_wb_cumul",
                title = f"Water Balance Components, {settings.location_name}, {settings.year}, {settings.drain_spacing}"
            )

        if settings.plot == 1:
            create_plot(
                x = df['Date'],
                y_list = [-df['sGw_1'], -df['sGw_0']],
                label_list = ["Ground water level - macropores", "Ground water level - soil matrix"],
                yaxis_title = "Depth [m]",
                save_name = settings.plots_folder + "ground_water_levels",
                title = f"Ground Water levels, {settings.location_name}, {settings.year}, {settings.drain_spacing}"
            )

        if settings.plot == 2:
            create_plot(
                x = df['Date'],
                y_list = [snow_water_eq],
                label_list = ["Snow water equivalent(oSnWaVo)"],
                yaxis_title = "Snow Water Equivalent [mm]",
                save_name = settings.plots_folder + "swe",
                title = f"Snow Water Equivalent, {settings.location_name}, {settings.year}"
            )

        else:
            print("Error in selection has occurred! Please check your inputs.")





