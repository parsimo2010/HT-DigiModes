"""Measure a single recorded M17 test burst against its packed transmit vector."""
import argparse
from pathlib import Path

import numpy as np
from gnuradio.filter import firdes
from scipy import signal


def metrics(iq, vector):
    rate = 960000
    # One millisecond bins. The cropped recording includes idle on both sides.
    samples = iq[:len(iq) // 960 * 960].reshape(-1, 960)
    level = 10 * np.log10(np.maximum(np.mean(abs(samples) ** 2, axis=1), 1e-15))
    idle = np.median(np.r_[level[:50], level[-50:]])
    active = np.flatnonzero(level > idle + 10)
    runs = [r for r in np.split(active, np.flatnonzero(np.diff(active) > 2) + 1) if len(r) >= 10]
    if not runs:
        raise ValueError("No RF burst 10 dB above idle")
    run = max(runs, key=len)
    start, end = int(run[0]), int(run[-1]) + 1
    rf = iq[start * 960:end * 960]

    # Fit the non-repeating LSF and six stream frames independently. The fitted
    # offset and gain are in Hz and Hz per unit symbol level, respectively.
    lowpass = signal.firwin(401, 18000, fs=rate)
    narrow = signal.resample_poly(iq, 1, 20, window=lowpass)
    fm = np.angle(narrow[1:] * narrow[:-1].conj()).astype(float) * 48000 / (2 * np.pi)
    levels = (1, 3, -1, -3)
    symbols = [levels[(v >> shift) & 3] for v in vector for shift in (6, 4, 2, 0)]
    taps = firdes.root_raised_cosine(10, 10, 1, 0.2, 121)
    reference = signal.upfirdn(taps, symbols, up=10)[60:]
    n = 1920
    window = np.ones(n) / n
    means = signal.fftconvolve(fm, window, mode="valid")
    variance = np.maximum(signal.fftconvolve(fm ** 2, window, mode="valid") - means ** 2, 1e-9)
    positions, offsets, gains = [], [], []
    for frame in range(1, 8):
        v = reference[frame * n:(frame + 1) * n]
        covariance = signal.correlate(fm, v - v.mean(), mode="valid", method="fft") / n
        rho = covariance / np.sqrt(variance * v.var())
        at = int(np.argmax(rho))
        if rho[at] < 0.75:
            raise ValueError(f"Could not locate complete reference frame {frame}")
        positions.append(at)
        gains.append(covariance[at] / v.var())
        offsets.append(means[at] - gains[-1] * v.mean())
    if not np.all(abs(np.diff(positions) - n) < 10):
        raise ValueError("Reference frames do not have consecutive 40 ms intervals")
    period = np.polyfit(np.arange(7) * 192, positions, 1)[0] / 48000

    # Integrate the noise-subtracted two-sided PSD within +/-35 kHz. Exclude
    # 8 ms at each key transition to describe the modulated occupied spectrum.
    f, psd = signal.welch(rf[7680:-7680], rate, nperseg=8192, return_onesided=False)
    f, psd = np.fft.fftshift(f), np.fft.fftshift(psd)
    band = abs(f) < 35000
    p = np.maximum(psd[band] - np.median(psd[band]), 0)
    cumulative = (p.cumsum() - 0.5 * p) / p.sum()
    edges = np.interp([0.005, 0.995], cumulative, f[band])
    return {
        "duration_ms": end - start, "idle_dbfs": idle, "burst_dbfs": np.median(level[run]),
        "peak_component_fs": max(abs(rf.real).max(), abs(rf.imag).max()),
        "symbols_per_second": 1 / period, "offset_hz": np.median(offsets),
        "outer_deviation_hz": 3 * np.median(gains), "occupied_99_hz": edges[1] - edges[0],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("iq", type=Path, help="960 ksample/s complex float32, one burst and at least 50 ms idle on each side")
    parser.add_argument("vector", type=Path, help="432 bytes in modem transmit order")
    args = parser.parse_args()
    vector = args.vector.read_bytes()
    if len(vector) != 432:
        parser.error("expected the 432-byte physical PTT vector")
    iq = np.fromfile(args.iq, dtype="<c8")
    if len(iq) < 460800:
        parser.error("expected a complete burst with idle on each side")
    for key, value in metrics(iq, vector).items():
        print(f"{key}={value:.4f}")


if __name__ == "__main__":
    main()
