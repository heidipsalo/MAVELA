import customtkinter
import tkinter
import sys, os
from gui_p1 import ScrollableFrame1
from gui_p2 import ScrollableFrame2
from gui_p3 import ScrollableFrame3
from gui_p4 import ScrollableFrame4
from gui_settings import Settings
from pre_process import PreProcess
from subprocess import Popen
from soil_param_user import SoilParamUser
from plotting import PlotResults


customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# # https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS  # may need to try sys._MEIPASS2
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)


# class TextRedirector(object):
#     def __init__(self, widget, tag="stdout"):
#         self.widget = widget
#         self.tag = tag
#
#     def write(self, string):
#         self.widget.configure(state="normal")
#         self.widget.insert("end", string, (self.tag,))
#         self.widget.configure(state="disabled")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("An agricultural field drainage modeling tool")
        self.geometry(f"{1100}x{580}")

        # configure geometry
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.settings = Settings()

        self.scrollable_frame1 = ScrollableFrame1(self, title='Step 1')
        self.scrollable_frame1.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.button_1 = customtkinter.CTkButton(self, text="Clear data", command=self.clear_data_callback)
        self.button_1.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_2 = customtkinter.CTkButton(self, text="Next step", command=self.next_to_frame2)
        self.button_2.grid(row=1, column=1, padx=10, pady=10, sticky="we")


    def next_to_frame2(self):
        self.get_data_frame1()
        self.scrollable_frame1.grid_forget()
        self.button_1.grid_forget()
        self.button_2.grid_forget()

        if self.settings.use_report == 'Yes':
            self.settings.create_folders_and_file_paths()
            self.settings.load_settings_from_file()
            if not self.settings.is_custom_soils:
                self.next_to_frame3_bypass_frame2()
                return
        self.scrollable_frame2 = ScrollableFrame2(self, title='Step 2')
        self.scrollable_frame2.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.button_3 = customtkinter.CTkButton(self, text="Back", command=self.back_to_frame1)
        self.button_3.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_4 = customtkinter.CTkButton(self, text="Next step", command=self.next_to_frame3)
        self.button_4.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        if self.settings.use_report == 'Yes' and self.settings.is_custom_soils:
            SoilParamUser(self.settings)

    def next_to_frame3_bypass_frame2(self):
        self.scrollable_frame3 = ScrollableFrame3(self, title='Step 3')
        self.scrollable_frame3.grid(row=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # sys.stdout = TextRedirector(self.scrollable_frame3.textbox_1, "stdout")
        # sys.stderr = TextRedirector(self.scrollable_frame3.textbox_1, "stderr")

        if self.settings.use_report == 'Yes' and not self.settings.is_custom_soils:
            self.button_5 = customtkinter.CTkButton(self, text="Back", command=self.back_to_frame1_from_frame3)
        else:
            self.button_5 = customtkinter.CTkButton(self, text="Back", command=self.back_to_frame2)
        self.button_5.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_6 = customtkinter.CTkButton(self, text="Start Flush modeling", command=self.start_flush)
        self.button_6.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.button_7 = customtkinter.CTkButton(self, text="Plot results", command=self.next_to_frame4)
        self.button_7.grid(row=1, column=2, padx=10, pady=10, sticky="we")

    def back_to_frame1(self):
        self.scrollable_frame2.grid_forget()
        self.button_3.grid_forget()
        self.button_4.grid_forget()
        self.scrollable_frame1.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.button_1.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_2.grid(row=1, column=1, padx=10, pady=10, sticky="we")

    def next_to_frame3(self):
        self.get_data_frame2()
        self.scrollable_frame2.grid_forget()
        self.button_3.grid_forget()
        self.button_4.grid_forget()
        self.scrollable_frame3 = ScrollableFrame3(self, title='Step 3')
        self.scrollable_frame3.grid(row=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # sys.stdout = TextRedirector(self.scrollable_frame3.textbox_1, "stdout")
        # sys.stderr = TextRedirector(self.scrollable_frame3.textbox_1, "stderr")

        self.button_5 = customtkinter.CTkButton(self, text="Back", command=self.back_to_frame2)
        self.button_5.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_6 = customtkinter.CTkButton(self, text="Start Flush modeling", command=self.start_flush)
        self.button_6.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.button_7 = customtkinter.CTkButton(self, text="Plot results", command=self.next_to_frame4)
        self.button_7.grid(row=1, column=2, padx=10, pady=10, sticky="we")

    def back_to_frame1_from_frame3(self):
        self.scrollable_frame3.grid_forget()
        self.button_5.grid_forget()
        self.button_6.grid_forget()
        self.button_7.grid_forget()
        self.scrollable_frame1.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.button_1.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_2.grid(row=1, column=1, padx=10, pady=10, sticky="we")

    def back_to_frame2(self):
        self.scrollable_frame3.grid_forget()
        self.button_5.grid_forget()
        self.button_6.grid_forget()
        self.button_7.grid_forget()
        self.scrollable_frame2.grid(row=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.button_3.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_4.grid(row=1, column=1, padx=10, pady=10, sticky="we")

    def back_to_frame3(self):
        self.scrollable_frame4.grid_forget()
        self.button_8.grid_forget()
        self.button_9.grid_forget()
        self.scrollable_frame3.grid(row=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.button_5.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_6.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.button_7.grid(row=1, column=2, padx=10, pady=10, sticky="we")

    def next_to_frame4(self):
        self.scrollable_frame3.grid_forget()
        self.button_5.grid_forget()
        self.button_6.grid_forget()
        self.button_7.grid_forget()
        self.scrollable_frame4 = ScrollableFrame4(self, title='Step 4')
        self.scrollable_frame4.grid(row=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        self.button_8 = customtkinter.CTkButton(self, text="Back", command=self.back_to_frame3)
        self.button_8.grid(row=1, column=0, padx=10, pady=10, sticky="we")
        self.button_9 = customtkinter.CTkButton(self, text="Plot", command=self.start_plotting)
        self.button_9.grid(row=1, column=1, padx=10, pady=10, sticky="we")
        self.button_10 = customtkinter.CTkButton(self, text="Exit", command=self.exit_app)
        self.button_10.grid(row=1, column=2, padx=10, pady=10, sticky="we")

    def exit_app(self):
        self.destroy()
    def clear_data_callback(self):
        for widget in self.scrollable_frame1.winfo_children():
            if isinstance(widget, customtkinter.CTkFrame):
                for inner_widget in widget.winfo_children():
                    if isinstance(inner_widget, customtkinter.CTkEntry):
                        inner_widget.delete(0, 'end')
                    if isinstance(inner_widget, customtkinter.CTkTextbox):
                        inner_widget.delete('1.0', tkinter.END)
                    for inner_widget_2 in inner_widget.winfo_children():
                        if isinstance(inner_widget_2, customtkinter.CTkEntry):
                            inner_widget_2.delete(0, 'end')
                        if isinstance(inner_widget_2, customtkinter.CTkTextbox):
                            inner_widget_2.delete('1.0', tkinter.END)
            else:
                if isinstance(widget, customtkinter.CTkEntry):
                    widget.delete(0, 'end')
                if isinstance(widget, customtkinter.CTkTextbox):
                    widget.delete('1.0', tkinter.END)

    def get_data_frame1(self):
        self.settings.flush_folder = self.scrollable_frame1.get_flush_folder()
        self.settings.use_report = self.scrollable_frame1.get_use_report()
        self.settings.year = self.scrollable_frame1.get_year()
        self.settings.location_name = self.scrollable_frame1.get_location_name()
        self.settings.coordinates = self.scrollable_frame1.get_coordinates()
        self.settings.veg_start = self.scrollable_frame1.get_veg_start()
        self.settings.veg_stop = self.scrollable_frame1.get_veg_stop()
        self.settings.drain_spacing = self.scrollable_frame1.get_drain_spacing()
        self.settings.user_depth = self.scrollable_frame1.get_user_depth()
        self.settings.slope = self.scrollable_frame1.get_slope()
        self.settings.drain_type = self.scrollable_frame1.get_drain_type()
        self.settings.control_level = self.scrollable_frame1.get_control_level()
        self.settings.control_time = self.scrollable_frame1.get_control_time()
        self.settings.is_open_ditch = self.scrollable_frame1.get_is_open_ditch()
        self.settings.open_ditch_dist = self.scrollable_frame1.get_open_ditch_dist()

    def get_data_frame2(self):
        self.settings.is_custom_soils = self.scrollable_frame2.get_is_custom_soils()
        if self.settings.is_custom_soils:
            self.settings.create_folders_and_file_paths()
            SoilParamUser(self.settings)
        else:
            self.settings.top_soil_layer = self.scrollable_frame2.get_top_soil_layer()
            self.settings.top_soil_macros = self.scrollable_frame2.get_top_soil_macros()
            self.settings.bottom_soil_layer = self.scrollable_frame2.get_bottom_soil_layer()
            self.settings.bottom_soil_macros = self.scrollable_frame2.get_bottom_soil_macros()

    def start_flush(self):
        self.scrollable_frame3.textbox_1.insert(tkinter.END, 'Flush modeling started. Please wait.\n')
        self.scrollable_frame3.update()
        preprocess = PreProcess(self.settings)
        p = Popen(fr"{self.settings.flush_folder}\run.bat", cwd=self.settings.flush_folder)
        stdout, stderr = p.communicate()
        self.scrollable_frame3.update()
        self.scrollable_frame3.textbox_1.insert(tkinter.END, 'Flush modeling completed. Please proceed to the next step.\n')
        self.scrollable_frame3.update()

    def start_plotting(self):
        self.settings.plot = self.scrollable_frame4.get_chosen_plot()
        if self.settings.plot == 0:
            self.settings.plot_type = self.scrollable_frame4.get_chosen_plot_type()
        PlotResults(self.settings)

if __name__ == "__main__":
    app = App()
    app.mainloop()
