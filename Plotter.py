import nidaqmx
from matplotlib import pyplot as plt


class Plotter:

    def __init__(self, line_width=1, line_style='-', line_color='blue', sample_rate=0.01):

        #   'True' follows the time as set in the sample rate:
        self.true_time = [0]
        self.synched_time = []

        #   Synchronized follows the actual rate at which the camera saves the images.
        self.true_amplitude = [[0], [0], [0], [0]]
        self.synced_amplitude = [[0], [0], [0], [0]]
        self.line_width = [line_width, line_width, line_width, line_width]
        self.line_style = [line_style, line_style, line_style, line_style]
        self.line_color = ["b", "r", "g", "m"]
        self.legend = ["Channel 0", "Channel 1", "Channel 2", "Channel 3"]
        self.sample_rate = sample_rate

        self.figure_on = False

    def plot_analog_input(self):
        """
        This function receives digital input from the NI hardware card, records it and plots it in real time.
        :param SampleRate: The desired sampling rate for the data acquisition, i.e., the amount of time between points.
        :return: Data arrays
        """
        self.figure_on = True
        #   Create the figure
        fig = plt.figure()
        plt.title("Real Time plot")
        plt.xlabel("time (sec)")
        plt.ylabel("Voltage Input [V]")
        plt.legend(self.legend)
        plt.grid()

        #   Start real time recording & plotting
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Dev1/ai0:1")

            i = 0
            while self.figure_on:
                #   Acquire data from card
                input_data_signal_from_card = task.read(number_of_samples_per_channel=1)

                #   Plot data
                plt.plot(self.true_time, self.true_amplitude[0], linewidth=self.line_width[0], linestyle=self.line_style[0], color=self.line_color[0])
                plt.plot(self.true_time, self.true_amplitude[1], linewidth=self.line_width[1], linestyle=self.line_style[1], color=self.line_color[1])
                plt.plot(self.true_time, self.true_amplitude[2], linewidth=self.line_width[2], linestyle=self.line_style[2], color=self.line_color[2])
                plt.plot(self.true_time, self.true_amplitude[3], linewidth=self.line_width[3], linestyle=self.line_style[3], color=self.line_color[3])

                #   Save data in memory
                self.true_amplitude[0].append(input_data_signal_from_card[0])
                self.true_amplitude[1].append(input_data_signal_from_card[1])
                self.true_amplitude[2].append(input_data_signal_from_card[2])
                self.true_amplitude[3].append(input_data_signal_from_card[3])
                self.true_time.append(i)

                #   Pause period
                plt.pause(1 / self.sample_rate)
                i += 1 / self.sample_rate

            plt.show()

    def get_current_amplitudes(self):
        return [self.true_amplitude[0][-1],
                self.true_amplitude[1][-1],
                self.true_amplitude[2][-1],
                self.true_amplitude[3][-1]]

    def get_current_time(self):
        return self.true_time[-1]

    def save_to_synched_vectors(self):
        """
            Saves the current amplitude vs time vectors into the syncronized vectors
        :return: Nothing
        """
        self.synched_time.append[self.get_current_time()]
        current_amplitudes = self.get_current_amplitudes()
        for i in range(4):
            self.synched_amplitude[i].append(current_amplitudes[i])

    def save_to_csv(self, directory):
        true_vectors = [self.true_time,
                        self.true_amplitude[0],
                        self.true_amplitude[1],
                        self.true_amplitude[2],
                        self.true_amplitude[3]]
        df = transpose(array(true_vectors))
        filepath = directory + '/True Data.csv'
        savetxt(filepath, df, delimiter=',', header='time [s], CH0 [V], CH1[V], CH2 [V], CH3 [V]', fmt='%s')

        synched_vectors = [self.synched_time,
                            self.synched_amplitude[0],
                            self.synched_amplitude[1],
                            self.synched_amplitude[2],
                            self.synched_amplitude[3]]
        df = transpose(array(synched_vectors))
        filepath = directory + '/Synchronized Data.csv'
        savetxt(filepath, df, delimiter=',', header='time [s], CH0 [V], CH1[V], CH2 [V], CH3 [V]', fmt='%s')
