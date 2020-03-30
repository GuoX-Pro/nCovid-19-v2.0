# 爬取新冠状病毒数据并绘制地图
# -*- coding: utf-8 -*-
import requests , json , sys , re , warnings
from pyecharts.charts import Map
from pyecharts import options
from countryname import * # 国家名中英字典
warnings.filterwarnings("ignore")
# 获取命令行参数
if len(sys.argv) == 2:
   mapf = sys.argv[1]
else:
   mapf = '世界' # 无参数默认绘制世界地图
# 获取新浪微博新冠状病毒数据
url = 'https://interface.sina.cn/news/wap/fymap2020_data.d.json?1580097300739&&callback=sinajp_1580097300873005379567841634181'
headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
result = requests.get(url, headers=headers)
# 使用Json正则表达式处理数据
json_str = re.search("\(+([^)]*)\)+", result.text).group(1)
html = f"{json_str}"
table = json.loads(html)
nameMap = dict(zip(nameMap.values(),nameMap.keys())) # 字典KEY、VAL互换
if mapf == '世界' or mapf == 'world' or mapf == '全球':
   # 获取全球国家名称和对应确认数据（不包括中国）
   world_data = []
   for country in table['data']['otherlist']:
       country['name'] = nameMap[country['name']]
       world_data.append((country['name'], country['value']))
   # 创建全球地图
   map_world =  Map()
   map_world.set_global_opts(title_opts = options.TitleOpts(title = "全球新冠状病毒实时疫情地图",subtitle = "累计确诊人数（不含中国）：" + table['data']['othertotal']['certain'] + " 人（新增 " + str(table['data']['othertotal']["certain_inc"]).replace('+','') + " 人）" + "累计死亡人数：" + str(table['data']['othertotal']["die"]) + " 人"),visualmap_opts = options.VisualMapOpts(is_piecewise=True,#设置是否为分段显示
                pieces = [
                    {"min": 1000, "label": '>1000人', "color": "#6F171F"},
                    {"min": 500, "max": 1000, "label": '500-1000人', "color": "#C92C34"},
                    {"min": 100, "max": 499, "label": '100-499人', "color": "#E35B52"},
                    {"min": 10, "max": 99, "label": '10-99人', "color": "#F39E86"},
                    {"min": 1, "max": 9, "label": '1-9人', "color": "#FDEBD0"}]))
   # 全球地图，maptype要对应world
   map_world.add('累计确诊',world_data, maptype = "world",is_map_symbol_show = False)
   map_world.render("全球新冠状病毒实时疫情地图.html")
   print("全球新冠状病毒实时疫情地图已生成！！！")
elif mapf == '中国' or mapf == 'china' or mapf == '中华人民共和国':
   # 获取中国省份名称和对应的确诊数据
   province_data = []
   for province in table['data']['list']:
       province_data.append((province['name'], province['econNum']))
   # 创建全国地图
   map_country = Map()
   map_country.set_global_opts(title_opts=options.TitleOpts(title = "全国新冠状病毒实时疫情地图 现存确诊：" + str(table['data']["econNum"]) + " 人",subtitle = "累计确诊人数：" + str(table['data']["gntotal"]) +" 人（新增 " + str(table['data']['add_daily']["addcon"]) + " 人）" + "累计死亡人数：" + str(table['data']["deathtotal"]) + " 人"), visualmap_opts=options.VisualMapOpts(is_piecewise=True,
                pieces = [
                    {"min": 101, "label": '>100人', "color": "#6F171F"},
                    {"min": 50, "max": 100, "label": '50-100人', "color": "#C92C34"},
                    {"min": 10, "max": 49, "label": '10-49人', "color": "#E35B52"},
                    {"min": 1, "max": 9, "label": '1-9人', "color": "#F39E86"},
                    {"min": 0, "max": 0, "label": '无确诊病人', "color": "#FDEBD0"}]))
   # 中国地图，maptype要对应china
   map_country.add("现存确诊", province_data, maptype = "china",is_map_symbol_show = False)
   map_country.render("全国新冠状病毒实时疫情地图.html")
   print("全国新冠状病毒实时疫情地图已生成！！！")
else:
   # 获取全国省份名称和对应的确诊数据
   province_data = []
   for province in table['data']['list']:
       province_data.append((province['name'],province['econNum'],province['value'],province['conadd'],province['deathNum']))
       if province['name'] == mapf:
          # 获取城市名称和对应的确诊数据
          city_data = []
          for city in province['city']:
              city_data.append((city['mapName'], city['econNum']))  # 注意对应上地图的名字需要使用mapName这个字段
          # 创建指定省份地图
          map_province = Map()
          # 设置地图上的标题和数据标记，添加省份和确诊人数
          map_province.set_global_opts(title_opts = options.TitleOpts(title = province['name'] + "新冠状病毒实时疫情地图 现存确诊：" + str(province["econNum"]) + " 人",subtitle = "累计确诊人数：" + str(province["value"]) +" 人（新增 " + str(province["conadd"]) + " 人）" + "累计死亡人数：" + province["deathNum"] + " 人"), visualmap_opts=options.VisualMapOpts(is_piecewise=True,#设置是否为分段显示
                # 自定义数据范围和对应的颜色，这里是取色工具获取的颜色值
                pieces = [
                    {"min": 100, "label": '>100人', "color": "#6F171F"},  # 不指定 max，表示 max 为无限大（Infinity）。
                    {"min": 50, "max": 100, "label": '50-100人', "color": "#C92C34"},
                    {"min": 10, "max": 49, "label": '10-49人', "color": "#E35B52"},
                    {"min": 1, "max": 9, "label": '1-9人', "color": "#F39E86"},
                    {"min": 0, "max":0, "label": '无确诊病人', "color": "#FDEBD0"}]))
          # 将数据添加进去，省份地图，maptype要对应省份。
          map_province.add("现存确诊", city_data, maptype = province['name'],is_map_symbol_show=False)  # is_map_symbol_show=False 去掉小红点
          # 一切完成，那么生成一个省份的html网页文件，取上对应省份的名字
          map_province.render(province['name'] + "新冠状病毒实时疫情地图.html")
          break
   if mapf == province['name']:
      print(province['name'] + "新冠状病毒实时疫情地图已生成！！！")
   else:
      print("对不起，我还不能到达火星！！！")
