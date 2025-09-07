import numpy as np
import pandas as pd
from pathlib import Path

# Paths
CSV_PATH = Path("simulated_power_trace.csv")
OUT_DIR = Path("problem1_outputs")
OUT_DIR.mkdir(exist_ok=True)

# Hamming weight lookup
HW = np.array([bin(x).count("1") for x in range(256)], dtype=np.uint8)


def hex2bytes16(h):
    return np.frombuffer(bytes.fromhex(h), dtype=np.uint8)


# Load CSV
df = pd.read_csv(CSV_PATH, header=None)
ciphertexts = [hex2bytes16(x.strip()) for x in df.iloc[:, 0].astype(str)]
C = np.vstack(ciphertexts)  # ciphertexts as (N,16) array
traces = df.iloc[:, 1:].values.astype(float)
N, T = traces.shape
print(f"Loaded {N} traces with {T} samples each")

# Normalize traces
tr_z = (traces - traces.mean(axis=0)) / (traces.std(axis=0) + 1e-15)

best_key = []

for byte_idx in range(16):
    c = C[:, byte_idx]
    hyp = np.empty((256, N))
    for k in range(256):
        hyp[k] = HW[c ^ k]  # leakage model
    hyp = (hyp - hyp.mean(axis=1, keepdims=True)) / (hyp.std(axis=1, keepdims=True) + 1e-15)
    corr = (hyp @ tr_z) / (N - 1)
    scores = np.abs(corr).max(axis=1)

    # Best guess
    best = int(np.argmax(scores))
    best_key.append(best)
    print(f"Byte {byte_idx:02d}: best=0x{best:02x}, score={scores[best]:.4f}")

    # Save ranking file
    order = np.argsort(-scores)
    subdir = OUT_DIR / "problem1"
    subdir.mkdir(parents=True, exist_ok=True)

    with open(subdir / f"byte_{byte_idx:02d}.txt", "w") as f:
        for rank, k in enumerate(order, 1):
            f.write(f"{k:02x},{k},{scores[k]:.6f},{rank}\n")

# Write recovered key
key_hex = bytes(best_key).hex()
print("Recovered key:", key_hex)
with open(OUT_DIR / "key.txt", "w") as f:
    f.write(key_hex + "\n")
