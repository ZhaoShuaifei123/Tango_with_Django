import json
import urllib.request
import urllib.parse


def read_webhose_key():
    """
    从search.key中获取webhoseAPI密钥
    """
    webhose_api_key =None

    try:
        with open('search.key','r') as f:
            webhose_api_key=f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key


def run_query(search_terms,size=10):
    """
    指定搜索词条和结果数量（默认为 10），把 Webhose API 返回的结果存入列表
    每个结果都有标题、链接地址和摘要
    """
    webhose_api_key=read_webhose_key()

    if not webhose_api_key:
        raise KeyError("webhose key not found")

    root_url='http://webhose.io/filterWebContent'

    query_str=urllib.parse.quote(search_terms)
    search_url=('{root_url}?token={key}&format=json&'
                '&sort=relevancy&q={query}&size={size}').format(
        root_url=root_url,
        key=webhose_api_key,
        query=query_str,
        size=size)

    #results是列表
    results=[]

    try:
        #向链接发送请求，并读取响应，读取内容用utf-8格式解码
        response=urllib.request.urlopen(search_url).read().decode('utf-8')

        #把json转成字典格式
        json_response=json.loads(response)

        for post in json_response['posts']:
            # results是列表
            results.append({
                'title':post['title'],
                'link':post['url'],
                'summary':post['text'][:200]
            })

    except:
        print('连接失败')

    return results


def main():
    print("qingshuru:")
    raw=input()
    result_list=[]
    result_list=run_query(raw)
    for result in result_list:
        print(result['title'])
        print(result['link'])
        print(result['summary'])



if __name__ == '__main__':
    main()





