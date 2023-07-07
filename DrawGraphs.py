import loss_finder
import peak_finder


class DrawGraph:
    def __init__(self):
        self._plot_ref = None      
        self._plot_ref_peak = None
        self._plot_ref_bar = []

    # bars(bool) if true will draw bars for the R5IM dips
    def draw(self, canvas, x_data, y_data, bars, peaks_finder):
        if self._plot_ref == None:
            plot_ref = canvas.axes.plot(x_data, y_data)
            self._plot_ref = plot_ref[0]

        else:
            self._plot_ref.set_ydata(y_data)

        if bars:
            for i in range(len(self._plot_ref_bar)):
                self._plot_ref_bar[i].remove()
            self._plot_ref_bar = []
            drops = loss_finder.find_drops(y_data, 50, -0.4)  #(data, sampleRate, significanceLevel)
            for i in range(len(drops)):
                self._plot_ref_bar.append(canvas.axes.axvspan(drops[i][0] * (11/2200) - 0.5, drops[i][1] * (11/2200) - 0.5, color="red", alpha=0.3))
        
        # plots peaks for blm
        if peaks_finder:
            if self._plot_ref_peak:
                self._plot_ref_peak.remove()

            peaks_x, peaks_y = peak_finder.get_peaks_x_y(y_data, 4, 30, 2) #data, maxNumberOfPeaks, (relative)minPeakSize, filterLevel
            self._plot_ref_peak = canvas.axes.scatter(peaks_x * (11/2200) - 0.5, peaks_y, s=35, marker='o', color="red", alpha=0.7)


class DrawGraphDemo:
    def __init__(self):
        self.counter = 0
        self._plot_ref= None
        self._plot_ref_peak = None
        self._plot_ref_bar = []

    def draw(self, canvas, x_data, y_data, bars):
        if self.counter >= len(y_data):
            self.counter = 0

        if self._plot_ref == None:
            plot_ref = canvas.axes.plot(x_data, y_data[self.counter])
            self._plot_ref = plot_ref[0]

        else:
            self._plot_ref.set_ydata(y_data[self.counter])

        if bars:
            for i in range(len(self._plot_ref_bar)):
                self._plot_ref_bar[i].remove()
            self._plot_ref_bar = []
            drops = loss_finder.find_drops(y_data[self.counter], 50, -0.4)  #(data, sampleRate, significanceLevel)
            for i in range(len(drops)):
                self._plot_ref_bar.append(canvas.axes.axvspan(drops[i][0] * (11/2200) - 0.5, drops[i][1] * (11/2200) - 0.5, color="red", alpha=0.3))
        else:
            if self._plot_ref_peak:
                self._plot_ref_peak.remove()
            peaks_x, peaks_y = peak_finder.get_peaks_x_y(y_data[self.counter], 4, 0.5) #data, maxNumberOfPeaks, (relative)minPeakSize
            self._plot_ref_peak = canvas.axes.scatter(peaks_x * (11/2200) - 0.5, peaks_y, s=35, marker='o', color="red", alpha=0.7)

        self.counter += 1