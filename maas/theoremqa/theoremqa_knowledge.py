# theoremqa_knowledge.py
"""
TheoremQA 数学知识库
"""
from typing import Dict, List

class TheoremQAKnowledgeBase:
    """TheoremQA专用数学知识库"""
    
    def __init__(self):
        self.theorems = {
            'prime_number': {
                'definition': 'A prime number is a natural number greater than 1 that has no positive divisors other than 1 and itself.',
                'examples': ['2', '3', '5', '7', '11'],
                'counterexamples': ['1', '4', '6', '8', '9'],
                'key_facts': ['1 is not a prime number', '2 is the only even prime number']
            },
            'triangle': {
                'definition': 'A triangle is a polygon with three edges and three vertices.',
                'angle_sum': 'The sum of the interior angles of a triangle is always 180 degrees.',
                'types': ['equilateral', 'isosceles', 'scalene', 'right', 'acute', 'obtuse']
            },
            'pythagorean_theorem': {
                'statement': 'In a right triangle, the square of the hypotenuse equals the sum of the squares of the other two sides.',
                'formula': 'a² + b² = c²',
                'conditions': ['Only applies to right triangles', 'c must be the hypotenuse']
            },
            'derivative': {
                'definition': 'The derivative of a function measures the sensitivity to change of the function value with respect to a change in its argument.',
                'rules': {
                    'constant': 'd/dx[c] = 0',
                    'power': 'd/dx[xⁿ] = n*xⁿ⁻¹',
                    'sum': 'd/dx[f(x) + g(x)] = f\'(x) + g\'(x)'
                }
            }
        }
    
    def get_knowledge(self, concept: str) -> Dict:
        """获取特定概念的数学知识"""
        return self.theorems.get(concept.lower(), {})
    
    def search_concepts(self, question: str) -> List[str]:
        """从问题中搜索相关数学概念"""
        found_concepts = []
        question_lower = question.lower()
        
        for concept in self.theorems.keys():
            if concept in question_lower:
                found_concepts.append(concept)
            elif concept == 'prime_number' and ('prime' in question_lower or 'primality' in question_lower):
                found_concepts.append(concept)
            elif concept == 'pythagorean_theorem' and ('pythagoras' in question_lower or 'right triangle' in question_lower):
                found_concepts.append(concept)
                
        return found_concepts