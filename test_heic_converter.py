import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(f'file://{os.path.abspath("index.html")}')

        # Test single file conversion to JPEG
        print("Testing single file JPEG conversion...")
        await page.set_input_files('input#file-input', 'sample.heic')
        await page.select_option('select#format-select', 'jpeg')
        await page.click('button#convert-btn')
        await page.wait_for_selector('text=✓ Completed')
        print('Single file JPEG conversion successful')

        # Test single file conversion to PNG
        print("Testing single file PNG conversion...")
        await page.set_input_files('input#file-input', 'sample.heic')
        await page.select_option('select#format-select', 'png')
        await page.click('button#convert-btn')
        await page.wait_for_selector('text=✓ Completed')
        print('Single file PNG conversion successful')

        # Test multiple file conversion
        print("Testing multiple file conversion...")
        # Create a second sample file for this test
        with open('sample2.heic', 'wb') as f:
            with open('sample.heic', 'rb') as f_in:
                f.write(f_in.read())
        await page.set_input_files('input#file-input', ['sample.heic', 'sample2.heic'])
        await page.click('button#convert-btn')
        await page.wait_for_selector('text=✓ Completed >> nth=1')
        print('Multiple file conversion successful')

        # Test single file download
        print("Testing single file download...")
        await page.set_input_files('input#file-input', 'sample.heic')
        await page.click('button#convert-btn')
        await page.wait_for_selector('text=✓ Completed')
        async with page.expect_download() as download_info:
            await page.click('text=Download 1 file(s)')
        download = await download_info.value
        path = await download.path()
        print(f'Single file download successful: {path}')
        assert os.path.getsize(path) > 0

        # Test multiple file download
        print("Testing multiple file download...")
        await page.set_input_files('input#file-input', ['sample.heic', 'sample2.heic'])
        await page.click('button#convert-btn')
        await page.wait_for_selector('text=✓ Completed >> nth=1')
        async with page.expect_download() as download_info:
            await page.click('text=Download 2 file(s)')
        download = await download_info.value
        path = await download.path()
        print(f'Multiple file download successful: {path}')
        assert os.path.getsize(path) > 0


        await browser.close()

        # Clean up sample files
        os.remove('sample.heic')
        os.remove('sample2.heic')

asyncio.run(main())
