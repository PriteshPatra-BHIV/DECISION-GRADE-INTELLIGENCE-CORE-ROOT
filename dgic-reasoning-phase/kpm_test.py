from multi_state_model import EpistemicState, EpistemicStateSet
from knowledge_propagation_model import KnowledgePropagationModel


# Node A
node_a = EpistemicStateSet()

node_a.add_state(
    EpistemicState("THREAT",0.7,0.3,["S1"])
)

# Node B
node_b = EpistemicStateSet()

node_b.add_state(
    EpistemicState("THREAT",0.5,0.5,["S2"])
)

node_b.add_state(
    EpistemicState("SENSOR_ERROR",0.4,0.6,["S3"])
)

prop = KnowledgePropagationModel()

result = prop.propagate([node_a,node_b])

print(result.to_list())