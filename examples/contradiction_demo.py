"""Scientific contradiction protocol demo."""

from origin.core.contradiction import scientific_contradiction_index, scientific_contradiction_protocol


if __name__ == "__main__":
    ci = scientific_contradiction_index(e_treat=0.8, e_cause=0.8)
    print(ci, scientific_contradiction_protocol(ci, destructive=True))
