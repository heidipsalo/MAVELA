import time
import customtkinter
from gridded_data import download_gridded_data_runner
from download_and_format_input_files_helper import download_weather_data_runner
import tkinter


class ScrollableFrame3(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure((0,1,2,3), weight=1)

        self.downloaded_data_folder = ''

        self.button_1 = customtkinter.CTkButton(self, text="Download FMI data", command=self.start_download)
        self.button_1.grid(row=0, column=0, padx=5, pady=20, sticky="we")

        self.button_2 = customtkinter.CTkButton(self, text="Select and Proceed with stored data", command=self.select_path_to_stored_data)
        self.button_2.grid(row=0, column=2, padx=5, pady=20, sticky="we")

        self.label_1 = customtkinter.CTkLabel(self, text='or', fg_color="transparent", justify='center')
        self.label_1.grid(row=0, column=1, pady=20, sticky="we")

        self.textbox_1 = customtkinter.CTkTextbox(self, fg_color="transparent", wrap="word")
        self.textbox_1.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky="we")
        self.textbox_1.configure(state='normal')

        master.settings.create_folders_and_file_paths()
        master.settings.create_flush_bat_file()
        if master.settings.use_report == 'Yes':
            master.settings.load_settings_from_file()
        else:
            val = master.settings.validate()
            if val != 1:
                self.label_2 = customtkinter.CTkLabel(self, text=f'Validation of input parameters failed. Error message: {val}', text_color='red', fg_color="transparent", justify='center')
                self.label_2.grid(row=1, column=0, padx=5, pady=20, sticky="we")
            else:
                master.settings.convert_to_backend_settings()
        master.settings.define_weather_start_stop_download_time()
        master.settings.create_settings_file()
        self.master = master

    def start_download(self):
        self.textbox_1.delete('1.0', tkinter.END)
        self.textbox_1.insert(tkinter.END, "Downloading gridded data from FMI web... Please wait...\n")
        self.update()
        gridded_data_array_size = download_gridded_data_runner(self.master.settings, self.textbox_1)
        self.update()
        self.textbox_1.insert(tkinter.END, "Downloading weather data now. Please wait...\n")
        self.update()
        download_weather_data_runner(self.master.settings, gridded_data_array_size, self.textbox_1)
        self.update()
        self.textbox_1.insert(tkinter.END, "Downloading completed. Please proceed with Flush modeling.\n")
        self.update()

    def select_path_to_stored_data(self):
        self.downloaded_data_folder = customtkinter.filedialog.askdirectory().replace('\n','')
        self.master.settings.temp_folder = self.downloaded_data_folder
