# Deployment Notes - ClauseGuard

Use this document to track local or testnet contract addresses and client settings.

## Local Simulator Addresses

*   **Sanity Contract (`storage_test.py`)**:
    *   Address: `0x...`
    *   Deploy Tx: `0x...`
*   **Main Contract (`clauseguard.py`)**:
    *   Address: `0x...`
    *   Deploy Tx: `0x...`

## Studio Deployment Addresses

*   **Main Contract (`clauseguard.py`)**:
    *   Address: `0x...`
    *   Deploy Tx: `0x...`

---

## SDK Configuration Parameters

To connect to your local net or local simulator using `genlayer-js`:

```javascript
import { createClient } from "genlayer-js";
import { localnet } from "genlayer-js/chains";

const client = createClient({
  chain: localnet,
});
```
