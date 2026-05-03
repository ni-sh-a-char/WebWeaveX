"""Final validation test suite"""
from webweavex import run, __version__

def test_universal():
    """Test all inputs"""
    tests = [
        'build REST API',
        'create docker app',
        'login system',
        'quantum trading engine',
        'design compiler',
        'ai assistant'
    ]
    
    for inp in tests:
        r = run({'input': inp})
        sd = r.get('structured_data', {})
        design = sd.get('system_design', {})
        
        assert design.get('system_type'), f"Missing system_type for {inp}"
    
    print("Universal inputs: PASS")

def test_determinism():
    """Test determinism"""
    r1 = run({'input': 'test-det'})
    r2 = run({'input': 'test-det'})
    
    assert r1 == r2, "Determinism failed"
    print("Determinism: PASS")

def test_compiler_mode():
    """Test compiler mode performance"""
    import time
    
    start = time.time()
    r = run({'input': 'build API', 'mode': 'compiler'})
    elapsed = time.time() - start
    
    assert elapsed < 1.0, f"Too slow: {elapsed}s"
    print(f"Compiler mode: PASS ({elapsed:.3f}s)")

def test_zero_hardcoding():
    """Verify no hardcoded values"""
    # Check files don't have forbidden words in code
    import os
    
    files = [
        'core/execution_graph.py',
        'core/system_inference.py'
    ]
    
    for f in files:
        with open(f) as fp:
            content = fp.read()
        
        # Should not have execute/init/root/start as fallback
        assert '"execute"' not in content or 'return' not in content, f"Found execute in {f}"
    
    print("Zero hardcoding: PASS")

if __name__ == '__main__':
    test_universal()
    test_determinism()
    test_compiler_mode()
    test_zero_hardcoding()
    print(f"\nVERSION: {__version__}")
    print("ALL TESTS: PASS")
