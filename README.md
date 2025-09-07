# Problem 1: AES Key Recovery from Simulated Power Traces

## Problem Statement
We were given a CSV file containing simulated power traces of an **unmasked AES implementation**.

- Each row in the file corresponds to one encryption trace.
- The first column is the ciphertext (128 bits in hex).
- The remaining columns are simulated power values recorded during encryption.

The task was to recover the **16-byte AES secret key** using these traces and produce:

1. `key.txt` → the recovered key (16 bytes in hex).  
2. `byte_00.txt … byte_15.txt` → ranking files listing all 256 possible values of each key byte in order of likelihood.

---

## Approach

### Leakage Model
AES leakage is assumed to follow the **Hamming Weight (HW)** model.  
Since we only have ciphertexts, we modeled the last AES round:


where `C` is the ciphertext byte and `k` is the key guess.  
(Alternatively, `HW(inv_sbox(C ⊕ k))` could be used.)

### Hypothesis Building
- For each of the 16 key bytes, test all 256 possible guesses.  
- For each guess, compute the predicted leakage (HW) across all traces.

### Correlation Power Analysis (CPA)
- Normalize both measured traces and hypothetical leakages.  
- Compute Pearson correlation between them.  
- For each key guess, take the maximum correlation across all time samples.  
- The guess with the highest score is the best candidate.

### Ranking
- All 256 guesses are sorted by their correlation score.  
- Results are saved into per-byte ranking files (`byte_xx.txt`).

---

## Implementation
A Python script was developed to:

- Load the CSV with `pandas`.
- Parse ciphertexts and traces.
- Run CPA for all 16 key bytes.
- Save outputs to `problem1_outputs/`.

---

## Results

- **Traces analyzed:** 5000 traces × 12 samples  
- **Recovered AES-128 Key (hex):**

- **Generated files:**
- `key.txt` → final key  
- `byte_00.txt … byte_15.txt` → ranked guesses per byte  

---

## Conclusion
Using a simple CPA with the Hamming Weight model, the AES-128 key was successfully recovered from simulated, noise-free traces.
