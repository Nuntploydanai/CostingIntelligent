"""
Check what the server is actually receiving and calculating
"""
import sys
sys.path.insert(0, r'C:\Users\dploy\.openclaw\workspace\basicshirts_web')

# Add debug to see what's happening
import total_cost_calc

# Monkey patch to see what's being passed
original_compute = total_cost_calc.compute_total_cost_summary

def debug_compute(*args, **kwargs):
    print(f"\n{'='*80}")
    print("DEBUG: compute_total_cost_summary called with:")
    print(f"  gender: '{kwargs.get('gender', args[6] if len(args) > 6 else 'NOT PROVIDED')}'")
    print(f"  silhouette: '{kwargs.get('silhouette', args[7] if len(args) > 7 else 'NOT PROVIDED')}'")
    print(f"  size: '{kwargs.get('size', args[8] if len(args) > 8 else 'NOT PROVIDED')}'")

    result = original_compute(*args, **kwargs)

    print(f"\nDEBUG: Result:")
    print(f"  total_sewing_thread_cost: {result['total_sewing_thread_cost']}")
    print(f"  total_sewing_thread_cost_pct: {result['total_sewing_thread_cost_pct']}")
    print(f"{'='*80}\n")

    return result

total_cost_calc.compute_total_cost_summary = debug_compute

# Now test
from total_cost_calc import compute_total_cost_summary

result = compute_total_cost_summary(
    fabric_cost=0.14,
    trim_cost=16.8,
    print_embroidery_cost=1.05,
    display_packaging_cost='-',
    transit_packaging_cost='-',
    label_cost='-',
    labour_cost=0.144907,
    gender="Men",
    silhouette="Tank Top/A Shirt",  # This is what the dropdown sends
    size="S-XL",
    supplier_margin_percent=10.0,
)

print(f"\nFinal Result: Sewing Thread = ${result['total_sewing_thread_cost']}")
