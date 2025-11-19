"""
Automated screenshot capture for Scribe simulation validation.
Captures all 7 screens for comparison with actual Scribe.com onboarding.
"""
import asyncio
import os
from playwright.async_api import async_playwright

async def capture_all_screens():
    """Capture screenshots of all 7 simulation screens."""
    html_file = os.path.abspath("scribe-simulation.html")
    screenshots_dir = "validation_screenshots"

    # Create screenshots directory
    os.makedirs(screenshots_dir, exist_ok=True)

    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page(viewport={"width": 1280, "height": 720})

        # Open HTML file
        await page.goto(f"file:///{html_file}")
        await page.wait_for_timeout(1000)

        print("📸 Capturing screenshots...")

        # Screen 1: Cover screen
        print("  1/7 - Cover screen")
        await page.screenshot(path=f"{screenshots_dir}/01_cover_screen.png", full_page=False)
        await page.wait_for_timeout(500)

        # Click "Start Onboarding" to go to homepage
        await page.click(".start-button")
        await page.wait_for_timeout(1000)

        # Screen 2: Homepage (use cases)
        print("  2/7 - Homepage with use cases")
        await page.screenshot(path=f"{screenshots_dir}/02_homepage_use_cases.png", full_page=False)
        await page.wait_for_timeout(500)

        # Click first use case card (Onboard)
        await page.click(".use-case-card:first-child")
        await page.wait_for_timeout(1000)

        # Screen 3: Sign in screen
        print("  3/7 - Sign in screen")
        await page.screenshot(path=f"{screenshots_dir}/03_sign_in.png", full_page=False)
        await page.wait_for_timeout(500)

        # Click "Sign in with Google"
        await page.click(".google-button")
        await page.wait_for_timeout(1000)

        # Screen 4: Account chooser
        print("  4/7 - Account chooser")
        await page.screenshot(path=f"{screenshots_dir}/04_account_chooser.png", full_page=False)
        await page.wait_for_timeout(500)

        # Click first account
        await page.click(".account-option:first-child")
        await page.wait_for_timeout(1000)

        # Screen 5: OAuth permissions
        print("  5/7 - OAuth permissions")
        await page.screenshot(path=f"{screenshots_dir}/05_oauth_permissions.png", full_page=False)
        await page.wait_for_timeout(500)

        # Click "Allow"
        await page.click(".oauth-allow-button")
        await page.wait_for_timeout(1000)

        # Screen 6: Team naming
        print("  6/7 - Team naming")
        await page.screenshot(path=f"{screenshots_dir}/06_team_naming.png", full_page=False)
        await page.wait_for_timeout(500)

        # Enter team name
        await page.fill("#team-name-input", "Test Team")
        await page.wait_for_timeout(500)

        # Take screenshot with validation success
        await page.screenshot(path=f"{screenshots_dir}/06b_team_naming_validated.png", full_page=False)

        # Click "Continue"
        await page.click(".continue-button")
        await page.wait_for_timeout(1000)

        # Screen 7: Completion screen
        print("  7/7 - Completion screen")
        await page.screenshot(path=f"{screenshots_dir}/07_completion.png", full_page=False)
        await page.wait_for_timeout(500)

        await browser.close()

    print(f"\n✅ Screenshots saved to '{screenshots_dir}/' directory")
    print("📁 Files created:")
    for filename in sorted(os.listdir(screenshots_dir)):
        if filename.endswith('.png'):
            file_path = os.path.join(screenshots_dir, filename)
            file_size = os.path.getsize(file_path) / 1024  # KB
            print(f"   - {filename} ({file_size:.1f} KB)")

if __name__ == "__main__":
    asyncio.run(capture_all_screens())
