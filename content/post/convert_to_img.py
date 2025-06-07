import os.path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import argparse
import os.path as osp
import numpy as np

def html_to_png(html_path, out_path, mobile_friendly=False): 
    if out_path is None:
        out_path = os.path.dirname(html_path)
    
    # Convert to absolute path and proper file URL
    html_path = os.path.abspath(html_path)
    if not html_path.startswith('file://'):
        html_path = 'file://' + html_path
    
    # Mobile viewport settings
    if mobile_friendly:
        mobile_width = 375  # iPhone width
        mobile_height = 812  # iPhone height
        mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1"
    
    # Try Chrome first (more commonly available on macOS)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 不知为啥只能在无头模式执行才能截全屏
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  # Add for better compatibility
        options.add_argument('--disable-dev-shm-usage')  # Add for better compatibility
        
        # Add mobile-specific options
        if mobile_friendly:
            options.add_argument(f'--user-agent={mobile_user_agent}')
            options.add_argument(f'--window-size={mobile_width},{mobile_height}')
            # Enable mobile emulation
            mobile_emulation = {
                "deviceMetrics": {"width": mobile_width, "height": mobile_height, "pixelRatio": 3.0},
                "userAgent": mobile_user_agent
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        
        driver = webdriver.Chrome(options=options)
        print("Using Chrome browser" + (" (Mobile mode)" if mobile_friendly else ""))
        
    except Exception as chrome_error:
        print(f"Chrome failed: {chrome_error}")
        try:
            # Fallback to Edge if Chrome fails
            options = webdriver.EdgeOptions()
            options.add_argument('--headless') 
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Add mobile-specific options for Edge
            if mobile_friendly:
                options.add_argument(f'--user-agent={mobile_user_agent}')
                options.add_argument(f'--window-size={mobile_width},{mobile_height}')
            
            # Specify Edge binary location if needed
            options.binary_location = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
            
            edge_service = EdgeService(executable_path='/Users/zyy/Applications/edgedriver_mac64_m1/msedgedriver')
            driver = webdriver.Edge(service=edge_service, options=options)
            print("Using Edge browser" + (" (Mobile mode)" if mobile_friendly else ""))
            
        except Exception as edge_error:
            print(f"Edge also failed: {edge_error}")
            print("Please install Chrome or Edge browser, or check your driver paths")
            return

    try:
        driver.get(html_path)
        
        # Set mobile viewport if mobile_friendly is enabled
        if mobile_friendly:
            driver.set_window_size(mobile_width, mobile_height)
            # Add viewport meta tag if it doesn't exist
            driver.execute_script("""
                if (!document.querySelector('meta[name="viewport"]')) {
                    var meta = document.createElement('meta');
                    meta.name = 'viewport';
                    meta.content = 'width=device-width, initial-scale=1.0';
                    document.getElementsByTagName('head')[0].appendChild(meta);
                }
            """)
        
        sections = driver.find_elements(By.XPATH, "//h3 | //h4")
        h3_height_list = []
        for section in sections:    
            # 使用JavaScript执行脚本来获取章节元素在网页中的位置信息
            location = driver.execute_script("return arguments[0].getBoundingClientRect();", section)
            h3_height_list.append((location['left'],location['top']))

        index = 0
        size = []
        
        if mobile_friendly:
            # Mobile approach: scroll and capture separate images
            total_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            window_height = mobile_height
            driver.set_window_size(mobile_width, window_height)
            
            # Take screenshots by scrolling
            offset = 0
            blog_index = 0
            
            while offset < total_height:
                # Scroll to position
                driver.execute_script(f"window.scrollTo(0, {offset});")
                time.sleep(0.2)  # Allow time for rendering
                
                # Take screenshot of current viewport
                screenshot_filename = f"blog{blog_index:02d}.png"
                driver.get_screenshot_as_file(osp.join(out_path, screenshot_filename))
                print(f"Saved {screenshot_filename}")
                
                # Prepare for next screenshot
                blog_index += 1
                offset += window_height
                
            # Also save full screenshot for section processing if needed
            driver.set_window_size(mobile_width, total_height)
            driver.execute_script(f"window.scrollTo(0, 0);")
            time.sleep(0.2)
            driver.get_screenshot_as_file(osp.join(out_path, "screenshot_mobile.png"))
            
        else:
            # Use original full-width approach for desktop
            scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
            scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
            driver.set_window_size(scroll_width, scroll_height)
            driver.get_screenshot_as_file(osp.join(out_path, "screenshot.png"))
        
        # Process section screenshots
        screenshot_filename = "screenshot_mobile.png" if mobile_friendly else "screenshot.png"
        
        for item in h3_height_list:
            if index > 0:
                screenshot = Image.open(osp.join(out_path, screenshot_filename))
                # 裁剪出感兴趣的位置
                cropped_image = screenshot.crop((0, int(size[1]), 
                                                scroll_width if not mobile_friendly else mobile_width, 
                                                int(item[1])))
                # 保存裁剪后的图片
                suffix = "_mobile" if mobile_friendly else ""
                cropped_image.save(osp.join(out_path, f"{index}{suffix}.png"))
            size = item
            index += 1
        driver.quit()
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--html_path', type=str, required=True)
    parser.add_argument('-o','--out_path', type=str, required=False)
    parser.add_argument('-m','--mobile_friendly', action='store_true', help='Take mobile-friendly screenshots')
    args = parser.parse_args()
    html_to_png(args.html_path, args.out_path, args.mobile_friendly)

if __name__ == '__main__':
    main()
