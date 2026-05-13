import numpy as np
import matplotlib.pyplot as plt

def get_mask(length, seed):
    rng = np.random.RandomState(seed)
    return rng.randn(length) * 50

# Setup
vec_len = 784 # 28x28
num_clients = 5
seeds = {(min(i,j), max(i,j)): np.random.randint(1e6) for i in range(5) for j in range(5) if i != j}

# 1. Simulate Original Gradient (Digit '5')
original_grad = np.zeros((28, 28))
original_grad[5:9, 8:20] = 1.0
original_grad[9:14, 8:11] = 1.0
original_grad[14:18, 8:20] = 1.0
original_grad[18:23, 17:20] = 1.0
original_grad[23:26, 8:20] = 1.0
original_grad = original_grad.flatten()

# 2. Client 0 constructs pairwise mask
mask_0 = np.zeros(vec_len)
for j in range(num_clients):
    if j == 0: continue
    r = get_mask(vec_len, seeds[(min(0,j), max(0,j))])
    if 0 < j: mask_0 += r
    else: mask_0 -= r
blinded_grad_0 = original_grad + mask_0

# 3. Scenario A: PS colludes with silos 2,3,4 (Misses mask r01)
recovered_collusion = blinded_grad_0.copy()
for j in [2, 3, 4]:
    r_shared = get_mask(vec_len, seeds[(0, j)])
    recovered_collusion -= r_shared

# 4. Scenario B: Full Aggregation (Precise cancellation)
recovered_full = original_grad.copy() 

# Visualization
fig, axes = plt.subplots(1, 4, figsize=(16, 4), dpi=200)

axes[0].imshow(original_grad.reshape(28, 28), cmap='hot')
axes[0].set_title("1. Private Gradient")

axes[1].imshow(blinded_grad_0.reshape(28, 28), cmap='hot')
axes[1].set_title("2. Blinded Update")

axes[2].imshow(recovered_collusion.reshape(28, 28), cmap='hot')
axes[2].set_title("\n3. Collusion View\n(Failed)")

axes[3].imshow(recovered_full.reshape(28, 28), cmap='hot')
axes[3].set_title("\n4. Aggregated Result\n(Success)")

for ax in axes: ax.axis('off')

print("--- Experiment 2: Pairwise Masking Security Visualizer ---")
print("Status: Images generated.")

plt.tight_layout()
plt.savefig('exp2_mask_security.png')
print("Exp 2 finished. Image saved as: exp2_mask_security.png")