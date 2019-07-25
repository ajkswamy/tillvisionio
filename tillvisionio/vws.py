import textfsm
import pkg_resources
import pandas as pd
import numpy as np
import pathlib as pl


def get_vws_log_template_filename():
    return pkg_resources.resource_filename('tillvisionio',
                                           "textfsm_templates/VWS_LOG_FSM_TEMPLATE.txt")


def is_snapshot(row_entry: pd.Series) -> bool:
    return row_entry["Timing_ms"].values == "(No calibration available)"


def load_pst(filename):
    """
    Implementation based on legacy code by Giovanni Galizia and Georg Raiser
    read tillvision based .pst files as uint16.
    """
    # filename can have an extension (e.g. .pst), or not
    # reading stack size from inf
    #inf_path = os.path.splitext(filename)[0] + '.inf'
    #this does not work for /data/030725bR.pst\\dbb10F, remove extension by hand,
    #assuming it is exactly 3 elements
    if filename[-4] == '.':
        filename = filename[:-4] #reomove extension
    meta = {}
    with open(filename+'.inf','r') as fh:
    #    fh.next()
        for line in fh.readlines():
            try:
                k,v = line.strip().split('=')
                meta[k] = v
            except:
                pass
    # reading stack from pst
    shape = np.int32((meta['Width'],meta['Height'],meta['Frames']))
    raw   = np.fromfile(filename+'.pst',dtype='int16')
    data  = np.reshape(raw,shape,order='F')

    # was swapping x, y axes; commented out to retain original order
    # data  = data.swapaxes(0,1)

    data = data.astype('uint16')
    return data


class VWSDataManager(object):

    def __init__(self, vws_log_file):

        self.vws_log_file = vws_log_file
        self.vws_log_file_path = pl.Path(vws_log_file)

        with open(self.vws_log_file) as vws_fle:
            vws_log_text = vws_fle.read()

        with open(get_vws_log_template_filename()) as template_fle:
            textfsm_template = textfsm.TextFSM(template_fle)
            data = textfsm_template.ParseText(vws_log_text)
            self.data_df = pd.DataFrame(columns=textfsm_template.header, data=data)
            self.data_df.replace("", np.NaN, inplace=True)
            self.data_df = self.data_df.apply(pd.to_numeric, errors='ignore')

    def get_measurement_metadata(self):
        """
        Get metadata of those entries having timing information
        :return: pandas.DataFrame
        """

        return self.data_df.loc[lambda s: ~is_snapshot(s), :]

    def get_snapshot_metadata(self):
        """
        Get metadata of those entries having timing information
        :return: pandas.DataFrame
        """

        return self.data_df.loc[lambda s: is_snapshot(s), :]

    def get_all_metadata(self):
        """
        Get all metadata entries
        :return: pandas.DataFrame
        """

        return self.data_df

    def get_image_data(self, label):
        """
        Get the image data contained in the pst file corresponding to the entry with label <label>
        :param label: string
        :return: numpy.ndarray converted to uint16
        """

        subset_matching_label = self.data_df.loc[lambda s: s["Label"] == label, :]

        assert subset_matching_label.shape[0] == 1, f"More than one entries found in {self.vws_log_file}" \
                                                    f"with label={label}"

        dbb_file_name_as_recorded = subset_matching_label["Location"].iloc[0]

        dbb_file_path_as_recorded = pl.PureWindowsPath(dbb_file_name_as_recorded)

        dbb_file_path_now = self.vws_log_file_path.parent / dbb_file_path_as_recorded.parts[-2] / \
                            dbb_file_path_as_recorded.parts[-1]

        image_data = load_pst(str(dbb_file_path_now))

        return image_data




