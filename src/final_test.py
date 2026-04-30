from src.rag_assistant import MutualFundAssistant
import sys

# Fix Windows console encoding
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def run_final_tests():
    assistant = MutualFundAssistant()
    
    test_queries = [
        "What is the exit load of HDFC ELSS Fund?",
        "Who is the fund manager for HDFC Equity Fund?",
        "Which HDFC fund should I invest in for high returns?",
        "What is the minimum SIP for HDFC Focused Fund?"
    ]
    
    print("="*60)
    print("MUTUAL FUND FAQ ASSISTANT - FINAL SYSTEM TEST")
    print("="*60)
    
    for i, query in enumerate(test_queries):
        print(f"\nTEST {i+1}: {query}")
        print("-" * 30)
        try:
            response = assistant.ask(query)
            print(f"RESPONSE:\n{response}")
        except Exception as e:
            print(f"ERROR: {e}")
        print("-" * 30)
        
    print("\nSYSTEM TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_final_tests()
