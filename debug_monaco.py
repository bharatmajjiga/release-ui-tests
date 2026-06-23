"""
Debug script to investigate Monaco editor issue in OCP 4.18.
Tests various Monaco API access methods.
"""

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


# Load environment variables
load_dotenv()

CONSOLE_URL = os.getenv("CONSOLE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")


async def debug_monaco_editor() -> None:
    """Debug Monaco editor in OCP 4.18 Pipeline Builder YAML view."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--ignore-certificate-errors"])
        context = await browser.new_context(ignore_https_errors=True)
        page = await context.new_page()

        try:
            print("\n🔍 Debugging Monaco Editor on OCP 4.18")
            print(f"Console URL: {CONSOLE_URL}\n")

            # Login
            print("1. Logging in...")
            await page.goto(f"{CONSOLE_URL}/k8s/cluster/projects")
            await page.fill('input[name="username"]', USERNAME)
            await page.fill('input[name="password"]', PASSWORD)
            await page.click('button[type="submit"]')
            await page.wait_for_load_state("networkidle")
            print("   ✓ Login successful\n")

            # Navigate to Pipelines
            print("2. Navigating to Pipelines...")
            await page.click('button:has-text("Pipelines")')
            await page.wait_for_timeout(500)
            await page.click('a:has-text("Pipelines")')
            await page.wait_for_load_state("networkidle")
            print("   ✓ On Pipelines page\n")

            # Click Create button
            print("3. Opening Pipeline Builder...")
            await page.click('button:has-text("Create")')
            await page.wait_for_timeout(500)
            await page.click('role=menuitem[name="Pipeline"]')
            await page.wait_for_timeout(2000)
            print("   ✓ Pipeline Builder opened\n")

            # Switch to YAML view
            print("4. Switching to YAML view...")
            await page.click('button:has-text("YAML view")')
            await page.wait_for_timeout(2000)
            print("   ✓ YAML view active\n")

            # Test Monaco API availability
            print("5. Testing Monaco API methods:\n")

            # Method 1: window.monaco.editor.getModels()
            result1 = await page.evaluate(
                """
                () => {
                    try {
                        if (window.monaco && window.monaco.editor) {
                            const models = window.monaco.editor.getModels();
                            return {
                                available: true,
                                modelCount: models ? models.length : 0,
                                hasValue: models && models.length > 0 ? typeof models[0].getValue === 'function' : false
                            };
                        }
                        return { available: false, error: 'window.monaco not available' };
                    } catch (e) {
                        return { available: false, error: e.toString() };
                    }
                }
                """
            )
            print("   Method 1 (window.monaco.editor.getModels()):")
            print(f"      Available: {result1.get('available')}")
            print(f"      Model count: {result1.get('modelCount', 'N/A')}")
            print(f"      Has getValue: {result1.get('hasValue', 'N/A')}")
            if "error" in result1:
                print(f"      Error: {result1['error']}")
            print()

            # Method 2: document.querySelector('.monaco-editor')._editor
            result2 = await page.evaluate(
                """
                () => {
                    try {
                        const editorElement = document.querySelector('.monaco-editor');
                        if (editorElement) {
                            return {
                                available: true,
                                hasEditor: !!editorElement._editor,
                                hasGetValue: editorElement._editor ? typeof editorElement._editor.getValue
                                === 'function' : false
                            };
                        }
                        return { available: false, error: '.monaco-editor not found' };
                    } catch (e) {
                        return { available: false, error: e.toString() };
                    }
                }
                """
            )
            print("   Method 2 (.monaco-editor._editor):")
            print(f"      Element found: {result2.get('available')}")
            print(f"      Has _editor: {result2.get('hasEditor', 'N/A')}")
            print(f"      Has getValue: {result2.get('hasGetValue', 'N/A')}")
            if "error" in result2:
                print(f"      Error: {result2['error']}")
            print()

            # Method 3: Check for data-test="code-editor"
            result3 = await page.evaluate(
                """
                () => {
                    const codeEditor = document.querySelector('[data-test="code-editor"]');
                    return {
                        found: !!codeEditor,
                        visible: codeEditor ? window.getComputedStyle(codeEditor).display !== 'none' : false
                    };
                }
                """
            )
            print("   Method 3 ([data-test='code-editor']):")
            print(f"      Found: {result3.get('found')}")
            print(f"      Visible: {result3.get('visible')}")
            print()

            # Method 4: List all Monaco-related elements
            monaco_elements = await page.evaluate(
                """
                () => {
                    const elements = {
                        'monaco-editor': document.querySelectorAll('.monaco-editor').length,
                        'view-lines': document.querySelectorAll('.view-lines').length,
                        'monaco-textarea': document.querySelectorAll('.monaco-editor textarea').length,
                        'data-test-code-editor': document.querySelectorAll('[data-test="code-editor"]').length
                    };
                    return elements;
                }
                """
            )
            print("   Monaco-related elements on page:")
            for selector, count in monaco_elements.items():
                print(f"      {selector}: {count} element(s)")
            print()

            # Method 5: Try to get current YAML content (should be default template)
            print("6. Attempting to read default YAML content:\n")
            current_content = await page.evaluate(
                """
                () => {
                    // Try all methods
                    if (window.monaco && window.monaco.editor) {
                        const models = window.monaco.editor.getModels();
                        if (models && models.length > 0) {
                            return { method: 'getModels', content: models[0].getValue() };
                        }
                    }

                    const editorElement = document.querySelector('.monaco-editor');
                    if (editorElement && editorElement._editor) {
                        return { method: '_editor', content: editorElement._editor.getValue() };
                    }

                    return { method: 'none', content: null };
                }
                """
            )
            print(f"   Method used: {current_content.get('method')}")
            if current_content.get("content"):
                content_preview = current_content["content"][:200]
                print("   Content preview (first 200 chars):")
                print(f"      {content_preview}...")
            else:
                print("   Content: No content available")
            print()

            # Method 6: Test setting content
            print("7. Testing set content operation:\n")
            test_yaml = "apiVersion: tekton.dev/v1\\nkind: Pipeline\\nmetadata:\\n  name: test-pipeline"
            set_result = await page.evaluate(
                """
                (content) => {
                    try {
                        if (window.monaco && window.monaco.editor) {
                            const models = window.monaco.editor.getModels();
                            if (models && models.length > 0) {
                                models[0].setValue(content);
                                return { success: true, method: 'getModels' };
                            }
                        }

                        const editorElement = document.querySelector('.monaco-editor');
                        if (editorElement && editorElement._editor) {
                            editorElement._editor.setValue(content);
                            return { success: true, method: '_editor' };
                        }

                        return { success: false, error: 'No Monaco API available' };
                    } catch (e) {
                        return { success: false, error: e.toString() };
                    }
                }
                """,
                test_yaml,
            )
            print("   Set content result:")
            print(f"      Success: {set_result.get('success')}")
            print(f"      Method: {set_result.get('method', 'N/A')}")
            if "error" in set_result:
                print(f"      Error: {set_result['error']}")
            print()

            # Pause for manual inspection
            print("✓ Debug complete. Browser will stay open for 30 seconds for inspection...")
            await page.wait_for_timeout(30000)

        except Exception as e:
            print(f"\n❌ Error during debugging: {e}")
            import traceback

            traceback.print_exc()

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_monaco_editor())
