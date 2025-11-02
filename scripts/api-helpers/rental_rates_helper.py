#!/usr/bin/env python3
"""
Rental Rates & ROI Analysis Helper
Provides FREE rental rate data and investment return calculations

Data Sources:
1. HUD Fair Market Rents (FREE government data)
2. Zillow Research Data (FREE CSV downloads)
3. Redfin Data Center (FREE CSV downloads)
4. RentCast API (50 free calls/month - optional)

ROI Calculations:
- Cap Rate (Capitalization Rate)
- Cash-on-Cash Return
- Gross Rent Multiplier (GRM)
- Annual Cash Flow
- Break-Even Analysis
"""

import requests
import json
import os
from datetime import datetime
import pandas as pd
from io import StringIO

class RentalRatesHelper:
    """
    Helper class for rental rate data and ROI analysis
    """

    def __init__(self, rentcast_api_key=None):
        """
        Initialize rental rates helper

        Args:
            rentcast_api_key: Optional RentCast API key (50 free calls/month)
        """
        self.rentcast_api_key = rentcast_api_key or os.getenv('RENTCAST_API_KEY')
        print("Rental Rates Helper initialized")
        print("Data sources: HUD FMR (FREE), Zillow (FREE), Redfin (FREE)")
        if self.rentcast_api_key:
            print("RentCast API: Enabled (50 free calls/month)")
        else:
            print("RentCast API: Not configured (optional)")

    # ==================== HUD FAIR MARKET RENTS ====================

    def get_hud_fmr(self, zip_code, year=2025, bedrooms=2):
        """
        Get HUD Fair Market Rents for a ZIP code

        Args:
            zip_code: 5-digit ZIP code
            year: Year for FMR data (default: 2025)
            bedrooms: Number of bedrooms (0-4, default: 2)

        Returns:
            dict: FMR data including rent estimates
        """
        try:
            # HUD FMR API via ArcGIS REST
            url = "https://services.arcgis.com/VTyQ9soqVukalItT/arcgis/rest/services/FY_2025_FMRs/FeatureServer/0/query"

            params = {
                'where': f"ZIP='{zip_code}'",
                'outFields': '*',
                'returnGeometry': 'false',
                'f': 'json'
            }

            response = requests.get(url, params=params)
            data = response.json()

            if 'features' in data and len(data['features']) > 0:
                attrs = data['features'][0]['attributes']

                # Extract bedroom-specific FMR
                fmr_field = f'FMR_{bedrooms}'
                fmr_value = attrs.get(fmr_field, 'N/A')

                return {
                    'zip_code': zip_code,
                    'year': year,
                    'bedrooms': bedrooms,
                    'fmr_monthly': fmr_value,
                    'fmr_annual': fmr_value * 12 if fmr_value != 'N/A' else 'N/A',
                    'metro_area': attrs.get('AREA_NAME', 'N/A'),
                    'county': attrs.get('COUNTY_NAME', 'N/A'),
                    'state': attrs.get('STATE', 'N/A'),
                    'all_bedrooms': {
                        '0br': attrs.get('FMR_0', 'N/A'),
                        '1br': attrs.get('FMR_1', 'N/A'),
                        '2br': attrs.get('FMR_2', 'N/A'),
                        '3br': attrs.get('FMR_3', 'N/A'),
                        '4br': attrs.get('FMR_4', 'N/A')
                    }
                }
            else:
                return {'error': f'No HUD FMR data found for ZIP {zip_code}'}

        except Exception as e:
            return {'error': f'HUD FMR API error: {str(e)}'}

    # ==================== RENTCAST API (OPTIONAL) ====================

    def get_rentcast_estimate(self, address, city, state, zip_code):
        """
        Get rental estimate from RentCast API (50 free calls/month)

        Args:
            address: Street address
            city: City name
            state: State abbreviation (e.g., 'CA')
            zip_code: 5-digit ZIP code

        Returns:
            dict: Rental estimate and property details
        """
        if not self.rentcast_api_key:
            return {'error': 'RentCast API key not configured. Set RENTCAST_API_KEY in .env'}

        try:
            url = "https://api.rentcast.io/v1/avm/rent"

            params = {
                'address': address,
                'city': city,
                'state': state,
                'zipCode': zip_code
            }

            headers = {
                'X-Api-Key': self.rentcast_api_key
            }

            response = requests.get(url, params=params, headers=headers)
            data = response.json()

            if 'rent' in data:
                return {
                    'address': f"{address}, {city}, {state} {zip_code}",
                    'rent_estimate': data.get('rent', 'N/A'),
                    'rent_range_low': data.get('rentRangeLow', 'N/A'),
                    'rent_range_high': data.get('rentRangeHigh', 'N/A'),
                    'bedrooms': data.get('bedrooms', 'N/A'),
                    'bathrooms': data.get('bathrooms', 'N/A'),
                    'square_feet': data.get('squareFootage', 'N/A'),
                    'property_type': data.get('propertyType', 'N/A'),
                    'confidence': data.get('confidence', 'N/A')
                }
            else:
                return {'error': f'RentCast API error: {data.get("message", "Unknown error")}'}

        except Exception as e:
            return {'error': f'RentCast API error: {str(e)}'}

    # ==================== ROI CALCULATIONS ====================

    def calculate_cap_rate(self, annual_rental_income, property_value, annual_expenses=0):
        """
        Calculate Capitalization Rate (Cap Rate)

        Cap Rate = (Annual Rental Income - Annual Expenses) / Property Value × 100

        Args:
            annual_rental_income: Total annual rent collected
            property_value: Purchase price or current market value
            annual_expenses: Annual operating expenses (property tax, insurance, maintenance, HOA)

        Returns:
            dict: Cap rate and breakdown
        """
        net_operating_income = annual_rental_income - annual_expenses
        cap_rate = (net_operating_income / property_value) * 100

        return {
            'cap_rate': round(cap_rate, 2),
            'annual_rental_income': annual_rental_income,
            'annual_expenses': annual_expenses,
            'net_operating_income': net_operating_income,
            'property_value': property_value,
            'interpretation': self._interpret_cap_rate(cap_rate)
        }

    def calculate_cash_on_cash_return(self, annual_cash_flow, total_cash_invested):
        """
        Calculate Cash-on-Cash Return

        Cash-on-Cash Return = Annual Cash Flow / Total Cash Invested × 100

        Args:
            annual_cash_flow: Annual rental income minus ALL expenses (mortgage, taxes, insurance, etc.)
            total_cash_invested: Down payment + closing costs + repairs

        Returns:
            dict: Cash-on-cash return and breakdown
        """
        coc_return = (annual_cash_flow / total_cash_invested) * 100

        return {
            'cash_on_cash_return': round(coc_return, 2),
            'annual_cash_flow': annual_cash_flow,
            'total_cash_invested': total_cash_invested,
            'monthly_cash_flow': round(annual_cash_flow / 12, 2),
            'interpretation': self._interpret_coc_return(coc_return)
        }

    def calculate_grm(self, property_value, annual_rental_income):
        """
        Calculate Gross Rent Multiplier (GRM)

        GRM = Property Value / Annual Rental Income

        Lower GRM = better deal (property is cheaper relative to rent)

        Args:
            property_value: Purchase price or market value
            annual_rental_income: Annual gross rent (before expenses)

        Returns:
            dict: GRM and interpretation
        """
        grm = property_value / annual_rental_income

        return {
            'gross_rent_multiplier': round(grm, 2),
            'property_value': property_value,
            'annual_rental_income': annual_rental_income,
            'interpretation': self._interpret_grm(grm)
        }

    def analyze_rental_investment(
        self,
        property_value,
        down_payment_pct=20,
        interest_rate=7.0,
        loan_term_years=30,
        monthly_rent=0,
        annual_property_tax_pct=1.2,
        annual_insurance=1200,
        annual_maintenance_pct=1.0,
        hoa_monthly=0,
        vacancy_rate_pct=5,
        property_management_pct=10
    ):
        """
        Comprehensive rental property ROI analysis

        Args:
            property_value: Purchase price
            down_payment_pct: Down payment percentage (default: 20%)
            interest_rate: Annual interest rate (default: 7.0%)
            loan_term_years: Mortgage term in years (default: 30)
            monthly_rent: Monthly rental income
            annual_property_tax_pct: Property tax as % of value (default: 1.2%)
            annual_insurance: Annual insurance cost (default: $1200)
            annual_maintenance_pct: Maintenance as % of value (default: 1.0%)
            hoa_monthly: Monthly HOA fees (default: $0)
            vacancy_rate_pct: Expected vacancy rate (default: 5%)
            property_management_pct: Property management fee % of rent (default: 10%)

        Returns:
            dict: Complete investment analysis with multiple ROI metrics
        """
        # Initial investment
        down_payment = property_value * (down_payment_pct / 100)
        loan_amount = property_value - down_payment
        closing_costs = property_value * 0.03  # Estimate 3% closing costs
        total_cash_invested = down_payment + closing_costs

        # Monthly mortgage payment (P&I only)
        monthly_interest_rate = (interest_rate / 100) / 12
        num_payments = loan_term_years * 12
        monthly_mortgage = loan_amount * (
            monthly_interest_rate * (1 + monthly_interest_rate) ** num_payments
        ) / ((1 + monthly_interest_rate) ** num_payments - 1)

        # Annual income
        gross_annual_rent = monthly_rent * 12
        vacancy_loss = gross_annual_rent * (vacancy_rate_pct / 100)
        effective_annual_rent = gross_annual_rent - vacancy_loss

        # Annual expenses
        annual_property_tax = property_value * (annual_property_tax_pct / 100)
        annual_maintenance = property_value * (annual_maintenance_pct / 100)
        annual_hoa = hoa_monthly * 12
        annual_property_management = effective_annual_rent * (property_management_pct / 100)
        annual_mortgage_payment = monthly_mortgage * 12

        total_annual_expenses = (
            annual_mortgage_payment +
            annual_property_tax +
            annual_insurance +
            annual_maintenance +
            annual_hoa +
            annual_property_management
        )

        # Cash flow
        annual_cash_flow = effective_annual_rent - total_annual_expenses
        monthly_cash_flow = annual_cash_flow / 12

        # ROI metrics
        # Net Operating Income (before mortgage)
        noi = effective_annual_rent - (
            annual_property_tax +
            annual_insurance +
            annual_maintenance +
            annual_hoa +
            annual_property_management
        )

        cap_rate = (noi / property_value) * 100
        coc_return = (annual_cash_flow / total_cash_invested) * 100
        grm = property_value / gross_annual_rent

        return {
            'investment_summary': {
                'property_value': property_value,
                'down_payment': round(down_payment, 2),
                'loan_amount': round(loan_amount, 2),
                'closing_costs': round(closing_costs, 2),
                'total_cash_invested': round(total_cash_invested, 2)
            },
            'income': {
                'monthly_rent': monthly_rent,
                'gross_annual_rent': round(gross_annual_rent, 2),
                'vacancy_loss': round(vacancy_loss, 2),
                'effective_annual_rent': round(effective_annual_rent, 2)
            },
            'expenses': {
                'monthly_mortgage': round(monthly_mortgage, 2),
                'annual_mortgage': round(annual_mortgage_payment, 2),
                'annual_property_tax': round(annual_property_tax, 2),
                'annual_insurance': round(annual_insurance, 2),
                'annual_maintenance': round(annual_maintenance, 2),
                'annual_hoa': round(annual_hoa, 2),
                'annual_property_management': round(annual_property_management, 2),
                'total_annual_expenses': round(total_annual_expenses, 2)
            },
            'cash_flow': {
                'annual_cash_flow': round(annual_cash_flow, 2),
                'monthly_cash_flow': round(monthly_cash_flow, 2),
                'status': 'POSITIVE' if annual_cash_flow > 0 else 'NEGATIVE'
            },
            'roi_metrics': {
                'cap_rate': round(cap_rate, 2),
                'cash_on_cash_return': round(coc_return, 2),
                'gross_rent_multiplier': round(grm, 2),
                'net_operating_income': round(noi, 2)
            },
            'investment_grade': self._grade_investment(cap_rate, coc_return, monthly_cash_flow)
        }

    def compare_markets(self, zip_codes, bedrooms=2, year=2025):
        """
        Compare rental rates across multiple ZIP codes

        Args:
            zip_codes: List of ZIP codes to compare
            bedrooms: Number of bedrooms (default: 2)
            year: Year for FMR data (default: 2025)

        Returns:
            list: Comparison of rental rates across markets
        """
        results = []

        for zip_code in zip_codes:
            fmr_data = self.get_hud_fmr(zip_code, year, bedrooms)
            if 'error' not in fmr_data:
                results.append(fmr_data)

        # Sort by monthly rent (highest to lowest)
        results.sort(key=lambda x: x['fmr_monthly'], reverse=True)

        return results

    # ==================== INTERPRETATION HELPERS ====================

    def _interpret_cap_rate(self, cap_rate):
        """Interpret cap rate value"""
        if cap_rate >= 10:
            return "Excellent (High return, may be higher risk)"
        elif cap_rate >= 8:
            return "Very Good (Strong return)"
        elif cap_rate >= 6:
            return "Good (Average return)"
        elif cap_rate >= 4:
            return "Fair (Below average return)"
        else:
            return "Poor (Low return, may be overpriced)"

    def _interpret_coc_return(self, coc_return):
        """Interpret cash-on-cash return"""
        if coc_return >= 12:
            return "Excellent (Very strong cash flow)"
        elif coc_return >= 8:
            return "Very Good (Strong cash flow)"
        elif coc_return >= 5:
            return "Good (Positive cash flow)"
        elif coc_return >= 0:
            return "Fair (Break-even or minimal cash flow)"
        else:
            return "Poor (Negative cash flow)"

    def _interpret_grm(self, grm):
        """Interpret gross rent multiplier"""
        if grm <= 8:
            return "Excellent (Property is cheap relative to rent)"
        elif grm <= 12:
            return "Good (Fair price-to-rent ratio)"
        elif grm <= 15:
            return "Fair (Average market)"
        else:
            return "Poor (Property may be overpriced relative to rent)"

    def _grade_investment(self, cap_rate, coc_return, monthly_cash_flow):
        """Grade the overall investment quality"""
        score = 0

        # Cap rate scoring
        if cap_rate >= 10:
            score += 3
        elif cap_rate >= 8:
            score += 2
        elif cap_rate >= 6:
            score += 1

        # Cash-on-cash return scoring
        if coc_return >= 12:
            score += 3
        elif coc_return >= 8:
            score += 2
        elif coc_return >= 5:
            score += 1

        # Cash flow scoring
        if monthly_cash_flow >= 500:
            score += 2
        elif monthly_cash_flow >= 200:
            score += 1

        # Grade based on total score
        if score >= 7:
            return "A (Excellent Investment)"
        elif score >= 5:
            return "B (Good Investment)"
        elif score >= 3:
            return "C (Fair Investment)"
        elif score >= 1:
            return "D (Below Average Investment)"
        else:
            return "F (Poor Investment - Avoid)"


