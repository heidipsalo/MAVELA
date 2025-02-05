import customtkinter
import tkinter


class ControlFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1), weight=1)

        self.label_1 = customtkinter.CTkLabel(self, text='What is the control level (m)', fg_color="transparent", anchor='w')
        self.label_1.grid(row=0, column=0, padx=5, pady=(0,0), sticky="we")

        self.entry_1 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_1.grid(row=1, column=0, sticky="we")
        self.entry_1.configure(state='normal')

        self.label_2 = customtkinter.CTkLabel(self, text='What is control time from (DD.MM)', fg_color="transparent", anchor='w')
        self.label_2.grid(row=2, column=0, padx=5, pady=(0,0), sticky="we")

        self.label_3 = customtkinter.CTkLabel(self, text='What is control time to (DD.MM)', fg_color="transparent", anchor='w')
        self.label_3.grid(row=2, column=1, padx=15, pady=(0,0), sticky="we")

        self.entry_2 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_2.grid(row=3, column=0, sticky="we")
        self.entry_2.configure(state='normal')

        self.entry_3 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_3.grid(row=3, column=1, padx=10, sticky="we")
        self.entry_3.configure(state='normal')


class ConvDrainageFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.open_ditch = 'Off'

        self.label_1 = customtkinter.CTkLabel(self, text='Open ditch', fg_color="transparent", anchor='w')
        self.label_1.grid(row=0, column=0, padx=5, pady=(0,0), sticky="we")

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self, values=['Off', 'On'], command=self.choose_open_ditch)
        self.seg_button_1.grid(row=1, column=0, padx=0, pady=0, sticky="we")
        self.seg_button_1.set('Off')

        self.entry_1 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)

    def choose_open_ditch(self, value):
        self.open_ditch = value if value else False

        if self.open_ditch == 'On':
            self.label_2 = customtkinter.CTkLabel(self, text='Distance to open ditch (m)', fg_color="transparent", anchor='w')
            self.label_2.grid(row=2, column=0, padx=5, pady=(0,0), sticky="we")

            self.entry_1 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
            self.entry_1.grid(row=3, column=0, sticky="we")
            self.entry_1.configure(state='normal')

        if self.open_ditch == 'Off':
            self.label_2.destroy()
            self.entry_1.destroy()
            self.entry_1 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)


class NotUseReportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.drainage_type = 'Conventional Subsurface Drainage'
        self.control_frame = None
        self.conv_drain_frame = None

        self.label_3 = customtkinter.CTkLabel(self, text='Modeling year', fg_color="transparent", anchor='w')
        self.label_3.grid(row=0, column=0, padx=5, pady=(5,0), sticky="we")

        self.entry_2 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_2.grid(row=1, column=0, sticky="we")
        self.entry_2.configure(state='normal')

        self.label_4 = customtkinter.CTkLabel(self, text='Name of the location', fg_color="transparent", anchor='w')
        self.label_4.grid(row=2, column=0, padx=5, pady=(5,0), sticky="we")

        self.entry_3 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_3.grid(row=3, column=0, sticky="we")
        self.entry_3.configure(state='normal')

        self.label_5 = customtkinter.CTkLabel(self, text='Field coordinates (N)', fg_color="transparent", anchor='w')
        self.label_5.grid(row=4, column=0, padx=5, pady=(5,0), sticky="we")

        self.label_6 = customtkinter.CTkLabel(self, text='Field coordinates (E)', fg_color="transparent", anchor='w')
        self.label_6.grid(row=4, column=1, padx=15, pady=(5,0), sticky="we")

        self.label_7 = customtkinter.CTkLabel(self, text='in ESPG 3067', fg_color="transparent", anchor='w')
        self.label_7.grid(row=5, column=2, padx=15, pady=(5,0), sticky="we")

        self.entry_4 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_4.grid(row=5, column=0, sticky="we")
        self.entry_4.configure(state='normal')

        self.entry_5 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_5.grid(row=5, column=1, sticky="we", padx=10)
        self.entry_5.configure(state='normal')

        self.label_8 = customtkinter.CTkLabel(self, text='Start of growing season (DD.MM)', fg_color="transparent", anchor='w')
        self.label_8.grid(row=6, column=0, padx=5, pady=(5,0), sticky="we")

        self.label_9 = customtkinter.CTkLabel(self, text='End of growing season (DD.MM)', fg_color="transparent", anchor='w')
        self.label_9.grid(row=6, column=1, padx=15, pady=(5,0), sticky="we")

        self.entry_6 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_6.grid(row=7, column=0, sticky="we")
        self.entry_6.configure(state='normal')

        self.entry_7 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_7.grid(row=7, column=1, sticky="we", padx=10)
        self.entry_7.configure(state='normal')

        self.label_10 = customtkinter.CTkLabel(self, text='Drain spacing (m)', fg_color="transparent", anchor='w')
        self.label_10.grid(row=8, column=0, padx=5, pady=(5,0), sticky="we")

        self.entry_8 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_8.grid(row=9, column=0, sticky="we")
        self.entry_8.configure(state='normal')

        self.label_11 = customtkinter.CTkLabel(self, text='Depth of subsurface drainage (m)', fg_color="transparent", anchor='w')
        self.label_11.grid(row=10, column=0, padx=5, pady=(5,0), sticky="we")

        self.entry_9 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_9.grid(row=11, column=0, sticky="we")
        self.entry_9.configure(state='normal')

        self.label_12 = customtkinter.CTkLabel(self, text='Slope (%)', fg_color="transparent", anchor='w')
        self.label_12.grid(row=12, column=0, padx=5, pady=(5,0), sticky="we")

        self.entry_10 = customtkinter.CTkEntry(self, width=100, height=25, corner_radius=5)
        self.entry_10.grid(row=13, column=0, sticky="we")
        self.entry_10.configure(state='normal')

        self.label_13 = customtkinter.CTkLabel(self, text='Drainage type', fg_color="transparent", anchor='w')
        self.label_13.grid(row=14, column=0, padx=5, pady=(5,0), sticky="we")

        optionmenu_default_var = customtkinter.StringVar(value=self.drainage_type)
        self.optionmenu_1 = customtkinter.CTkOptionMenu(self,
                values=['Control Drainage', 'Conventional Subsurface Drainage'],
                anchor='w',
                command=self.select_drainage,
                variable=optionmenu_default_var
        )
        self.optionmenu_1.grid(row=15, column=0, padx=0, pady=0, columnspan=1)

        self.conv_drain_frame = ConvDrainageFrame(self)
        self.control_frame = ControlFrame(self)

        if self.drainage_type == 'Conventional Subsurface Drainage':
            self.conv_drain_frame = ConvDrainageFrame(self)
            self.conv_drain_frame.grid(row=16, column=0, padx=10, pady=10, sticky="nsew")

    def select_drainage(self, choice):
        self.drainage_type = choice
        if self.drainage_type == 'Conventional Subsurface Drainage':
            self.control_frame.destroy() if self.control_frame else False
            self.conv_drain_frame.destroy() if self.conv_drain_frame else False
            self.conv_drain_frame = ConvDrainageFrame(self)
            self.conv_drain_frame.grid(row=16, column=0, sticky="nsew")
            self.control_frame = ControlFrame(self)
        else:
            self.conv_drain_frame.destroy() if self.conv_drain_frame else False
            self.control_frame = ControlFrame(self)
            self.control_frame.grid(row=16, column=0, sticky="nsew")
            self.conv_drain_frame = ConvDrainageFrame(self)
            self.conv_drain_frame.grid(row=17, column=0, sticky="nsew")


