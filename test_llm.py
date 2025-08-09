from vibetrack.llm_analyzer import analyze_diff

diff = """- total = price * quantity
+ total = price * quantity * (1 - discount)
"""

result = analyze_diff(diff)
print("🔍 AI Explanation:\n", result)
