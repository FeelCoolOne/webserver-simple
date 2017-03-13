#coding:utf-8
import os
import sys
'''
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
'''

class out(object):
    '''out put xml'''
    def __init__(self, data, name):
        self.cache_dir = 'xml'
        self.name_xml = name
        self.data = data
        self.dictionary = {
            u'单据名称': 'DanJuMingCheng',
            u'银行名称': 'YinHangMingCheng',
            u'报文种类': 'BaoWenZhongLei',
            u'客户号': 'KeHuHao',
            u'币种': 'BiZhong',
            u'现转标志': 'XianZhuanBiaoZhi',
            u'钞汇标志': 'ChaoHuiBiaoZhi',
            u'费率种类': 'FeiLvZhongLei',
            u'费率名称': 'FeiLvMingCheng',
            u'交易日期': 'JiaoYiRiQi',
            u'交易时间': 'JiaoYiShiJian',
            u'委托日期': 'WeiTuoRiQi',
            u'回单编号': 'HuiDanBianHao',
            u'交易流水号': 'JiaoYiLiuShuiHao',
            u'交易序号': 'JiaoYiXuHao',
            u'收付标志': 'ShouFuBiaoZhi',
            u'付款方名称': 'FuKuanFangMingCheng',
            u'付款方银行账号': 'FuKuanFangYinHangZhangHao',
            u'发起行行号': 'FaQiHangHangHao',
            u'发起行名称': 'FaQiHangMingCheng',
            u'付款方开户银行代码': 'FuKuanFangKaiHuYinHangDaiMa',
            u'付款方开户银行': 'FuKuanFangKaiHuYinHang',
            u'付款地点': 'FuKuanDiDian',
            u'交款人名称及税号': 'JiaoKuanRenMingChengJiShuihao',
            u'现金缴款人': 'XianJinJiaoKuanRen',
            u'收款方开户银行代码': 'ShouKuanFangKaiHuYinHangDaiMa',
            u'收款方开户银行': 'ShouKuanFangYinHang',
            u'收款地点': 'ShouKuanDiDian',
            u'税票号码': 'ShuiPiaoHaoMa',
            u'起始日期': 'QiShiRiQi',
            u'截止日期': 'JieZhiRiQi',
            u'利率': 'LiLv',
            u'利息': 'LiXi',
            u'明细': 'MingXi',
            u'项目名称': 'XiangMuMingCheng',
            u'所属期间': 'SuoShuQiJian',
            u'单价': 'DanJia',
            u'金额': 'JinE',
            u'合计金额（大写）': 'HeJiJinE_DaXie',
            u'合计金额': 'HeJiJinE',
            u'应收金额': 'YingShouJinE',
            u'实收金额': 'ShiShouJinE',
            u'存款种类': 'CunKuanZhongLei',
            u'业务种类': 'YeWuZhongLei',
            u'产品名称': 'ChanPinMinChen',
            u'业务编号': 'YeWuBianHao',
            u'费用名称': 'FeiYongMingCheng',
            u'存款账号': 'CunKuanZhangHao',
            u'支付密码': 'ZhiFuMiMa',
            u'交易方式': 'JiaoYiFangShi',
            u'付款人卡号': 'FuKuanRenKaHao',
            u'用途': 'YongTu',
            u'附言': 'FuYan',
            u'摘要': 'ZhaiYao',
            u'备注': 'BeiZhu',
            u'银行印章': 'YinHangYinZhang',
            u'打印日期': 'DaYinRiQi',
            u'打印次数': 'DaYinCiShu',
            u'交易柜员': 'JiaoYiGuiYuan',
            u'交易机构代码': 'JiaoYiJiGouDaiMa',
            u'交易机构名称': 'JiaoYiJiGouMingCheng',
            u'查验网址': 'ChaYanWangZhi',
            u'单据种类': 'DanJuZhongLei',
            u'单据号码': 'DanJuHaoMa',
            u'验证码': 'YanZhengMa',
            u'交易码': 'JiaoYiMa',
        }

    def createXml(self, data):
        """
        创建XML格式文件
        data: [{'\u65b9\u5f00\u6237\u884c\u53ca\u53f7':'15107615112016931', 'width': 777, 'top: 1828, "height": 75, "left": 582}
           , {'\u65b9\u5f00\u6237\u884c\u53ca\u53f7':'15107615112016931', 'width': 777, 'top: 1828, "height": 75, "left": 582}]
        """
        root = """<?xml version="1.0" encoding="utf-8"?>\n"""
        root += u"""<root><type>银行回执单</type>\n<value>{}</value></root>"""
        element = u''
        for lineelement in data:
            label = filter(lambda x: x not in ['width', 'top', 'height', 'left'], lineelement.keys())[0]
            key = self.dictionary.get(label)
            text = lineelement[label]
            # location = lineelement['location']
            height, left, top, width = lineelement['height'], lineelement['left'], lineelement['top'], lineelement['width']
            element += u'<{} height="{}" left="{}"  top="{}" width="{}" >{}</{}>\n'.format(key, height, left, top, width, text, key)
        return root.format(element)

    def process(self):
        xml = self.createXml(self.data)
        with open(os.path.join(self.cache_dir, self.name_xml), 'w') as f:
            print xml.encode('utf-8')
            f.write(xml.encode('utf-8'))
        return 0


if __name__ == '__main__':
    data = [{u'单价': '15107615112016931', 'width': 7, 'top': 18, "height": 7, "left": 82},
            {u'交易方式': '15107615112016931', 'width': 777, 'top': 1828, "height": 75, "left": 582}]
    out(data, 'test.xml').process()
