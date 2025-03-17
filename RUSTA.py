import pandas as pd
import requests
import time
import os
import random
import json

def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36"
    ]
    return random.choice(user_agents)

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

def save_data_to_excel(data, file_path):
    df = pd.DataFrame(data, columns=[
        'original_tcin', 'specifications', 'title', 'Currency', 'current_retail',
        'reg_retail', 'average', 'count', 'item_type_name','item_type', 
        'standard_sales_start_time', 'canonical_url', 'primary_brand_name','is_bestseller',
        'is_new','is_exclusive', 'primary_image', 'alternate_image', 'data_source'
    ])
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(file_path, index=False)
    print(f"数据已保存到 {file_path}")

def getAllInfo(productInfoList, image_save_dir):
    count_num = 0                                                                                   #计数器，用于打印进度
    batch_count = 0                                                                                 #批量计数器，保存数据
    batch_data = []                                                                                 #存储当前批次的数据

    start_time = time.time()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # image_save_directory = os.path.join(current_dir, "images_TARGET")
    data_file_path = os.path.join(current_dir, "productInfo_RUSTA.xlsx")
    # links_file_path = os.path.join(current_dir, "links.xlsx")


    for result in productInfoList:
        try:
            # original_tcin
            original_tcin = result['code']                                                 #产品货号
            print(original_tcin)

            # item.product_description
            title = result['subTitle']                                                      #产品关键特性/亮点

            specifications = title.split("cm")[0]+"cm" if "cm" in title else ''             #产品规格

            Currency = "SEK"                                                                        #货币单位

            #当前零售价格
            current_retail = result['price']['current']['inclVat']

            reg_retail = result['price']['original']['inclVat']                                              #常规零售价格

            # ratings_and_reviews
            average = ''
            
            count = ''

            item_type_name = result['displayName']                       #产品类型名称

            item_type = result['category']                            #产品类型编号
            
            # item.eligibility_rules
            standard_sales_start_time = ''                       

            canonical_url = 'https://www.rusta.com' + result['url']          #规范url

            primary_brand_name = item_type_name                                         #品牌名称

            is_bestseller = ''

            # item.ribbons
            is_new = result['isNew']                        #是否为新售卖产品

            is_exclusive = result['campaignLabel']['text'] if result['campaignLabel'] is not None else ''                                                     #是否为独家产品

            primary_image_url = 'https://www.rusta.com' + result['images'][0]['url']                      #主图
            # 获取商品图
            primary_image = original_tcin + ".jpg"  # 构建文件名
            download_image(primary_image_url, image_save_dir, primary_image)

            alternate_image = ''

            data_source = "RUSTA"                                                                  #数据来源

            data_tuple = (original_tcin, specifications, title, Currency, current_retail,
                    reg_retail, average, count, item_type_name,item_type, 
                    standard_sales_start_time, canonical_url, primary_brand_name,is_bestseller,
                    is_new, is_exclusive,primary_image, alternate_image, data_source)
            batch_data.append(data_tuple)

            count_num += 1
            batch_count += 1
            if count_num % 20 == 0:
                print(f"已抓取 {count_num} 条数据")
            if batch_count % 20 == 0:
                save_data_to_excel(batch_data, data_file_path)  # 每抓取一百条数据保存一次
                batch_data = []  # 清空当前批次的数据
                print(f"已将{batch_count}条数据保存到数据表中")
            if count_num % 50 == 0:
                print("已抓取50条数据，等待3s...")
                time.sleep(3)
            
        except Exception as e:
                    print(f"处理产品 {canonical_url} 时发生错误: {e}")
                    continue
    # 保存剩余的数据
    if batch_data:
        save_data_to_excel(batch_data, data_file_path)
        print("已保存剩余数据")

    print(f"共抓取 {count_num} 条数据")

    # 记录结束时间
    end_time = time.time()

    # 计算并打印运行时间
    elapsed_time = end_time - start_time
    print(f"代码运行时间为: {elapsed_time:.2f} 秒")

