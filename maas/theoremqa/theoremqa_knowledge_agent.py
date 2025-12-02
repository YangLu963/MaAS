# theoremqa_knowledge_agent.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TheoremQA Knowledge Retrieval Agent
"""
import json
from typing import Dict, Any
from pydantic import Field

from maas.actions.action import Action
from maas.schema import Message
from .theoremqa_knowledge import TheoremQAKnowledgeBase


class TheoremQAKnowledgeRetriever(Action):
    """TheoremQA Knowledge Retrieval Agent - Retrieve relevant mathematical theorems and definitions"""
    
    name: str = "TheoremQAKnowledgeRetriever"
    knowledge_base: TheoremQAKnowledgeBase = Field(default_factory=TheoremQAKnowledgeBase)
    
    async def run(self, question: str) -> Message:
        """Retrieve relevant knowledge based on question"""
        
        print(f"📚 [TheoremQAKnowledgeRetriever] Retrieving question: {question[:50]}...")
        
        # Extract concepts directly from question (simplified version)
        concepts = self.knowledge_base.search_concepts(question)
        
        # Retrieve relevant knowledge
        knowledge_results = {}
        for concept in concepts:
            knowledge = self.knowledge_base.get_knowledge(concept)
            if knowledge:
                knowledge_results[concept] = knowledge
        
        # Build knowledge result
        knowledge_package = {
            'retrieved_concepts': list(knowledge_results.keys()),
            'knowledge_data': knowledge_results,
            'coverage_score': len(knowledge_results) / max(1, len(concepts)),
            'original_question': question
        }
        
        print(f"   ✅ Retrieved knowledge for {len(knowledge_results)} concepts")
        
        return Message(
            content=json.dumps(knowledge_package),
            role="assistant", 
            cause_by=self.name
        )