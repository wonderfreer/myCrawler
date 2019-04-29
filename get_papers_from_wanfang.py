#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/5 20:31
# @Author  : WangFei
# @Des     : 
import json
import codecs
import re
import requests


def filter_html(content):
    content = re.sub(r'<.+?>', "", content)
    out = re.sub(r'^ +', "", content)
    return out


def filter_meta(meta):
    new_meta = []
    for content in meta:
        new_content = re.sub(r'\u000a', "", content)
        new_meta.append(new_content)
    return new_meta


headers = {
    'Host': 'www.wanfangdata.com.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'firstvisit_backurl=http%3A//www.wanfangdata.com.cn; CASTGC=TGT-5401124-4OsaaDvjbpWpydiagruofM9dTI62zNgvKwCKeuQlF5EbFtIzy6-my.wanfangdata.com.cn; JSESSIONID=EC2EBC2922498D656E5A8CDEAC7922C7; zh_choose=n; Hm_lvt_838fbc4154ad87515435bf1e10023fab=1540261993,1540355606,1540361283,1540447526; Hm_lpvt_838fbc4154ad87515435bf1e10023fab=1540447530; SEARCHHISTORY_0=UEsDBBQACAgIAGx4WU0AAAAAAAAAAAAAAAABAAAAMO2b%2FU%2FbRhjH%2F5UpkqtNC2Dfi31GQpMDScl4%0AaRNeSlknZBITAokTYocQpkpsWlvarWurtWtZ0daiMsZG22ndVkrb9Y8ZDuG%2F2Nm8tIHYhZaGkpgf%0A4sfne%2BzjuY%2B%2F9%2Bb77AuPLg8mlE45qXga1Wwi4fXEo55GT1cg3X%2BqPRMQsejxerKakglGtzJoipyJ%0ADHfn09SFoxczCerQsJEaVrRsQm%2BIKboUHZfViBLtstLro6lPdOrRlBtKZwcTcW24Lq1k4qkBOaPH%0AI3LCG1ViGUWp2zhsp0ZS6pCSUeh96kxzOz0t64qq120cBpSEkqRHr6bLalTORLW6bcurK1uFqjPN%0AgYxlexNKLK4lZD2eUrW6V08sh62s6VRG98bkSUXXFSUzoCq5uu0zzTw9pukZWoZYvmn1%2BWxx6pxx%0A%2Bcbq88uNH57xGN%2FeXF1ZKk7%2Ftra4Qn%2BNe4vGvQXj%2Fi9nPB%2FRgCoTaVoQjT6Qhm5%2FrroVd09h9mdj%0A%2BtJ%2FU1%2FSC9SPGqvPfiw%2BeGAay98b04vUKNy5YFw4T421hWuFS1OF6auFn2bN9Ec3igtfv0y%2FNG9c%0As241%2B0fhhyfGi5v0MWo2GUhlVVrpHIA8T%2Bs5klHov9odN0nhMGIRZkXEUUDOeu0oag1ODHahjgkI%0AkEvRm1O0T3IOlRaEIOaF3bRAHgACIMD2tKh8dwjn082ICC4tLi08QITY0xLvO06GBidPQw7XFi1H%0Auc0pbVhYXuBwmcpnWZ4FkOPtKz%2FqH5toE9CngsBXpPJfifny0%2FW5W%2FuN9h6dSuJcEiuIkLg7UkAE%0AhOcEQbCP1ERangyOirwocgcbqbKvw%2BGxuYFkKV%2BEh2XwAiJLABJFYB%2B0dCjd2ZI%2FFcSwMtpy2K90%0ASdgElkNluns0bAIWMXR4K0db0lktFgCYZWtLkt1Bw65BAyuwAixLEYQCZjl7inp9JyZxqL0Nkcpo%0Au0vR0aOIIIRp99Ch3fPjdgXkesZ57GqRS5ENRZD2iigg9hTJwWy30DWikQPuPFUrRGtLS6vLUxs8%0AmCQUpqaKL26vP7lShprX5K04JjxfDhHAIcgSh%2BYK6WJf7%2FHT4wIGVclIDcjJ26kIFRAe09p3GK2O%0A%2BUZQMNwsEugiUqOIQEhr3x6RLDcUbW1rUwCszvWWN0WkYrMt7xALSCApBwXCmKP1bQ9FT1gNasm0%0ARtugvUExrOvpxoaGXC5Xn5PVIVmNRWVdro%2BkkvURdZOYzUN7XNNNSF7ep0lOJI5tnJ5KZaJNjB8x%0AvhZGbGb8hCEsQ3AjAwDjxwwhjEhMwycyPkgTP96d18pHU%2FDmJdLSaFmEkVoYv8CI1LYy%2BXyMTzLd%0AfAIjBRg%2Fz0gcI9FLIiP6GMKbeaghWU8282DTXaKP8Zlekp%2Fx%2BTcN6mheYs2bmwYtHW%2FdR7TcebN8%0ARNxMEVmriJiRmi0jQMtWXmYaKUjTt4wnj854PigRntXl%2B2vX%2FzaerhQfPyzcnV%2B%2Ffd64PWc8nl%2F7%0A9Zvig3%2BLD%2B6u3bm%2BtvjP%2BsxcYfbi%2BsxV49yScWV5f%2BTtIGxnD2eLy%2B2uzjaC1C4unF%2Bfu1bCIigH%0AIuAEjjJmD2Ik0pcfkYcgQu5gquqatgMaTPGABQJCDj3lQSy3qnnSzr1XcsZb8hCwLksM8e9DzmhS%0AMyMKm67SRm6qRNKW%2BkivpFChQWbipiFYRgsjWQol%2BSxFFcwUU6F480m0XKY7YHzAQddsNasw83B1%0A5budmmWH0%2Frvt9buXyzcmCl%2B9ee2bB2qVJWbg6aQYcRxDovIE1wk1R9q78GkxpYFXanau1QhJAiY%0AOKxk5E8O6mLkeBgCd8R2RFl5W0QEWvfAYcTWFe4J9nGBOGJdRGoTEXPeB7EO3eYAHM%2BMSXpSRG5b%0A9EbTx8azO4Wb88ZfF%2FYwfbwjb%2BVbm%2FKzxywWkUNDcwJmE8kQjJEqXex0VeS1a1C8SIjTSuZwx0h%2F%0Az%2BkeRajQxyhHXkWOEjwHth4OIKaAOKyH94c7cWCCh9WpM%2B8YIjsOXgOQk9v7A4%2FIQo5nnT7syreC%0AsJZUT2K%2BOtc4XQk6CIoEDmLeYcQkZ3tjIalfFio0i3zY1VH6dQGLeFQ%2BbPTPadp0uHs02i3n%2FPxB%0Ab6I50l%2FwUtSAw9CreTI8BkhEh2KN7SU5OmunZXYEQNobLrsfABNz%2Fdy%2BusNBQSUdLf2IcxuoGtk6%0ABGlXFpfbOoSpMogUBHtaxjv4E4Oh3hEAqvNjC5eWfW00ExAFwZ4WJTTMdSVb%2FQJwPwKt9c6vw1Zo%0AFlFA7CkK6mAoOtqZwNilyKXIhiKO9nQoIGc%2F%2Fx9QSwcI6PuVeawGAACYQQAA%0A',
    'Origin': 'http://www.wanfangdata.com.cn',
    'Referer': 'http://www.wanfangdata.com.cn/searchResult/getAdvancedSearch.do?searchType=all'
}


