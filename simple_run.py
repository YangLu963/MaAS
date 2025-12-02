# simple_run.py (placed in /Users/luyang/MaAS/ directory)
#!/usr/bin/env python3
"""
TheoremQA Direct Dataset Testing - Simplified Version
"""
import asyncio
import json

async def main():
    print("🎯 TheoremQA Direct Dataset Testing")
    
    try:
        from maas.theoremqa.theoremqa_coordinator import TheoremQACoordinator
        
        # Create coordinator
        coordinator = TheoremQACoordinator()
        
        # Directly load dataset
        with open('maas/data/theoremqa_test.json', 'r') as f:
            data = json.load(f)
        
        print(f"📊 Loaded {len(data)} questions")
        
        # Run first 20 questions for analysis
        results = []
        for i in range(min(20, len(data))):
            item = data[i]
            question = item.get('Question') or item.get('question', 'Unknown')
            
            print(f"\n{i+1}. Question: {question}")
            
            result = await coordinator.solve_question(question)
            results.append((question, result))
            
            if result.get('success'):
                answer = result['final_answer'].get('answer', 'No answer')
                print(f"   ✅ Success - Answer: {answer}")
            else:
                print(f"   ❌ Failed - Error: {result.get('error')}")
        
        # Direct result analysis
        print(f"\n📈 Analysis Results:")
        successes = [r for q, r in results if r.get('success')]
        failures = [r for q, r in results if not r.get('success')]
        
        print(f"Success: {len(successes)}")
        print(f"Failures: {len(failures)}")
        
        # Assignment required analysis
        if failures:
            print(f"\n🔍 Top 5 simplest failure cases:")
            for i, (question, result) in enumerate(failures[:5]):
                print(f"  {i+1}. {question[:50]}...")
                
        if successes:
            print(f"\n🏆 Top 5 most complex success cases:")
            for i, (question, result) in enumerate(successes[:5]):
                workflow = result.get('workflow_used', [])
                print(f"  {i+1}. {question[:50]}... (Workflow: {workflow})")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())