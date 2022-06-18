import nidaqmx
from matplotlib import pyplot as plt


class Plotter:

    def __init__(self, line_width=1, line_style='-', line_color='blue', sample_rate=0.01):

        self.line_width = line_width
        self.line_style = line_style
        self.line_color = line_color
        self.sample_rate = sample_rate

    def plot_analog_input(self):
        """
        This function receives digital input from the NI hardware card, records it and plots it in real time.
        :param SampleRate: The desired sampling rate for the data acquisition, i.e., the amount of time between points.
        :return: Data arrays
        """

        #   Create the figure
        fig = plt.figure()
        plt.title("Real Time plot")
        plt.xlabel("time (sec)")
        plt.ylabel("Voltage Input [V]")
        plt.grid()

        #   Data will be stored in suiting arrays
        voltage_0 = []
        voltage_1 = []
        time = []

        #   Start real time recording & plotting
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1")

            i = 0
            while True:
                #   Acquire data from card
                data = task.read(number_of_samples_per_channel=1)

                #   Plot data
                plt.plot(time, voltage_0, linewidth=self.line_width, linestyle='dashed', color='grey')
                plt.plot(time, voltage_1, linewidth=self.line_width, linestyle=self.line_style, color=self.line_color)

                #   Save data in memory
                voltage_0.append(data[0])
                voltage_1.append(data[1])
                time.append(i)

                #   Pause period
                plt.pause(self.sample_rate)
                i += self.sample_rate

            plt.show()

            return time, voltage_0, voltage_1



