import os
import time
import requests
from typing import List, Dict
import openai

class OpenAIClient:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")

    def generate_tips(self, aggregates: Dict, budget_status: Dict) -> List[Dict]:
        """Generate personalized saving tips using OpenAI"""
        prompt = self._build_prompt(aggregates, budget_status)

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a friendly personal finance assistant. Provide 3 actionable, prioritized saving suggestions with estimated monthly savings numbers and one follow-up question. Keep responses concise and include confidence levels (low/medium/high)."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )

            tips_text = response.choices[0].message.content.strip()
            return self._parse_tips(tips_text)

        except Exception as e:
            print(f"OpenAI API error: {e}")
            # Fallback to rule-based tips
            from processor import Processor
            return Processor.generate_saving_tips(aggregates, budget_status)

    def _build_prompt(self, aggregates: Dict, budget_status: Dict) -> str:
        """Build prompt with aggregated data"""
        top_cats = ", ".join([f"{cat}: {amt:.2f}" for cat, amt in aggregates['top_categories']])
        budget_gap = budget_status.get('budget_gap', 0)
        savings_goal = budget_status.get('savings_goal', 0)

        return f"""AGGREGATES: {aggregates['total']:.2f} total this month; TOP_CATS: {top_cats}; BUDGET_GAP: {budget_gap:.2f}; USER_GOAL: {savings_goal:.2f}.

Provide 3 prioritized, actionable tips to save money (each with an estimated monthly savings number, confidence level, and brief math explanation) and one clarifying question."""

    def _parse_tips(self, tips_text: str) -> List[Dict]:
        """Parse OpenAI response into structured tips"""
        import re
        tips = []

        # Split by numbered tips (1., 2., 3.)
        tip_pattern = r'(\d+)\.\s*\*\*(.*?)\*\*(.*?)(?=\d+\.|$)'
        matches = re.findall(tip_pattern, tips_text, re.DOTALL)

        for match in matches[:3]:  # Limit to 3 tips
            tip_text = match[1].strip()
            details = match[2].strip()

            # Extract savings amount (look for $ followed by number)
            savings_match = re.search(r'\$(\d+(?:\.\d{2})?)', details)
            estimated_savings = float(savings_match.group(1)) if savings_match else 50.0

            # Extract confidence (low/medium/high)
            confidence = 'medium'  # default
            if 'high' in details.lower():
                confidence = 'high'
            elif 'low' in details.lower():
                confidence = 'low'

            # Extract math explanation (everything after confidence)
            math = 'Estimated based on patterns'
            confidence_match = re.search(r'\((low|medium|high)\s*confidence\)\s*(.*)', details, re.IGNORECASE)
            if confidence_match:
                math = confidence_match.group(2).strip()
                if not math:
                    math = 'Estimated based on patterns'

            tips.append({
                'tip': tip_text,
                'estimated_savings': estimated_savings,
                'confidence': confidence,
                'math': math
            })

        # If no matches, fallback to simple parsing
        if not tips:
            lines = tips_text.split('\n')
            for line in lines:
                if line.strip() and not line.lower().startswith('question'):
                    # Look for tip with $amount
                    match = re.match(r'(.*?)\s*\$\s*(\d+(?:\.\d{2})?)\s*\((low|medium|high)\s*confidence\)\s*(.*)', line.strip(), re.IGNORECASE)
                    if match:
                        tip_text = match.group(1).strip()
                        estimated_savings = float(match.group(2))
                        confidence = match.group(3).lower()
                        math = match.group(4).strip() if match.group(4) else 'Estimated based on patterns'
                        tips.append({
                            'tip': tip_text,
                            'estimated_savings': estimated_savings,
                            'confidence': confidence,
                            'math': math
                        })
                    else:
                        # Simple fallback
                        parts = line.split('$')
                        if len(parts) >= 2:
                            tip_text = parts[0].strip()
                            rest = '$'.join(parts[1:])
                            savings_match = re.search(r'(\d+(?:\.\d{2})?)', rest)
                            estimated_savings = float(savings_match.group(1)) if savings_match else 50.0
                            tips.append({
                                'tip': tip_text,
                                'estimated_savings': estimated_savings,
                                'confidence': 'medium',
                                'math': 'Estimated based on patterns'
                            })
                    if len(tips) >= 3:
                        break

        return tips[:3]
