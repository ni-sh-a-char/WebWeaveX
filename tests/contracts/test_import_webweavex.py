def test_webweavex_import_and_version():
    import webweavex

    assert webweavex.__version__ == "2.1.0"
    assert hasattr(webweavex, "run_canonical_pipeline")
    assert hasattr(webweavex, "UniversalInput")