for i in range(3):
    cookies = {
        'EPiServer_Commerce_AnonymousId': '2e96506d-7b30-4a74-8a23-5bc3b445ad32',
        'ai_user': 'gOAGh|2024-12-24T01:16:10.327Z',
        '_ga': 'GA1.1.807401865.1735177688',
        '_gcl_au': '1.1.904424794.1735177688',
        '_va': 'VA632.993694211',
        '_fbp': 'fb.1.1735177688850.552344563118744387',
        '_tt_enable_cookie': '1',
        '_ttp': 'UiDdyLtiIn7URzyu5yfrW4RblBF.tt.1',
        '_hjSessionUser_127933': 'eyJpZCI6ImE2ZWI2NjM5LTlkOTctNWZhNi04YjM4LWEyMzZlMzVkZDEzNyIsImNyZWF0ZWQiOjE3MzUxNzc2ODkwODIsImV4aXN0aW5nIjp0cnVlfQ==',
        'OptanonAlertBoxClosed': '2024-12-26T03:07:30.839Z',
        '_clck': 'hin4z9%7C2%7Cftr%7C0%7C1821',
        'Culture': 'sv-SE',
        'EPiStateMarker': 'true',
        'ARRAffinity': '780bb34fe11d9d1cdcd8ed2fd260f18264aaf54661274da18bc24dcae4afa00f',
        'ARRAffinitySameSite': '780bb34fe11d9d1cdcd8ed2fd260f18264aaf54661274da18bc24dcae4afa00f',
        'ContentIndexSessionId': '4de8b2ce506840df9fbfb59731b83c88',
        'breakpoint': '6',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Wed+Feb+26+2025+18%3A22%3A36+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.37.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=%3B',
        '_uetsid': 'ad2bd440f34d11ef9690d79701d08879',
        '_uetvid': '74f7f030c32b11efb7dfff6ecab3cdd7',
        '_clsk': '18fy2oo%7C1740565373106%7C4%7C0%7Co.clarity.ms%2Fcollect',
        'ai_session': '0BFW9|1740564804693.7|1740565502211.4',
        '_ga_8EL6FFDXHZ': 'GS1.1.1740565356.14.0.1740565510.60.0.1178010302',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/json',
        'priority': 'u=1, i',
        'referer': 'https://www.rusta.com/sv-se/hem-och-inredning/dekoration/konstvaxter?page=2',
        'request-context': 'appId=cid-v1:9de4a2da-fcfd-4ca7-bb73-faa6f79cc17a',
        'request-id': '|3854eeee0685418ca3cf8647c5cbb3dd.f2aee60c13394499',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'x-client-version': '5.0.24',
        'x-requested-with': 'XMLHttpRequest',
        # 'cookie': 'EPiServer_Commerce_AnonymousId=2e96506d-7b30-4a74-8a23-5bc3b445ad32; ai_user=gOAGh|2024-12-24T01:16:10.327Z; _ga=GA1.1.807401865.1735177688; _gcl_au=1.1.904424794.1735177688; _va=VA632.993694211; _fbp=fb.1.1735177688850.552344563118744387; _tt_enable_cookie=1; _ttp=UiDdyLtiIn7URzyu5yfrW4RblBF.tt.1; _hjSessionUser_127933=eyJpZCI6ImE2ZWI2NjM5LTlkOTctNWZhNi04YjM4LWEyMzZlMzVkZDEzNyIsImNyZWF0ZWQiOjE3MzUxNzc2ODkwODIsImV4aXN0aW5nIjp0cnVlfQ==; OptanonAlertBoxClosed=2024-12-26T03:07:30.839Z; _clck=hin4z9%7C2%7Cftr%7C0%7C1821; Culture=sv-SE; EPiStateMarker=true; ARRAffinity=780bb34fe11d9d1cdcd8ed2fd260f18264aaf54661274da18bc24dcae4afa00f; ARRAffinitySameSite=780bb34fe11d9d1cdcd8ed2fd260f18264aaf54661274da18bc24dcae4afa00f; ContentIndexSessionId=4de8b2ce506840df9fbfb59731b83c88; breakpoint=6; OptanonConsent=isGpcEnabled=0&datestamp=Wed+Feb+26+2025+18%3A22%3A36+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=6.37.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=%3B; _uetsid=ad2bd440f34d11ef9690d79701d08879; _uetvid=74f7f030c32b11efb7dfff6ecab3cdd7; _clsk=18fy2oo%7C1740565373106%7C4%7C0%7Co.clarity.ms%2Fcollect; ai_session=0BFW9|1740564804693.7|1740565502211.4; _ga_8EL6FFDXHZ=GS1.1.1740565356.14.0.1740565510.60.0.1178010302',
    }

    params = {
        'page': str(i+1),
        'loadMore': 'true',
    }

    response = requests.get(
        'https://www.rusta.com/sv-se/hem-och-inredning/dekoration/konstvaxter',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    # print(response.json())

    results_json = response.json()

    current_dir = os.getcwd()
    image_save_directory = os.path.join(current_dir, "RUSTA")

    getAllInfo(results_json,image_save_directory)


