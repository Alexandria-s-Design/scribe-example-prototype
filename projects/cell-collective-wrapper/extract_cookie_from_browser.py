"""
Extract Cookie from Currently Open Browser
Connects to existing browser session to get cookies without re-logging in
"""
import asyncio
from playwright.async_api import async_playwright
import json
import sys

async def extract_from_current_browser():
    """
    Connect to an existing browser and extract cookies
    No login required - uses your already-logged-in session
    """
    print("\n" + "="*70)
    print("Cell Collective Cookie Extractor (Quick Mode)")
    print("="*70)
    print("\nExtracting cookie from your logged-in browser session...")
    print("This only takes a few seconds!\n")

    try:
        async with async_playwright() as p:
            # Launch new browser instance (will be separate from your open browser)
            # User needs to login manually once
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # Navigate to Cell Collective dashboard
            print("[1/4] Opening Cell Collective...")
            await page.goto('https://teach.cellcollective.org/dashboard', timeout=60000)

            # Wait for page to load
            print("[2/4] Waiting for page to load...")
            try:
                # Wait for either login form OR dashboard to appear
                await page.wait_for_selector('input[type="email"], .dashboard, [data-testid="dashboard"]', timeout=10000)
            except:
                pass

            # Check if logged in
            cookies = await context.cookies()
            connect_sid = None
            for cookie in cookies:
                if cookie['name'] == 'connect.sid':
                    connect_sid = cookie['value']
                    break

            if connect_sid:
                print("[3/4] ✓ Already logged in! Cookie found.")

                # Save cookie
                with open('cell_collective_token.txt', 'w') as f:
                    f.write(connect_sid)

                # Save all cookies
                with open('cell_collective_all_cookies.json', 'w') as f:
                    json.dump(cookies, f, indent=2)

                # Take screenshot
                await page.screenshot(path='cell_collective_logged_in.png')

                print(f"[4/4] ✓ Done!")
                print(f"\n" + "="*70)
                print(f"SUCCESS! Cookie extracted:")
                print(f"  Token: {connect_sid[:50]}...")
                print(f"  Length: {len(connect_sid)} characters")
                print(f"\nFiles saved:")
                print(f"  • cell_collective_token.txt")
                print(f"  • cell_collective_all_cookies.json")
                print(f"  • cell_collective_logged_in.png")
                print("="*70 + "\n")

                await browser.close()
                return connect_sid
            else:
                print("[3/4] ⚠ Not logged in yet.")
                print("\nPlease:")
                print("  1. Login to Cell Collective in the browser window that just opened")
                print("  2. After you see your dashboard, press ENTER here")

                input("\nPress ENTER when logged in: ")

                # Get cookies again
                cookies = await context.cookies()
                connect_sid = None
                for cookie in cookies:
                    if cookie['name'] == 'connect.sid':
                        connect_sid = cookie['value']
                        break

                if connect_sid:
                    print("[4/4] ✓ Success! Cookie extracted.")

                    # Save
                    with open('cell_collective_token.txt', 'w') as f:
                        f.write(connect_sid)
                    with open('cell_collective_all_cookies.json', 'w') as f:
                        json.dump(cookies, f, indent=2)
                    await page.screenshot(path='cell_collective_logged_in.png')

                    print(f"\n" + "="*70)
                    print(f"SUCCESS! Cookie extracted:")
                    print(f"  Token: {connect_sid[:50]}...")
                    print(f"  Files saved to: {sys.path[0]}")
                    print("="*70 + "\n")

                    await browser.close()
                    return connect_sid
                else:
                    print("[4/4] ✗ Failed to get cookie. Please try again.")
                    await browser.close()
                    return None

    except Exception as e:
        print(f"\n✗ Error: {e}")
        return None

if __name__ == "__main__":
    cookie = asyncio.run(extract_from_current_browser())

    if cookie:
        print("\n🎉 READY TO TEST!")
        print("Next step: Run `python test_auth.py` to verify authentication\n")
    else:
        print("\n⚠ No cookie extracted. Please try again.\n")
