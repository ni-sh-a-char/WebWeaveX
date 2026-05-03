from webweavex import run

def test_determinism():
    input = "python list sorting"
    results = [run({"input": input}) for _ in range(5)]
    for r in results[1:]:
        assert r == results[0]
    print("Determinism: strong")
    
    # For different
    input2 = "calculator app"
    r2 = run({"input": input2})
    assert r2 != results[0]
    print("Different inputs produce different outputs")

if __name__ == "__main__":
    test_determinism()