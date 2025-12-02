# Бэрхшээлийн Түвшинг Сайжруулах Заавар

## Хийгдсэн Сайжруулалтууд

### 1. **Дэлгэрэнгүй Difficulty Guidelines** ✅

**Өмнө:**
```python
difficulty_map = {
    "easy": "Test fundamental facts or definitions.",
    "medium": "Test understanding and application.",
    "hard": "Test analysis, synthesis, or multi-step reasoning.",
}
```

**Одоо:**
- Тус бүр түвшинд дэлгэрэнгүй зааварчилгаа
- Асуултын бүтэц, урт, хэлбэрийн тодорхойлолт
- Хариултын сонголтуудын урт, нарийн төвөгтэй байдал
- Ойлголтын түвшин (Bloom's Taxonomy)
- Жишээ асуултууд
- Тайлбарын гүнзгий байдал

### 2. **Prompt-д Тодорхой Зааварчилгаа** ✅

LLM-д одоо дараах мэдээлэл өгөгдөж байна:
- Асуултын урт (easy: 5-10 үг, medium: 8-15 үг, hard: 12-20 үг)
- Хариултын сонголтуудын урт
- Асуултын хэлбэр (жишээ: "What is..." vs "When designing... what are...")
- Ойлголтын түвшин

## Нэмэлт Сайжруулалтын Санал

### 3. **Few-Shot Examples (Жишээ Асуултууд)**

Prompt-д жишээ асуултууд нэмэх:

```python
def _get_difficulty_examples(self, difficulty: str) -> str:
    examples = {
        "easy": """
EXAMPLE EASY QUESTION:
Question: "What is considered the overriding principle for successful software documentation?"
Choices: 
  A. "Minimizing documentation length"
  B. "Ensuring technical accuracy"  
  C. "Making the software usable" ✓
  D. "Providing comprehensive guides"
""",
        "medium": """
EXAMPLE MEDIUM QUESTION:
Question: "What is the primary goal of task-oriented software documentation?"
Choices:
  A. "To provide step-by-step instructions for every function"
  B. "To adapt the software to the user's job, enabling real-world tasks" ✓
  C. "To list all technical specifications"
  D. "To explain internal architecture"
""",
        "hard": """
EXAMPLE HARD QUESTION:
Question: "When designing effective technical software documentation that helps adapt software to a user's job, what are the core user motivators that the documentation should emphasize?"
Choices:
  A. "Advanced customization and aesthetic appeal"
  B. "Compliance with industry regulations"
  C. "Ease of installation and troubleshooting"
  D. "Discovery and efficiency" ✓
"""
    }
    return examples.get(difficulty.lower(), "")
```

### 4. **Post-Generation Validation**

Одоо `_validate_difficulty_level()` функц нэмэгдсэн боловч ашиглаагүй байна. 
`generate_mcqs()` функцэд нэмэх:

```python
if self._validate_mcq(mcq_payload):
    # Optional: Validate difficulty level
    if not self._validate_difficulty_level(mcq_payload, difficulty):
        # Log warning or regenerate
        pass
    mcq_payload["question_number"] = idx + 1
    mcqs.append(mcq_payload)
```

### 5. **Temperature Parameter (LLM Settings)**

Бэрхшээлийн түвшингээс хамааран temperature өөрчлөх:

```python
def _get_temperature_for_difficulty(self, difficulty: str) -> float:
    """Higher temperature for harder questions = more creative/varied."""
    return {
        "easy": 0.3,    # More deterministic, consistent
        "medium": 0.5,  # Balanced
        "hard": 0.7,    # More creative, varied phrasing
    }.get(difficulty.lower(), 0.5)

# Usage in _generate_single_mcq:
response = genai_client.models.generate_content(
    model=GEMINI_MODEL,
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "temperature": self._get_temperature_for_difficulty(difficulty),
    },
)
```

### 6. **Concept Selection by Difficulty**

Одоо бүх түвшинд ижил концептууд ашиглагдаж байна. 
Хэцүү асуултуудад илүү нарийн концептууд сонгох:

```python
def extract_concepts(self, pdf_id: str, page_start: int, page_end: int, difficulty: str = "medium") -> List[str]:
    """Extract concepts with difficulty-aware selection."""
    results = self.rag.fetch_pages(pdf_id, page_start, page_end)
    combined_text = "\n\n".join(results.get("documents", []))
    if not combined_text:
        return []
    
    concepts = self.concept_extractor.extract(combined_text)
    
    # For hard: prefer complex, multi-part concepts
    # For easy: prefer simple, single-concept items
    if difficulty == "hard":
        # Filter for longer, more complex concept descriptions
        concepts = [c for c in concepts if len(c.split()) > 5]
    elif difficulty == "easy":
        # Prefer shorter, simpler concepts
        concepts = [c for c in concepts if len(c.split()) <= 5]
    
    return concepts
```

### 7. **Distractor Quality by Difficulty**

Хэцүү асуултуудад илүү нарийн, ойролцоо distractors үүсгэх:

```python
# Prompt-д нэмэх:
distractor_guidelines = {
    "easy": "Distractors should be clearly wrong but related to the topic.",
    "medium": "Distractors should be plausible but miss key nuances or context.",
    "hard": "Distractors should be sophisticated, requiring careful reasoning to eliminate. They may contain partial truths or common misconceptions.",
}
```

## Хэрэгжүүлэх Дараалал

### Phase 1: Одоо хийгдсэн ✅
1. ✅ Дэлгэрэнгүй difficulty guidelines
2. ✅ Prompt сайжруулалт

### Phase 2: Хурдан сайжруулалт (1-2 цаг)
3. Few-shot examples нэмэх
4. Temperature parameter нэмэх
5. Distractor guidelines сайжруулах

### Phase 3: Гүнзгий сайжруулалт (3-5 цаг)
6. Difficulty validation идэвхжүүлэх
7. Concept selection by difficulty
8. Testing болон fine-tuning

## Тестлэх

Сайжруулалтын дараа тест хийх:

```python
# Ижил концепт дээр 3 түвшний асуулт үүсгэх
easy_q = generator.generate_mcqs(pdf_id, 1, 10, 1, "easy")
medium_q = generator.generate_mcqs(pdf_id, 1, 10, 1, "medium")  
hard_q = generator.generate_mcqs(pdf_id, 1, 10, 1, "hard")

# Харьцуулах:
# - Асуултын урт
# - Хариултын нарийн төвөгтэй байдал
# - Ойлголтын түвшин
```

## Хүлээгдэж Буй Үр Дүн

**Easy:**
- Асуулт: 5-10 үг, шууд баримт
- Хариулт: 3-8 үг, энгийн
- Ойлголт: Remembering

**Medium:**
- Асуулт: 8-15 үг, харьцуулалт/хэрэглээ
- Хариулт: 8-15 үг, дунд нарийн төвөгтэй
- Ойлголт: Applying

**Hard:**
- Асуулт: 12-20+ үг, олон талын дүн шинжилгээ
- Хариулт: 15-25+ үг, нарийн
- Ойлголт: Analyzing/Synthesizing

