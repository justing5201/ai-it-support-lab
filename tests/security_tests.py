from app import get_it_support_response


TEST_TICKETS = [
    {
        "name": "wifi_connection",
        "ticket": "My Windows laptop cannot connect to Wi-Fi, but my phone can.",
        "expected_category": "Network",
        "acceptable_priorities": ["Low", "Medium"]
    },
    {
        "name": "password_reset",
        "ticket": "I forgot my company account password and cannot log in.",
        "expected_category": "Authentication",
        "acceptable_priorities": ["Medium", "High"]
    },
    {
        "name": "slow_computer",
        "ticket": "My Windows computer has become extremely slow since yesterday.",
        "expected_category": "Hardware",
        "acceptable_priorities": ["Low", "Medium"]
    },
    {
        "name": "printer_problem",
        "ticket": "I can see the office printer, but my documents will not print.",
        "expected_category": "Printer",
        "acceptable_priorities": ["Low", "Medium"]
    },
    {
        "name": "possible_phishing",
        "ticket": (
            "I received an unexpected email asking me to sign in to Microsoft 365 "
            "using a link in the email."
        ),
        "expected_category": "Security",
        "acceptable_priorities": ["High", "Critical"]
    }
]


def evaluate_test(test, result):
    category_pass = (
        result["category"].lower()
        == test["expected_category"].lower()
    )

    priority_pass = (
        result["priority"]
        in test["acceptable_priorities"]
    )

    overall_pass = category_pass and priority_pass

    return category_pass, priority_pass, overall_pass


def run_baseline_tests():
    print("AI IT SUPPORT LAB - BASELINE TESTS")
    print("=" * 50)

    passed = 0
    failed = 0

    for test in TEST_TICKETS:
        print(f"\nTEST: {test['name']}")
        print(f"TICKET: {test['ticket']}")

        try:
            result = get_it_support_response(test["ticket"])

            category_pass, priority_pass, overall_pass = (
                evaluate_test(test, result)
            )

            print("\nRESULT")
            print(f"Category: {result['category']}")
            print(f"Priority: {result['priority']}")

            print("\nEXPECTED")
            print(f"Category: {test['expected_category']}")
            print(
                "Acceptable priorities: "
                + ", ".join(test["acceptable_priorities"])
            )

            print("\nCHECKS")
            print(
                f"Category: {'PASS' if category_pass else 'FAIL'}"
            )
            print(
                f"Priority: {'PASS' if priority_pass else 'FAIL'}"
            )
            print(
                f"Overall: {'PASS' if overall_pass else 'FAIL'}"
            )

            if overall_pass:
                passed += 1
            else:
                failed += 1

        except Exception as error:
            failed += 1

            print("\nSTATUS: ERROR")
            print(f"ERROR: {error}")

        print("-" * 50)

    total = passed + failed

    print("\nBASELINE SUMMARY")
    print("=" * 50)
    print(f"Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

    if total > 0:
        pass_rate = (passed / total) * 100
        print(f"Pass rate: {pass_rate:.1f}%")


if __name__ == "__main__":
    run_baseline_tests()
