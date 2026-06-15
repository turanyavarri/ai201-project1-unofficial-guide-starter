# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

Rutgers University campus dining, student opinions on dining halls, meal plans, and food locations across all four campuses. This knowledge is valuable because official Rutgers Dining sources only show menus and hours, not honest student experiences like which halls are consistently crowded, which food is hit or miss, or which meal swipe locations give the best value. Students share this knowledge informally on Reddit and Google Reviews but it's scattered and hard to search.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Reddit r/rutgers | Forum thread | Is_Rutgers_food_that_bad.txt |
| 2 | Reddit r/rutgers | Forum thread | Guide_to_dining_halls.txt |
| 3 | Reddit r/rutgers | Forum thread | Meal_Swipe_Location_Tier_List.txt |
| 4 | Reddit r/rutgers | Forum thread | What_meal_plan_do_Yall_recommend.txt |
| 5 | Reddit r/rutgers | Forum thread | How_s_food_at_Rutgers.txt |
| 6 | Reddit r/rutgers | Forum thread | Busch_Dining_Hall_Is_Best_I_Will_Di.txt |
| 7 | Rutgers Dining Services | Official announcement | Summer_dining_hours_begin_Thursday_.txt |
| 8 | Google Reviews | Student reviews | Salma_Mukhtar.txt |
| 9 | Rutgers Dining / Nutrislice | Official menu PDF | Nutrislice___Rutgers_University.pdf |
| 10 | Rutgers Dining / Nutrislice | Official menu PDF | Nutrislice-livingston__Rutgers_University.pdf |

---

## Chunking Strategy

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** Documents are mostly short Reddit comments and informal reviews, so 400 characters captures one complete opinion without merging unrelated comments together. Overlap of 50 characters ensures that opinions split across chunk boundaries still have enough context to be retrievable.

**Final chunk count:** 228 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers. Runs locally with no API key or rate limits.

**Production tradeoff reflection:** For a real deployment I would consider OpenAI's text-embedding-3-small, which has better accuracy on informal conversational text like Reddit comments. Tradeoffs to weigh would be cost (API calls per query vs free local model), latency (cloud roundtrip vs local inference), and context length since some Reddit threads are long and a model with a larger context window would handle them better. For a Rutgers-specific system, domain accuracy on informal text matters most, so a larger API-hosted model would likely be worth the cost.

---

## Grounded Generation

**System prompt grounding instruction:** You are a helpful assistant answering questions about Rutgers University dining. Answer the question using ONLY the information provided in the documents below. If the documents do not contain enough information to answer the question, say "I don't have enough information on that." Do not use any outside knowledge.

**How source attribution is surfaced in the response:** Source filenames are collected programmatically from ChromaDB metadata for every retrieved chunk and appended to the response in a separate Sources field in the Gradio UI. Attribution is guaranteed by the pipeline, not left to the LLM.

---

## Sample Chunks

Below are 5 representative chunks produced by the ingestion pipeline:

**Chunk 1**
- Source: Busch_Dining_Hall_Is_Best_I_Will_Di.txt
- Text: "staff know you appreciate them ybnnahmirr Plz tell livi to make more citrus salmon lol ThatRUDiningGuy I got you StealthNider the chickpea & tofu garam masala they had sunday night was really good! would love to see it more often"

**Chunk 2**
- Source: Busch_Dining_Hall_Is_Best_I_Will_Di.txt
- Text: "jalapenopizza_ Livi is objectively the best in terms of food. Neilson was the homiest one and my favorite even if Livi had better food but then they changed the decor. SecretPotatoChip Pasta on Busch is better, but Livi has burgers"

**Chunk 3**
- Source: Is_Rutgers_food_that_bad.txt
- Text: "Henry's Diner is usually packed but well worth the wait. Traditional sit down diner on Livi, right across from the first bus stop. They stop accepting swipes around 5 and close at 6-7."

**Chunk 4**
- Source: Meal_Swipe_Location_Tier_List.txt
- Text: "Henry's Diner: Truly an elite institution that gives you the true Jersey Diner experience for the cost of only one meal swipe."

