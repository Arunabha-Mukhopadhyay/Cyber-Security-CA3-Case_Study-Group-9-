"""
WazirX / Bybit-style Multisig "Blind-Signing" Vulnerability Simulation
------------------------------------------------------------------------
Educational, self-contained simulation (no real blockchain calls) that
demonstrates the root-cause pattern common to the WazirX (Jul 2024) and
Bybit (Feb 2025) multisig-wallet breaches: signers approving a
transaction based on data RENDERED BY A UI/INTERFACE LAYER, without
independently verifying the raw transaction hash / calldata that is
actually executed on-chain.

Two execution paths are modelled:
1. vulnerable_execute()  -> mirrors the real-world flaw
2. secure_execute()      -> adds an independent hash-verification
                            control (the recommended mitigation)
"""

import hashlib
import json


def compute_tx_hash(raw_tx: dict) -> str:
    """Deterministic SHA-256 hash of the ACTUAL transaction payload."""
    canonical = json.dumps(raw_tx, sort_keys=True).encode()
    return hashlib.sha256(canonical).hexdigest()


class MultisigWallet:
    def __init__(self, signers, threshold):
        self.signers = signers
        self.threshold = threshold

    # ---- VULNERABLE PATH (pre-2024 WazirX / pre-2025 Bybit pattern) ----
    def vulnerable_execute(self, displayed_tx, actual_tx, approvals):
        """
        Signers approve 'displayed_tx' (what a compromised interface
        shows them), but the wallet's back-end actually executes
        'actual_tx'. No independent hash check is performed, so a
        masked / spoofed UI can silently swap the payload.
        """
        if approvals < self.threshold:
            raise PermissionError("Insufficient approvals")
        print("[VULNERABLE] Signers approved the DISPLAYED transaction:")
        print(f"\t{displayed_tx}")
        print("[VULNERABLE] Wallet contract actually EXECUTES:")
        print(f"\t{actual_tx}")
        return actual_tx

    # ---- SECURE PATH (recommended mitigation) --------------------------
    def secure_execute(self, actual_tx, trusted_hash, approvals):
        """
        Each signer is assumed to have obtained 'trusted_hash' from an
        out-of-band, tamper-evident channel (e.g. a hardware wallet's
        own clear-signing display, or independent recomputation on a
        second, air-gapped client) BEFORE approving. Execution is only
        permitted if the hash of the payload that will actually run
        matches the independently verified value.
        """
        actual_hash = compute_tx_hash(actual_tx)
        if actual_hash != trusted_hash:
            raise ValueError(
                "Hash mismatch: on-chain calldata does not match the "
                "independently verified transaction. Approval blocked."
            )
        if approvals < self.threshold:
            raise PermissionError("Insufficient approvals")
        print("[SECURE] Independent hash verification passed. Executing:")
        print(f"\t{actual_tx}")
        return actual_tx


if __name__ == "__main__":
    wallet = MultisigWallet(
        signers=["Signer1", "Signer2", "Signer3", "Custodian"],
        threshold=4)

    # What the (compromised) interface shows the signers:
    displayed_tx = {"to": "0xKnownWhitelistedAddress",
                    "value": 0, "op": "routine_rebalance"}

    # What is actually encoded in the calldata and will run on-chain:
    actual_tx = {"to": "0xAttackerControlledAddress",
                 "value": "ALL_FUNDS", "op": "upgrade_mastercopy"}

    # 1) Vulnerable flow -> the attack succeeds (mirrors real incidents)
    wallet.vulnerable_execute(displayed_tx, actual_tx, approvals=4)

    print()

    # 2) Secure flow -> trusted_hash is computed on the HONEST payload
    #    that a signer independently verified out-of-band; comparing it
    #    against the hash of the actual calldata exposes the tampering.
    trusted_hash = compute_tx_hash(displayed_tx)
    try:
        wallet.secure_execute(actual_tx, trusted_hash, approvals=4)
    except ValueError as exc:
        print(f"[SECURE] Attack blocked -> {exc}")
