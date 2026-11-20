"""Product-description milestones: dataset, LoRA fine-tune, generation, scoring, merge."""

import json
import re
from pathlib import Path


# ---------------------------------------------------------------------------
# Milestone 1: Compile a small dataset of product specs and marketing descriptions.
# ---------------------------------------------------------------------------
def milestone_1():
    """Return a dataset of (spec, description) pairs plus summary statistics."""
    dataset = [
        {
            "spec": "Wireless Bluetooth headphones, 40mm drivers, 20hr battery, foldable, USB-C charging",
            "description": "Experience rich, immersive sound with these premium wireless Bluetooth headphones. Featuring powerful 40mm drivers that deliver crisp highs and deep bass, you'll lose yourself in your favourite music. With an impressive 20-hour battery life and fast USB-C charging, they're built for all-day listening. The sleek foldable design makes them perfect for commuters and travellers on the go.",
        },
        {
            "spec": "Stainless steel water bottle, 750ml, double-wall insulated, leak-proof lid, BPA-free",
            "description": "Stay hydrated in style with our stainless steel insulated water bottle. The double-wall vacuum insulation keeps drinks cold for 24 hours or hot for 12, so your beverage is always at the perfect temperature. The 750ml capacity is ideal for the gym, hikes, or long work days. Its leak-proof lid and BPA-free construction mean you can toss it in your bag with total confidence.",
        },
        {
            "spec": "Men's slim-fit chino trousers, 98% cotton 2% elastane, available in navy/khaki/olive, machine washable",
            "description": "Elevate your everyday wardrobe with our versatile slim-fit chino trousers. Crafted from a premium 98% cotton and 2% elastane blend, they offer a sharp tailored look with the comfort and flexibility you need for a full day's wear. Available in classic navy, khaki, and olive colourways, these machine-washable trousers pair effortlessly with everything from casual tees to smart shirts.",
        },
        {
            "spec": "Smart LED desk lamp, 5 colour temperatures, touch dimmer, USB-A charging port, flexible gooseneck arm",
            "description": "Illuminate your workspace with the ultimate in modern lighting. Our smart LED desk lamp offers five colour temperatures—from warm relaxing tones to cool daylight—so you can optimise your environment for work, study, or creative tasks. The touch dimmer lets you dial in the perfect brightness in seconds, while the built-in USB-A port keeps your devices charged. The flexible gooseneck arm bends to direct light exactly where you need it.",
        },
        {
            "spec": "Non-stick ceramic frying pan, 28cm, induction compatible, oven safe to 220°C, PFOA-free",
            "description": "Cook with confidence using our premium ceramic non-stick frying pan. The advanced ceramic coating ensures effortless food release and easy clean-up without the use of harmful PFOA chemicals. At 28cm, it's the perfect size for family meals, and its induction-compatible base means it works on all hob types. Pop it in the oven up to 220°C to finish dishes to perfection.",
        },
        {
            "spec": "Yoga mat, 6mm thick, natural rubber base, alignment lines, carry strap included, 183x61cm",
            "description": "Deepen your practice with our professional-grade yoga mat. The 6mm cushioning provides superior joint support during every pose, while the natural rubber base grips the floor firmly so you can focus entirely on your flow. Printed alignment lines help you perfect your form, and the included carry strap makes transport effortless. Measuring 183x61cm, it offers ample space for practitioners of all sizes.",
        },
        {
            "spec": "4K action camera, waterproof to 30m, 170° wide-angle lens, built-in WiFi, 2 rechargeable batteries",
            "description": "Capture your adventures in breathtaking 4K detail with our rugged action camera. Waterproof to 30 metres straight out of the box, it's ready for surfing, diving, snowboarding, and beyond. The 170° ultra-wide-angle lens ensures you never miss a moment of the action, and built-in WiFi lets you share footage instantly from your smartphone. Two rechargeable batteries are included so you can shoot all day long.",
        },
        {
            "spec": "Mechanical gaming keyboard, TKL layout, red linear switches, RGB per-key lighting, detachable USB-C cable",
            "description": "Gain the competitive edge with our tenkeyless mechanical gaming keyboard. Smooth, responsive red linear switches register every keystroke with precision and minimal actuation force, keeping you one step ahead in fast-paced games. Per-key RGB lighting with millions of customisable colours lets you personalise your setup to match your style. The detachable braided USB-C cable makes transportation and desk management a breeze.",
        },
        {
            "spec": "Women's running trainers, breathable mesh upper, EVA midsole, anti-slip rubber outsole, UK sizes 3-9",
            "description": "Run further and faster in our high-performance women's running trainers. The lightweight breathable mesh upper promotes airflow to keep your feet cool and dry, mile after mile. A cushioned EVA midsole absorbs impact to protect your joints on every stride, while the anti-slip rubber outsole provides reliable grip on roads, tracks, and light trails. Available in UK sizes 3–9 for a perfect fit.",
        },
        {
            "spec": "Portable power bank, 20000mAh, dual USB-A + USB-C output, 22.5W fast charge, LED battery indicator",
            "description": "Never run out of power on the road again. Our high-capacity 20000mAh power bank provides multiple full charges for smartphones, tablets, and earbuds. With dual USB-A outputs and a USB-C port delivering 22.5W fast charging, you can charge two devices simultaneously at full speed. The handy LED battery indicator keeps you informed of remaining capacity at a glance.",
        },
        {
            "spec": "Bamboo cutting board, 40x30cm, juice groove, non-slip feet, end-grain construction",
            "description": "Upgrade your kitchen prep with our eco-friendly bamboo cutting board. The end-grain construction is exceptionally gentle on knife edges, extending the life of your blades, while the deep juice groove channels liquids away from your worktop. Measuring 40x30cm, it provides ample prep space for every task, and the non-slip rubber feet keep it firmly anchored during use. Bamboo is naturally antimicrobial and sustainably sourced.",
        },
        {
            "spec": "Smart thermostat, WiFi-enabled, voice control compatible, 7-day programming, energy usage reports",
            "description": "Take control of your home's comfort and cut your energy bills with our intelligent smart thermostat. Set personalised 7-day heating and cooling schedules that adapt to your lifestyle, and adjust the temperature from anywhere in the world using your smartphone. Compatible with Alexa and Google Assistant for seamless voice control. Detailed energy usage reports help you spot savings and reduce your carbon footprint.",
        },
        {
            "spec": "Men's merino wool crew-neck sweater, 100% merino, mid-weight, ribbed cuffs and hem, hand-wash recommended",
            "description": "Indulge in the timeless luxury of our 100% merino wool crew-neck sweater. Merino's naturally fine fibres are supremely soft against the skin—no scratching or itching—and provide outstanding temperature regulation, keeping you warm in winter and cool in milder weather. The mid-weight knit strikes the ideal balance between warmth and versatility, while ribbed cuffs and hem add a refined, well-tailored finish.",
        },
        {
            "spec": "Electric toothbrush, sonic technology, 40000 strokes/min, 4 cleaning modes, 2-min timer, 30-day battery",
            "description": "Achieve a dentist-clean smile every day with our advanced sonic electric toothbrush. Generating 40,000 brush strokes per minute, it removes up to 10x more plaque than a manual brush, promoting healthier gums and brighter teeth. Choose from four cleaning modes—Clean, White, Sensitive, and Gum Care—to suit your needs, and let the built-in 2-minute timer ensure you brush for the dentist-recommended duration. A single charge lasts up to 30 days.",
        },
        {
            "spec": "Indoor plant pot set, 3 sizes (10/14/18cm), drainage holes, terracotta finish, matching saucers",
            "description": "Bring natural warmth and texture to any room with our elegant terracotta-finish plant pot set. The set of three graduated sizes—10cm, 14cm, and 18cm—lets you create beautiful, layered displays with your favourite indoor plants. Each pot features drainage holes to prevent waterlogging, promoting healthy root growth, and comes with a matching saucer to protect your surfaces. The classic terracotta aesthetic complements every interior style.",
        },
        {
            "spec": "Coffee grinder, burr mill, 18 grind settings, 200g hopper, stainless steel burrs, anti-static",
            "description": "Unlock the full flavour potential of your coffee beans with our precision burr coffee grinder. With 18 grind settings ranging from ultra-fine espresso to coarse French press, you'll find the perfect grind for every brewing method. The stainless steel conical burrs grind consistently and evenly, preserving the beans' delicate aromatic oils. The generously sized 200g hopper handles enough beans for a full week, and the anti-static design keeps your counter mess-free.",
        },
        {
            "spec": "Laptop stand, aluminium, adjustable height 15-45cm, foldable, compatible with 11-17\" laptops, 8kg load",
            "description": "Transform your workstation ergonomics with our sleek aluminium laptop stand. Raising your screen to eye level prevents neck and shoulder strain during long work sessions. The smooth height adjustment from 15 to 45cm lets you find the ideal position whether you're sitting or standing, and the sturdy build supports laptops up to 8kg. When the day is done, it folds flat in seconds for easy portability between home, office, and coffee shop.",
        },
        {
            "spec": "Wool-blend throw blanket, 130x170cm, herringbone pattern, machine washable, fringed edges",
            "description": "Wrap yourself in cosy sophistication with our premium wool-blend throw blanket. The classic herringbone weave lends timeless elegance to sofas, armchairs, and beds, while the luxurious wool-blend fabric provides exceptional warmth without weight. At 130x170cm, it's generously sized for two, and the delicate fringed edges add a stylish artisanal touch. Machine washable for effortless care—simply pop it in and it's ready to cosy up with again.",
        },
        {
            "spec": "Stainless steel multi-tool, 14 functions, nylon pouch included, full-size pliers, 420HC steel",
            "description": "Be prepared for anything with our professional-grade stainless steel multi-tool. Crafted from tough 420HC stainless steel, its 14 functions—including full-size pliers, knife, scissors, saw, file, and screwdrivers—handle every task from trail fixes to workshop jobs. All tools lock open securely for safe, confident use. The included nylon belt pouch means your multi-tool is always within reach when you need it most.",
        },
        {
            "spec": "Memory foam pillow, contour design, bamboo cover, anti-allergy, medium firmness, 60x40cm",
            "description": "Wake up refreshed with the support your neck deserves. Our contour memory foam pillow is engineered to cradle the head and neck in perfect alignment, relieving pressure points that cause morning stiffness and discomfort. The breathable bamboo-derived cover wicks moisture and regulates temperature throughout the night, while the anti-allergy treatment makes it ideal for sensitive sleepers. Medium firmness suits a wide range of sleep positions.",
        },
        {
            "spec": "Hardside suitcase, 65L, TSA-approved lock, 360° spinner wheels, polycarbonate shell, expandable 15%",
            "description": "Travel in style and security with our ultra-durable hardside suitcase. The lightweight polycarbonate shell absorbs knocks and bumps without adding unnecessary weight to your luggage allowance, while the TSA-approved combination lock keeps your belongings safe at every border. Smooth 360° spinner wheels glide effortlessly across any surface, and the expandable zip adds 15% extra packing capacity when you need it.",
        },
        {
            "spec": "Garden kneeler and seat, foldable, steel frame, foam pad, tool pouches on sides, 150kg capacity",
            "description": "Make gardening more comfortable than ever with our versatile kneeler and seat. Flip it upright as a kneeler to protect your knees on hard ground, or flip it over to use as a stable seat with a maximum capacity of 150kg. The thick foam pad provides generous cushioning in both positions, and the handy side tool pouches keep your trowel, gloves, and seed packets within arm's reach. The foldable steel frame collapses for compact storage.",
        },
        {
            "spec": "USB-C hub, 7-in-1, 4K HDMI, 100W pass-through, 3x USB-A 3.0, SD/microSD reader, aluminium",
            "description": "Expand your laptop's connectivity effortlessly with our slim 7-in-1 USB-C hub. Connect a 4K HDMI monitor for stunning external display output, transfer data at USB 3.0 speeds across three USB-A ports, and read SD and microSD cards simultaneously—all from a single connection. The 100W USB-C pass-through keeps your laptop charged while you work, and the premium aluminium casing matches the aesthetic of modern ultrabooks perfectly.",
        },
        {
            "spec": "Sous vide precision cooker, 1000W, 0.1°C accuracy, 15L capacity, touchscreen, WiFi app control",
            "description": "Achieve restaurant-quality results at home with our professional sous vide precision cooker. Set your target temperature to within 0.1°C accuracy and let the 1000W heater circulate water evenly around your food for flawlessly cooked meat, fish, and vegetables every time. The intuitive touchscreen makes setup simple, and WiFi app control lets you monitor and adjust your cook from anywhere in the house. Suits containers up to 15 litres.",
        },
        {
            "spec": "Backpack, 30L, laptop compartment up to 15.6\", waterproof nylon, padded shoulder straps, USB charging port",
            "description": "Carry everything you need in organised comfort with our 30-litre everyday backpack. The dedicated padded laptop compartment safely fits screens up to 15.6 inches, while multiple inner and outer pockets keep your essentials sorted and accessible. Durable waterproof nylon shields your gear from unexpected showers, and padded, adjustable shoulder straps distribute weight evenly for all-day comfort. A built-in USB charging port lets you top up your devices on the move.",
        },
        {
            "spec": "Portable Bluetooth speaker, IP67 waterproof, 360° sound, 24hr playtime, built-in mic, TWS pairing",
            "description": "Take your music anywhere with our rugged IP67-rated Bluetooth speaker. Fully waterproof and dustproof, it's built for beaches, campsites, and pool parties. The 360° omnidirectional driver fills any space with rich, full-bodied sound, while the 24-hour playtime means the music keeps going long after the sun goes down. Pair two speakers together via True Wireless Stereo for an even more immersive listening experience.",
        },
        {
            "spec": "Cast iron skillet, 25cm, pre-seasoned, dual pour spouts, helper handle, oven safe to 260°C",
            "description": "Build the perfect sear and develop flavours you simply can't achieve in an ordinary pan. Our pre-seasoned cast iron skillet arrives ready to cook from day one and only improves with use. The 25cm diameter is ideally sized for steaks, chops, and cornbread, and dual pour spouts make draining fat or basting juices effortless. With a secondary helper handle for safe manoeuvring and oven safety up to 260°C, it transitions seamlessly from hob to oven.",
        },
        {
            "spec": "Electric standing desk, 120x60cm, dual motor, 3 memory presets, anti-collision, weight capacity 80kg",
            "description": "Invest in your health and productivity with our electric height-adjustable standing desk. The powerful dual-motor system raises and lowers your 120x60cm workspace smoothly and quietly at the touch of a button, with three memory presets so you switch between your favourite heights in an instant. The intelligent anti-collision system reverses direction if it detects an obstacle, protecting your equipment and your desk. Supports up to 80kg of monitors, books, and kit.",
        },
        {
            "spec": "Protein powder, whey isolate, 2kg, 25g protein per serving, chocolate flavour, low sugar, NSF certified",
            "description": "Fuel your training and accelerate recovery with our premium NSF Certified whey isolate protein powder. Each serving delivers 25 grams of fast-absorbing, high-quality protein with minimal sugar, making it ideal for lean muscle building and post-workout nutrition. Our rich chocolate flavour mixes smoothly with water or milk for a shake that actually tastes great. The 2kg tub provides over 60 servings of consistent, lab-tested quality you can trust.",
        },
        {
            "spec": "Smart doorbell, 1080p HD camera, motion detection, two-way audio, night vision, app notifications, cloud storage",
            "description": "Know who's at your door before you open it. Our smart video doorbell streams crystal-clear 1080p HD footage directly to your smartphone, wherever you are. Advanced motion detection alerts you the moment someone approaches, and two-way audio lets you speak with visitors or deter unwanted callers with ease. Full-colour night vision ensures you never miss a detail after dark, while optional cloud storage keeps a rolling archive of recordings for complete peace of mind.",
        },
    ]

    specs = [d["spec"] for d in dataset]
    descriptions = [d["description"] for d in dataset]

    avg_spec_length = sum(len(s.split()) for s in specs) / len(specs)
    avg_desc_length = sum(len(d.split()) for d in descriptions) / len(descriptions)

    return {
        "dataset": dataset,
        "num_examples": len(dataset),
        "avg_spec_length": round(avg_spec_length, 2),
        "avg_desc_length": round(avg_desc_length, 2),
    }


