"""
Automatic Cookie Extractor for Cell Collective
Uses Playwright to open browser, let you login, then extracts cookie
"""
import asyncio
from playwright.async_api import async_playwright
import json

async def get_cell_collective_cookie():
    """
    Opens Cell Collective in a browser, waits for you to be logged in,
    then extracts the connect.sid cookie automatically
    """
    print("\n" + "="*70)
    print("Cell Collective Cookie Extractor")
    print("="*70)
    print("\nThis will:")
    print("1. Open Cell Collective in a browser window")
    print("2. Wait for you to login (if not already)")
    print("3. Automatically extract your session cookie")
    print("4. Save it for the backend to use")
    print("\n" + "="*70)

    async with async_playwright() as p:
        # Launch browser (visible, not headless)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to Cell Collective
        print("\n[1] Opening Cell Collective...")
        await page.goto('https://teach.cellcollective.org/dashboard')

        print("\n[2] Waiting for page to load...")
        await page.wait_for_load_state('networkidle')

        print("\n" + "-"*70)
        print("PLEASE LOGIN TO CELL COLLECTIVE IF NEEDED")
        print("Once you see your dashboard, press ENTER here...")
        print("-"*70)

        # Wait for user to login
        input("\nPress ENTER when you're logged in and can see your dashboard: ")

        print("\n[3] Extracting cookies...")

        # Get all cookies
        cookies = await context.cookies()

        # Find connect.sid
        connect_sid = None
        for cookie in cookies:
            if cookie['name'] == 'connect.sid':
                connect_sid = cookie['value']
                break

        if connect_sid:
            print(f"\n SUCCESS! Found cookie:")
            print(f"\nToken: {connect_sid}")
            print(f"Length: {len(connect_sid)} characters")

            # Save to file
            with open('cell_collective_token.txt', 'w') as f:
                f.write(connect_sid)

            print(f"\n Cookie saved to: cell_collective_token.txt")

            # Take a screenshot as proof
            await page.screenshot(path='cell_collective_logged_in.png')
            print(f" Screenshot saved to: cell_collective_logged_in.png")

            # Also save all cookies for debugging
            with open('cell_collective_all_cookies.json', 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f" All cookies saved to: cell_collective_all_cookies.json")

        else:
            print("\n ERROR: Could not find connect.sid cookie!")
            print("This means you might not be fully logged in.")
            print("Please try again and make sure you can see your dashboard.")

        print("\n[4] Closing browser...")
        await browser.close()

        return connect_sid

if __name__ == "__main__":
    cookie = asyncio.run(get_cell_collective_cookie())

    if cookie:
        print("\n" + "="*70)
        print("DONE! Your token is ready.")
        print("="*70)
        print(f"\nTo use it, paste this into the lesson page:")
        print(f"\n{cookie}")
        print("\n" + "="*70)
