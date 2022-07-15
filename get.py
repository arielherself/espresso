import requests
import datetime

def get(proxy=False, http_proxy='', https_proxy=''):
    try:
        if proxy:
            raw = requests.get('https://www.economist.com/the-world-in-brief', proxies={'http': http_proxy, 'https': https_proxy})
        else:
            raw = requests.get('https://www.economist.com/the-world-in-brief')
    except:
        return None #####################################
    content = raw.text
    pre = []
    details = []
    titles = []
    '''pre-content'''
    slice = content[:content.find('<h3')]
    while slice.find('<p>') != -1:
        pre.append(slice[slice.find('<p>')+3:slice.find('</p>')])
        slice = slice[slice.find('</p>')+4:]
    # print(pre)
    while content.find('<h3') != -1:
        content = content[content.find('<h3')+3:]
        content = content[content.find('>')+1:]
        titles.append(content[:content.find('</h3>')])
        content = content[content.find('</h3>')+5:]
        # print(content[content.find('<p>')+3:])
        part = content[:content[content.find('<p>')+3:].find('</div>')+content.find('<p>')+3]
        # print(part)
        ps = []
        while part.find('<p>') != -1:
            ps.append(part[part.find('<p>')+3:part.find('</p')])
            part = part[part.find('</p>')+4:]
            content = content[content.find('</p>')+4:]
        details.append(ps)
    # while content.find('<p>') != -1:

    # print(titles, details)
    # print(len(titles), len(details))
    return pre, titles, details

