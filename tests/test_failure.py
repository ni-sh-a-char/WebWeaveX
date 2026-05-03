from webweavex import run

def test_failure():
    try:
        run({"input": ""})
        assert False, "Should raise"
    except Exception as e:
        print("Empty input raises:", type(e).__name__)

    try:
        run(None)
        assert False
    except Exception as e:
        print("None input raises:", type(e).__name__)

    try:
        run({"wrong": "key"})
        assert False
    except Exception as e:
        print("Wrong key raises:", type(e).__name__)

if __name__ == "__main__":
    test_failure()