**Chunk 5**
- Source: What_meal_plan_do_Yall_recommend.txt
- Text: "The minimum for freshman is 210. That's two meals a day, if you can live off 2 meals a day, do 210. Also 285 had been changed to become infinite or something like that look it up"

---

## Retrieval Test Results

**Query 1: "Which dining hall is the best at Rutgers?"**

Top returned chunks:
- [0.321] (Is_Rutgers_food_that_bad.txt) "the main thing you should be concerned about dining-wise is the chicken from the busch dining hall or the atrium..."
- [0.468] (Is_Rutgers_food_that_bad.txt) "one of the best college dining halls in my opinion. I've invited friends from different colleges, such as Amherst..."
- [0.485] (Salma_Mukhtar.txt) "Food isn't bad. A little pricey to get in without a Rutgers meal swipe. The staff is pretty friendly too. Definitely the second best dining hall at Rutgers..."

Why these chunks are relevant: All three chunks directly discuss dining hall quality at Rutgers. The second chunk compares Rutgers dining to other colleges, and the third explicitly ranks dining halls, both of which are semantically close to the query.

**Query 2: "What meal plan should a freshman get?"**

Top returned chunks:
- [0.684] (What_meal_plan_do_Yall_recommend.txt) "What meal plan do Yall recommend?..."
- [0.799] (What_meal_plan_do_Yall_recommend.txt) "That's two meals a day, if you can live off meals a day, do 210. Also 285 had been changed to become infinite..."
- [0.805] (Salma_Mukhtar.txt) "the food is available here for all types of students and students can eat unlimited food..."

Why these chunks are relevant: The first two chunks come directly from the meal plan recommendation thread and contain the specific 210 plan advice. The third chunk is less relevant but mentions unlimited food which is semantically related to meal plan coverage.

**Query 3: "What makes Henry's Diner worth using a meal swipe on?"**

Top returned chunks:
- [0.692] (Is_Rutgers_food_that_bad.txt) "accepts swipes (has a weekend deal, swipes for a full pie and a liter). They're pretty good. Henry's Diner is usually packed but well worth the wait..."
- [0.888] (Meal_Swipe_Location_Tier_List.txt) "Henry's and the Starbucks truck. I feel like the Starbucks truck should be higher..."
- [0.890] (Meal_Swipe_Location_Tier_List.txt) "when not dining hall restaurants didn't accept meal swipes. Henry's was added in when I was there..."

Why these chunks are relevant: The first chunk directly describes Henry's Diner as worth the wait and mentions the swipe deal. The second and third chunks come from the tier list document which ranked Henry's as S-tier.

---

## Example Responses

**Response 1 — What meal plan should a freshman get?**

Answer: The minimum meal plan for freshmen is 210, which is equivalent to two meals a day. It is recommended to start with this plan as it can be increased later, but not decreased after the first two weeks of the semester.

Sources:
- What meal plan do Yall recommend.txt
- Salma Mukhtar.txt
- Meal Swipe Location Tier List.txt
- Is Rutgers food that bad.txt

**Response 2 — What are student complaints about the Atrium on College Ave?**

Answer: Student complaints about the Atrium on College Ave include: food poisoning (at least two instances reported by one student), bad food quality specifically that the meat is not good, food being super oily or processed, and difficulty eating there multiple times a week due to poor food quality, with one student reporting weight gain from eating there frequently.

Sources:
- Is Rutgers food that bad.txt
- Meal Swipe Location Tier List.txt
- Guide to dining halls.txt
- What meal plan do Yall recommend.txt

**Out-of-scope refusal — What are the parking rules at Rutgers?**

Answer: I don't have enough information on that.

Sources:
- How's food at Rutgers.txt
- Is Rutgers food that bad.txt
- Meal Swipe Location Tier List.txt
- Salma Mukhtar.txt

---

## Query Interface

