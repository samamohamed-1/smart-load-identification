import serial
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, sosfiltfilt
from scipy.ndimage import uniform_filter1d
import joblib
import requests

plt.style.use('bmh')

# =========================
# CONFIGURATION
# =========================
FILTER_TYPE = "moving_average"
BUTTER_CUTOFF_HZ = 800
BUTTER_ORDER = 4
MOVING_AVG_WINDOW = 7
FS = 2380

PHASE_CALIBRATION_SAMPLES = 0
PHASE_CALIBRATION_FRAC = 0.0

VI_SMOOTH_WINDOW = 20

# =========================
# BLYNK & TELEGRAM CONFIG
# =========================
BLYNK_TOKEN = ""   #priv  ---use your own tocken
BLYNK_BASE = "https://blynk.cloud/external/api/update"

BOT_TOKEN = ""     #priv ---use your own tocken
CHAT_ID = ""       #---use your own chat IDs

# =========================
# ENERGY CONFIG
# =========================
PRICE_PER_KWH = 50
cumulative_energy = 0.0


# =========================
# COLLECT DATA FROM BLUETOOTH
# =========================
def collect_data_from_bt(port="COM7", baud=115200, file_name="data.csv"):
    ser = serial.Serial(port, baud, timeout=1)
    data = []
    print("Receiving data...")
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line == "END":
            break
        try:
            v, i = line.split(",")
            data.append([float(v), float(i)])
        except:
            pass
    with open(file_name, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Voltage", "Current"])
        writer.writerows(data)
    print("Saved CSV:", file_name)
    return file_name


# =========================
# READ DATA
# =========================
def read_data(path):
    df = pd.read_csv(path)
    voltage = df.iloc[:, 0].values.astype(float)
    current = df.iloc[:, 1].values.astype(float)
    return voltage, current


# =========================
# DC OFFSET REMOVAL
# =========================
def remove_dc_offset(signal):
    return signal - np.mean(signal)


# =========================
# DIGITAL FILTERING
# =========================
def butterworth_lowpass(signal, cutoff_hz, fs, order=4):
    nyq = fs / 2.0
    normal_cutoff = cutoff_hz / nyq
    normal_cutoff = np.clip(normal_cutoff, 1e-4, 0.9999)
    sos = butter(order, normal_cutoff, btype='low', analog=False, output='sos')
    return sosfiltfilt(sos, signal)


def moving_average_filter(signal, window=11):
    return uniform_filter1d(signal, size=window, mode='nearest')


def filter_signal(signal, filter_type=FILTER_TYPE):
    signal = remove_dc_offset(signal)
    if filter_type == "butterworth":
        return butterworth_lowpass(signal, BUTTER_CUTOFF_HZ, FS, BUTTER_ORDER)
    elif filter_type == "moving_average":
        return moving_average_filter(signal, MOVING_AVG_WINDOW)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")
 
# =========================
# METRICS CALCULATION
# =========================
def calculate_metrics(v, i):
    v = v - np.mean(v)
    i = i - np.mean(i)
    v_rms = np.sqrt(np.mean(v ** 2))
    i_rms = np.sqrt(np.mean(i ** 2))
    power = np.mean(v * i)
    apparent = v_rms * i_rms
    pf = power / (apparent + 1e-9)
    return v_rms, i_rms, pf


def calculate_thd(i):
    i = i - np.mean(i)
    fft_vals = np.fft.rfft(i)
    mag = np.abs(fft_vals)
    mag[0] = 0
    fundamental = np.max(mag)
    if fundamental == 0:
        return 0
    harmonics = np.sqrt(np.sum(mag ** 2) - fundamental ** 2)
    return harmonics / (fundamental + 1e-9)


def crest_factor(i):
    i = i - np.mean(i)
    rms = np.sqrt(np.mean(i ** 2))
    peak = np.max(np.abs(i))
    return peak / (rms + 1e-9)


def calculate_energy_cost(active_power, signal_length, fs=FS):
    batch_seconds = signal_length / fs
    batch_hours = batch_seconds / 3600.0
    energy_kwh = abs(active_power) * batch_hours / 1000.0
    cost_egp = energy_kwh * PRICE_PER_KWH
    return energy_kwh, cost_egp


# =========================
# COMMUNICATION FUNCTIONS
# =========================
def send_to_blynk(pin, value):
    try:
        url = f"{BLYNK_BASE}?token={BLYNK_TOKEN}&{pin}={value}"
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            print(f"   Blynk {pin.upper()} = {value}")
        else:
            print(f"   Blynk {pin.upper()} failed: {r.status_code}")
    except Exception as e:
        print(f"   Blynk error on {pin}: {e}")


def send_all_to_blynk(power, v_rms, i_rms, load_name, energy_kwh, cost_egp):
    print("\n Sending to Blynk...")
    send_to_blynk("v1", round(power, 4))
    send_to_blynk("v2", round(v_rms, 4))
    send_to_blynk("v4", load_name)
    send_to_blynk("v3", round(i_rms, 5))
    send_to_blynk("v5", round(energy_kwh, 6))
    send_to_blynk("v6", round(cost_egp, 4))


def send_telegram(power, v_rms, i_rms, load_name, energy_kwh, cost_egp, pf, thd, cf):
    try:
        message = (
            f" *NILM Load Monitor*\n"
            f"━━━━━━━━━━━━━━━\n"
            f" Load     : `{load_name}`\n"
            f" Power    : `{power:.4f} W`\n"
            f" V RMS    : `{v_rms:.4f} V`\n"
            f" I RMS    : `{i_rms:.5f} A`\n"
            f" PF       : `{pf:.4f}`\n"
            f"〰 THD      : `{thd * 100:.1f}%`\n"
            f" CF       : `{cf:.4f}`\n"
            f"━━━━━━━━━━━━━━━\n"
            f" Energy   : `{energy_kwh:.6f} kWh`\n"
            f" Cost     : `{cost_egp:.4f} EGP`\n"
        )
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        r = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }, timeout=5)
        if r.status_code == 200:
            print("   Telegram message sent.")
        else:
            print(f"   Telegram failed: {r.status_code} — {r.text}")
    except Exception as e:
        print(f"   Telegram error: {e}")


