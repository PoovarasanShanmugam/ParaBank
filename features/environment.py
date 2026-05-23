import os
import uuid
from config.global_config import Config
from utils.browser_manager import BrowserManager
from utils.scenario_context import ScenarioContext

def before_scenario(context, scenario):
    """
    Setup hook run before each scenario.
    Initializes ScenarioContext and starts browser session if running in UI mode.
    """
    print(f"\n[SCENARIO] Starting scenario: {scenario.name}")
    
    context.scenario_context = ScenarioContext()
    
    if Config.is_ui_mode():
        print(f"[ENV] Starting browser context...")
        context.browser_manager = BrowserManager()
        context.page = context.browser_manager.start()
    else:
        print(f"[ENV] Skipping browser startup. Run Mode: {Config.RUN_MODE}")

def after_scenario(context, scenario):
    """
    Teardown hook run after each scenario.
    Takes screenshots and video recordings if scenario passed, then closes browser.
    """
    status = "PASSED" if scenario.status.name == "passed" else "FAILED"
    print(f"[SCENARIO] Finished scenario: {scenario.name} | Status: {status}\n")
    
    is_success = (scenario.status.name == "passed")
    
    if Config.is_ui_mode() and hasattr(context, "browser_manager") and context.browser_manager:
        proof_dir = os.path.join(os.getcwd(), "proof")
        screenshots_dir = os.path.join(proof_dir, "screenshots")
        videos_dir = os.path.join(proof_dir, "videos")
        
        os.makedirs(screenshots_dir, exist_ok=True)
        os.makedirs(videos_dir, exist_ok=True)
        
        safe_name = scenario.name.replace(" ", "_").replace("/", "_").lower()
        screenshot_path = os.path.join(screenshots_dir, f"{safe_name}_passed.png")
        temp_video_path = context.browser_manager.video_path
        
        if is_success:
            # Capture screenshot only on success as requested
            try:
                context.page.screenshot(path=screenshot_path, full_page=True)
                print(f"[ENV] Screenshot saved to: {screenshot_path}")
            except Exception as e:
                print(f"[ENV] [WARNING] Failed to take screenshot: {e}")
        else:
            print("[ENV] Scenario failed. Skipping screenshot capture.")

        # Clean up browser session
        print("[ENV] Closing browser session...")
        context.browser_manager.stop()
        
        if temp_video_path and os.path.exists(temp_video_path):
            if is_success:
                dest_video_path = os.path.join(videos_dir, f"{safe_name}_passed.webm")
                try:
                    if os.path.exists(dest_video_path):
                        os.remove(dest_video_path)
                    os.rename(temp_video_path, dest_video_path)
                    print(f"[ENV] Video recording saved to: {dest_video_path}")
                except Exception as e:
                    print(f"[ENV] [WARNING] Failed to rename video: {e}")
            else:
                try:
                    os.remove(temp_video_path)
                    print("[ENV] Scenario failed. Temporary video file deleted.")
                except Exception as e:
                    print(f"[ENV] [WARNING] Failed to delete video: {e}")
                
    context.scenario_context.clear()

