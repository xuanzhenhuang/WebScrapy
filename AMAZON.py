from DrissionPage import ChromiumPage, ChromiumOptions
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import os
import time
import random


def scrollDown(driver, times):
    '''
    在浏览器中向下滑动
    :param driver:浏览器的驱动对象
    :param times:滑动的次数
    :return:无
    '''
    driver.scroll(5000)
    time.sleep(1)
    for i in range(times):
        time.sleep(1)
        # 用JavaScript进行滑动
        driver.scroll(5000)


def clickLoadButton(driver):
    '''
    点击加载更多内容控件，如果控件不存在则不进行点击
    :param driver: chrome 浏览器的驱动对象
    :return: 无
    '''
    try:
        loadButton = driver.ele('.a-last')

        # 检查加载按钮是否可点击
        if loadButton:
            # 使用 JavaScript 点击按钮，以避免某些情况下元素不可点击的问题
            loadButton.click()
            print("已加载更多内容")
        else:
            print("加载按钮存在但不可点击")

    except Exception as e:
        # 如果在规定时间内没有找到加载按钮或者元素不存在
        print(f"已没有更多内容: {e}")
        return  # 停止进一步操作


# 提取所有商品链接
def getAllProductlink(tab):
    allproduct = tab.eles('.a-column a-span12 a-text-center _cDEzb_grid-column_2hIsc')
    print(len(allproduct))
    for product in allproduct:
        try:
            product_link = product.ele('.a-link-normal aok-block').attr('href')
            if product_link:
                print(f"{product_link}")
                all_product_links.append(product_link)
        except Exception as e:
            print(f"提取商品链接时出错: {e}")
            continue
    print(f"共找到 {len(all_product_links)} 个商品链接")


def download_image(img_url, save_dir, Filename):
    """
    下载图片并保存到本地
    :param img_url: 图片的URL
    :param save_dir: 保存图片的目录
    :param Filename: 文件名（包括扩展名）
    :return: 图片保存路径或None（如果下载失败）
    """
    try:
        # 确保保存图片的目录存在
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            filepath = os.path.join(save_dir, Filename)
            with open(filepath, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"图片已成功保存为 {filepath}")
            return filepath
        else:
            print("无法下载图片，状态码:", response.status_code)
            return None
    except Exception as e:
        print(f"下载图片时发生错误: {e}")
        return None



