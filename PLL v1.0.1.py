import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


phase_vco = 0
fs = 200
dt = 1.0 / fs
t = np.arange(0, 1.0, 1.0 / fs)
noise = np.random.normal(0,0.2,len(t))

ref =5
vco = 5
f0 = 5
phase_vco += 2 * np.pi * vco * dt
sine_ref = np.sin(2 * np.pi * ref * t + np.pi /4)

Kp = 0.5
Ki = 0.05
k0 = 1
integral = 0

def pi_controller(kp, ki, integral, error, time):
  integral += error * dt
  P = kp * error
  I = ki * integral
  pi = P+I

  return pi,integral

sine_ref_n = sine_ref + noise
square_ref = sine_ref_n >= 0                               # sine -> square wave


phase_detector = []
ref_out = []
pi_result = []
sine_vco = np.zeros(len(t))
f_vco = np.zeros(len(t))

square_vco = sine_vco >= 0

ref_out = np.zeros(len(t))

phase_ref = 2 * np.pi * ref * t + np.pi / 4
phase_vco_arr = 2 * np.pi * vco * t

for i in range(len(t)):

  phase_detect = square_vco[i] != square_ref[i]
  phase_detector.append(phase_detect)

  phase_error = phase_ref[i] - phase_vco

  pi_val, integral = pi_controller(Kp, Ki, integral, phase_error, dt)
  pi_result.append(pi_val)
  ref_out[i] = sine_ref_n[i] - pi_val

  current_vco = f0 + k0 * pi_val

  phase_vco += 2 * np.pi * vco * dt
  f_vco[i] = current_vco

  phase_vco += 2 * np.pi * current_vco * dt

  sine_vco[i] = np.sin(phase_vco)

  ref_out[i] = sine_vco[i]


plt.figure()
fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

axs[0].plot(t, sine_ref_n, label='Reference (noisy)')
axs[0].plot(t, sine_vco, label='VCO')
axs[0].set_ylabel('Amplitude')
axs[0].legend()
axs[0].set_title('Reference and VCO signals')

axs[1].plot(t, phase_detector, label='Phase Detector Output', color='orange')
axs[1].set_ylabel('Phase Error (bool)')
axs[1].legend()

axs[2].plot(t, ref_out, label='Reference (clean)', linestyle='--', alpha=0.6)
axs[2].set_ylabel('Amplitude')
axs[2].legend()
plt.show()