def web_process(**kwargs):
    pre, titles, details = get(**kwargs)
    mdlines = []
    mdlines.append('[English](https://github.com/arielherself/espresso/blob/main/README.md)|[中文](https://github-com.translate.goog/arielherself/espresso/blob/main/README.md?_x_tr_sl=en&_x_tr_tl=zh-CN&_x_tr_hl=zh-CN&_x_tr_pto=wapp)')
    mdlines.append('<div align="center"><img src="https://cdn.static-economist.com/sites/all/themes/econfinal/images/svg/logo.svg" align-center /></div>')
    mdlines.append(f'# <p align="center">The world in brief {str(datetime.date.today())}</p>')
    mdlines.append('## <p align="center">Catch up quickly on the global stories that matter</p>')
    mdlines.append('<p align="center">Origin: <a href="https://www.economist.com/the-world-in-brief">https://www.economist.com/the-world-in-brief</a><hr>')
    for each in pre:
        if each == '':
            continue
        processed_detail = each
        while processed_detail.find('<strong>') != -1:
            if processed_detail[processed_detail.find('<strong>')-1] == ' ':
                if processed_detail[processed_detail.find('<strong>')+8] == ' ':
                    processed_detail = processed_detail[:processed_detail.find('<strong>')]+'**'+processed_detail[processed_detail.find('<strong>')+9:]
                else:
                    processed_detail = processed_detail[:processed_detail.find('<strong>')]+'**'+processed_detail[processed_detail.find('<strong>')+8:]
            else:
                if processed_detail[processed_detail.find('<strong>')+8] == ' ':
                    processed_detail = processed_detail[:processed_detail.find('<strong>')]+' **'+processed_detail[processed_detail.find('<strong>')+9:]
                else:
                    processed_detail = processed_detail[:processed_detail.find('<strong>')]+' **'+processed_detail[processed_detail.find('<strong>')+8:]
        while processed_detail.find('</strong') != -1:
            if processed_detail[processed_detail.find('</strong>')+9] == ' ':
                if processed_detail[processed_detail.find('</strong>')-1] == ' ':
                    processed_detail = processed_detail[:processed_detail.find('</strong>')-1]+'**'+processed_detail[processed_detail.find('</strong>')+9:]
                else:
                    processed_detail = processed_detail[:processed_detail.find('</strong>')]+'**'+processed_detail[processed_detail.find('</strong>')+9:]
            else:
                if processed_detail[processed_detail.find('</strong>')-1] == ' ':
                    processed_detail = processed_detail[:processed_detail.find('</strong>')-1]+'** '+processed_detail[processed_detail.find('</strong>')+9:]
                else:
                    processed_detail = processed_detail[:processed_detail.find('</strong>')]+'** '+processed_detail[processed_detail.find('</strong>')+9:]
        while processed_detail.find('<a ') != -1:
            # print(len(processed_detail))
            # print(processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6)
            # print(processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1)
            # print(processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="'):].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1])
            # processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1]
            # exit(0)
            hyperlink = processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6]
            if hyperlink.startswith('//'):
                hyperlink = 'https:' + hyperlink
            elif hyperlink.startswith('/'):
                hyperlink = 'https://www.economist.com' + hyperlink
            processed_detail = processed_detail[:processed_detail.find('<a ')]+f'[{processed_detail[processed_detail[processed_detail.find("<a "):].find(">")+processed_detail.find("<a ")+1:processed_detail[processed_detail.find("<a ")+1:].find("</a>")+processed_detail.find("<a ")+1]}]('+hyperlink+')'+processed_detail[processed_detail.find('</a>')+4:]
            # print(processed_detail)
        while processed_detail.find('<br/>') != -1:
            processed_detail = processed_detail[:processed_detail.find('<br/>')]+'\n'+processed_detail[processed_detail.find('<br/>')+5:]
        mdlines.append(processed_detail)
    mdlines.append('----------')
    for i in range(len(titles)):
        mdlines.append(f'## {titles[i]}')
        for j in range(len(details[i])):
            processed_detail = details[i][j]
            while processed_detail.find('<strong>') != -1:
                if processed_detail[processed_detail.find('<strong>')-1] == ' ':
                    if processed_detail[processed_detail.find('<strong>')+8] == ' ':
                        processed_detail = processed_detail[:processed_detail.find('<strong>')]+'**'+processed_detail[processed_detail.find('<strong>')+9:]
                    else:
                        processed_detail = processed_detail[:processed_detail.find('<strong>')]+'**'+processed_detail[processed_detail.find('<strong>')+8:]
                else:
                    if processed_detail[processed_detail.find('<strong>')-1] == ' ':
                        processed_detail = processed_detail[:processed_detail.find('<strong>')]+' **'+processed_detail[processed_detail.find('<strong>')+9:]
                    else:
                        processed_detail = processed_detail[:processed_detail.find('<strong>')]+' **'+processed_detail[processed_detail.find('<strong>')+8:]
            while processed_detail.find('</strong') != -1:
                if processed_detail[processed_detail.find('</strong>')+9] == ' ':
                    if processed_detail[processed_detail.find('</strong>')-1] == ' ':
                        processed_detail = processed_detail[:processed_detail.find('</strong>')-1]+'**'+processed_detail[processed_detail.find('</strong>')+9:]
                    else:
                        processed_detail = processed_detail[:processed_detail.find('</strong>')]+'**'+processed_detail[processed_detail.find('</strong>')+9:]
                else:
                    if processed_detail[processed_detail.find('</strong>')-1] == ' ':
                        processed_detail = processed_detail[:processed_detail.find('</strong>')-1]+'** '+processed_detail[processed_detail.find('</strong>')+9:]
                    else:
                        processed_detail = processed_detail[:processed_detail.find('</strong>')]+'** '+processed_detail[processed_detail.find('</strong>')+9:]
            while processed_detail.find('<a ') != -1:
                # print(len(processed_detail))
                # print(processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6)
                # print(processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1)
                # print(processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="'):].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1])
                # processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+1]
                # exit(0)
                hyperlink = processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:processed_detail[processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6:].find('"')+processed_detail[processed_detail.find("<a "):].find('href="')+processed_detail.find("<a ")+6]
                if hyperlink.startswith('//'):
                    hyperlink = 'https:' + hyperlink
                elif hyperlink.startswith('/'):
                    hyperlink = 'https://www.economist.com' + hyperlink
                processed_detail = processed_detail[:processed_detail.find('<a ')]+f'[{processed_detail[processed_detail[processed_detail.find("<a "):].find(">")+processed_detail.find("<a ")+1:processed_detail[processed_detail.find("<a ")+1:].find("</a>")+processed_detail.find("<a ")+1]}]('+hyperlink+')'+processed_detail[processed_detail.find('</a>')+4:]
                # print(processed_detail)
            while processed_detail.find('<br/>') != -1:
                processed_detail = processed_detail[:processed_detail.find('<br/>')]+'\n'+processed_detail[processed_detail.find('<br/>')+5:]
            mdlines.append(processed_detail)
    mdlines.append('----------')
    mdlines.append("*Owing to the difference between time zones of servers in which our auto-update script is running, content above probably doesn't match the one in your region.*")
    return mdlines

if __name__ == '__main__':
    page = web_process(proxy=False)
    with open('README.md', 'w', encoding='utf8') as fil:
        print(*page, sep='\n\n', file=fil)
