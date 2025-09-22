import customtkinter
import tkinter
from mass_balance_helper import calc_balance


class MassBalanceFrame(customtkinter.CTkFrame):
    def __init__(self, master, flush_results_file, drain_spacing):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.flush_results_file = flush_results_file
        self.drain_spacing = drain_spacing
        self.calc_mass_balance = False
        self.mass_balance = 0.0
        self.textbox_1 = None

        self.label_1 = customtkinter.CTkLabel(self, text='Mass balance check', fg_color="transparent", anchor='w')
        self.label_1.grid(row=0, column=0, padx=5, pady=(10,0), sticky="we")

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self, values=['Yes', 'No'], command=self.mass_balance_check)
        self.seg_button_1.grid(row=1, column=0, padx=5, pady=(5,0), sticky="we")
        self.seg_button_1.set('No')

    def mass_balance_check(self, value):
        self.calc_mass_balance = True if value == 'Yes' else False

        if self.calc_mass_balance:
            self.mass_balance = calc_balance(self.flush_results_file, self.drain_spacing)
            self.label_2 = customtkinter.CTkLabel(self, text='Mass balance error', fg_color="transparent", anchor='w')
            self.label_2.grid(row=2, column=0, padx=5, pady=(10,0), sticky="we")
            self.textbox_1 = customtkinter.CTkTextbox(self, width=100, height=15, corner_radius=5, activate_scrollbars=False)
            self.textbox_1.grid(row=3, column=0, padx=5, pady=(10,0), sticky="we")
            self.textbox_1.insert('0.0', '{} %'.format(self.mass_balance))
            self.textbox_1.configure(state='disabled', wrap='word')
        else:
            self.textbox_1.destroy() if self.textbox_1 else False


class CumulativeInstantValues(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.label_1 = customtkinter.CTkLabel(self, text='Value', fg_color="transparent", anchor='w')
        self.label_1.grid(row=0, column=0, padx=5, pady=(20,0), sticky="we")
        self.radio_var_1 = tkinter.IntVar(value=0)
        self.radio_button_1 = customtkinter.CTkRadioButton(self, text='Instantaneous', variable=self.radio_var_1, value=0)
        self.radio_button_1.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(self, text='Cumulative', variable=self.radio_var_1, value=1)
        self.radio_button_2.grid(row=2, column=0, padx=5, pady=5, sticky="w")


class ScrollableFrame4(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure((0,1,2,3), weight=1)
        self.cumulative_instant_frame = None

        self.mass_balance_frame = MassBalanceFrame(self, master.settings.flush_results_file, master.settings.drain_spacing)
        self.mass_balance_frame.grid(row=0, column=0, sticky='nswe')

        self.label_1 = customtkinter.CTkLabel(self, text='Plot', fg_color="transparent", anchor='w')
        self.label_1.grid(row=1, column=0, padx=5, pady=(20,0), sticky="we")

        self.radio_var_1 = tkinter.IntVar(value=0)
        self.radio_button_1 = customtkinter.CTkRadioButton(self, text='Total water balance', variable=self.radio_var_1, value=0, command=self.check_for_cumulative)
        self.radio_button_1.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_2 = customtkinter.CTkRadioButton(self, text='Ground water levels', variable=self.radio_var_1, value=1, command=self.check_for_cumulative)
        self.radio_button_2.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.radio_button_3 = customtkinter.CTkRadioButton(self, text='Snow water equivalent', variable=self.radio_var_1, value=2, command=self.check_for_cumulative)
        self.radio_button_3.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.cumulative_instant_frame = CumulativeInstantValues(self)
        self.cumulative_instant_frame.grid(row=5, column=0, sticky='nswe')

    def check_for_cumulative(self):
        if self.radio_var_1.get() == 0:
            self.cumulative_instant_frame = CumulativeInstantValues(self)
            self.cumulative_instant_frame.grid(row=5, column=0, sticky='nswe')
        else:
            self.cumulative_instant_frame.destroy() if self.cumulative_instant_frame else False

    def get_chosen_plot(self):
        return self.radio_var_1.get()

    def get_chosen_plot_type(self):
        return self.cumulative_instant_frame.radio_var_1.get()
