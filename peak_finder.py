import numpy as np
from scipy.signal import find_peaks
from scipy.signal import lfilter

#return the minimum and maximum when given a set of data
def find_min_max(data):
    return min(data), max(data)

#return a normalised set of data (maximum is 1 and the minimum is 0) when given a set of data
def normalise_data(data):
    normalised = data.copy()
    minimum, maximum = find_min_max(data)
    for i in range(len(data)):
        normalised[i] = (data[i]-minimum)/(maximum-minimum)
    return normalised

#return a list of the n largest values in a list and a list of their indexes in the original list
def find_n_largest_indexes(list, n, minimumSize):
    indexes = []
    sortedSet = sorted(list, reverse=True)
    if len(list) <= n:
        for i in range(0, len(list)):
            indexes.append(i)
    else:
        for i in range(n):
            indexes.append(np.where(list == sortedSet[i])[0][0])
    deleted = 0
    for i in range(len(indexes)):
        if list[indexes[i - deleted]] < minimumSize:
            indexes = np.delete(indexes, i - deleted)
            deleted += 1
    return indexes  #can also return sortedSet[:n] to get the largest values and not just their indexes

def get_peaks_x_y(data, maxNumberOfPeaks, minPeakSize, filterLevel):
    b = [1.0 / filterLevel] * filterLevel
    a = 1
    filteredData = lfilter(b, a, data)
    peaks, properties = find_peaks(normalise_data(filteredData), width = 0, height=0)
    peakSizes = ((properties['peak_heights'] - properties['width_heights'])*100) * (properties['widths'] / len(filteredData)) * 1000
    largestPeakIndexes = find_n_largest_indexes(peakSizes, maxNumberOfPeaks, minPeakSize)
    return peaks[largestPeakIndexes], data[peaks][largestPeakIndexes]   #peaks[largestPeakIndxexs] is the index of peaks in the data (so 0-2199), data[peaks][largestPeakIndexes] is the data values (y_data) of the peaks