# ---------------------------------------------------------------------------
# Milestone 2: Implement LoRA adapter injection and training on a pre-trained LLM.
# ---------------------------------------------------------------------------
def milestone_2(fast: bool = False, steps: int = 8):
    """
    Inject LoRA adapters into GPT-2 and fine-tune for a few steps.

    Parameters
    ----------
    fast : bool
        When True, skip the actual model download (used by unit tests).
    steps : int
        Optimizer steps on the first eight training pairs.
    """
    import torch
    import torch.nn as nn

    if fast:
        # Lightweight stub used by tests in CI — no model download required.
        class _FakeModel:
            pass

        class _FakeTokenizer:
            pass

        return {
            "model": _FakeModel(),
            "tokenizer": _FakeTokenizer(),
            "lora_params_count": 32768,
            "training_loss": 0.5,
        }

    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    # --- Load GPT-2 (small, ~117M params) ---
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    for parameter in model.parameters():
        parameter.requires_grad = False

    # --- LoRA hyper-parameters ---
    RANK = 4          # low-rank dimension
    ALPHA = 16        # scaling factor
    SCALE = ALPHA / RANK

    # --- Inject LoRA adapters ---
    class LoRALinear(nn.Module):
        """Wraps an existing nn.Linear with two trainable low-rank matrices."""

        def __init__(self, original: nn.Linear, rank: int, scale: float):
            super().__init__()
            self.original = original
            self.scale = scale
            # Freeze original weights
            for p in self.original.parameters():
                p.requires_grad = False
            # Low-rank matrices
            in_f = original.weight.shape[1]
            out_f = original.weight.shape[0]
            self.lora_A = nn.Parameter(torch.randn(rank, in_f) * 0.01)
            self.lora_B = nn.Parameter(torch.zeros(out_f, rank))

        def forward(self, x):
            base_out = self.original(x)
            lora_out = (x @ self.lora_A.T) @ self.lora_B.T
            return base_out + lora_out * self.scale

    lora_params_count = 0
    for block in model.transformer.h:
        old_attn = block.attn.c_attn   # Conv1D acting as linear
        # Convert Conv1D to Linear for compatibility
        in_f = old_attn.weight.shape[0]
        out_f = old_attn.weight.shape[1]
        new_linear = nn.Linear(in_f, out_f, bias=(old_attn.bias is not None))
        with torch.no_grad():
            new_linear.weight.copy_(old_attn.weight.T)
            if old_attn.bias is not None:
                new_linear.bias.copy_(old_attn.bias)
        lora_wrapper = LoRALinear(new_linear, RANK, SCALE)
        block.attn.c_attn = lora_wrapper
        lora_params_count += lora_wrapper.lora_A.numel() + lora_wrapper.lora_B.numel()

    # --- Prepare mini training dataset ---
    data = milestone_1()["dataset"][:8]  # use 8 examples for speed
    texts = [f"Spec: {ex['spec']}\nDescription: {ex['description']}" for ex in data]
    encodings = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128,
    )

    # Only LoRA params are trainable
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad], lr=1e-3
    )

    input_ids = encodings["input_ids"]
    attention_mask = encodings["attention_mask"]
    labels = input_ids.clone()
    labels[attention_mask == 0] = -100

    def _eval_loss():
        model.eval()
        with torch.no_grad():
            return float(
                model(input_ids=input_ids, attention_mask=attention_mask, labels=labels).loss.item()
            )

    baseline_loss = _eval_loss()
    model.train()
    total_loss = 0.0
    loss_history = []
    for step in range(steps):
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        loss_history.append(float(loss.item()))
        total_loss += loss_history[-1]
        print(f"lora step {step + 1}/{steps} loss {loss_history[-1]:.4f}", flush=True)

    final_eval_loss = _eval_loss()

    avg_loss = total_loss / max(steps, 1)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "lora_params_count": lora_params_count,
        "training_loss": round(avg_loss, 4),
        "baseline_loss": round(baseline_loss, 4),
        "final_loss": round(loss_history[-1], 4) if loss_history else None,
        "final_eval_loss": round(final_eval_loss, 4),
        "loss_history": [round(value, 4) for value in loss_history],
        "steps": steps,
        "rank": RANK,
        "alpha": ALPHA,
    }


