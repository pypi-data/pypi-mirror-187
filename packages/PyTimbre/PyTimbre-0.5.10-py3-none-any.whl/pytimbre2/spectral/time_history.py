from .spectrum import Spectrum, SpectrumByDigitalFilters, SpectrumByFFT, Waveform
from ..audio_files.wavefile import WaveFile
import numpy as np
import warnings
import datetime


class TimeHistory:
    """
    This class wraps the ability of the analysis to contain multiple spectrum objects and create a variation across
    time.

    Remarks
    2022-12-13 - FSM - added a function to collect the sound quality metrics from each of the spectra
    2022-12-13 - FSM - added a function to collect the times past midnight from the spectra objects
    """

    def __init__(self, a: Waveform = None, integration_time: float = 0.25):
        """
        Constructor - this will build a class object for the TimeHistory and instantiate all properties and protected
        elements.

        Parameters
        ----------
        :param a: This is the waveform object that we want to process into a TimeHistory object
        :param integration_time: float - the size of the independent waveforms that will be processed into a series of
            Spectrum objects
        """

        self._spectra = None
        self._times = None
        self._waveform = a
        self._integration_time = integration_time
        self._header = None

    def _calculate_spectrogram(self):
        warnings.warn("This function must be implemented in any child class to create the collection of spectra objects"
                      " that define the time history")
        pass

    def save(self, filename: str):
        from ..audio_files.ansi_standard_formatted_files import StandardBinaryFile
        import datetime
        """
        This function saves the data from the waveform's header and the spectral information to a file 

        Parameters:
        -----------
        :param filename: string - the fill path to the output file
        """

        #   open the output file

        file = open(filename, 'wt')

        #   If the header dictionary is present, write it to the output file

        if isinstance(self.waveform, StandardBinaryFile):
            header_dict = self.waveform.header
        elif isinstance(self.waveform, WaveFile):
            if self.waveform.header is not None:
                header_dict = self.waveform.header
        elif isinstance(self.header, dict):
            header_dict = self.header
            del header_dict['HEADER SIZE']
        else:
            header_dict = None

        if header_dict is not None:
            header_line = ';{},{}\n'.format("HEADER SIZE", len(header_dict.keys()) + 2)
            file.write(header_line)

            unwanted_strs = [',']

            for key in header_dict.keys():
                for str in unwanted_strs:
                    new_key = key.replace(str, "_")
                header_line = ';{},{}\n'.format(new_key.upper(), header_dict[key])
                file.write(header_line)

        #   Now write the last header row which will have the time and frequency array

        header_line = ';{}'.format('year').ljust(7, ' ')
        header_line += ',{}'.format('month').ljust(7, ' ')
        header_line += ',{}'.format('day').ljust(7, ' ')
        header_line += ',{}'.format('hour').ljust(7, ' ')
        header_line += ',{}'.format('minute').ljust(7, ' ')
        header_line += ',{}'.format('second').ljust(7, ' ')

        for f in self.frequencies:
            header_line += ',{:6.2f}'.format(f).ljust(10, ' ')

        header_line += '\n'
        file.write(header_line)

        #   Now loop through the data
        for time_idx in range(len(self.spectra)):
            if isinstance(self.spectra[time_idx].time, datetime.datetime):
                data_line = '{:04.0f}'.format(self.spectra[time_idx].time.year).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.month).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.day).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(self.spectra[time_idx].time.minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(self.spectra[time_idx].time.second +
                                                self.spectra[time_idx].time.microsecond * 1e-6).ljust(7, ' ')
            else:
                hour = np.floor(self.spectra[time_idx].time / 3600)
                minute = np.floor((self.spectra[time_idx].time - hour * 3600) / 60)
                second = self.spectra[time_idx].time - 60 * (60 * hour + minute)

                data_line = '{:04.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(0).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(hour).ljust(7, ' ')
                data_line += ',{:02.0f}'.format(minute).ljust(7, ' ')
                data_line += ',{:02.3f}'.format(second).ljust(7, ' ')

            #   Add the decibel data to the data_line object

            for j in range(len(self.frequencies)):
                data_line += ',{:03.2f}'.format(self.spectra[time_idx].pressures_decibels[j]).ljust(10, ' ')

            data_line += '\n'
            file.write(data_line)

        file.close()

    @staticmethod
    def load(filename: str):
        """
        This function will load the data from a file, and create the spectrum representation from the information within

        Parameters
        ----------

        filename: str - the full path to the
        """
        import os.path
        import pandas as pd

        if not os.path.exists(filename):
            raise ValueError("The filename must exist")

        file = open(filename, "rt")
        contents = file.readlines()
        file.close()

        th = TimeHistory()

        if contents[0][0] == ';':
            th._header = dict()

            n = 0

            while contents[n][0] == ';' and not (contents[n][:5] == ";year"):
                #   Split the data apart based on the comma
                elements = contents[n].split(',')
                if len(elements) == 2:
                    th._header[elements[0][1:]] = elements[1][:-1]
                else:
                    value = elements[-1][:-1]
                    name = ','.join(elements[:-1])
                    th._header[name[1:]] = value

                #   increment the line
                n += 1

                if contents[n] == "\n":
                    n += 1

            elements = contents[n].split(',')
            f = list()
            for freq_index in range(6, len(elements)):
                f.append(float(elements[freq_index]))

            frequencies = np.asarray(f)
            n += 1

            th._spectra = np.empty((len(contents)-n,), dtype=Spectrum)

            for line_index in range(n, len(contents)):
                elements = contents[line_index].split(',')

                if int(elements[0]) == int(elements[1]) == int(elements[2]) == 0:
                    time = 60 * (60 * float(elements[3]) + float(elements[4])) + float(elements[5])
                else:
                    year = int(elements[0])
                    month = int(elements[1])
                    day = int(elements[2])
                    hour = int(elements[3])
                    minute = int(elements[4])
                    seconds = float(elements[5])
                    second = int(np.floor(seconds))
                    microsecond = int(np.floor(1e6 * (seconds - second)))
                    time = datetime.datetime(year, month, day, hour, minute, second, microsecond)

                spl = np.zeros((len(frequencies),))
                for spl_idx in range(6, len(elements)):
                    spl[spl_idx-6] = float(elements[spl_idx])

                th._spectra[line_index - n] = Spectrum()
                th._spectra[line_index - n]._frequencies = frequencies
                th._spectra[line_index - n]._acoustic_pressures_pascals = 20e-6 * 10**(spl/20)
                th._spectra[line_index - n]._time0 = time

            return th

    @property
    def waveform(self):
        return self._waveform

    @property
    def signal(self):
        return self.waveform.samples

    @property
    def sample_rate(self):
        return self._sample_rate

    @property
    def integration_time(self):
        return self._integration_time

    @property
    def duration(self):
        return self._waveform.duration

    @property
    def times(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        if self._times is None:
            if self.spectra[0]._time0 is not None:
                t = np.zeros((len(self._spectra),), dtype=datetime.datetime)
            else:
                t = np.zeros((len(self._spectra),))

            for i in range(len(self.spectra)):
                if self.spectra[i].waveform is not None:
                    t[i] = self.spectra[i].time
                else:
                    t[i] = self.spectra[i].time_past_midnight

            self._times = t

        return self._times

    @property
    def sample_size(self):
        return int(np.floor(self.integration_time * self.sample_rate))

    @property
    def frequencies(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra[0].frequencies

    @property
    def spectra(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        return self._spectra

    @property
    def spectrogram_array_decibels(self):
        if self._spectra is None:
            self._calculate_spectrogram()

        spectrogram = np.zeros([len(self._spectra), len(self._spectra[0].frequencies)])
        for i in range(len(self._spectra)):
            spectrogram[i, :] = self._spectra[i].pressures_decibels

        return spectrogram

    @property
    def overall_level(self):
        """
        Overall sound pressure level, unweighted (i.e. flat wieghted, Z-weighted) time history.  Calculated as the
        energetic sum of the fractional octave band spectral time history.
        """
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_level

        return levels

    @property
    def overall_a_weighted_level(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        levels = np.zeros((len(self.times)), )

        for i in range(len(self.spectra)):
            levels[i] = self.spectra[i].overall_a_weighted_level

        return levels

    @property
    def header(self):
        return self._header

    @property
    def roughness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        roughness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            roughness[i] = self.spectra[i].roughness

        return roughness

    @property
    def loudness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        loudness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            loudness[i] = self.spectra[i].loudness

        return loudness

    @property
    def sharpness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        sharpness = np.zeros((len(self.times),))

        for i in range(len(self.times)):
            sharpness[i] = self.spectra[i].sharpness

        return sharpness

    @property
    def spectral_centroid(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times), ))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_centroid

        return r

    @property
    def spectral_spread(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_spread

        return r

    @property
    def spectral_skewness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_skewness

        return r

    @property
    def spectral_kurtosis(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_kurtosis

        return r

    @property
    def spectral_slope(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_slope

        return r

    @property
    def spectral_decrease(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_decrease

        return r

    @property
    def spectral_roll_off(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_roll_off

        return r

    @property
    def spectral_energy(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_energy

        return r

    @property
    def spectral_flatness(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_flatness

        return r

    @property
    def spectral_crest(self):
        if self.spectra is None:
            self._calculate_spectrogram()

        r = np.zeros((len(self.times),))

        for i in range(len(r)):
            r[i] = self.spectra[i].spectral_crest

        return r

    @property
    def times_past_midnight(self):
        tpm = np.zeros((len(self.spectra), ))

        for i in range(len(tpm)):
            tpm[i] = self.spectra[i].time_past_midnight

        return tpm


class Narrowband_TimeHistory(TimeHistory):
    """
    This class implements the _calculate_spectrogram function using the Narrowband_Spectrum class
    """

    def __init__(self, a: Waveform, integration_time: float = 0.25, fft_size: int = None):
        super().__init__(a, integration_time)

        self._fft_size = fft_size

        #   There is no default value for the FFT size, so let's do some analysis to determine what the most optimal
        #   value of this should be if it is not provided.
        if self._fft_size is None:

            #   Set the default block size
            sub_wfm_length = self.integration_time * self.waveform.sample_rate
            self._fft_size = int(2 ** np.floor(np.log2(sub_wfm_length)))

        elif (self._fft_size > len(self.waveform.samples)) or \
                (self.fft_size > self.integration_time * self.sample_rate):
            raise ValueError('FFT block size cannot be greater than the total length of the signal.')

    @property
    def fft_size(self):
        return self._fft_size

    def _calculate_spectrogram(self):
        from ..waveform import trimming_methods

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = int(np.floor(self.duration / self.integration_time))

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByFFT)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self.waveform.trim(s0, s0 + self.sample_size, trimming_methods.samples)

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByFFT(subset, self.fft_size)

            #   increment the starting sample
            s0 += self.sample_size


class LogarithmicBand_TimeHistory(TimeHistory):
    """
    This function possesses the digital filtered version of the spectrum
    """

    def __init__(self, a: Waveform, integration_time: float = 0.25, fob_band_width: int = 3, f0: float = 10,
                 f1: float = 10000):
        super().__init__(a, integration_time)

        self._bandwidth = fob_band_width
        self._start_frequency = f0
        self._stop_frequency = f1

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def start_frequency(self):
        return self._start_frequency

    @property
    def stop_frequency(self):
        return self._stop_frequency

    @property
    def settle_time(self):
        return self.settle_samples / self.sample_rate

    @property
    def settle_samples(self):
        """
        Based on requirements of Matlab filtering, you must have at least 3 times the number of coefficients to
        accurately filter data. So this will start with that minimum, and then move through the full octave frequency
        band numbers to determine the minimum number of samples that are required for the filter to adequately settle.
        """

        return self.spectra[0].settle_samples

    def _calculate_spectrogram(self):
        from ..waveform import trimming_methods

        """
        This function will divide the waveform up into contiguous sections of the waveform
        """

        #   Determine the maximum number of whole samples that exist within the waveform.
        N = int(np.floor(self.duration / self.integration_time))

        #   Create the list of spectra that will be used later
        self._spectra = np.empty((N,), dtype=SpectrumByDigitalFilters)

        #   Set the starting sample
        s0 = 0

        #   Loop through the elements and create the spectral object
        for n in range(N):
            #   get the subset of data from the waveform
            subset = self.waveform.trim(s0, s0 + self.sample_size, trimming_methods.samples)

            #   Create the spectrum object and add it as the ith element in the array
            self._spectra[n] = SpectrumByDigitalFilters(subset, self.bandwidth, self.start_frequency,
                                                          self.stop_frequency)

            #   increment the starting sample
            s0 += self.sample_size

    def calculate_engineering_scale_factor(self, calibration_level: float = 94, calibration_frequency=1000):
        sensitivities = np.zeros((len(self.spectra),))

        for i in range(len(self.spectra)):
            sensitivities[i] = self.spectra[i].calculate_engineering_unit_scale_factor(calibration_level,
                                                                                       calibration_frequency)

        return np.mean(sensitivities)
