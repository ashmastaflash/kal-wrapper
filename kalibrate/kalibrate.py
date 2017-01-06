import os
import fn
import subprocess


class Kal:
    """A valid file is required here- the path to
    the kal binary.  Oftentimes located at /usr/bin/kal

    This was built and tested against kalibrate for rtl-sdr
    """

    def __init__(self, kal_bin):
        self.kal_bin = kal_bin
        if not os.path.isfile(kal_bin):
            errno = 69
            err_txt = "Kal binary not at location specified: %s" % kal_bin
            raise IOError(errno, err_txt)

    def scan_band(self, band, **kwargs):
        """Run Kalibrate for a band.

        Supported keyword arguments:
        gain    -- Gain in dB
        device  -- Index of device to be used
        error   -- Initial frequency error in ppm

        """

        kal_run_line = fn.build_kal_scan_band_string(self.kal_bin,
                                                     band, kwargs)
        raw_output = subprocess.check_output(kal_run_line.split(' '),
                                             stderr=subprocess.STDOUT)
        kal_normalized = fn.parse_kal_scan(raw_output)
        return kal_normalized

    def scan_channel(self, channel, **kwargs):
        """Run Kalibrate.

        Supported keyword arguments:
        gain    -- Gain in dB
        device  -- Index of device to be used
        error   -- Initial frequency error in ppm

        """

        kal_run_line = fn.build_kal_scan_channel_string(self.kal_bin,
                                                        channel, kwargs)
        raw_output = subprocess.check_output(kal_run_line.split(' '),
                                             stderr=subprocess.STDOUT)
        kal_normalized = fn.parse_kal_channel(raw_output)
        return kal_normalized
