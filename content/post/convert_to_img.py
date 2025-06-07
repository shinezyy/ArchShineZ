import os.path

from PIL import Image
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import argparse
import os.path as osp

def html_to_png(html_path, out_path): 
    if out_path is None:
        out_path = os.path.dirname(html_path)
    
    # Convert to absolute path and proper file URL
    html_path = os.path.abspath(html_path)
    if not html_path.startswith('file://'):
        html_path = 'file://' + html_path
    
    # Try Chrome first (more commonly available on macOS)
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # 不知为啥只能在无头模式执行才能截全屏
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')  # Add for better compatibility
        options.add_argument('--disable-dev-shm-usage')  # Add for better compatibility
        
        driver = webdriver.Chrome(options=options)
        print("Using Chrome browser")
        
    except Exception as chrome_error:
        print(f"Chrome failed: {chrome_error}")
        try:
            # Fallback to Edge if Chrome fails
            options = webdriver.EdgeOptions()
            options.add_argument('--headless') 
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Specify Edge binary location if needed
            options.binary_location = '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge'
            
            edge_service = EdgeService(executable_path='/Users/zyy/Applications/edgedriver_mac64_m1/msedgedriver')
            driver = webdriver.Edge(service=edge_service, options=options)
            print("Using Edge browser")
            
        except Exception as edge_error:
            print(f"Edge also failed: {edge_error}")
            print("Please install Chrome or Edge browser, or check your driver paths")
            return

    try:
        driver.get(html_path)
        sections = driver.find_elements(By.XPATH, "//h3 | //h4")
        h3_height_list = []
        for section in sections:    
            # 使用JavaScript执行脚本来获取章节元素在网页中的位置信息
            location = driver.execute_script("return arguments[0].getBoundingClientRect();", section)
            h3_height_list.append((location['left'],location['top']))

        index = 0
        size = []
        scroll_width = driver.execute_script('return document.body.parentNode.scrollWidth')
        scroll_height = driver.execute_script('return document.body.parentNode.scrollHeight')
        driver.set_window_size(scroll_width, scroll_height)
        driver.get_screenshot_as_file(osp.join(out_path, "screenshot.png"))
        for item in h3_height_list:
            if index > 0:
                screenshot = Image.open(osp.join(out_path, "screenshot.png"))
                # 裁剪出感兴趣的位置
                cropped_image = screenshot.crop((0, int(size[1]), scroll_width, int(item[1])))
                # 保存裁剪后的图片
                cropped_image.save(osp.join(out_path, "%d.png" % index))
            size = item
            index += 1
        driver.quit()
    except Exception as e:
        print(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--html_path', type=str, required=True)
    parser.add_argument('-o','--out_path', type=str, required=False)
    args = parser.parse_args()
    html_to_png(args.html_path, args.out_path)

if __name__ == '__main__':
    main()
