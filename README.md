# ClauseGuard

**ClauseGuard** is a self-executing sponsorship and endorsement protocol for the creator economy built on GenLayer. It allows brands to lock native GEN tokens in escrow, which are automatically settled by an on-chain AI jury checking real-world proof of work and brand safety guidelines from the live web.

---

## Architecture Overview

```mermaid
sequenceDiagram
    participant Brand
    participant ClauseGuard as ClauseGuard Contract
    participant Creator
    participant Web as Live Internet (post/conduct)
    participant AI as AI Jury (LLM)

    Brand->>ClauseGuard: create_campaign(creator, brief, requirements, morality_standard, amount, deadline)
    Brand->>ClauseGuard: fund(campaign_id) [locks escrow]
    Creator->>ClauseGuard: submit_work(campaign_id, submission_url)
    Note over Brand, Creator: (Optional) Anyone can add conduct evidence URLs
    Brand->>ClauseGuard: adjudicate(campaign_id)
    activate ClauseGuard
    ClauseGuard->>Web: Render submission & conduct URLs (mode="text")
    Web-->>ClauseGuard: Web page text contents
    ClauseGuard->>AI: Ask for verdict JSON (exec_prompt)
    AI-->>ClauseGuard: Verdict (RELEASE | PARTIAL_RELEASE | WITHHOLD | CLAWBACK_WITH_PENALTY)
    ClauseGuard->>ClauseGuard: Deterministic settle based on verdict bps
    deactivate ClauseGuard
    Creator->>ClauseGuard: withdraw() [transfers GEN tokens]
```

---

## Repository Structure

*   `contracts/clauseguard.py`: Main Intelligent Contract.
*   `contracts/storage_test.py`: Sanity checking contract.
*   `prompts/jury_prompt.md`: AI jury brand safety rubric.
*   `tests/test_clauseguard.py`: Direct mode unit tests mocking LLM/Web rendering.
*   `docs/DEPLOY_STUDIO.md`: Deployment instructions for GenLayer Studio.
*   `scripts/deploy_notes.md`: Development tracking notes.

---

## Getting Started

### Prerequisites

*   Python 3.12+
*   Node.js 18+
*   GenLayer Studio or Simulator

### Installing Dependencies

Install python testing dependencies:
```bash
pip install genlayer-test pytest
```

---

## Testing

Run tests locally in Direct Mode (in-memory):
```bash
gltest tests/ -v
```

---

## Deployment to GenLayer Studio

For step-by-step instructions on deploying the sanity contract first, resetting storage, and deploying the main contract, see [docs/DEPLOY_STUDIO.md](docs/DEPLOY_STUDIO.md).
