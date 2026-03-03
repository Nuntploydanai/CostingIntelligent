"""
Check for syntax errors in server.py
"""
import sys
import ast

sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

# Check server.py syntax
try:
    with open(r'C:\Users\dploy\.openclaw\workspace\basicshirts_web\server.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("OK: server.py syntax is valid")
except SyntaxError as e:
    print(f"SYNTAX ERROR in server.py:")
    print(f"  Line {e.lineno}: {e.msg}")
    print(f"  {e.text}")

# Check total_cost_calc.py syntax
try:
    with open(r'C:\Users\dploy\.openclaw\workspace\basicshirts_web\total_cost_calc.py', 'r', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
    print("OK: total_cost_calc.py syntax is valid")
except SyntaxError as e:
    print(f"SYNTAX ERROR in total_cost_calc.py:")
    print(f"  Line {e.lineno}: {e.msg}")
    print(f"  {e.text}")

# Try importing
try:
    from total_cost_calc import compute_total_cost_summary
    print("OK: total_cost_calc imported")
    
    # Test it
    result = compute_total_cost_summary(
        fabric_cost=0.14,
        trim_cost=16.8,
        print_embroidery_cost=1.05,
        display_packaging_cost=0.01,
        transit_packaging_cost=0.1,
        label_cost=0.02884,
        labour_cost=0.144907,
        gender="Men",
        silhouette="Tank top/A Shirt",
    )
    print(f"OK: Function works, sewing_thread_cost = {result['total_sewing_thread_cost']}")
    
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
