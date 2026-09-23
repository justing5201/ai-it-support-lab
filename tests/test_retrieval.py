from rag.retriever import retrieve_relevant_sops


TEST_QUERIES = [
    {
        "query": (
            "GlobalProtect keeps saying authentication failed, "
            "but I can sign in to Microsoft 365."
        ),
        "expected": "vpn.md",
    },
    {
        "query": (
            "I entered my password incorrectly several times "
            "and now my company account says it is locked."
        ),
        "expected": "password_reset.md",
    },
    {
        "query": (
            "The accounting printer shows offline on my computer, "
            "but other employees can print."
        ),
        "expected": "printer.md",
    },
    {
        "query": (
            "I received an unexpected Microsoft login email "
            "with a link asking me to sign in."
        ),
        "expected": "phishing.md",
    },
    {
        "query": (
            "My Windows laptop has become extremely slow "
            "and programs take several minutes to open."
        ),
        "expected": "windows_performance.md",
    },
]


def main():
    passed = 0

    for test in TEST_QUERIES:
        results = retrieve_relevant_sops(
            test["query"],
            top_k=3
        )

        top_result = results[0]

        actual = top_result["source"]
        score = top_result["score"]

        test_passed = actual == test["expected"]

        if test_passed:
            passed += 1

        print("\n" + "=" * 60)
        print(f"QUERY: {test['query']}")
        print(f"EXPECTED: {test['expected']}")
        print(f"RETRIEVED: {actual}")
        print(f"SCORE: {score:.4f}")
        print(f"RESULT: {'PASS' if test_passed else 'FAIL'}")

        print("\nTOP 3:")

        for number, result in enumerate(
            results,
            start=1
        ):
            print(
                f"{number}. {result['source']} "
                f"({result['score']:.4f})"
            )

    total = len(TEST_QUERIES)

    print("\n" + "=" * 60)
    print("RETRIEVAL TEST SUMMARY")
    print("=" * 60)
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy: {(passed / total) * 100:.1f}%")


if __name__ == "__main__":
    main()