# ---------------------------------------------------------------------------
# Milestone 3: Generate enhanced descriptions (core logic used by Streamlit UI).
# ---------------------------------------------------------------------------
def milestone_3(spec: str, model=None, tokenizer=None, max_new_tokens: int = 60):
    """
    Generate a marketing description for the given product spec.

    If model/tokenizer are None, a template built from the spec is returned.
    That template is the non-neural baseline, not a fine-tuned model.
    """
    if model is None or tokenizer is None:
        # Rule-based fallback for testing / offline environments
        words = spec.replace(",", "").split()
        keywords = [w for w in words if len(w) > 4][:5]
        return (
            f"Discover the ultimate {' '.join(keywords[:2])} experience. "
            f"Engineered with precision, this product features {spec.lower()}. "
            f"Perfect for anyone seeking quality and performance."
        )

    import torch

    prompt = f"Spec: {spec}\nDescription:"
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=128)

    model.eval()
    with torch.no_grad():
        output_ids = model.generate(
            inputs["input_ids"],
            max_new_tokens=max_new_tokens,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    generated = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Extract everything after "Description:"
    if "Description:" in generated:
        description = generated.split("Description:", 1)[1].strip()
    else:
        description = generated.strip()
    return description


def _score_pair(spec: str, generated: str) -> dict:
    """Score one description against its spec. Scores are proxies, not human ratings."""
    spec_words = spec.split()
    gen_words = generated.lower().split()
    length_ratio = len(gen_words) / max(len(spec_words), 1)

    stopwords = {
        "a", "an", "the", "and", "or", "in", "on", "at", "to", "for",
        "of", "with", "is", "are", "it", "its", "this", "that", "be",
    }
    spec_keywords = {
        word.strip(",.%°/()") for word in spec.lower().split()
        if word.strip(",.%°/()") not in stopwords and len(word) > 2
    }
    generated_lower = generated.lower()
    matched = sum(1 for keyword in spec_keywords if keyword in generated_lower)
    keyword_overlap = matched / max(len(spec_keywords), 1)

    sentences = [sentence.strip() for sentence in re.split(r"[.!?]", generated) if sentence.strip()]
    unique_starts = len({sentence.split()[0].lower() for sentence in sentences if sentence.split()})
    sentence_variety = unique_starts / max(len(sentences), 1)

    length_score = min(length_ratio / 5.0, 1.0)
    composite = (length_score + keyword_overlap + sentence_variety) / 3.0
    return {
        "length_ratio": round(length_ratio, 2),
        "keyword_overlap": round(keyword_overlap, 2),
        "sentence_variety": round(sentence_variety, 2),
        "composite_score": round(composite, 2),
    }


# ---------------------------------------------------------------------------
# Milestone 4: Assess the creativity and relevance of generated descriptions.
# ---------------------------------------------------------------------------
def milestone_4(model=None, tokenizer=None):
    """
    Evaluate generated descriptions for creativity and relevance.

    Returns per-sample scores and aggregate statistics.
    """
    data = milestone_1()["dataset"][:10]  # evaluate on first 10 samples
    scores = []

    for ex in data:
        spec = ex["spec"]
        generated = milestone_3(spec, model, tokenizer)
        scores.append({"spec": spec, "generated": generated, **_score_pair(spec, generated)})

    avg_composite = sum(s["composite_score"] for s in scores) / len(scores)
    avg_keyword_overlap = sum(s["keyword_overlap"] for s in scores) / len(scores)
    avg_length_ratio = sum(s["length_ratio"] for s in scores) / len(scores)

    return {
        "scores": scores,
        "num_evaluated": len(scores),
        "avg_composite_score": round(avg_composite, 2),
        "avg_keyword_overlap": round(avg_keyword_overlap, 2),
        "avg_length_ratio": round(avg_length_ratio, 2),
    }


# ---------------------------------------------------------------------------
# Milestone 5: Implement adapter merging for inference.
# ---------------------------------------------------------------------------
def milestone_5(trained_result: dict):
    """
    Merge LoRA adapter weights into the base model for efficient inference.

    Takes the dict returned by milestone_2(), merges LoRA A×B into base
    weights, and returns a plain GPT-2 model (no extra parameters).
    """
    import torch
    import torch.nn as nn

    model = trained_result["model"]
    tokenizer = trained_result["tokenizer"]

    # Detect our LoRA wrappers and merge them (skip if model is a stub)
    if not hasattr(model, "transformer"):
        # Fast/stub model — nothing to merge; return totals of 0 and empty output
        return {
            "model": model,
            "tokenizer": tokenizer,
            "total_params": 0,
            "sample_output": "",
        }

    for block in model.transformer.h:
        layer = block.attn.c_attn
        if hasattr(layer, "lora_A") and hasattr(layer, "lora_B"):
            # Merged weight = W_original + B @ A * scale
            with torch.no_grad():
                delta = (layer.lora_B @ layer.lora_A) * layer.scale
                layer.original.weight.data += delta
            # Replace the LoRA wrapper with the now-merged plain Linear
            block.attn.c_attn = layer.original

    # Quick verification: forward pass should not error
    model.eval()
    prompt = "This product features"
    inputs = tokenizer(prompt, return_tensors="pt")
    with torch.no_grad():
        output_ids = model.generate(
            inputs["input_ids"],
            max_new_tokens=20,
            pad_token_id=tokenizer.eos_token_id,
        )
    sample_output = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    # Count parameters — should equal standard GPT-2 (no extra LoRA params)
    total_params = sum(p.numel() for p in model.parameters())

    return {
        "model": model,
        "tokenizer": tokenizer,
        "total_params": total_params,
        "sample_output": sample_output,
    }


def _row(spec: str, generated: str, method: str) -> dict:
    return {"method": method, "spec": spec, "generated": generated, **_score_pair(spec, generated)}


def run_recorded_evaluation(steps: int = 8, sample_count: int = 3) -> dict:
    """Compare a template, untouched GPT-2, and GPT-2 after a short LoRA run.

    The three samples are the first rows of the hand-written dataset. Generation
    is greedy so the same command reproduces the same text.
    """
    import gc

    import torch
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    info = milestone_1()
    samples = info["dataset"][:sample_count]
    specs = [item["spec"] for item in samples]

    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    tokenizer.pad_token = tokenizer.eos_token
    base = GPT2LMHeadModel.from_pretrained("gpt2")
    base.eval()
    untouched = [
        _row(spec, milestone_3(spec, base, tokenizer, max_new_tokens=40), "untouched GPT-2")
        for spec in specs
    ]
    del base
    gc.collect()

    trained = milestone_2(steps=steps)
    merged = milestone_5(trained)
    lora_rows = [
        _row(
            spec,
            milestone_3(spec, merged["model"], merged["tokenizer"], max_new_tokens=40),
            "LoRA, merged",
        )
        for spec in specs
    ]
    template_rows = [_row(spec, milestone_3(spec), "template") for spec in specs]

    def _avg(rows, key):
        return round(sum(row[key] for row in rows) / len(rows), 2)

    report = {
        "base_model": "gpt2",
        "data_source": (
            f"{info['num_examples']} spec/description pairs written for this project and stored in "
            "milestone_1. They are not scraped from a shop."
        ),
        "num_examples": info["num_examples"],
        "avg_spec_words": info["avg_spec_length"],
        "avg_description_words": info["avg_desc_length"],
        "lora": {
            "rank": trained["rank"],
            "alpha": trained["alpha"],
            "trainable_parameters": trained["lora_params_count"],
            "steps": trained["steps"],
            "baseline_loss": trained["baseline_loss"],
            "final_loss": trained["final_loss"],
            "final_eval_loss": trained["final_eval_loss"],
            "mean_loss": trained["training_loss"],
            "loss_history": trained["loss_history"],
            "parameters_after_merge": merged["total_params"],
        },
        "averages": {
            "template_keyword_overlap": _avg(template_rows, "keyword_overlap"),
            "untouched_keyword_overlap": _avg(untouched, "keyword_overlap"),
            "lora_keyword_overlap": _avg(lora_rows, "keyword_overlap"),
            "template_composite": _avg(template_rows, "composite_score"),
            "untouched_composite": _avg(untouched, "composite_score"),
            "lora_composite": _avg(lora_rows, "composite_score"),
        },
        "samples": template_rows + untouched + lora_rows,
        "limits": [
            "Training uses the first 8 pairs, truncated to 128 tokens, for a few AdamW steps at 1e-3. Padding positions are ignored. Only the rank-4 adapters on each attention c_attn layer are trained.",
            "Keyword overlap counts spec words that reappear in the description. The template baseline pastes the spec into a sentence, so its overlap looks strong without any language-model training.",
            "The three scored specs are inside the eight pairs the adapter trains on. A short GPT-2 run still does not reliably copy the long marketing style of the reference descriptions, and untouched outputs often wander off the product.",
            "The composite score mixes length, keyword overlap, and whether sentences start with different words. It is not a rating of whether a shopper would trust the copy.",
            "There is no held-out shop catalogue. A spec written like the training rows is the only setting these numbers describe.",
        ],
    }
    del trained, merged
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    return report


def save_evaluation(path: str | Path = "results/evaluation.json", steps: int = 40) -> dict:
    """Run the comparison and write it where the Streamlit page and README can read it."""
    report = run_recorded_evaluation(steps=steps)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
