import math


class UncertaintyViolation(Exception):
    pass


class UncertaintyModel:

    def __init__(self, probabilities):
        if abs(sum(probabilities.values()) - 1.0) > 1e-6:
            raise ValueError("Probabilities must sum to 1.")

        self.probabilities = probabilities
        self.previous_entropy = self.entropy()

    def entropy(self):
        h = 0
        for p in self.probabilities.values():
            if p > 0:
                h -= p * math.log2(p)
        return h

    def update(self, new_probabilities, evidence=False):
        if abs(sum(new_probabilities.values()) - 1.0) > 1e-6:
            raise ValueError("Probabilities must sum to 1.")

        new_entropy = 0
        for p in new_probabilities.values():
            if p > 0:
                new_entropy -= p * math.log2(p)

        # Entropy reduction requires evidence
        if new_entropy < self.previous_entropy and not evidence:
            raise UncertaintyViolation(
                "Entropy decreased without evidence."
            )

        self.probabilities = new_probabilities
        self.previous_entropy = new_entropy

        return new_entropy


if __name__ == "__main__":
    model = UncertaintyModel({
        "Known": 0.25,
        "Inferred": 0.25,
        "Ambiguous": 0.25,
        "Unknown": 0.25,
    })

    print("Initial entropy:", model.entropy())

    try:
        model.update({
            "Known": 1.0,
            "Inferred": 0.0,
            "Ambiguous": 0.0,
            "Unknown": 0.0,
        }, evidence=False)
    except UncertaintyViolation as e:
        print("Blocked:", e)