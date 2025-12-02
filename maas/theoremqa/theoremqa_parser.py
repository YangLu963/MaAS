# theoremqa_parser.py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TheoremQA 问题解析智能体
"""
from typing import Dict, Any
from pydantic import Field

from maas.actions.action import Action
from maas.schema import Message
from .theoremqa_knowledge import TheoremQAKnowledgeBase


class TheoremQAParser(Action):
    """TheoremQA问题解析智能体 - 分析数学问题类型和结构"""
    
    name: str = "TheoremQAParser"
    knowledge_base: TheoremQAKnowledgeBase = Field(default_factory=TheoremQAKnowledgeBase)
    
    async def run(self, question: str) -> Message:
        """解析数学问题类型和关键概念"""
        
        print(f"🔍 [TheoremQAParser] 解析问题: {question}")
        
        # 分析问题类型
        question_lower = question.lower()
        
        if any(word in question_lower for word in ['true', 'false', 'correct', 'incorrect']):
            question_type = "boolean_verification"
        elif any(word in question_lower for word in ['calculate', 'compute', 'what is', '=']):
            question_type = "calculation" 
        elif any(word in question_lower for word in ['definition', 'define', 'what is a']):
            question_type = "definition_query"
        elif any(word in question_lower for word in ['prove', 'show that', 'demonstrate']):
            question_type = "proof"
        else:
            question_type = "general_reasoning"
        
        # 提取数学概念
        math_concepts = self.knowledge_base.search_concepts(question)
        
        # 构建解析结果 - 修复缩进
        analysis_text = f"""问题类型: {question_type}
原始问题: {question}
需要知识检索: {question_type in ["definition_query", "proof"]}
需要计算: {'calculate' in question_lower or 'compute' in question_lower}
数学概念: {math_concepts}"""
        
        print(f"   ✅ 识别为: {question_type}, 概念: {math_concepts}")
        
        return Message(
            content=analysis_text,  # 使用字符串
            role="assistant",
            cause_by=self.name
        )