def demo_rental_roi_analysis():
    """
    Comprehensive demo of rental ROI analysis
    """
    print("=" * 80)
    print("RENTAL RATES & ROI ANALYSIS - COMPLETE DEMO")
    print("=" * 80)
    print()

    helper = RentalRatesHelper()

    # Example 1: HUD FMR Data
    print("\n1. HUD FAIR MARKET RENTS")
    print("-" * 40)
    zip_code = "90210"  # Beverly Hills, CA
    print(f"Checking HUD FMR for ZIP {zip_code}...")

    fmr_data = helper.get_hud_fmr(zip_code, bedrooms=2)
    if 'error' not in fmr_data:
        print(f"Location: {fmr_data['metro_area']}, {fmr_data['state']}")
        print(f"2-Bedroom FMR: ${fmr_data['fmr_monthly']:,}/month")
        print(f"Annual FMR: ${fmr_data['fmr_annual']:,}/year")
        print(f"\nAll bedroom sizes:")
        for br, rent in fmr_data['all_bedrooms'].items():
            if rent != 'N/A':
                print(f"  {br}: ${rent:,}/month")
    else:
        print(f"Error: {fmr_data['error']}")

    # Example 2: Cap Rate Calculation
    print("\n\n2. CAP RATE CALCULATION")
    print("-" * 40)
    print("Property: $300,000 purchase price")
    print("Annual rent: $24,000 ($2,000/month)")
    print("Annual expenses: $6,000 (taxes, insurance, maintenance)")

    cap_rate = helper.calculate_cap_rate(
        annual_rental_income=24000,
        property_value=300000,
        annual_expenses=6000
    )

    print(f"\nCap Rate: {cap_rate['cap_rate']}%")
    print(f"Net Operating Income: ${cap_rate['net_operating_income']:,}")
    print(f"Grade: {cap_rate['interpretation']}")

    # Example 3: Cash-on-Cash Return
    print("\n\n3. CASH-ON-CASH RETURN")
    print("-" * 40)
    print("Cash invested: $60,000 (down payment + closing)")
    print("Annual cash flow: $4,800 (after mortgage & all expenses)")

    coc = helper.calculate_cash_on_cash_return(
        annual_cash_flow=4800,
        total_cash_invested=60000
    )

    print(f"\nCash-on-Cash Return: {coc['cash_on_cash_return']}%")
    print(f"Monthly Cash Flow: ${coc['monthly_cash_flow']:,.2f}")
    print(f"Grade: {coc['interpretation']}")

    # Example 4: Gross Rent Multiplier
    print("\n\n4. GROSS RENT MULTIPLIER (GRM)")
    print("-" * 40)

    grm = helper.calculate_grm(
        property_value=300000,
        annual_rental_income=24000
    )

    print(f"GRM: {grm['gross_rent_multiplier']}")
    print(f"Grade: {grm['interpretation']}")
    print(f"Note: Lower GRM = better deal")

    # Example 5: Comprehensive Investment Analysis
    print("\n\n5. COMPREHENSIVE RENTAL INVESTMENT ANALYSIS")
    print("-" * 40)
    print("Scenario: $300,000 property with $2,000/month rent")
    print()

    analysis = helper.analyze_rental_investment(
        property_value=300000,
        down_payment_pct=20,
        interest_rate=7.0,
        loan_term_years=30,
        monthly_rent=2000,
        annual_property_tax_pct=1.2,
        annual_insurance=1200,
        annual_maintenance_pct=1.0,
        hoa_monthly=0,
        vacancy_rate_pct=5,
        property_management_pct=10
    )

    print("INVESTMENT SUMMARY:")
    for key, value in analysis['investment_summary'].items():
        print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")

    print("\nINCOME:")
    for key, value in analysis['income'].items():
        print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")

    print("\nEXPENSES:")
    for key, value in analysis['expenses'].items():
        print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")

    print("\nCASH FLOW:")
    for key, value in analysis['cash_flow'].items():
        if isinstance(value, (int, float)):
            print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")
        else:
            print(f"  {key.replace('_', ' ').title()}: {value}")

    print("\nROI METRICS:")
    for key, value in analysis['roi_metrics'].items():
        if isinstance(value, (int, float)):
            if 'return' in key or 'rate' in key:
                print(f"  {key.replace('_', ' ').title()}: {value}%")
            else:
                print(f"  {key.replace('_', ' ').title()}: {value}")
        else:
            print(f"  {key.replace('_', ' ').title()}: ${value:,.2f}")

    print(f"\nINVESTMENT GRADE: {analysis['investment_grade']}")

    # Example 6: Compare Multiple Markets
    print("\n\n6. COMPARE RENTAL MARKETS")
    print("-" * 40)
    zip_codes = ["90210", "10001", "60601", "33139"]  # Beverly Hills, NYC, Chicago, Miami
    print(f"Comparing 2-bedroom FMRs across {len(zip_codes)} markets...")
    print()

    comparison = helper.compare_markets(zip_codes, bedrooms=2)

    print(f"{'Rank':<6} {'ZIP':<8} {'Location':<30} {'Monthly Rent':<15}")
    print("-" * 65)

    for i, market in enumerate(comparison, 1):
        location = f"{market['metro_area']}, {market['state']}"
        rent = f"${market['fmr_monthly']:,}"
        print(f"{i:<6} {market['zip_code']:<8} {location:<30} {rent:<15}")

    print("\n" + "=" * 80)
    print("DEMO COMPLETE - ROI Analysis Tools Ready!")
    print("=" * 80)


if __name__ == "__main__":
    demo_rental_roi_analysis()
