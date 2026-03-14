"""Comprehensive test suite for DGIC reasoning layer."""

import unittest
from multi_state_model import EpistemicState, EpistemicStateSet
from state_evolution_engine import StateEvolutionEngine
from state_interference_model import StateInterferenceModel
from collapse_policy_engine import CollapsePolicyEngine
from knowledge_propagation_model import KnowledgePropagationModel
from exceptions import ValidationError, EvolutionError, InterferenceError, CollapseError, PropagationError
from config import ReasoningConfig, set_config


class TestEpistemicState(unittest.TestCase):
    """Test EpistemicState validation and behavior."""
    
    def test_valid_state_creation(self):
        """Test creating valid epistemic state."""
        state = EpistemicState(
            epistemic_state="THREAT",
            confidence=0.7,
            entropy=0.3,
            evidence_set=["S1", "S2"]
        )
        self.assertEqual(state.epistemic_state, "THREAT")
        self.assertEqual(state.confidence, 0.7)
    
    def test_invalid_confidence_too_high(self):
        """Test that confidence > 1.0 raises error."""
        with self.assertRaises(ValidationError):
            EpistemicState(
                epistemic_state="THREAT",
                confidence=1.5,
                entropy=0.3,
                evidence_set=["S1"]
            )
    
    def test_invalid_confidence_negative(self):
        """Test that negative confidence raises error."""
        with self.assertRaises(ValidationError):
            EpistemicState(
                epistemic_state="THREAT",
                confidence=-0.1,
                entropy=0.3,
                evidence_set=["S1"]
            )
    
    def test_invalid_entropy_too_high(self):
        """Test that entropy > 1.0 raises error."""
        with self.assertRaises(ValidationError):
            EpistemicState(
                epistemic_state="THREAT",
                confidence=0.7,
                entropy=1.5,
                evidence_set=["S1"]
            )
    
    def test_empty_epistemic_state(self):
        """Test that empty epistemic_state raises error."""
        with self.assertRaises(ValidationError):
            EpistemicState(
                epistemic_state="",
                confidence=0.7,
                entropy=0.3,
                evidence_set=["S1"]
            )
    
    def test_invalid_evidence_set_type(self):
        """Test that non-list evidence_set raises error."""
        with self.assertRaises(ValidationError):
            EpistemicState(
                epistemic_state="THREAT",
                confidence=0.7,
                entropy=0.3,
                evidence_set="S1"
            )
    
    def test_evidence_hash_deterministic(self):
        """Test that evidence hash is deterministic."""
        state1 = EpistemicState(
            epistemic_state="THREAT",
            confidence=0.7,
            entropy=0.3,
            evidence_set=["S1", "S2"]
        )
        state2 = EpistemicState(
            epistemic_state="THREAT",
            confidence=0.7,
            entropy=0.3,
            evidence_set=["S2", "S1"]
        )
        self.assertEqual(state1.evidence_hash(), state2.evidence_hash())


class TestEpistemicStateSet(unittest.TestCase):
    """Test EpistemicStateSet operations."""
    
    def test_add_state(self):
        """Test adding states to set."""
        state_set = EpistemicStateSet()
        state = EpistemicState(
            epistemic_state="THREAT",
            confidence=0.7,
            entropy=0.3,
            evidence_set=["S1"]
        )
        state_set.add_state(state)
        self.assertEqual(state_set.size(), 1)
    
    def test_deterministic_ordering(self):
        """Test that states are returned in deterministic order."""
        state_set = EpistemicStateSet()
        state1 = EpistemicState("THREAT", 0.7, 0.3, ["S1"])
        state2 = EpistemicState("SENSOR_ERROR", 0.5, 0.5, ["S2"])
        
        state_set.add_state(state2)
        state_set.add_state(state1)
        
        states = state_set.get_states()
        self.assertEqual(states[0].epistemic_state, "SENSOR_ERROR")
        self.assertEqual(states[1].epistemic_state, "THREAT")
    
    def test_invalid_state_type(self):
        """Test that adding non-EpistemicState raises error."""
        state_set = EpistemicStateSet()
        with self.assertRaises(ValidationError):
            state_set.add_state("not a state")


class TestStateEvolutionEngine(unittest.TestCase):
    """Test state evolution engine."""
    
    def setUp(self):
        self.engine = StateEvolutionEngine()
    
    def test_evolution_with_supporting_evidence(self):
        """Test state evolution with supporting evidence."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state_set.add_state(state)
        
        evidence = {"signal_id": "S2", "type": "THREAT"}
        evolved = self.engine.evolve_states(state_set, evidence)
        
        evolved_state = evolved.get_states()[0]
        self.assertGreater(evolved_state.confidence, 0.6)
        self.assertLess(evolved_state.entropy, 0.4)
    
    def test_evolution_with_contradicting_evidence(self):
        """Test state evolution with contradicting evidence."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state_set.add_state(state)
        
        evidence = {"signal_id": "S2", "type": "CONTRADICTION"}
        evolved = self.engine.evolve_states(state_set, evidence)
        
        evolved_state = evolved.get_states()[0]
        self.assertLess(evolved_state.confidence, 0.6)
        self.assertGreater(evolved_state.entropy, 0.4)
    
    def test_invalid_evidence_missing_signal_id(self):
        """Test that missing signal_id raises error."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state_set.add_state(state)
        
        evidence = {"type": "THREAT"}
        with self.assertRaises(ValidationError):
            self.engine.evolve_states(state_set, evidence)
    
    def test_invalid_evidence_missing_type(self):
        """Test that missing type raises error."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state_set.add_state(state)
        
        evidence = {"signal_id": "S2"}
        with self.assertRaises(ValidationError):
            self.engine.evolve_states(state_set, evidence)


