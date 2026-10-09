# WazirX / Bybit-Style Multisig "Blind-Signing" Vulnerability Simulation

**Case Study:** Root-Cause Analysis of the WazirX Multisignature Wallet Breach (July 2024)
**Course:** Cyber Security – Computer Science and Engineering (2023–2027)
**Group:** 9 | **Faculty:** Dr. Pooja Bagane, Dr. Jitendra Rajpurohit

| Member | PRN |
|---|---|
| Harsh Rajput | 23070122102 |
| Ayush Siddhant | 23070122066 |
| Om Dhamame | 23070122155 |
| Arunabha Mukhopadhyay | 23070122049 |
| Garvit Tyagi | 23070122094 |

**GitHub Repository:** `https://github.com/Arunabha-Mukhopadhyay/Cyber-Security-CA3-Case_Study-Group-9-`

---

## 1. About the Project

On 18 July 2024, the Indian exchange **WazirX** lost about **USD 234.9 million** from an Ethereum multisig wallet (4-of-6 scheme, hardware wallets, address whitelist, custodian: Liminal). Attackers (attributed to North Korea's Lazarus Group) exploited **blind signing**: the signers approved a transaction as shown by the interface, while the calldata actually executed on-chain was different. The same root cause appeared in the **Bybit** breach (Feb 2025, ~USD 1.5 billion).

This project is a **safe, self-contained Python simulation** (no real blockchain calls, no exploit code) that demonstrates:

1. **Vulnerable path** – `vulnerable_execute()`: signers approve the *displayed* transaction, but a *different* payload is executed. The attack succeeds.
2. **Secure path** – `secure_execute()`: execution is allowed only if the SHA-256 hash of the real payload matches an independently verified (out-of-band) hash. The attack is blocked.

The full analysis (attack chain, vulnerability classification, WazirX vs Bybit comparison, impact, mitigations) is in the project report.

## 2. Repository Contents

```
.
├── wazirx_multisig_simulation.py   # Source code (simulation)
├── build_exe.bat                   # Builds the Windows .exe (optional)
├── README.md                       # This file
├── .gitignore
└── dist/
    └── wazirx_multisig_simulation.exe   # Executable (after build, included in submission zip)
```

## 3. Requirements

- **Python 3.8 or newer**
- No third-party libraries (uses only the standard library: `hashlib`, `json`)
- *Only for building the .exe:* `pyinstaller` (installed automatically by `build_exe.bat`)

## 4. How to Execute

### Option A – Run the source code
```bash
git clone <YOUR_GITHUB_REPO_LINK>
cd <repo-folder>
python wazirx_multisig_simulation.py
```
(Use `python3` on Linux/macOS.)

### Option B – Run the executable (Windows)
Double-click `dist\wazirx_multisig_simulation.exe`, or from a terminal:
```cmd
dist\wazirx_multisig_simulation.exe
```
To rebuild the executable yourself, run `build_exe.bat` (or manually: `pip install pyinstaller` then `pyinstaller --onefile wazirx_multisig_simulation.py`).

## 5. Expected Output

```
[VULNERABLE] Signers approved the DISPLAYED transaction:
	{'to': '0xKnownWhitelistedAddress', 'value': 0, 'op': 'routine_rebalance'}
[VULNERABLE] Wallet contract actually EXECUTES:
	{'to': '0xAttackerControlledAddress', 'value': 'ALL_FUNDS', 'op': 'upgrade_mastercopy'}

[SECURE] Attack blocked -> Hash mismatch: on-chain calldata does not match the independently verified transaction. Approval blocked.
```

## 6. How the Code Works

| Component | Purpose |
|---|---|
| `compute_tx_hash(raw_tx)` | Deterministic SHA-256 hash of the canonical JSON of a transaction. |
| `MultisigWallet(signers, threshold)` | Models a multisig wallet (4 signers, threshold 4). |
| `vulnerable_execute(displayed_tx, actual_tx, approvals)` | Executes `actual_tx` once approvals ≥ threshold, with **no** check that it matches what signers saw. |
| `secure_execute(actual_tx, trusted_hash, approvals)` | Recomputes the hash of `actual_tx` and blocks execution if it differs from the out-of-band `trusted_hash`. |

**Key lesson:** multisig alone is not enough if the human-facing verification layer can be manipulated. Recommended defence-in-depth: hardware-wallet clear-signing, out-of-band hash verification, transaction simulation, and continuous wallet-infrastructure monitoring.

## 7. Disclaimer

This project is for **educational purposes only**. It contains no real exploit code, performs no network or blockchain calls, and uses placeholder addresses.