# =========================
# VISUALIZATION LOGIC
# =========================
def smooth_vi_trajectory(v, i, window, sort_data=True):
    if sort_data:
        sort_idx = np.argsort(v)
        v_plot = v[sort_idx]
        i_plot = i[sort_idx]
        filter_mode = 'nearest'
    else:
        v_plot = v
        i_plot = i
        filter_mode = 'wrap'

    v_smoothed = uniform_filter1d(v_plot, size=window, mode=filter_mode)
    i_smoothed = uniform_filter1d(i_plot, size=window, mode=filter_mode)
    return v_smoothed, i_smoothed


# =========================================================
# MAIN
# =========================================================
def main():
    global cumulative_energy

    plt.ion()
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    while True:
        try:
            # --- 1. Collect / Load data ---
            file_path = collect_data_from_bt()
            v_raw, i_raw = read_data(file_path)

            # --- 2. Filter signals ---
            print("\n[Filter] Filtering signals...")
            v_filt = filter_signal(v_raw)
            i_filt = filter_signal(i_raw)

            # --- 3. Calculate Base Metrics ---
            v_rms, i_rms, pf = calculate_metrics(v_filt, i_filt)
            thd = calculate_thd(i_filt)
            cf = crest_factor(i_filt)

            # --- 4. MACHINE LEARNING ---
            try:
                model = joblib.load('load_classifier.pkl')
                ml_prediction = model.predict([[v_rms, i_rms, pf, thd, cf]])
                detected = ml_prediction[0]

            except FileNotFoundError:
                detected = "Unknown"
                print("Error: load_classifier.pkl not found.")

            except Exception as e:
                detected = "Unknown"
                print(f"Error loading ML model: {e}")    

            # --- 5. Energy & Cost Calculation ---
            active_power = v_rms * i_rms * pf
            energy_kwh, cost_egp = calculate_energy_cost(active_power, len(v_filt))
            cumulative_energy += energy_kwh

            print("\n===== RESULTS =====")
            print(f"V_RMS          = {v_rms:.4f} V")
            print(f"I_RMS          = {i_rms:.5f} A")
            print(f"Power Factor   = {pf:.4f}")
            print(f"THD            = {thd:.4f} ({thd * 100:.1f}%)")
            print(f"Crest Factor   = {cf:.4f}")
            print(f"Active Power   = {active_power:.4f} W")
            print(f"Session Cost   = {cost_egp:.6f} EGP")
            print(f"\n>>> Detected Load: {detected} <<<")

            # --- 6. Send to Blynk & Telegram ---
            send_all_to_blynk(active_power, v_rms, i_rms, detected, cumulative_energy,
                              cumulative_energy * PRICE_PER_KWH)
            print("\n Sending to Telegram...")
            send_telegram(active_power, v_rms, i_rms, detected, cumulative_energy, cumulative_energy * PRICE_PER_KWH,
                          pf, thd, cf)

            # --- 7. Visualization Processing ---
            visual_window = 5
            do_sort = True   

            # --- 8. Plotting (Update the existing window) ---
            axes[0].clear()
            axes[1].clear()
            axes[2].clear()

            fig.suptitle(f"NILM Analysis — Detected: {detected}", fontsize=14, fontweight='bold')

            samples = min(350, len(v_filt))
            t = np.arange(samples)
            vf_plot = v_filt[:samples]
            ic_plot = i_filt[:samples]

            # Plot 1
            axes[0].plot(t, vf_plot, label="Voltage", linewidth=1.5)
            axes[0].plot(t, ic_plot * 15, '--', label="Current ×15", linewidth=1.5, alpha=0.85)
            axes[0].set_title("Time Domain")
            axes[0].legend(fontsize=8)
            axes[0].grid(True, alpha=0.3)

            # Plot 2
            v_raw_dc = remove_dc_offset(v_raw)[:samples]
            i_raw_dc = remove_dc_offset(i_raw)[:samples]
            axes[1].plot(v_raw_dc, i_raw_dc, alpha=0.5, linewidth=0.7, color='gray', label="Raw")
            axes[1].set_title("V-I Trajectory (Raw)")
            axes[1].legend(fontsize=8)
            axes[1].grid(True, alpha=0.3)

            # Plot 3
            v_smooth, i_smooth = smooth_vi_trajectory(vf_plot, ic_plot, window=visual_window, sort_data=do_sort)
            axes[2].plot(v_smooth, i_smooth, linewidth=2.0, color='steelblue', label="Processed")
            axes[2].set_title("V-I Trajectory (Clean)")
            axes[2].legend(fontsize=8)
            axes[2].grid(True, alpha=0.3)

            metrics_text = f"PF = {pf:.3f}\nTHD = {thd * 100:.1f}%\nCF = {cf:.2f}"
            axes[2].text(0.02, 0.97, metrics_text, transform=axes[2].transAxes, fontsize=8,
                         verticalalignment='top', bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.7))

            plt.tight_layout()
            plt.savefig("nilm_output_final.png", dpi=150, bbox_inches='tight')

            plt.pause(3)

        except KeyboardInterrupt:
            print("\n Monitor stopped by user.")
            break
        except Exception as e:
            print(f"\n Unexpected error in loop: {e}")
            plt.pause(2)


if __name__ == "__main__":
    main()