class ScrollableFrame1(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.flush_folder = ''
        self.use_report = 'No'

        self.label_1 = customtkinter.CTkLabel(self, text='Add path to FLUSH folder', fg_color="transparent", anchor='w')
        self.label_1.grid(row=0, column=0, padx=5, pady=(0,0), sticky="we")

        self.entry_1 = customtkinter.CTkTextbox(self, width=100, height=15, corner_radius=5, activate_scrollbars=False)
        self.entry_1.grid(row=1, column=0, sticky="we")
        self.entry_1.configure(state='normal', wrap='word')

        self.button_1 = customtkinter.CTkButton(self, text="Choose folder", command=self.choose_folder_callback)
        self.button_1.grid(row=1, column=1, padx=10, pady=0, sticky="we")

        self.label_2 = customtkinter.CTkLabel(self, text='Downloading input from Report file', fg_color="transparent", anchor='w')
        self.label_2.grid(row=2, column=0, padx=5, pady=(5,0), sticky="we")

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self, values=['Yes', 'No'], command=self.choose_use_report)
        self.seg_button_1.grid(row=3, column=0, padx=0, pady=0, sticky="we")
        self.seg_button_1.set('No')

        self.not_use_report_frame = NotUseReportFrame(self)
        self.not_use_report_frame.grid(row=4, columnspan=4, sticky="nsew")

    def choose_folder_callback(self):
        self.flush_folder = customtkinter.filedialog.askdirectory()
        self.entry_1.delete('1.0', tkinter.END)
        self.entry_1.insert('0.0', self.flush_folder)

    def choose_use_report(self, value):
        self.use_report = value if value else False
        if self.use_report == 'Yes':
            self.not_use_report_frame.destroy()
            self.not_use_report_frame = NotUseReportFrame(self)
        else:
            self.not_use_report_frame = NotUseReportFrame(self)
            self.not_use_report_frame.grid(row=4, columnspan=4, sticky="nsew")

    def get_flush_folder(self):
        return self.entry_1.get('1.0', tkinter.END).replace('\n','')

    def get_use_report(self):
        return self.use_report

    def get_year(self):
        return self.not_use_report_frame.entry_2.get()

    def get_location_name(self):
        return self.not_use_report_frame.entry_3.get()

    def get_coordinates(self):
        xx = self.not_use_report_frame.entry_4.get()
        yy = self.not_use_report_frame.entry_5.get()
        return [xx, yy]

    def get_veg_start(self):
        return self.not_use_report_frame.entry_6.get()

    def get_veg_stop(self):
        return self.not_use_report_frame.entry_7.get()

    def get_drain_spacing(self):
        return self.not_use_report_frame.entry_8.get()

    def get_user_depth(self):
        return self.not_use_report_frame.entry_9.get()

    def get_slope(self):
        return self.not_use_report_frame.entry_10.get()

    def get_drain_type(self):
        return self.not_use_report_frame.drainage_type

    def get_control_level(self):
        return self.not_use_report_frame.control_frame.entry_1.get()

    def get_control_time(self):
        start = self.not_use_report_frame.control_frame.entry_2.get()
        stop = self.not_use_report_frame.control_frame.entry_3.get()
        return [start, stop]

    def get_is_open_ditch(self):
        return self.not_use_report_frame.conv_drain_frame.open_ditch

    def get_open_ditch_dist(self):
        return self.not_use_report_frame.conv_drain_frame.entry_1.get()

