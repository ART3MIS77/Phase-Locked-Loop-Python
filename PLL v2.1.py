import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


fs = 250
dt = 1.0 / fs
t = np.arange(0, 1.0, 1.0 / fs)
noise = np.random.normal(0,0.2,len(t))

phase_vco = 0
ref = 5
f0 = 5                               # vco free frequency
sine_ref = np.sin(2 * np.pi * ref * t + 2 * np.pi / 3)

Kp = 1.1
Ki = 0.9
k0 = 1
integral = 0


def pi_controller(kp, ki, integral, error, dt):
  integral += error * dt
  P = kp * error
  I = ki * integral
  pi = P+I

  return pi,integral, P, I

sine_ref_n = sine_ref + noise
square_ref = sine_ref_n >= 0                               # sine -> square wave
                                                           # square_ref = np.zeros(len(t), dtype=bool)

phase_detector = []
ref_out = []
pi_result = []
p_result = []
i_result = []
sine_vco = np.zeros(len(t))
square_vco = np.zeros(len(t))

current_vco = f0

for i in range(len(t)):
  phase_vco += 2 * np.pi * current_vco * dt

  sine_vco[i] = np.sin(phase_vco)
  square_vco[i] = sine_vco[i] >= 0

  phase_detect = square_vco[i] != square_ref[i]
  phase_detector.append(phase_detect)

  #phase_error = phase_ref[i] - phase_vco  | funny thing is that it works the same as XOR phase detection. if you put phase error or phase detect it will give the exact same result

  pi_val, integral, p_val, i_val = pi_controller(Kp, Ki, integral, phase_detect, dt)
  pi_result.append(pi_val)
  p_result.append(p_val)
  i_result.append(i_val)

  current_vco = f0 + k0 * pi_val
  ref_out.append(sine_vco[i])

  #phase_vco += 2 * np.pi * current_vco * dt

fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), sharex=True)

axs[0].plot(t, sine_ref_n, label='Reference (noisy)')
axs[0].plot(t, sine_vco, label='VCO')
axs[0].set_ylabel('Amplitude')
axs[0].legend()

axs[1].plot(t, pi_result, label='PI controller', color='orange')
axs[1].legend()

axs[2].plot(t, ref_out, label='Recovered signal', linestyle='--', alpha=0.6, color='green')
axs[2].set_ylabel('Amplitude')
axs[2].legend()
plt.show()


fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
axs[0].plot(t, square_ref, label='Square red')
axs[0].plot(t, square_vco, label='Square vco')
axs[0].legend()
axs[1].plot(t, phase_detector, label='Phase Detector Output', color='orange')
axs[1].legend()
plt.show()

fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(10, 10), sharex=True)
axs[0].plot(t, p_result, label='Proportional')
axs[0].legend()
axs[1].plot(t, i_result, label='Integral')
axs[1].legend()
axs[2].plot(t, pi_result, label='P+I')
axs[2].legend()

plt.show()
