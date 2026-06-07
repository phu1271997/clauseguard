# GenLayer Studio Deploy & Troubleshooting Guide

Follow these steps to deploy and test ClauseGuard in GenLayer Studio.

## Recommended Deploy Procedure

1. **Open GenLayer Studio**: Go to [https://studio.genlayer.com/run-debug](https://studio.genlayer.com/run-debug).
2. **Reset Storage**: Go to Settings -> **Reset Storage** -> Click **Confirm**. This ensures no stale storage schemas conflict with your deployment.
3. **Hard Refresh**: Perform a hard refresh using `Cmd+Shift+R` (macOS) or `Ctrl+F5` (Windows/Linux) to clear browser caches.
4. **Deploy Sanity Contract**:
    * Load `contracts/storage_test.py` into the editor.
    * Click **Deploy**.
    * Wait for the transaction to finalize. Click the transaction in the sidebar and ensure `Result: SUCCESS` is shown.
5. **Deploy Main Contract**:
    * Load `contracts/clauseguard.py`.
    * Click **Deploy**.
    * Confirm that the transaction result is `Result: SUCCESS`.

---

## Troubleshooting Map

Refer to this troubleshooting map if you encounter compilation or runtime errors:

| Error Message / Symptom | Cause | Resolution |
| :--- | :--- | :--- |
| `Contract Queues not found` or similar | Missing `# v0.2.16` | Ensure the first line of the contract is exactly `# v0.2.16` |
| `AssertionError: Is right the same storage type? TreeMap <- TreeMap` | Reassigned `TreeMap`/`DynArray` in `__init__` | Remove any assignments of `TreeMap` or `DynArray` in the `__init__` constructor. GenVM automatically initializes these collection types. |
| Schema / Compile Error | `float` used in signatures or incorrect collection types | Ensure all public method signatures use allowed types (e.g., `int`, `u256`, `str`, `Address`). Replace any `float` types with integer representations (minor units). Use `TreeMap`/`DynArray` instead of Python `dict`/`list` in contract storage. |
| "Not deployed yet" but transaction is `FINALIZED` | Deployment transaction failed internally | Click the finalized transaction in the sidebar and inspect the `Result` field to read the Python stack trace. |
| Unexpected compilation errors after updates | Stale browser cache or storage state | Reset Storage under Studio settings, then perform a hard refresh (`Cmd+Shift+R`). |
