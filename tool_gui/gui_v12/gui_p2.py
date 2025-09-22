import customtkinter
import tkinter


class ScrollableFrame2(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.customize_soils = False
        self.custom_soils_frame = None
        self.available_soils_frame = None

        if master.settings.use_report == 'Yes' and master.settings.is_custom_soils:
            self.seg_button_1 = customtkinter.CTkSegmentedButton(self, values=['Customize soils'], command=self.callback_custom_soils)
            self.seg_button_1.grid(row=0, column=0, padx=5, pady=(5,0), sticky="we")
            self.seg_button_1.set('Customize soils')
            self.custom_soils_frame = CustomSoilsFrame(self)
            self.custom_soils_frame.grid(row=1, column=0, sticky='nswe', columnspan=1)
            self.available_soils_frame = AvalableSoilsFrame(self)
        else:
            self.seg_button_1 = customtkinter.CTkSegmentedButton(self, values=['Use available soil libraries', 'Customize soils'], command=self.callback_custom_soils)
            self.seg_button_1.grid(row=0, column=0, padx=5, pady=(5,0), sticky="we")
            self.seg_button_1.set('Use available soil libraries')
            self.available_soils_frame = AvalableSoilsFrame(self)
            self.available_soils_frame.grid(row=1, column=0, sticky='nswe')

    def callback_custom_soils(self, value):
        self.customize_soils = True if value == 'Customize soils' else False
        self.available_soils_frame.destroy() if self.available_soils_frame else False
        self.custom_soils_frame.destroy() if self.custom_soils_frame else False
        if self.customize_soils == True:
            self.custom_soils_frame = CustomSoilsFrame(self)
            self.custom_soils_frame.grid(row=1, column=0, sticky='nswe', columnspan=1)
        else:
            self.available_soils_frame = AvalableSoilsFrame(self)
            self.available_soils_frame.grid(row=1, column=0, sticky='nswe')

    def get_is_custom_soils(self):
        return self.customize_soils

    def get_top_soil_layer(self):
        return self.available_soils_frame.radio_var_1.get()

    def get_top_soil_macros(self):
        return self.available_soils_frame.radio_var_2.get()

    def get_bottom_soil_layer(self):
        return self.available_soils_frame.radio_var_3.get()

    def get_bottom_soil_macros(self):
        return self.available_soils_frame.radio_var_4.get()


class AvalableSoilsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.label_1 = customtkinter.CTkLabel(self, text='Top soil layer', fg_color="transparent", anchor='w')
        self.label_1.grid(row=1, column=0, padx=5, pady=(10,0), sticky="we")
        self.radio_var_1 = tkinter.StringVar(value='Clay')
        self.radio_button_1 = customtkinter.CTkRadioButton(self, text='Clay', variable=self.radio_var_1, value='Clay')
        self.radio_button_1.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(self, text='Silt', variable=self.radio_var_1, value='Silt')
        self.radio_button_2.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(self, text='Peat', variable=self.radio_var_1, value='Peat')
        self.radio_button_3.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.label_2 = customtkinter.CTkLabel(self, text='Top soil macropores size', fg_color="transparent", anchor='w')
        self.label_2.grid(row=5, column=0, padx=5, pady=(10,0), sticky="we")
        self.radio_var_2 = tkinter.StringVar(value='High')
        self.radio_button_4 = customtkinter.CTkRadioButton(self, text='High', variable=self.radio_var_2, value='High')
        self.radio_button_4.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_5 = customtkinter.CTkRadioButton(self, text='Low', variable=self.radio_var_2, value='Low')
        self.radio_button_5.grid(row=7, column=0, padx=5, pady=5, sticky="w")

        self.label_3 = customtkinter.CTkLabel(self, text='Bottom soil layer', fg_color="transparent", anchor='w')
        self.label_3.grid(row=8, column=0, padx=5, pady=(10,0), sticky="we")
        self.radio_var_3 = tkinter.StringVar(value='Clay')
        self.radio_button_6 = customtkinter.CTkRadioButton(self, text='Clay', variable=self.radio_var_3, value='Clay')
        self.radio_button_6.grid(row=9, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_7 = customtkinter.CTkRadioButton(self, text='Silt', variable=self.radio_var_3, value='Silt')
        self.radio_button_7.grid(row=10, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_8 = customtkinter.CTkRadioButton(self, text='Peat', variable=self.radio_var_3, value='Peat')
        self.radio_button_8.grid(row=11, column=0, padx=5, pady=5, sticky="w")

        self.label_4 = customtkinter.CTkLabel(self, text='Bottom soil macropores size', fg_color="transparent", anchor='w')
        self.label_4.grid(row=12, column=0, padx=5, pady=(10,0), sticky="we")
        self.radio_var_4 = tkinter.StringVar(value='High')
        self.radio_button_9 = customtkinter.CTkRadioButton(self, text='High', variable=self.radio_var_4, value='High')
        self.radio_button_9.grid(row=13, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_10 = customtkinter.CTkRadioButton(self, text='Low', variable=self.radio_var_4, value='Low')
        self.radio_button_10.grid(row=14, column=0, padx=5, pady=5, sticky="w")


class CustomSoilsFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.msg = """Empty soil files are generated in input folder. Please add your soil parameters in

        geom_layers_01.txt
        dt_soillib_geom_01.txt
        dt_soillib_water_01.txt
        dt_soillib_crack_01.txt
        dt_soillib_solute_01.txt
        dt_soillib_heat_01.txt
        """

        self.textbox_1 = customtkinter.CTkTextbox(self, height=200, corner_radius=5, activate_scrollbars=False)
        self.textbox_1.grid(row=1, column=0, padx=0, pady=10, sticky="we")
        self.textbox_1.insert('0.0', self.msg)
        self.textbox_1.configure(state='disabled', wrap='word')
