import numpy as np
from custom_interface import MyInterface
from biosiglive.gui.plot import LivePlot
from biosiglive import (
    # LivePlot,
    save,
    load,
    ViconClient,
    RealTimeProcessingMethod,
    RealTimeProcessing,
    PlotType,
)

from time import sleep, time

try:
    import biorbd
except ImportError:
    pass


def get_custom_function(device_interface):
    custom_processing = RealTimeProcessing(
        data_rate=device_interface.get_device(name="emg").rate, processing_window=1000
    )
    custom_processing.bpf_lcut = 10
    custom_processing.bpf_hcut = 425
    custom_processing.lpf_lcut = 5
    custom_processing.lp_butter_order = 4
    custom_processing.bp_butter_order = 2
    custom_processing.moving_average_windows = 200
    return custom_processing.process_emg


if __name__ == "__main__":
    try_offline = True

    output_file_path = "trial_x.bio"
    if try_offline:
        interface = MyInterface(system_rate=100, data_path="abd.bio")
        # Get prerecorded data from pickle file for a shoulder abduction
        # offline_emg = load("abd.bio")["emg"]
    else:
        # init trigno community client
        interface = ViconClient(ip="localhost", system_rate=100)

    # Add markerSet to Vicon interface
    n_electrodes = 4

    muscle_names = [
        "Pectoralis major",
        "Deltoid anterior",
        "Deltoid medial",
        "Deltoid posterior",
    ]

    # Add device to Vicon interface
    interface.add_device(
        nb_channels=n_electrodes,
        device_type="emg",
        name="emg",
        rate=2000,
        device_data_file_key="emg",
        processing_method=RealTimeProcessingMethod.ProcessEmg,
        # moving_average_window=600,
        moving_average=False,
        absolute_value=False,
    )

    # Add plot
    emg_plot = LivePlot(
        name="emg", rate=100, plot_type=PlotType.Curve, nb_subplots=n_electrodes, channel_names=muscle_names
    )
    emg_plot.init(plot_windows=10000, y_labels="Processed EMG (mV)")

    emg_raw_plot = LivePlot(
        name="emg_raw", rate=100, plot_type=PlotType.Curve, nb_subplots=n_electrodes, channel_names=muscle_names
    )
    emg_raw_plot.init(plot_windows=10000, colors=(255, 0, 0), y_labels="EMG (mV)")

    time_to_sleep = 1 / 100
    count = 0
    while True:
        tic = time()
        raw_emg = interface.get_device_data(device_name="emg")
        emg_proc = interface.devices[0].process()
        emg_plot.update(emg_proc[:, -20:])
        emg_raw_plot.update(raw_emg)
        count += 1
        loop_time = time() - tic
        real_time_to_sleep = time_to_sleep - loop_time
        if real_time_to_sleep > 0:
            sleep(real_time_to_sleep)
