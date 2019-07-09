import textfsm
import pkg_resources
import pandas as pd


def get_vws_log_template_filename():
    return pkg_resources.resource_filename('tillvisionio',
                                           "textfsm_templates/VWS_LOG_FSM_TEMPLATE.txt")

class VWSDataManager(object):

    def __init__(self, vws_log_file):

        self.vws_log_file = vws_log_file

        with open(self.vws_log_file) as vws_fle:
            vws_log_text = vws_fle.read()

        with open(get_vws_log_template_filename()) as template_fle:
            textfsm_template = textfsm.TextFSM(template_fle)
            data = textfsm_template.ParseText(vws_log_text)
            self.data_df = pd.DataFrame(columns=textfsm_template.header, data=data)

    def get_measurement_metadata(self):

        pass

    def get_snapshot_metadata(self):

        pass





