#!/usr/bin/env python3
"""
Example: Real Estate Investment ROI Analysis

This script shows how to analyze rental property investments
and calculate rates of return.
"""

import sys
sys.path.insert(0, 'C:/Users/MarieLexisDad/scripts/api-helpers')
from rental_rates_helper import RentalRatesHelper

def main():
    helper = RentalRatesHelper()

    print("=" * 80)
    print("REAL ESTATE INVESTMENT ROI ANALYSIS")
    print("=" * 80)
    print()

    # Example Investment Scenario
    # You're looking at a property and want to know if it's a good investment

    property_value = 250000  # Purchase price
    monthly_rent = 2200      # Expected monthly rent

    print(f"Analyzing property: ${property_value:,}")
    print(f"Expected rent: ${monthly_rent:,}/month")
    print()
    print("-" * 80)

    # Run comprehensive analysis
    analysis = helper.analyze_rental_investment(
        property_value=property_value,
        down_payment_pct=20,           # 20% down
        interest_rate=7.0,             # 7% mortgage rate
        loan_term_years=30,            # 30-year mortgage
        monthly_rent=monthly_rent,     # Monthly rent
        annual_property_tax_pct=1.2,   # 1.2% property tax
        annual_insurance=1200,         # $1,200/year insurance
        annual_maintenance_pct=1.0,    # 1% of value for maintenance
        hoa_monthly=0,                 # No HOA
        vacancy_rate_pct=5,            # 5% vacancy
        property_management_pct=10     # 10% property management
    )

    print("\n1. INITIAL INVESTMENT REQUIRED")
    print("-" * 40)
    inv = analysis['investment_summary']
    print(f"Down Payment (20%):     ${inv['down_payment']:>12,.2f}")
    print(f"Closing Costs (3%):     ${inv['closing_costs']:>12,.2f}")
    print(f"-----------------------------------------")
    print(f"TOTAL CASH NEEDED:      ${inv['total_cash_invested']:>12,.2f}")

    print("\n2. MONTHLY CASH FLOW BREAKDOWN")
    print("-" * 40)
    income = analysis['income']
    expenses = analysis['expenses']

    print(f"Monthly Rent:           ${income['monthly_rent']:>12,.2f}")
    print(f"Monthly Mortgage:      -${expenses['monthly_mortgage']:>12,.2f}")
    print(f"Property Tax:          -${expenses['annual_property_tax']/12:>12,.2f}")
    print(f"Insurance:             -${expenses['annual_insurance']/12:>12,.2f}")
    print(f"Maintenance:           -${expenses['annual_maintenance']/12:>12,.2f}")
    print(f"Property Management:   -${expenses['annual_property_management']/12:>12,.2f}")
    print(f"-----------------------------------------")

    cash_flow = analysis['cash_flow']
    if cash_flow['monthly_cash_flow'] >= 0:
        print(f"MONTHLY PROFIT:         ${cash_flow['monthly_cash_flow']:>12,.2f} [GOOD]")
    else:
        print(f"MONTHLY LOSS:           ${cash_flow['monthly_cash_flow']:>12,.2f} [BAD]")

    print("\n3. RETURN ON INVESTMENT (ROI) METRICS")
    print("-" * 40)
    roi = analysis['roi_metrics']

    print(f"Cap Rate:               {roi['cap_rate']:>12.2f}%")
    print(f"  (Industry standard: 8-12% is good)")
    print()
    print(f"Cash-on-Cash Return:    {roi['cash_on_cash_return']:>12.2f}%")
    print(f"  (How much you earn on your actual cash invested)")
    print()
    print(f"Annual Cash Flow:       ${cash_flow['annual_cash_flow']:>12,.2f}")
    print(f"  (Total profit/loss per year)")

    print("\n4. INVESTMENT GRADE")
    print("-" * 40)
    print(f"OVERALL RATING: {analysis['investment_grade']}")

    # Decision helper
    print("\n5. SHOULD YOU BUY THIS PROPERTY?")
    print("-" * 40)

    if cash_flow['monthly_cash_flow'] > 0 and roi['cash_on_cash_return'] >= 8:
        print("[YES] - Strong investment opportunity!")
        print(f"  - Positive cash flow of ${cash_flow['monthly_cash_flow']:.2f}/month")
        print(f"  - {roi['cash_on_cash_return']:.1f}% return on your cash")
    elif cash_flow['monthly_cash_flow'] > 0:
        print("[MAYBE] - Positive cash flow but lower returns")
        print(f"  - Profit of ${cash_flow['monthly_cash_flow']:.2f}/month")
        print(f"  - But only {roi['cash_on_cash_return']:.1f}% return")
        print("  - Consider if you have better investment options")
    else:
        print("[NO] - This property loses money every month")
        print(f"  - Monthly loss: ${abs(cash_flow['monthly_cash_flow']):.2f}")
        print(f"  - Annual loss: ${abs(cash_flow['annual_cash_flow']):,.2f}")
        print("  - Avoid unless you expect significant appreciation")

    print("\n" + "=" * 80)

    # Quick comparison - what if rent was higher?
    print("\nWHAT IF RENT WAS $2,500/MONTH INSTEAD?")
    print("-" * 40)

    better_analysis = helper.analyze_rental_investment(
        property_value=property_value,
        monthly_rent=2500,  # Higher rent
        down_payment_pct=20,
        interest_rate=7.0,
        loan_term_years=30,
        annual_property_tax_pct=1.2,
        annual_insurance=1200,
        annual_maintenance_pct=1.0,
        vacancy_rate_pct=5,
        property_management_pct=10
    )

    better_cf = better_analysis['cash_flow']
    better_roi = better_analysis['roi_metrics']

    print(f"Monthly Cash Flow: ${better_cf['monthly_cash_flow']:,.2f}")
    print(f"Cash-on-Cash Return: {better_roi['cash_on_cash_return']:.2f}%")
    print(f"Investment Grade: {better_analysis['investment_grade']}")
    print()

    # Quick formula reference
    print("\n" + "=" * 80)
    print("QUICK REFERENCE - ROI FORMULAS")
    print("=" * 80)
    print()
    print("Cap Rate = (Annual Rent - Annual Expenses) / Property Value × 100")
    print("  • Measures the property's income-generating potential")
    print("  • 8-12% is considered good")
    print("  • Doesn't account for financing")
    print()
    print("Cash-on-Cash Return = Annual Cash Flow / Total Cash Invested × 100")
    print("  • Measures return on YOUR actual money")
    print("  • Accounts for mortgage and all expenses")
    print("  • 8-12% is excellent")
    print()
    print("Gross Rent Multiplier (GRM) = Property Value / Annual Rent")
    print("  • Lower is better (property is cheaper relative to rent)")
    print("  • 8-12 is typical")
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
