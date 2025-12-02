#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
TheoremQA Multi-Agent Coordinator - Fixed Import Version
"""
import os
import sys
import json
from typing import Dict, Any, List

# Add project root directory path (for dataset path)
current_dir = os.path.dirname(os.path.abspath(__file__))
maas_dir = os.path.dirname(current_dir)
project_root = os.path.dirname(maas_dir)

# Import directly from maas package (since already in maas package)
from maas.schema import Message
from .theoremqa_parser import TheoremQAParser
from .theoremqa_knowledge_agent import TheoremQAKnowledgeRetriever
from .theoremqa_reasoner import TheoremQAReasoner

class TheoremQACoordinator:
    """TheoremQA Multi-Agent Coordinator - Manage agent collaboration"""
    
    def __init__(self):
        print("🔄 Initializing TheoremQA Coordinator...")
        self.parser = TheoremQAParser()
        self.knowledge_retriever = TheoremQAKnowledgeRetriever()
        self.reasoner = TheoremQAReasoner()
        
        # Define agent execution order
        self.workflows = {
            'default': ['parser', 'knowledge_retriever', 'reasoner'],
            'simple_verification': ['parser', 'reasoner'],
            'definition_query': ['parser', 'knowledge_retriever']
        }
        print("✅ TheoremQA Coordinator initialization completed")
    
    async def solve_question(self, question: str) -> Dict[str, Any]:
        """Multi-agent collaborative mathematical problem solving"""
        
        print(f"🚀 Starting processing: {question[:50]}...")
        
        intermediate_results = {}
        workflow = self.workflows['default']
        
        try:
            # 1. Problem parsing phase
            if 'parser' in workflow:
                print("   📝 Executing problem parsing...")
                parsed_result = await self.parser.run(question)
                intermediate_results['parsed'] = parsed_result.content
                
                # Simple problem type judgment (from string content)
                parsed_text = parsed_result.content.lower()
                if 'boolean_verification' in parsed_text:
                    workflow = self.workflows['simple_verification']
                elif 'definition_query' in parsed_text:
                    workflow = self.workflows['definition_query']
                else:
                    workflow = self.workflows['default']
                print(f"   Selected workflow: {workflow}")
            
            # 2. Knowledge retrieval phase
            if 'knowledge_retriever' in workflow:
                print("   🔍 Executing knowledge retrieval...")
                # Pass original question string
                knowledge_result = await self.knowledge_retriever.run(question)
                intermediate_results['knowledge'] = json.loads(knowledge_result.content)  # Parse JSON string
            
            # 3. Logical reasoning phase  
            if 'reasoner' in workflow:
                print("   🧠 Executing logical reasoning...")
                # Pass original question string and knowledge
                reasoning_result = await self.reasoner.run(
                    question,  # Pass original question
                    intermediate_results.get('knowledge', {'retrieved_concepts': [], 'knowledge_data': {}})
                )
                intermediate_results['reasoned'] = json.loads(reasoning_result.content)  # Parse JSON string
            
            # Build final result
            final_answer = intermediate_results.get('reasoned', {})
            
            return {
                'success': True,
                'final_answer': final_answer,
                'intermediate_steps': list(intermediate_results.keys()),
                'workflow_used': workflow,
                'question': question
            }
            
        except Exception as e:
            print(f"❌ Processing failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'question': question
            }
    
    async def evaluate_on_dataset(self, dataset_path: str, num_samples: int = 3) -> List[Dict[str, Any]]:
        """Evaluate system on TheoremQA dataset"""
        
        dataset_full_path = os.path.join(project_root, dataset_path)
        
        try:
            with open(dataset_full_path, 'r') as f:
                data = json.load(f)
            print(f"📊 Loaded dataset: {len(data)} questions")
        except Exception as e:
            print(f"❌ Data loading failed: {e}")
            return []
        
        results = []
        sample_count = min(num_samples, len(data))
        
        for i in range(sample_count):
            item = data[i]
            question = item.get('Question') or item.get('question', 'Unknown question')
            
            print(f"\n{'='*60}")
            print(f"🎯 Sample {i+1}/{sample_count}: {question[:80]}...")
            
            result = await self.solve_question(question)
            results.append(result)
            
            if result['success']:
                final_answer = result['final_answer']
                print(f"✅ Success")
                print(f"   Answer: {final_answer.get('answer', 'N/A')}")
                print(f"   Method: {final_answer.get('method_used', 'N/A')}")
            else:
                print(f"❌ Failed: {result['error']}")
        
        return results


# Independent running test
async def main():
    """Main test function"""
    print("🎯 TheoremQA Multi-Agent System Starting")
    print(f"📁 Project root directory: {project_root}")
    
    coordinator = TheoremQACoordinator()
    
   
    # Then test on dataset
    print(f"\n📊 Phase 2: Testing on TheoremQA Dataset")
    dataset_path = "data/theoremqa_test.json"
    results = await coordinator.evaluate_on_dataset(dataset_path, num_samples=2)
    
    # Summary results
    success_count = sum(1 for r in results if r['success'])
    print(f"\n📈 Final Summary: {success_count}/{len(results)} successful")
    
    return results


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())