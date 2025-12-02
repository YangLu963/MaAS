# theoremqa_reasoner.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TheoremQA Reasoning Agent
"""
import json
from typing import Dict, Any
from pydantic import Field

from maas.actions.action import Action
from maas.schema import Message


class TheoremQAReasoner(Action):
    """TheoremQA Reasoning Agent - Perform mathematical logical reasoning and verification"""
    
    name: str = "TheoremQAReasoner"
    
    async def run(self, question: str, knowledge_data: Dict[str, Any]) -> Message:
        """Perform mathematical reasoning based on question and knowledge"""
        
        print(f"🤔 [TheoremQAReasoner] Reasoning question: {question[:50]}...")
        
        concepts = knowledge_data.get('retrieved_concepts', [])
        
        # Rule-based reasoning
        base_reasoning = self._rule_based_reasoning(question, concepts)
        
        if base_reasoning['answer'] != "UNKNOWN":
            # Rule-based reasoning successful
            reasoning_result = base_reasoning
            method = "rule_based"
        else:
            # Need LLM reasoning
            llm_reasoning = await self._llm_based_reasoning(question, knowledge_data)
            reasoning_result = llm_reasoning
            method = "llm_based"
        
        # Build final result
        final_result = {
            'question': question,
            'answer': reasoning_result['answer'],
            'reasoning': reasoning_result['reasoning'],
            'confidence': reasoning_result['confidence'],
            'method_used': method,
            'concepts_applied': concepts,
            'question_type': 'auto_detected'
        }
        
        print(f"   ✅ Reasoning completed: {final_result['answer']} (method: {method})")
        
        return Message(
            content=json.dumps(final_result),
            role="assistant",
            cause_by=self.name
        )
    
    def _rule_based_reasoning(self, question: str, concepts: list) -> Dict[str, Any]:
        """Rule-based reasoning with predefined rules"""
        question_lower = question.lower()
        
        # Common mathematical problem rules
        if 'is 1 a prime number' in question_lower:
            return {
                'answer': 'False',
                'reasoning': '1 is not a prime number because it has only one positive divisor (1 itself), while prime numbers must have exactly two distinct positive divisors.',
                'confidence': 1.0
            }
        
        if 'sum of angles in a triangle' in question_lower:
            return {
                'answer': '180 degrees',
                'reasoning': 'The sum of the interior angles of any Euclidean triangle is always 180 degrees.',
                'confidence': 1.0
            }
        
        if 'derivative of constant' in question_lower:
            return {
                'answer': '0', 
                'reasoning': 'The derivative of any constant function is zero because constants do not change.',
                'confidence': 1.0
            }
        
        # Default return unknown, need LLM reasoning
        return {
            'answer': 'UNKNOWN',
            'reasoning': 'Cannot determine answer with rule-based reasoning.',
            'confidence': 0.0
        }
    
    async def _llm_based_reasoning(self, question: str, knowledge_data: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM for complex reasoning"""
        try:
            # Build LLM prompt
            prompt = self._build_reasoning_prompt(question, knowledge_data)
            
            # Use MaAS LLM for reasoning
            llm_response = await self._aask(prompt)
            
            return {
                'answer': self._extract_answer(llm_response),
                'reasoning': llm_response,
                'confidence': 0.7
            }
        except Exception as e:
            return {
                'answer': 'ERROR',
                'reasoning': f'LLM reasoning failed: {str(e)}',
                'confidence': 0.0
            }
    
    def _build_reasoning_prompt(self, question: str, knowledge_data: Dict[str, Any]) -> str:
        """Build reasoning prompt"""
        concepts = knowledge_data.get('retrieved_concepts', [])
        knowledge = knowledge_data.get('knowledge_data', {})
        
        prompt = f"""Please act as a mathematics expert and answer the following mathematical question.

Question: {question}

"""
        if concepts:
            prompt += "Relevant mathematical knowledge:\n"
            for concept in concepts:
                if concept in knowledge:
                    prompt += f"- {concept}: {knowledge[concept].get('definition', 'No definition')}\n"
        
        prompt += """
Please reason step by step:
1. Analyze the problem type and requirements
2. Apply relevant mathematical knowledge  
3. Perform logical reasoning
4. Provide the final answer

Please answer in the following format:
Answer: [your answer]
Reasoning: [detailed reasoning process]
"""
        return prompt
    
    def _extract_answer(self, llm_response: str) -> str:
        """Extract answer from LLM response"""
        lines = llm_response.split('\n')
        for line in lines:
            if line.startswith('Answer:'):
                return line.split(':', 1)[1].strip()
        return llm_response[:100]