class TestStateInterferenceModel(unittest.TestCase):
    """Test state interference model."""
    
    def setUp(self):
        self.model = StateInterferenceModel()
    
    def test_compatible_states_reinforce(self):
        """Test that compatible states reinforce each other."""
        state_set = EpistemicStateSet()
        state1 = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state2 = EpistemicState("THREAT", 0.5, 0.5, ["S2"])
        state_set.add_state(state1)
        state_set.add_state(state2)
        
        interfered = self.model.apply_interference(state_set)
        interfered_states = interfered.get_states()
        
        # Both should have increased confidence
        self.assertGreater(interfered_states[0].confidence, 0.5)
        self.assertGreater(interfered_states[1].confidence, 0.6)
    
    def test_conflicting_states_weaken(self):
        """Test that conflicting states weaken each other."""
        state_set = EpistemicStateSet()
        state1 = EpistemicState("THREAT", 0.6, 0.4, ["S1"])
        state2 = EpistemicState("SENSOR_ERROR", 0.7, 0.3, ["S2"])
        state_set.add_state(state1)
        state_set.add_state(state2)
        
        interfered = self.model.apply_interference(state_set)
        interfered_states = interfered.get_states()
        
        # Lower confidence state should be weakened
        threat_state = [s for s in interfered_states if s.epistemic_state == "THREAT"][0]
        self.assertLess(threat_state.confidence, 0.6)


class TestCollapsePolicyEngine(unittest.TestCase):
    """Test collapse policy engine."""
    
    def setUp(self):
        self.engine = CollapsePolicyEngine()
    
    def test_collapse_on_high_confidence(self):
        """Test collapse when confidence exceeds threshold."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.88, 0.12, ["S1", "S2"])
        state_set.add_state(state)
        
        result = self.engine.evaluate_collapse(state_set)
        self.assertIsNotNone(result)
        self.assertEqual(result.epistemic_state, "THREAT")
    
    def test_collapse_on_low_entropy(self):
        """Test collapse when entropy falls below floor."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.7, 0.15, ["S1", "S2"])
        state_set.add_state(state)
        
        result = self.engine.evaluate_collapse(state_set)
        self.assertIsNotNone(result)
    
    def test_collapse_on_dominance_gap(self):
        """Test collapse when dominance gap is large."""
        state_set = EpistemicStateSet()
        state1 = EpistemicState("THREAT", 0.8, 0.2, ["S1"])
        state2 = EpistemicState("SENSOR_ERROR", 0.5, 0.5, ["S2"])
        state_set.add_state(state1)
        state_set.add_state(state2)
        
        result = self.engine.evaluate_collapse(state_set)
        self.assertIsNotNone(result)
        self.assertEqual(result.epistemic_state, "THREAT")
    
    def test_no_collapse_ambiguous_state(self):
        """Test no collapse when ambiguity is high."""
        state_set = EpistemicStateSet()
        state1 = EpistemicState("THREAT", 0.55, 0.45, ["S1"])
        state2 = EpistemicState("SENSOR_ERROR", 0.50, 0.50, ["S2"])
        state_set.add_state(state1)
        state_set.add_state(state2)
        
        result = self.engine.evaluate_collapse(state_set)
        self.assertIsNone(result)
    
    def test_empty_state_set(self):
        """Test collapse on empty state set."""
        state_set = EpistemicStateSet()
        result = self.engine.evaluate_collapse(state_set)
        self.assertIsNone(result)


class TestKnowledgePropagationModel(unittest.TestCase):
    """Test knowledge propagation model."""
    
    def setUp(self):
        self.model = KnowledgePropagationModel()
    
    def test_propagate_single_node(self):
        """Test propagation from single node."""
        state_set = EpistemicStateSet()
        state = EpistemicState("THREAT", 0.7, 0.3, ["S1"])
        state_set.add_state(state)
        
        result = self.model.propagate([state_set])
        self.assertEqual(result.size(), 1)
    
    def test_propagate_multiple_nodes(self):
        """Test propagation from multiple nodes."""
        state_set1 = EpistemicStateSet()
        state_set1.add_state(EpistemicState("THREAT", 0.8, 0.2, ["S1"]))
        
        state_set2 = EpistemicStateSet()
        state_set2.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S2"]))
        
        result = self.model.propagate([state_set1, state_set2])
        states = result.get_states()
        
        self.assertEqual(len(states), 1)
        self.assertAlmostEqual(states[0].confidence, 0.7)
    
    def test_propagate_empty_list(self):
        """Test that empty node list raises error."""
        with self.assertRaises(ValidationError):
            self.model.propagate([])


class TestDeterminismReplay(unittest.TestCase):
    """Test determinism and replay stability."""
    
    def test_replay_identical_evolution(self):
        """Test that identical inputs produce identical outputs."""
        for _ in range(10):
            state_set = EpistemicStateSet()
            state_set.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S1"]))
            
            engine = StateEvolutionEngine()
            evidence = {"signal_id": "S2", "type": "THREAT"}
            result = engine.evolve_states(state_set, evidence)
            
            result_state = result.get_states()[0]
            self.assertEqual(result_state.confidence, 0.7)
            self.assertEqual(result_state.entropy, 0.3)
    
    def test_replay_identical_interference(self):
        """Test that interference is deterministic."""
        for _ in range(10):
            state_set = EpistemicStateSet()
            state_set.add_state(EpistemicState("THREAT", 0.6, 0.4, ["S1"]))
            state_set.add_state(EpistemicState("THREAT", 0.5, 0.5, ["S2"]))
            
            model = StateInterferenceModel()
            result = model.apply_interference(state_set)
            
            states = result.get_states()
            self.assertEqual(len(states), 2)


if __name__ == "__main__":
    unittest.main()