# 定义抓取函数，处理一组商品链接
def fetch_data_group(url_group, image_save_dir):
    product_info_list = []
    tab = browser.new_tab()
    for url in url_group:
        try:
            tab.get(url)
            # 等待页面加载开始
            # tab.wait.load_start()
            time.sleep(1.5)

            # 获取产品上架时间
            standard_sales_start_time = tab.ele('@data-19ax5a9jf=dingo').attr('data-aui-build-date').split("-", 1)[1]

            product = tab.ele('.a-container')

            # 提取产品货号
            original_tcin = product.ele('#ASIN').attr('value')

            # 获取产品描述
            title = product.ele('.a-size-large product-title-word-break').text

            # 获取到规格备注

            specifications = product.ele('.a-spacing-small po-item_depth_width_height')
            if specifications:
                specifications = specifications.ele('.a-size-base po-break-word').text
            elif product.ele('tag:th@text(): Package Dimensions '):
                specifications = product.ele('tag:th@text(): Package Dimensions ').next().text
            elif product.ele('tag:th@text(): Product Dimensions '):
                specifications = product.ele('tag:th@text(): Product Dimensions ').next().text
            elif product.ele('.a-size-base prodDetAttrValue'):
                specifications = product.ele('.a-size-base prodDetAttrValue').text
            else:
                specifications = ''

            # 获取到币种
            Currency = "USD"

            # 获取到完整的价格信息
            PriceWhole = tab.ele('.a-price-whole')
            PriceFraction = tab.ele('.a-price-fraction')
            # 获取到价格
            current_retail = PriceWhole.text + '.' + PriceFraction.text if PriceWhole and PriceFraction else PriceWhole.text if PriceWhole else ''

            # 获取到原先价格信息
            reg_Text = product.ele('.a-size-small aok-offscreen')
            reg_retail = reg_Text.text.split('$')[1] if reg_Text and ('price' or 'Price') in reg_Text.text else ''

            # 获取到评价人数
            RatingCount = tab.ele('#acrCustomerReviewText')
            count = RatingCount.text.split()[0].replace(',', '') if RatingCount else '' 

            # 获取到平均评价分数
            Rating = tab.ele('#averageCustomerReviews')
            average = Rating.ele('tag:span@class=a-size-base a-color-base').text if Rating else ''

            # 获取产品种类
            item_type_names = product.ele('.a-spacing-small po-brand')
            if item_type_names:
                item_type_name = item_type_names.ele('.a-size-base po-break-word').text
            else:
                item_type_name = ''

            # 获取产品种类编号
            item_types = product.ele('.a-spacing-small po-plant_or_animal_product_type')
            if item_types:
                item_type = item_types.ele('.a-size-base po-break-word').text
            else:
                item_type = ''

            # 获取产品标准url
            canonical_url = url

            # 获取品牌名称
            primary_brand_name = item_type_name

            # 初始化变量
            is_bestseller = ''
            is_new = ''
            is_exclusive = ''

            # 获取商品图
            img_element = product.eles('xpath://li[@class="a-spacing-small item imageThumbnail a-declarative"]')[0].ele(
            'xpath://img')
            img_url = img_element.attr('src')
            primary_image = original_tcin + ".jpg"  # 构建文件名
            download_image(img_url, image_save_dir, primary_image)

            # 获取场景图
            if len(product.eles('xpath://li[@class="a-spacing-small item imageThumbnail a-declarative"]')) < 2:
                alternate_image = ''
            else:
                img_element_S = product.eles('xpath://li[@class="a-spacing-small item imageThumbnail a-declarative"]')[1].ele(
            'xpath://img')
                img_url_S = img_element_S.attr('src')
                alternate_image = original_tcin + "Scene.jpg"  # 构建文件名
                download_image(img_url_S, image_save_dir, alternate_image)

            # 产品来源
            data_source = 'AMAZON'

            product_info = {
                'original_tcin': original_tcin,
                'specifications': specifications,
                'title': title,
                'Currency': Currency,
                'current_retail': current_retail,
                'reg_retail': reg_retail,
                'average': average,
                'count': count,
                'item_type_name': item_type_name,
                'item_type': item_type,
                'standard_sales_start_time': standard_sales_start_time,
                'canonical_url': canonical_url,
                'primary_brand_name': primary_brand_name,
                'is_bestseller': is_bestseller,
                'is_new': is_new,
                'is_exclusive': is_exclusive,
                'primary_image': primary_image,
                'alternate_image': alternate_image,
                'data_source': data_source
            }
            product_info_list.append(product_info)
        except Exception as e:
            print(f"处理产品 {url} 时发生错误: {e}")
            # 尝试刷新页面并重试
            print("尝试刷新页面并重试...")
            tab.refresh()
            time.sleep(random.uniform(1.5, 2.5))
            continue
        # except Exception as e:
        #     print(f"抓取 {url} 时发生错误: {e}")
            # product_info_list.append({'URL': url, 'original_tcin': f"Error: {str(e)}", 'specifications': "N/A",
            #                           'title': "N/A", 'Currency': "N/A", 'current_retail': "N/A", 'reg_retail': "N/A",
            #                           'average': "N/A", 'count': "N/A", 'item_type_name': "N/A", 'item_type': "N/A",
            #                           'standard_sales_start_time': "N/A", 'canonical_url': "N/A",
            #                           'primary_brand_name': "N/A", 'is_bestseller': "N/A", 'is_new': "N/A",
            #                           'is_exclusive': "N/A", 'primary_image': "N/A", 'alternate_image': "N/A",
            #                           'data_source': "N/A"})
    tab.close()  # 一组链接处理完后关闭标签页
    return product_info_list

# 记录开始时间
start_time = time.time()

# 定义要抓取的网页列表
detail_links_all = ["https://www.amazon.com/gp/bestsellers/home-garden/17833726011/ref=pd_zg_hrsr_home-garden"]

co = ChromiumOptions().set_paths(browser_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
# 新建页面对象
browser = ChromiumPage(co)
tab = browser.new_tab()
tab.get(detail_links_all[0])
current_dir = os.path.dirname(os.path.abspath(__file__))
image_save_directory = os.path.join(current_dir, "AMAZON")
data_file_path = os.path.join(current_dir, "productInfo_AMAZON.xlsx")

all_product_links = []
scrollDown(tab, 3)
time.sleep(1)
getAllProductlink(tab)
clickLoadButton(tab)
time.sleep(1)
scrollDown(tab, 3)
getAllProductlink(tab)
tab.close()



# 将商品链接列表切分成10份
num_chunks = 5
chunk_size = len(all_product_links) // num_chunks
if chunk_size == 0:
    link_chunks = [[link] for link in all_product_links]
else:
    link_chunks = [all_product_links[i:i + chunk_size] for i in range(0, len(all_product_links), chunk_size)]

# 使用 ThreadPoolExecutor 进行多线程抓取
all_results = []
with ThreadPoolExecutor() as executor:
    # 提交任务到线程池
    results = executor.map(fetch_data_group, link_chunks, [image_save_directory] * len(link_chunks))
    for result_list in results:
        all_results.extend(result_list)

if os.path.exists(data_file_path):
    os.remove(data_file_path)
# 将结果保存到 Excel 文件中
df = pd.DataFrame(all_results)
df.to_excel(data_file_path, index=False)

print("数据已成功保存到 productInfo_AMAZON.xlsx 文件中。")

# 记录结束时间
end_time = time.time()

# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"代码运行时间为: {elapsed_time:.2f} 秒")