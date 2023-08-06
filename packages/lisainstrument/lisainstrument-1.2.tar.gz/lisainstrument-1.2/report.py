#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produce various plots as a reporting and diagnostic tool.

The 'report' continuous-integration job runs various simulations with
different configurations (mostly individually-enabled noises), and produces
plots. These plots are used as quick human-eye diagnostic tool.
"""

import logging
import datetime
from multiprocessing import Process
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.signal import welch
from lisainstrument import Instrument
from lisainstrument.containers import ForEachMOSA, ForEachSC
from lisainstrument import __version__


logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


PARALLEL = False
"""bool: Whether to run reports in parallel"""

NPERSEG = 2**16 # ~ 65_000
"""int: Number of segments for Welch averaging"""

SIZE = NPERSEG * 3 # ~ 196_000
"""int: Size of simulations [samples]"""


def main():
    """Main function."""

    logging.info("Starting report")

    processes = [
        Process(target=func)
        for func in [
            no_noise,
            laser,
            testmass,
            oms,
            backlink,
            clock,
            ranging,
            modulation,
            jitter,
            dws,
            moc_time_correlation,
        ]
    ]

    for process in processes:
        process.start()
        if not PARALLEL:
            process.join()

    if PARALLEL:
        for process in processes:
            process.join()

    logging.info("Report complete")


def no_noise():
    """No-noise simulation."""

    logging.info("Running no-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.disable_all_noises()
    instru.write('no-noise.h5', mode='w')

    with PdfPages('no-noise.pdf') as pdf:

        plot_measurements(instru, pdf)
        write_metadata('no-noise', instru.orbit_file, pdf)


def laser():
    """Laser-noise simulation."""

    logging.info("Running laser-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.disable_all_noises(but='laser')
    instru.write('laser-noise.h5', mode='w')

    with PdfPages('laser-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.laser_noises[mosa], label=mosa)
        plt.ylabel('Frequency [Hz]')
        plt.title('Laser noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.laser_noises[mosa], label=mosa)
        plt.ylabel('ASD [Hz/sqrt(Hz)]')
        plt.title('Laser noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('laser-noise', instru.orbit_file, pdf)


def testmass():
    """Test mass-noise simulation."""

    logging.info("Running test mass-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_jitters()
    instru.backlink_asds = ForEachMOSA(0)
    instru.oms_isi_carrier_asds = ForEachMOSA(0)
    instru.oms_isi_usb_asds = ForEachMOSA(0)
    instru.oms_tmi_carrier_asds = ForEachMOSA(0)
    instru.oms_tmi_usb_asds = ForEachMOSA(0)
    instru.oms_rfi_carrier_asds = ForEachMOSA(0)
    instru.oms_rfi_usb_asds = ForEachMOSA(0)
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('testmass-noise.h5', mode='w')

    with PdfPages('testmass-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.testmass_noises[mosa], label=mosa)
        plt.ylabel('Velocity [m/s]')
        plt.title('Test-mass noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.testmass_noises[mosa], label=mosa)
        plt.ylabel('ASD [m/s/sqrt(Hz)]')
        plt.title('Test-mass noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('testmass-noise', instru.orbit_file, pdf)


def oms():
    """OMS-noise simulation."""

    logging.info("Running OMS-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_jitters()
    instru.backlink_asds = ForEachMOSA(0)
    instru.testmass_asds = ForEachMOSA(0)
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('oms-noise.h5', mode='w')

    with PdfPages('oms-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_isi_carrier_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS ISI carrier noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_tmi_carrier_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS TMI carrier noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_rfi_carrier_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS RFI carrier noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_isi_usb_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS ISI upper-sideband noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_tmi_usb_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS TMI upper-sideband noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.oms_rfi_usb_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('OMS RFI upper-sideband noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('oms-noise', instru.orbit_file, pdf)


def backlink():
    """Backlink-noise simulation."""

    logging.info("Running backlink-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_jitters()
    instru.testmass_asds = ForEachMOSA(0)
    instru.oms_isi_carrier_asds = ForEachMOSA(0)
    instru.oms_isi_usb_asds = ForEachMOSA(0)
    instru.oms_tmi_carrier_asds = ForEachMOSA(0)
    instru.oms_tmi_usb_asds = ForEachMOSA(0)
    instru.oms_rfi_carrier_asds = ForEachMOSA(0)
    instru.oms_rfi_usb_asds = ForEachMOSA(0)
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('backlink-noise.h5', mode='w')

    with PdfPages('backlink-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.backlink_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('Backlink noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('backlink-noise', instru.orbit_file, pdf)


def clock():
    """Clock-noise simulation."""

    logging.info("Running clock-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_ranging_noises()
    instru.disable_jitters()
    instru.disable_pathlength_noises()
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('clock-noise.h5', mode='w')

    with PdfPages('clock-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_tseries(instru.physics_t, instru.clock_noise_offsets[sc], label=sc)
        plt.ylabel('Fractional frequency deviations')
        plt.title('Clock noise offsets')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_tseries(instru.physics_t, instru.clock_noise_fluctuations[sc], label=sc)
        plt.ylabel('Fractional frequency deviations')
        plt.title('Clock noise fluctuations')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_asd(instru.physics_t, instru.clock_noise_fluctuations[sc], label=sc)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('Clock noise fluctuations')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('clock-noise', instru.orbit_file, pdf)


def ranging():
    """Ranging-noise simulation."""

    logging.info("Running ranging-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_jitters()
    instru.disable_pathlength_noises()
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('ranging-noise.h5', mode='w')

    with PdfPages('ranging-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.ranging_biases[mosa], label=mosa)
        plt.ylabel('Time [s]')
        plt.title('Ranging bias')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.ranging_noises[mosa], label=mosa)
        plt.ylabel('Time [s]')
        plt.title('Ranging noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.ranging_noises[mosa], label=mosa)
        plt.ylabel('ASD [s/sqrt(Hz)]')
        plt.title('Ranging noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('ranging-noise', instru.orbit_file, pdf)


def modulation():
    """Modulation-noise simulation."""

    logging.info("Running modulation-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_jitters()
    instru.disable_pathlength_noises()
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('modulation-noise.h5', mode='w')

    with PdfPages('modulation-noise.pdf') as pdf:\

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.modulation_noises[mosa], label=mosa)
        plt.ylabel('Fractional frequency deviations')
        plt.title('Modulation noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.modulation_noises[mosa], label=mosa)
        plt.ylabel('ASD [/sqrt(Hz)]')
        plt.title('Modulation noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('modulation-noise', instru.orbit_file, pdf)


def jitter():
    """Angular jitter-noise simulation."""

    logging.info("Running angular jitter-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_pathlength_noises()
    instru.dws_asds = ForEachMOSA(0)
    instru.sync_asds = ForEachSC(0)
    instru.write('jitter-noise.h5', mode='w')

    with PdfPages('jitter-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_asd(instru.physics_t, instru.sc_jitter_phis[sc], label=f'Phi {sc}')
            plot_asd(instru.physics_t, instru.sc_jitter_etas[sc], label=f'Eta {sc}')
            plot_asd(instru.physics_t, instru.sc_jitter_thetas[sc], label=f'Theta {sc}')
        plt.ylabel('ASD [rad/s/sqrt(Hz)]')
        plt.title('Spacecraft angular jitter noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.mosa_jitter_phis[mosa], label=f'Phi {mosa}')
            plot_asd(instru.physics_t, instru.mosa_jitter_etas[mosa], label=f'Eta {mosa}')
        plt.ylabel('ASD [rad/s/sqrt(Hz)]')
        plt.title('MOSA angular jitter noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('jitter-noise', instru.orbit_file, pdf)


def dws():
    """DWS-noise simulation."""

    logging.info("Running DWS-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.laser_asds = ForEachMOSA(0)
    instru.modulation_asds = ForEachMOSA(0)
    instru.disable_clock_noises()
    instru.disable_ranging_noises()
    instru.disable_pathlength_noises()
    instru.disable_jitters()
    instru.sync_asds = ForEachSC(0)
    instru.write('dws-noise.h5', mode='w')

    with PdfPages('dws-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_tseries(instru.physics_t, instru.dws_phi_noises[mosa], label=f'Phi {mosa}')
            plot_tseries(instru.physics_t, instru.dws_eta_noises[mosa], label=f'Eta {mosa}')
        plt.ylabel('Angular velocity [rad/s]')
        plt.title('DWS measurement noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for mosa in instru.MOSAS:
            plot_asd(instru.physics_t, instru.dws_phi_noises[mosa], label=f'Phi {mosa}')
            plot_asd(instru.physics_t, instru.dws_eta_noises[mosa], label=f'Eta {mosa}')
        plt.ylabel('ASD [rad/s/sqrt(Hz)]')
        plt.title('DWS measurement noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('dws-noise', instru.orbit_file, pdf)


def moc_time_correlation():
    """MOC time correlation-noise simulation."""

    logging.info("Running MOC time correlation-noise simulation")

    instru = Instrument(
        size=SIZE,
        orbits='tests/esa-trailing-orbits-2-0.h5',
        concurrent=True,
    )
    instru.disable_all_noises(but='moc-time-correlation')
    instru.write('moc-time-correlation-noise.h5', mode='w')

    with PdfPages('moc-time-correlation-noise.pdf') as pdf:

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_tseries(instru.physics_t, instru.moc_time_correlations[sc], label=sc)
        plt.ylabel('Time [s]')
        plt.title('MOC time correlation noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plt.figure(figsize=(16, 8))
        for sc in instru.SCS:
            plot_asd(instru.physics_t, instru.moc_time_correlations[sc], label=sc)
        plt.ylabel('ASD [s/sqrt(Hz)]')
        plt.title('MOC time correlation noise')
        plt.legend()
        pdf.savefig()
        plt.close()

        plot_measurements(instru, pdf)
        write_metadata('moc-time-correlation-noise', instru.orbit_file, pdf)


def plot_measurements(instru, pdf):
    """Generate plots for all measurements.

    Args:
        instru (Instrument): instrument instance
        pdf (PdfPages): PDF file instance
    """

    # Time-domain ISI carrier total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.isi_carriers[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.isi_carrier_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total ISI carrier beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain TMI carrier total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.tmi_carriers[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.tmi_carrier_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total TMI carrier beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain RFI carrier total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.rfi_carriers[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.rfi_carrier_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total RFI carrier beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain ISI upper-sideband total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.isi_usbs[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.isi_usb_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total ISI upper-sideband beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain TMI upper-sideband total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.tmi_usbs[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.tmi_usb_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total TMI upper-sideband beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain RFI upper-sideband total and offset beatnote frequencies
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.rfi_usbs[mosa], label=f'{mosa} (total)')
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.rfi_usb_offsets[mosa], linestyle='--', label=f'{mosa} (offsets)')
    plt.ylabel('Frequency [Hz]')
    plt.title('Total RFI upper-sideband beatnote frequencies')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD ISI carrier beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.isi_carrier_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('ISI carrier beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD TMI carrier beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.tmi_carrier_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('TMI carrier beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD RFI carrier beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.rfi_carrier_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('RFI carrier beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD ISI upper-sideband beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.isi_usb_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('ISI upper-sideband beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD TMI upper-sideband beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.tmi_usb_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('TMI upper-sideband beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD RFI upper-sideband beatnote frequency fluctuations
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.rfi_usb_fluctuations[mosa], label=mosa)
    plt.ylabel('ASD [Hz/sqrt(Hz)]')
    plt.title('RFI upper-sideband beatnote frequency fluctuations')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain MPR measurements
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_tseries(instru.t, instru.mprs[mosa], label=mosa)
    plt.ylabel('MPR [s]')
    plt.title('Measured pseudo-ranges (MPRs)')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD MPR measurements
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.mprs[mosa], detrend='linear', label=mosa)
    plt.ylabel('ASD [s/sqrt(Hz)]')
    plt.title('Measured pseudo-ranges (MPRs)')
    plt.legend()
    pdf.savefig()
    plt.close()

    # ASD DWS measurements
    plt.figure(figsize=(16, 8))
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.isi_dws_phis[mosa], label=f'DWS Phi {mosa}')
    for mosa in instru.MOSAS:
        plot_asd(instru.t, instru.isi_dws_etas[mosa], label=f'DWS Eta {mosa}')
    plt.ylabel('ASD [rad/s/sqrt(Hz)]')
    plt.title('Differential wavefront sensor (DWS) measurements')
    plt.legend()
    pdf.savefig()
    plt.close()

    # Time-domain TCB timer deviations
    plt.figure(figsize=(16, 8))
    for sc in instru.SCS:
        plot_tseries(instru.t, instru.tcb_timer_deviations[sc], skip=0, label=sc)
    plt.ylabel('Timer deviation [s]')
    plt.title('Timer deviations from TCB')
    plt.legend()
    pdf.savefig()
    plt.close()


def plot_tseries(x, y, skip=100, **kwargs):
    """Plot time series."""

    if 'alpha' not in kwargs:
        kwargs['alpha'] = 0.7

    x, y = np.broadcast_arrays(x, y)
    plt.plot(x[skip:], y[skip:], **kwargs)
    plt.xlabel('Time [s]')
    plt.grid(True)


def plot_asd(x, y, detrend=None, **kwargs):
    """Plot amplitude spectral density."""

    if 'alpha' not in kwargs:
        kwargs['alpha'] = 0.7

    x, y = np.broadcast_arrays(x, y)
    freq, psd = welch(
        y[300:],
        fs=1.0 / (x[1] - x[0]),
        nperseg=NPERSEG,
        window=('kaiser', 40),
        detrend=detrend)

    plt.loglog(freq, np.sqrt(psd), **kwargs)
    plt.xlabel('Frequency [Hz]')
    plt.grid(True)


def write_metadata(config, orbits, pdf):
    """Write metadata.

    Args:
        config (str): description of instrument configuration
        orbits (str): description of orbit file
        pdf(PdfPages): PDF file instance
    """
    info = pdf.infodict()
    info['Title'] = 'LISA Instrument Report'
    info['Author'] = 'LISA Instrument Continuous Integration'
    info['InstrumentConfiguration'] = config
    info['OrbitFile'] = orbits
    info['Version'] = __version__
    info['CreationDate'] = datetime.datetime.now()
    info['ModDate'] = datetime.datetime.now()


if __name__ == "__main__":
    main()
