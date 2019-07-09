from tillvisionio.vws import VWSDataManager


def VWS_read_test():
    """
    Testing the initialization of a tillvisionio.vws.VWSDataManager with a vws.log file
    """
    test_file = "tests/testFiles/HS_bee_OXON_PELM_180718.vws.log"
    vws_data = VWSDataManager(test_file)
    assert vws_data.data_df.shape == (34, 22)
