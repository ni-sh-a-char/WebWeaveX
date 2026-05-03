"""PHASE 6: Production Grade Test Suite"""
import time
import unittest
from webweavex import run, __version__


class TestUniversalInput(unittest.TestCase):
    """Test all inputs derive valid system designs."""
    
    inputs = [
        "build REST API",
        "quantum trading engine",
        "design compiler",
        "ai assistant",
        "distributed database",
        "real time chat system"
    ]
    
    def test_universal_input(self):
        for inp in self.inputs:
            r = run({"input": inp, "mode": "compiler"})
            sd = r.get("structured_data", {})
            sys = sd.get("system", {})
            
            # PURE: components exist (derived from input tokens)
            components = sys.get("components", [])
            self.assertIsInstance(components, list, f"Components not list for {inp}")
            self.assertTrue(len(components) > 0, f"No components derived for {inp}")


class TestDeterminism(unittest.TestCase):
    """Test deterministic output."""
    
    def test_determinism(self):
        r1 = run({"input": "test", "mode": "compiler"})
        r2 = run({"input": "test", "mode": "compiler"})
        r3 = run({"input": "test", "mode": "compiler"})
        
        self.assertEqual(r1, r2)
        self.assertEqual(r2, r3)


class TestZeroHardcoding(unittest.TestCase):
    """Test no hardcoded fallback words exist."""
    
    forbidden = ["init", "start", "root", "execute"]
    files = [
        "core/execution_graph.py",
        "core/system_inference.py",
        "core/semantic_graph.py"
    ]
    
    def test_zero_hardcoding(self):
        for f in self.files:
            with open(f) as fp:
                content = fp.read()
            
            for word in self.forbidden:
                self.assertNotIn(f'"{word}"', content, f"Found {word} in {f}")


class TestSemanticPurity(unittest.TestCase):
    """Test semantic engine purity."""
    
    def test_no_semantic_maps(self):
        with open("core/semantic_engine.py") as fp:
            content = fp.read()
        
        forbidden_maps = ["ENTITY_PATTERN_MAP", "ACTION_VERBS"]
        for m in forbidden_maps:
            self.assertNotIn(m, content, f"Found {m} in semantic_engine.py")


class TestPerformance(unittest.TestCase):
    """Test compiler mode performance."""
    
    def test_performance(self):
        start = time.time()
        r = run({"input": "build system", "mode": "compiler"})
        elapsed = time.time() - start
        
        self.assertLess(elapsed, 1.0, f"Too slow: {elapsed}s")


class TestGraphPurity(unittest.TestCase):
    """Test execution graph purity."""
    
    def test_graph_purity(self):
        r = run({"input": "test", "mode": "compiler"})
        sd = r.get("structured_data", {})
        edges = sd.get("execution_plan", {}).get("edges", [])
        
        for e in edges:
            self.assertNotEqual(e.get("from"), "init")
            self.assertNotEqual(e.get("to"), "start")


if __name__ == "__main__":
    print(f"VERSION: {__version__}")
    print("Running Phase 6 tests...")
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestUniversalInput))
    suite.addTests(loader.loadTestsFromTestCase(TestDeterminism))
    suite.addTests(loader.loadTestsFromTestCase(TestZeroHardcoding))
    suite.addTests(loader.loadTestsFromTestCase(TestSemanticPurity))
    suite.addTests(loader.loadTestsFromTestCase(TestPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphPurity))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if result.wasSuccessful():
        print("\nALL PHASE 6 TESTS PASSED")
    else:
        print("\nTESTS FAILED")