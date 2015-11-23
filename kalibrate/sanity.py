def scan_band_is_valid(band):
    supported_bands = ["GSM850",
                       "GSM-R",
                       "GSM900",
                       "EGSM",
                       "DCS",
                       "PCS"]
    if band in supported_bands:
        return True
    else:
        return False
