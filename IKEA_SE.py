from DrissionPage import ChromiumPage, ChromiumOptions
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import requests
import os
import time

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

# 记录结束时间
start_time = time.time()

# 定义要抓取的网页列表
detail_links_all = ["https://www.ikea.com/se/sv/cat/konstgjorda-vaexter-plastblommor-20492/",
                    "https://www.ikea.com/se/sv/cat/konstgjorda-vaexter-plastblommor-20492/?page=2",
                    "https://www.ikea.com/se/sv/cat/konstgjorda-vaexter-plastblommor-20492/?page=3",
                    "https://www.ikea.com/se/sv/cat/konstgjorda-vaexter-plastblommor-20492/?page=4"
                    ]

co = ChromiumOptions().set_paths(browser_path=r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
# 新建页面对象
browser = ChromiumPage(co)
current_dir = os.path.dirname(os.path.abspath(__file__))
image_save_directory = os.path.join(current_dir, "images_IKEA_SE")
data_file_path = os.path.join(current_dir, "productInfo_IKEA_SE.xlsx")

# 定义抓取函数
def fetch_data(url, image_save_dir):
    try:
        tab = browser.new_tab()
        tab.get(url)
        product_info_list = []
        for product in tab.eles('.plp-fragment-wrapper'):
            try:
                # 提取产品货号
                original_tcin = product.ele('tag:div@data-testid=plp-product-card').attr('data-product-number')

                # 获取产品描述
                title = product.ele('.plp-price-module__description').text
                # 获取到规格备注
                if len(title) > 0:
                    specifications = title.split(', ')[1] if len(title.split(', ')) > 1 else ''
                else:
                    specifications = ''

                # 获取到币种
                Currency = "SEK"

                # 获取到完整的价格信息
                current_retailText = product.eles('.plp-price__sr-text')
                if len(current_retailText) == 1:
                    delimiter1 = "/"
                    delimiter2 = " "
                    delimiter3 = ":-"
                    Result = current_retailText[0].text.split(delimiter1)
                    # 获取到价格
                    current_retail = Result[0].split(delimiter2)[1].split(delimiter3)[0]
                    reg_retail = ''
                    print(current_retail, reg_retail)
                elif len(current_retailText) == 2:
                    delimiter1 = "/"
                    delimiter2 = " "
                    delimiter3 = ":-"
                    Result = current_retailText[0].text.split(delimiter1)
                    # 获取到价格
                    current_retail = Result[0].split(delimiter2)[1].split(delimiter3)[0]

                    Result = current_retailText[1].text.split(delimiter1)
                    # 获取到价格
                    reg_retail = Result[0].split(delimiter2)[3].split(delimiter3)[0]
                    print(current_retail, reg_retail)

                # 获取产品平均得分
                review_info = product.ele('.plp-ratings plp-ratings--small plp-ratings--product-card notranslate')
                if review_info:
                    delimiter1 = "Recensera: "
                    delimiter2 = " utav 5 stjärnor. Totalt antal recensioner: "
                    average = review_info.attr('aria-label').split(delimiter1)[1].split(delimiter2)[0]
                    count = review_info.attr('aria-label').split(delimiter2)[1]
                else:
                    average = ''
                    count = ''
                
                # 获取产品种类
                item_type_name = product.ele('.notranslate plp-price-module__product-name').text

                # 获取产品种类编号
                item_type = product.ele('.notranslate plp-price-module__product-name').text

                # 获取产品上架时间
                standard_sales_start_time = ''

                # 获取产品标准url
                canonical_url = product.ele('. plp-price-link-wrapper  link').attr('href')

                # 获取品牌名称
                primary_brand_name = product.ele('.notranslate plp-price-module__product-name').text

                # 缓存热销产品元素查找结果
                bestseller_ele = product.ele('.plp-product-badge plp-product-badge--top-seller')
                is_bestseller = bestseller_ele.text if bestseller_ele else ''

                # 缓存新品元素查找结果
                new_ele = product.ele('.plp-commercial-message__title')
                is_new = new_ele.text if new_ele else ''

                # 是否为独家产品
                is_exclusive = ''

                # 获取商品图
                img_element = product.ele('.plp-image plp-product__image')
                img_url = img_element.attr('src')
                primary_image = original_tcin + ".jpg"  # 构建文件名
                download_image(img_url, image_save_dir, primary_image)

                # 获取场景图
                img_element_S = product.ele('.image plp-product__image plp-product__image--alt')
                img_url_S = img_element_S.attr('src')
                alternate_image = original_tcin + "Scene.jpg"  # 构建文件名
                download_image(img_url_S, image_save_dir, alternate_image)

                # 产品来源
                data_source = 'IKEA_SE'

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
                continue
        tab.close()  # 关闭当前标签页
        return product_info_list
    except Exception as e:
        print(f"抓取 {url} 时发生错误: {e}")
        return [{'URL': url, 'original_tcin': f"Error: {str(e)}", 'specifications': "N/A",
                 'title': "N/A", 'Currency': "N/A", 'current_retail': "N/A", 'reg_retail': "N/A",
                 'average': "N/A", 'count': "N/A", 'item_type_name': "N/A", 'item_type': "N/A",
                 'standard_sales_start_time': "N/A", 'canonical_url': "N/A",
                 'primary_brand_name': "N/A", 'is_bestseller': "N/A", 'is_new': "N/A",
                 'is_exclusive': "N/A", 'primary_image': "N/A", 'alternate_image': "N/A",
                 'data_source': "N/A"}]

# 使用 ThreadPoolExecutor 进行多线程抓取
all_results = []
with ThreadPoolExecutor() as executor:
    # 提交任务到线程池
    results = executor.map(fetch_data, detail_links_all, [image_save_directory] * len(detail_links_all))
    for result_list in results:
        all_results.extend(result_list)

if os.path.exists(data_file_path):
    os.remove(data_file_path)
# 将结果保存到 Excel 文件中
df = pd.DataFrame(all_results)
df.to_excel(data_file_path, index=False)

print("数据已成功保存到 productInfo_IKEA_SE.xlsx 文件中。")

# 记录结束时间
end_time = time.time()

# 计算并打印运行时间
elapsed_time = end_time - start_time
print(f"代码运行时间为: {elapsed_time:.2f} 秒")