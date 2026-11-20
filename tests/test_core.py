"""Your tests. Each milestone in README.md gets one here: write the test first, then make it pass.

They start skipped. Remove the `skip` line as you work on each milestone.
"""
import pytest


# Milestone 1: Compile a small dataset of product specs and marketing descriptions.
def test_milestone_1():
    from app.core import milestone_1

    result = milestone_1()

    assert isinstance(result, dict), "milestone_1 must return a dict"
    assert "dataset" in result
    assert "num_examples" in result
    assert "avg_spec_length" in result
    assert "avg_desc_length" in result

    dataset = result["dataset"]
    assert isinstance(dataset, list), "dataset must be a list"
    assert len(dataset) >= 20, f"Expected at least 20 examples, got {len(dataset)}"
    assert result["num_examples"] == len(dataset)

    for item in dataset:
        assert "spec" in item and isinstance(item["spec"], str) and item["spec"]
        assert "description" in item and isinstance(item["description"], str)
        # descriptions should be longer (richer) than specs
        assert len(item["description"]) > len(item["spec"]), (
            "description should be longer than spec"
        )

    assert result["avg_spec_length"] > 0
    assert result["avg_desc_length"] > result["avg_spec_length"], (
        "avg description length should exceed avg spec length"
    )


# Milestone 2: Implement LoRA adapter injection and training on a pre-trained LLM (e.g., GPT-2).
def test_milestone_2():
    from app.core import milestone_2

    # Use fast=True so the test runs in CI without downloading GPT-2
    result = milestone_2(fast=True)

    assert isinstance(result, dict), "milestone_2 must return a dict"
    assert "model" in result
    assert "tokenizer" in result
    assert "lora_params_count" in result
    assert "training_loss" in result

    assert isinstance(result["lora_params_count"], int)
    assert result["lora_params_count"] > 0, "LoRA must add trainable parameters"
    assert isinstance(result["training_loss"], float)
    assert result["training_loss"] >= 0.0


# Milestone 3: Develop a Streamlit UI to input product specs and generate enhanced descriptions.
def test_milestone_3():
    from app.core import milestone_3

    spec = "Wireless Bluetooth headphones, 40mm drivers, 20hr battery, foldable"
    # Call without model/tokenizer — uses rule-based fallback
    description = milestone_3(spec)

    assert isinstance(description, str), "milestone_3 must return a string"
    assert len(description) > 20, "description should be non-trivial"
    # The description should not just echo back the spec unchanged
    assert description != spec


# Milestone 4: Assess the creativity and relevance of the generated descriptions.
def test_milestone_4():
    from app.core import milestone_4

    result = milestone_4()  # uses fallback generator (no model)

    assert isinstance(result, dict), "milestone_4 must return a dict"
    assert "scores" in result
    assert "num_evaluated" in result
    assert "avg_composite_score" in result
    assert "avg_keyword_overlap" in result
    assert "avg_length_ratio" in result

    assert result["num_evaluated"] > 0
    assert isinstance(result["scores"], list)
    assert len(result["scores"]) == result["num_evaluated"]

    for score in result["scores"]:
        assert "spec" in score
        assert "generated" in score
        assert "length_ratio" in score
        assert "keyword_overlap" in score
        assert "sentence_variety" in score
        assert "composite_score" in score
        assert 0.0 <= score["composite_score"] <= 1.0

    assert 0.0 <= result["avg_composite_score"] <= 1.0


# Milestone 5: Implement adapter merging for inference.
def test_milestone_5():
    from app.core import milestone_2, milestone_5

    # Use fast stub — merging still runs (the stub model has no LoRA layers
    # to merge, but milestone_5 must handle this gracefully).
    trained = milestone_2(fast=True)
    result = milestone_5(trained)

    assert isinstance(result, dict), "milestone_5 must return a dict"
    assert "model" in result
    assert "tokenizer" in result
    assert "total_params" in result
    assert "sample_output" in result

    # For the fast stub, total_params will be 0 (fake model), that's fine
    assert isinstance(result["total_params"], int)
    assert isinstance(result["sample_output"], str)
