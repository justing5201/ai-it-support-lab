from ai_analyzer import MIN_RETRIEVAL_SCORE
from rag.retriever import retrieve_relevant_sops


TEST_CASES = [
    # -------------------------
    # Supported by our SOPs
    # -------------------------
    {
        "name": "vpn_authentication",
        "query": (
            "GlobalProtect says authentication failed, "
            "but Microsoft 365 works normally."
        ),
        "supported": True,
        "expected_source": "vpn.md",
    },
    {
        "name": "vpn_connection",
        "query": (
            "The VPN client will not connect from my laptop, "
            "but my internet connection works."
        ),
        "supported": True,
        "expected_source": "vpn.md",
    },
    {
        "name": "account_locked",
        "query": (
            "I entered the wrong password several times "
            "and now my account says it is locked."
        ),
        "supported": True,
        "expected_source": "password_reset.md",
    },
    {
        "name": "forgot_password",
        "query": (
            "I forgot my company password and cannot sign in."
        ),
        "supported": True,
        "expected_source": "password_reset.md",
    },
    {
        "name": "printer_offline",
        "query": (
            "The office printer shows offline on my computer."
        ),
        "supported": True,
        "expected_source": "printer.md",
    },
    {
        "name": "printer_queue",
        "query": (
            "My document is stuck in the print queue "
            "and nothing will print."
        ),
        "supported": True,
        "expected_source": "printer.md",
    },
    {
        "name": "phishing_link",
        "query": (
            "I received an unexpected Microsoft login email "
            "with a link asking for my password."
        ),
        "supported": True,
        "expected_source": "phishing.md",
    },
    {
        "name": "phishing_attachment",
        "query": (
            "I received a suspicious email with an attachment "
            "that I was not expecting."
        ),
        "supported": True,
        "expected_source": "phishing.md",
    },
    {
        "name": "slow_windows",
        "query": (
            "My Windows laptop is extremely slow "
            "and programs take several minutes to open."
        ),
        "supported": True,
        "expected_source": "windows_performance.md",
    },
    {
        "name": "high_resource_usage",
        "query": (
            "My Windows computer keeps freezing "
            "and Task Manager shows very high resource usage."
        ),
        "supported": True,
        "expected_source": "windows_performance.md",
    },

    # -------------------------
    # Not covered by our SOPs
    # -------------------------
    {
        "name": "webcam",
        "query": (
            "My webcam flickers during Teams meetings."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "excel_crash",
        "query": (
            "Excel crashes every time I open a spreadsheet."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "bluetooth_headset",
        "query": (
            "My Bluetooth headset keeps disconnecting."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "teams_microphone",
        "query": (
            "Nobody can hear me in Microsoft Teams "
            "but I can hear everyone else."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "docking_station",
        "query": (
            "My docking station is not detecting either monitor."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "onedrive_sync",
        "query": (
            "OneDrive has been stuck syncing my files all morning."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "browser_certificate",
        "query": (
            "My browser says the website certificate is invalid."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "usb_device",
        "query": (
            "Windows does not recognize my USB flash drive."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "monitor",
        "query": (
            "My second monitor says no signal."
        ),
        "supported": False,
        "expected_source": None,
    },
    {
        "name": "keyboard",
        "query": (
            "Several keys on my laptop keyboard stopped working."
        ),
        "supported": False,
        "expected_source": None,
    },
]


def main():
    passed = 0
    supported_total = 0
    unsupported_total = 0

    false_positives = 0
    false_negatives = 0
    wrong_sources = 0

    print("RAG SCOPE DETECTION TEST")
    print("=" * 70)
    print(f"Threshold: {MIN_RETRIEVAL_SCORE:.4f}")

    for test in TEST_CASES:
        results = retrieve_relevant_sops(
            test["query"],
            top_k=3
        )

        top_result = results[0]
        top_source = top_result["source"]
        top_score = top_result["score"]

        accepted = (
            top_score >= MIN_RETRIEVAL_SCORE
        )

        if test["supported"]:
            supported_total += 1

            correct_source = (
                top_source == test["expected_source"]
            )

            test_passed = (
                accepted and correct_source
            )

            if not accepted:
                false_negatives += 1
            elif not correct_source:
                wrong_sources += 1

        else:
            unsupported_total += 1

            test_passed = not accepted

            if accepted:
                false_positives += 1

        if test_passed:
            passed += 1

        print("\n" + "-" * 70)
        print(f"TEST: {test['name']}")
        print(f"QUERY: {test['query']}")
        print(
            f"EXPECTED: "
            f"{'SUPPORTED' if test['supported'] else 'UNSUPPORTED'}"
        )
        print(f"TOP SOP: {top_source}")
        print(f"TOP SCORE: {top_score:.4f}")
        print(f"ACCEPTED: {accepted}")

        if test["expected_source"]:
            print(
                f"EXPECTED SOP: "
                f"{test['expected_source']}"
            )

        print(
            f"RESULT: "
            f"{'PASS' if test_passed else 'FAIL'}"
        )

        print("TOP 3:")
        for number, result in enumerate(
            results,
            start=1
        ):
            print(
                f"  {number}. "
                f"{result['source']} "
                f"({result['score']:.4f})"
            )

    total = len(TEST_CASES)

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(
        f"Accuracy: "
        f"{(passed / total) * 100:.1f}%"
    )
    print()
    print(
        f"Supported cases: {supported_total}"
    )
    print(
        f"Unsupported cases: {unsupported_total}"
    )
    print(
        f"False positives: {false_positives}"
    )
    print(
        f"False negatives: {false_negatives}"
    )
    print(
        f"Wrong SOP selections: {wrong_sources}"
    )


if __name__ == "__main__":
    main()