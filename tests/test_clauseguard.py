import json
from gltest.types import MockedLLMResponse, MockedWebResponse


def test_clauseguard_workflow(
    direct_vm, direct_deploy, direct_alice, direct_bob, direct_charlie
):
    # Deploy contract
    contract = direct_deploy("contracts/clauseguard.py")

    from genlayer import Address
    alice = Address(direct_alice)
    bob = Address(direct_bob)
    charlie = Address(direct_charlie)

    # 1. Create campaign (Alice is Brand, Bob is Creator)
    brief = "Promotion of fitness shoes"
    requirements = "Instagram post, hashtag #ad, mention @fitshoes"
    morality_standard = "No references to drug use or competitive brands"
    milestone_amount = 1000
    deadline = 9999999999

    # Set sender as Alice (Brand)
    direct_vm.sender = direct_alice
    campaign_id = contract.create_campaign(
        bob,
        brief,
        requirements,
        morality_standard,
        milestone_amount,
        deadline,
    )

    assert campaign_id == "1"

    # Verify campaign details
    campaign_data = json.loads(contract.get_campaign(campaign_id))
    assert campaign_data["brand"] == str(alice)
    assert campaign_data["creator"] == str(bob)
    assert campaign_data["status"] == "CREATED"
    assert campaign_data["milestone_amount"] == 1000

    # 2. Fund campaign
    # Non-brand funding should revert
    direct_vm.sender = direct_charlie
    direct_vm.value = milestone_amount
    with direct_vm.expect_revert("Only the campaign brand can fund it"):
        contract.fund(campaign_id)

    # Brand funds it with insufficient value
    direct_vm.sender = direct_alice
    direct_vm.value = 500
    with direct_vm.expect_revert("Sent value is less than milestone amount"):
        contract.fund(campaign_id)

    # Brand funds successfully
    direct_vm.value = milestone_amount
    contract.fund(campaign_id)
    campaign_data = json.loads(contract.get_campaign(campaign_id))
    assert campaign_data["status"] == "FUNDED"

    # Reset vm value after transaction to be safe
    direct_vm.value = 0

    # 3. Submit Work
    submission_url = "https://instagram.com/p/bob_post"
    # Non-creator submission should revert
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("Only the campaign creator can submit work"):
        contract.submit_work(campaign_id, submission_url)

    # Creator submits successfully
    direct_vm.sender = direct_bob
    contract.submit_work(campaign_id, submission_url)
    campaign_data = json.loads(contract.get_campaign(campaign_id))
    assert campaign_data["status"] == "SUBMITTED"
    assert campaign_data["submission_url"] == submission_url

    # 4. Adjudicate - RELEASE verdict
    # Mock web render and LLM responses
    direct_vm.mock_web(
        r".*bob_post.*",
        {
            "status": 200,
            "body": "Loving my new shoes from @fitshoes! Best comfort ever. #ad",
        },
    )

    jury_verdict = {
        "deliverable_ok": True,
        "disclosure_ok": True,
        "morality_ok": True,
        "verdict": "RELEASE",
        "release_bps": 10000,
        "reason": "Full compliance achieved.",
    }
    direct_vm.mock_llm(r".*", json.dumps(jury_verdict))

    # Anyone can trigger adjudication
    direct_vm.sender = direct_charlie
    contract.adjudicate(campaign_id)

    campaign_data = json.loads(contract.get_campaign(campaign_id))
    assert campaign_data["status"] == "RESOLVED"
    assert campaign_data["verdict"]["verdict"] == "RELEASE"
    assert campaign_data["verdict"]["release_bps"] == 10000

    # Check ledgers: Bob (creator) should have 1000, Alice (brand) should have 0
    assert contract.get_ledger(str(bob)) == 1000
    assert contract.get_ledger(str(alice)) == 0

    # 5. Withdraw funds
    direct_vm.sender = direct_bob
    contract.withdraw()
    assert contract.get_ledger(str(bob)) == 0


def test_clauseguard_partial_verdict(
    direct_vm, direct_deploy, direct_alice, direct_bob
):
    contract = direct_deploy("contracts/clauseguard.py")

    from genlayer import Address
    alice = Address(direct_alice)
    bob = Address(direct_bob)

    brief = "Promotion"
    requirements = "Mention @fitshoes"
    morality_standard = "None"
    milestone_amount = 1000
    deadline = 9999999999

    direct_vm.sender = direct_alice
    campaign_id = contract.create_campaign(
        bob,
        brief,
        requirements,
        morality_standard,
        milestone_amount,
        deadline,
    )
    direct_vm.value = milestone_amount
    contract.fund(campaign_id)
    direct_vm.value = 0

    direct_vm.sender = direct_bob
    contract.submit_work(campaign_id, "https://instagram.com/p/bob_post2")

    # Mock web render and LLM responses for partial release
    direct_vm.mock_web(r".*", {"status": 200, "body": "Post without mention"})
    jury_verdict = {
        "deliverable_ok": False,
        "disclosure_ok": True,
        "morality_ok": True,
        "verdict": "PARTIAL_RELEASE",
        "release_bps": 5000,  # 50% payout
        "reason": "Missing competitor/mention but otherwise acceptable.",
    }
    direct_vm.mock_llm(r".*", json.dumps(jury_verdict))

    contract.adjudicate(campaign_id)

    # Bob gets 500, Alice gets 500 refund
    assert contract.get_ledger(str(bob)) == 500
    assert contract.get_ledger(str(alice)) == 500
