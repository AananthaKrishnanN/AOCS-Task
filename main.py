import numpy as np
import matplotlib.pyplot as plt
from control import tf, feedback, forced_response

# Define the transfer function of the system
# G(s) = 1 / (s^3 + 3s^2 + 5s + 1)
numerator = [1]
denominator = [1, 3, 5, 1]
plant = tf(numerator, denominator)

# PID Controller Parameters
Kp = 9.1     # Proportional Gain
Ki = 3.7   # Integral Gain
Kd = 5.5   # Derivative Gain

# Define PID Controller: C(s) = Kp + Ki/s + Kd*s
pid_controller = Kp + Ki / tf([1, 0], [1]) + Kd * tf([1, 0], [1])

# Closed-loop system: T(s) = (C(s) * G(s)) / (1 + C(s) * G(s))
closed_loop_system = feedback(pid_controller * plant, 1)

# Time vector for simulation
time = np.linspace(0, 20, 1000)

# Step Input starting from 2 seconds
step_input = np.where(time >= 2, 1.0, 0.0)

# Simulate system with the custom input
time, output = forced_response(closed_loop_system, time, step_input)

# Add periodic noise to the output
add_noise = True  # Set to True to add noise
if add_noise:
    noise = np.zeros_like(output)  # Initialize noise array
    for t in range(len(time)):
        if int(time[t]) % 5 == 0:  # Add noise every 5 seconds
            noise[t] = np.random.normal(0, 0.2)  # Random noise at this point
    output = output + noise

# Plot the input and output
plt.figure(figsize=(12, 6))

# Plotting Input
plt.subplot(2, 1, 1)
plt.plot(time, step_input, label='Input Signal')
plt.title('Input vs. Output of PID Controlled System with Periodic Noise')
plt.xlabel('Time (s)')
plt.ylabel('Input')
plt.legend()
plt.grid(True)

# Plotting Output
plt.subplot(2, 1, 2)
plt.plot(time, output, label='System Output', color='orange')
plt.xlabel('Time (s)')
plt.ylabel('Output')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()
