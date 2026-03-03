"""
Check for syntax errors in server.py
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

try:
    import server
    print("✅ server.py imported successfully")
except Exception as e:
    print(f"❌ Error importing server.py:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

try:
    from total_cost_calc import compute_total_cost_summary
    print("✅ total_cost_calc.py imported successfully")
    
    # Test the function
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
    print("✅ compute_total_cost_summary() works")
    print(f"   Result: {result}")
    
except Exception as e:
    print(f"❌ Error with total_cost_calc:")
    print(f"   {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
