from kalibrate import sanity

class TestSanity:
    def test_gsm850(self):
        assert sanity.scan_band_is_valid("GSM850")

    def test_gsm900(self):
        assert sanity.scan_band_is_valid("GSM900")

    def test_gsm_r(self):
        assert sanity.scan_band_is_valid("GSM-R")

    def test_egsm(self):
        assert sanity.scan_band_is_valid("EGSM")

    def test_dcs(self):
        assert sanity.scan_band_is_valid("DCS")

    def test_pcs(self):
        assert sanity.scan_band_is_valid("PCS")

    def test_bad_band(self):
        assert not sanity.scan_band_is_valid("BAD-BAND")