**Interface description:** The system uses a Gradio web UI accessible at http://localhost:7860. It has two input/output fields:
- Input: A text box labeled "Your question" where users type a plain-language question about Rutgers dining
- Output 1: A text box labeled "Answer" showing the LLM-generated response grounded in retrieved documents
- Output 2: A text box labeled "Sources" listing the document filenames the answer was drawn from

Users can submit by clicking the Ask button or pressing Enter.

**Sample interaction transcript:**

User: What makes Henry's Diner worth using a meal swipe on?

Answer: Henry's Diner is worth using a meal swipe on because it provides a "true Jersey Diner experience" for the cost of only one meal swipe, and it is considered an "elite institution". Additionally, the text mentions that it's "well worth the wait" and is the best place to eat if you're fine with waiting or get there early, implying that the quality of the food and the overall experience make it a good value for a meal swipe.

Sources:
- Meal Swipe Location Tier List.txt
- Is Rutgers food that bad.txt

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which dining hall do students consider the best at Rutgers? | Livingston Dining Hall | Said it couldn't determine which hall is best due to insufficient info in retrieved chunks | Partially relevant | Partially accurate |
| 2 | What meal plan should a freshman get? | 210 plan recommended as minimum | Correctly recommended 210 plan, explained it equals two meals a day and can be increased but not decreased | Relevant | Accurate |
| 3 | What makes Henry's Diner worth using a meal swipe on? | Real Jersey diner experience, S-tier value, worth the wait | Correctly described true Jersey Diner experience, elite institution, well worth the wait | Relevant | Accurate |
| 4 | What are student complaints about the Atrium on College Ave? | Oily food, food poisoning, large portions | Correctly listed food poisoning, bad meat, oily/processed food, weight gain | Relevant | Accurate |
| 5 | What food stations are available at Livingston Dining Hall? | Burger bar, pasta line, hibachi grill, pizza bar, salad bar | Returned "I don't have enough information on that" | Off-target | Inaccurate |

---

## Failure Case Analysis

**Question that failed:** What food stations are available at Livingston Dining Hall?

**What the system returned:** "I don't have enough information on that."

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure. The information about Livingston's food stations exists across multiple documents — Guide_to_dining_halls.txt and Meal_Swipe_Location_Tier_List.txt both mention the burger bar, pasta line, and hibachi grill. However, the 400-character chunking split these details across multiple chunks, and none of the individual chunks contained enough station-specific detail to match the query semantically. The embedding model returned general dining hall quality chunks instead of station-specific ones.

**What you would change to fix it:** Increase chunk size to 600-800 characters for documents that contain list-style content like dining hall features, so that multiple related details stay together in one chunk and can be retrieved as a complete unit.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before coding forced me to think about document structure first. Because I had noted that my documents were short Reddit comments, I chose 400-character chunks rather than a default 1000-character size, which would have merged unrelated comments together and hurt retrieval precision.

**One way your implementation diverged from the spec, and why:** My spec anticipated that chunk size of 400 characters would work well for all documents. In practice the Nutrislice PDF menus produced very repetitive chunks of repeated food item lists, which added noise to the vector store. I would have handled PDFs separately with a different chunking strategy if I had anticipated this during planning.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy and Documents sections from planning.md
- *What it produced:* An ingest.py script that loaded .txt and .pdf files, cleaned them, and split into 400-character chunks with 50-character overlap
- *What I changed or overrode:* The initial cleaning function didn't remove Reddit ads (JumpCloud, TruGreen). I identified the specific ad keywords appearing in my documents and directed Claude to add a line-by-line keyword filter to remove them before chunking.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section and architecture diagram from planning.md
- *What it produced:* An embed.py script that embedded chunks using all-MiniLM-L6-v2 and stored them in ChromaDB with source metadata, plus a retrieve() function
- *What I changed or overrode:* The initial version didn't include a step to delete and recreate the ChromaDB collection on each run, which caused duplicate embedding errors. I directed Claude to add a delete_collection step before creating a new one so the vector store rebuilds cleanly every time.