def get_paper_page(organization, page, classification):
    url = "http://www.wanfangdata.com.cn/searchResult/getCoreSearch.do?d=0.5887133238923017"
    organization = u"(作者单位" + ''':("''' + organization + '''"))''' + "*$subject_classcode_level:∷/" + classification
    # organization = '''作者单位:("''' + organization + '''")'''
    from_data = {"paramStrs": organization, "startDate": 2000, "endDate": 2018,
                 "classType": "wfpublish-perio_artical,degree-degree_artical,conference-conf_artical,patent-patent_element,standards-standards,techResult-tech_result,tech-tech_report,gazetteer_new-gazetteers_new",
                 "pageNum": page, "isSearchSecond": "false", "pageSize": 50}
    try:
        response = requests.post(url, data=from_data, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


if __name__ == '__main__':

    allpaper = []
    tagdic_new = ['TP']
    university_list = [
        "华中师范大学",
        "中南财经政法大学",
        "湖南大学"]
    o_cnt = 1
    for the_organization in university_list:
        # the_organization="北京航空航天大学"
        one_school_papers = []
        print(the_organization, o_cnt)
        o_cnt += 1  # 对学校计数

        for classification in tagdic_new:
            # 每个学校从1开始查
            cnt = 1
            while True:
                # cnt不能是0，0和1是一样的，0能得到整体信息

                this_json = get_paper_page(the_organization, cnt, classification)
                # print(this_json)
                if "pageRow" in this_json:
                    pageRow = this_json["pageRow"]
                    if len(pageRow) == 0:
                        break
                    for paperinfo in pageRow:
                        paperinfo[u"学校_查询"] = the_organization
                        one_school_papers.append(paperinfo)
                        if 'title' in paperinfo:
                            print(str(paperinfo['title']))
                print("\n")
                cnt += 1

        jsda1 = json.dumps(one_school_papers, ensure_ascii=False)
        fw1 = codecs.open(str(the_organization) + ".json", "w", encoding="utf-8")
        fw1.write(jsda1)
        print(len(one_school_papers))


