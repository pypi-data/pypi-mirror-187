import numpy as np
import struct
from ..waveform import Waveform
from .wavefile import WaveFile
import os.path
from datetime import datetime
from dateutil import parser


class StandardBinaryFile(Waveform):
    """
    This class holds the data for the standard ANSI Standard S12.75 formated
    binary files.  The class will permit access to the data, the header, and
    specific elements of the header that are required for various analyses that
    may be required.

    @author: frank mobley

    """

    def __init__(self, filename: str = None, wfm: Waveform = None):
        """
        This function is the default constructor that loads the data from the filename that is provided in the argument
        list.  This will load the header and the acoustic data into a series of arrays and DataFrames.

        Parameters
        ----------
        filename : STRING
            This is the full path to the location of the file that we want to load into the class


        Returns
        -------
        None.

        """

        self.header = None

        if filename is not None:
            try:
                #   Open the file for reading in binary format

                f_in = open(filename, 'rb')

                #   Read the lines of header information

                name, value = StandardBinaryFile.convert_header(StandardBinaryFile.read_line(f_in))

                #   This is the header line, so now we can determine how many total
                #   lines of header information is present in the file

                self.header_line_count = int(value)

                #   Read through the remainder of the header lines and parse out the
                #   information that is required as we go

                self.header = dict()
                for i in range(self.header_line_count - 1):

                    name, value = StandardBinaryFile.convert_header(StandardBinaryFile.read_line(f_in))

                    self.header[name] = value

                    cmd = name.upper()

                    if cmd == 'TIME (UTC ZULU)':
                        self.time0 = parser.parse(value)
                    elif cmd == 'SAMPLE RATE (HZ)':
                        self.fs = float(value)
                    elif cmd == 'SAMPLES TOTAL':
                        self.sample_count = int(value)

                #   Read the data

                self._samples = np.asarray(struct.unpack('f' * self.sample_count, f_in.read(4 * self.sample_count)))

                #   close the file

                f_in.close()
            except IndexError:
                f_in.close()

                raise ValueError()
            except ValueError:
                f_in.close()

                raise ValueError()
        elif wfm is not None:
            super().__init__(wfm.samples, wfm.sample_rate, wfm.start_time)
            self.header = None
        else:
            self._samples = None
            self.fs = None
            self.time0 = None
            self.header = None

    @staticmethod
    def convert_header(header_line):
        """
        This function will take the information within the header line and remove
        the semicolon in the front and all elipsoid markers to determine the name
        of the property.  It also splits based on the colon to determine the value

        @author: Frank Mobley

        Parameters
        ----------
        header_line : STRING
            The line of text from the header of the file

        Returns
        -------
        name : STRING
            The name of the property or attribute

        value : STRING
            The value of the property

        """

        #   Split the string based on the colon

        elements = header_line.split(':')

        if len(elements) > 2:
            value = ':'.join(elements[1:])
        else:
            value = elements[1].strip()
        name = elements[0][1:].split('.')[0]

        return name, value

    @staticmethod
    def read_line(binary_file):
        """
        Python does not provide the ability to read a line of text from a
        binary file.  This function will read from the current position in the
        file to the new line character.  The set of bytes is then converted to
        a string and returned to the calling function.

        @author: frank Mobley

        Parameters
        ----------
        binary_file : FILE
            The file pointer that will be read from

        Returns
        -------
        The string representing a line of ASCII characters from the file.

        """

        #   Get the current position within the file so that we can return here
        #   after determining where the end of the file is.

        current_position = binary_file.tell()

        #   Find the end of the file

        binary_file.seek(-1, 2)

        eof = binary_file.tell()

        #   Return to the point we were within the file

        binary_file.seek(current_position, 0)

        #   Read until the last character is a new line or we have reached the
        #   end of the file.

        characters = ''
        char = ' '
        while ord(char) != 10 or binary_file.tell() == eof - 1:
            char = binary_file.read(1)
            if ord(char) != 10:
                characters += char.decode()

        return characters

    @staticmethod
    def write_std_binary_file(wfm, orig_header, output_filename):
        """
        Static method that given a generic_time_waveform object and a header dict writes a standard binary file
        according to ANSI S12.75
        Parameters
        ----------
        wfm : generic_time_waveform object
            Waveform of measured data.

        orig_header : dict
            Header info.

        output_filename : str
            Output file path with full name of file and extension.
        """
        # Check that correct data type were given as inputs
        if not (isinstance(wfm, Waveform)) or not (isinstance(orig_header, dict)) or \
                not (isinstance(output_filename, str)):

            raise ValueError("Incorrect inputs, check that wfm is a generic time waveform object, header is a dict and "
                             "output_filename is a str that's a full file path to the output directory")

        header = orig_header.copy()

        # Append sample format and encoding method if they dont exist to the header dict

        header['SAMPLE RATE (HZ)'] = int(np.floor((wfm.sample_rate)))
        header['SAMPLES TOTAL'] = len(wfm.samples)
        header['TIME (UTC ZULU)'] = wfm.start_time.strftime('%Y/%m/%d %H:%M:%S.%f')
        header['SAMPLE FORMAT'] = "LITTLE ENDIAN"
        header['DATA FORMAT'] = 'REAL*4'

        # Check to see if output path exist and open file if it doesn't exist

        if not os.path.exists(output_filename):
            f = open(output_filename, 'wb')

            # Write header info from dict

            header_line = ';{}'.format("HEADER SIZE").ljust(41, '.') + ': {}\n'.format(len(header.keys())+1)
            f.write(header_line.encode('utf-8'))

            for key in header.keys():
                header_line = ';{}'.format(key.upper()).ljust(41, '.') + ': {}\n'.format(header[key])
                f.write(header_line.encode('utf-8'))

            # Write pressure data to end of file

            for i in range(len(wfm.samples)):
                f.write(struct.pack('<f', wfm.samples[i]))
            f.close()

    def make_wav_file(self, wav_path, archival_location=None, artist=None, commissioning_organization=None,
                      copyright=None, cropping_information=None, originating_object_dimensions=None, engineer_name=None,
                      subject_genre=None, key_words=None, originating_object_medium=None, title=None, subject_name=None,
                      description=None, data_source=None, original_form=None, digitizing_engineer=None,
                      track_number=None):
        """
        The data within the header can be created with the LIST chunk that is common with audio files.  This requires
        the generation of a set of information within the meta_data element of the id3_wave_file that forms the
        information, which is typically at the end of the audio file.  This function converts the data within the
        StandardBinaryFile into a scaled version of the wave file with a LIST tag dataset.
        :param wav_path: str - the output of path for the file
        :param archival_location: str - the location of the original and all additional copies of the data
        :param artist: str - the person who is making the recording
        :param commissioning_organization: str - the organization that requested the measurement
        :param copyright: str - any description of the copyright and classification of the data within the file
        :param cropping_information: str - was the data cropped, is so what was the start and stop sample
        :param originating_object_dimensions: str - any information regarding the dimensions of the object that was
            recorded
        :param engineer_name : str - the name of the engineer that recorded the data
        :param subject_genre : str - the genre of the data
        :param key_words: str - a comma delimited collection of key words that describes this data
        :param originating_object_medium: str - what was the original medium that contained this data
        :param title: str - the title of the file
        :param subject_name: str - a name for the subject of the file
        :param description: str - further descriptions of the data within this file
        :param data_source: str - the name of the source of the data, which is different from the commissioned
            organization in that we want to know where the digital file came from
        :param original_form: str - a description of the original form that this data existed in before the wav file
            was created
        :param digitizing_engineer: str - the name/identifier of the individual who is creating this file - if not
            supplied the username of the individual logged into the computer running this code is used
        :param track_number: int - the track number for this wav file
        """

        #   get the username of the person running this code

        import getpass
        username = getpass.getuser()

        #   Create the wave_file

        wav = WaveFile()

        #   Add the header information to the class

        for key in self.header.keys():
            wav.header[key] = self.header[key]

        #   Now we need to put the generic_time_waveform information into the class object

        wav.samples = self.samples
        wav.start_time = self.time0
        wav.sample_rate = self.sample_rate

        #   Now we can create the specific tags within the common LIST chunk with information from the header

        if archival_location is not None:
            wav.archival_location = archival_location
        if artist is not None:
            wav.artist = artist
        if commissioning_organization is not None:
            wav.commissioning_organization = commissioning_organization
        if copyright is not None:
            wav.copyright = copyright

        wav.creation_date = datetime.now()

        if cropping_information is not None:
            wav.cropping_information = cropping_information
        if originating_object_dimensions is not None:
            wav.originating_object_dimensions = originating_object_dimensions
        if engineer_name is not None:
            wav.engineer_name = engineer_name
        else:
            wav.engineer_name = username
        if subject_genre is not None:
            wav.subject_genre = subject_genre
        if key_words is not None:
            wav.key_words = key_words
        if originating_object_medium is not None:
            wav.originating_object_medium = originating_object_medium
        if title is not None:
            wav.title = title
        else:
            wav.title = os.path.basename(wav_path)
        if subject_name is not None:
            wav.subject_name = subject_name
        if description is not None:
            wav.description = description

        wav.creation_software = "Python, AFRL_Physical_Acoustics "

        if data_source is not None:
            wav.data_source = data_source
        if original_form is not None:
            wav.original_form = original_form
        if digitizing_engineer is not None:
            wav.digitizing_engineer = digitizing_engineer
        else:
            wav.digitizing_engineer = username

        if track_number is not None:
            wav.track_number = track_number

        #   Save the data to the file

        if not(os.path.exists(os.path.dirname(wav_path))):
            os.makedirs(os.path.dirname(wav_path))

        wav.normalized = True
        wav.save(wav_path)


