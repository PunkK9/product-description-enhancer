"""Write results/evaluation.json from a real GPT-2 LoRA run."""

from app.core import save_evaluation


def main():
    report = save_evaluation()
    lora = report["lora"]
    averages = report["averages"]
    print(
        f"loss {lora['baseline_loss']} -> {lora['final_eval_loss']} | "
        f"keyword overlap template {averages['template_keyword_overlap']}, "
        f"untouched {averages['untouched_keyword_overlap']}, "
        f"lora {averages['lora_keyword_overlap']}"
    )
    print("wrote results/evaluation.json")


if __name__ == "__main__":
    main()
