import math
import pandas
from charset_normalizer import detect
from flask import jsonify
import time


def read_data(csv_path):
    """
    读取波形csv，返回dataframe
    :param csv_path:
    :return: dataframe
    """
    with open(csv_path, 'rb+') as fp:
        content = fp.read()
        encoding = detect(content)['encoding']
        # df = pandas.read_csv(csv_path, encoding=encoding)
        content = content.decode(encoding).encode('utf8')
        fp.seek(0)
        fp.write(content)
        # yield from asyncio.sleep(1)

    df = pandas.read_csv(csv_path, encoding='utf8', low_memory=False)
    return df


class SpiSignalQuality:
    def check_back(self, csv_path, base, top):      # 需要兼容直接传数据进来
        """
        判断回勾
        :param csv_path: csv文件路径
        :param base: 低电平有效值
        :param top: 高电平有效值
        :return: 返回回勾数据dataframe
        """
        try:
            df = read_data(csv_path)
            # 串扰 < 200mV(高电平 / 低电平的峰峰值)
            # lower = base + 0.1 * (top - base)
            lower = float(base) + 0.2
            # topper = base + 0.9 * (top - base)
            topper = float(top) - 0.2

            data = pandas.DataFrame(df)  # 使用DataFrame获取数据
            data = data.reset_index()
            # 依据两套数据模板内容进行区分，兼容两套模板；
            if data.iloc[3, 1] == "Ampl" and data.iloc[3, 0] == "Time":
                data = data.iloc[4:, [0, 1]]
            else:
                data = data.iloc[:, [1, 2]]

            # 获取子表'坐标'和‘测试结果’列的数
            data.columns = ['time', 'voltage']  # 设置纵坐标
            data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

            # 获取voltage在(lower,topper)之间的所有数据
            data_analyse = data[(data.voltage > lower) & (data.voltage < topper)]
            #  取出连续片段的开始和结束加入字典的键和值

            dic = {}  # 字典，键为上升或下降区间的开始，值为结束
            temp_start = data_analyse.index[0]  # 记录开始位置，加入字典
            dic[temp_start] = 0
            temp = temp_start  # 临时变量记录索引

            for i in data_analyse.index[0:]:        # 耗时10秒
                if (i - temp) > 1:
                    dic[temp_start] = temp  # 临时加入字典
                    temp_start = i
                temp = i
            dic[temp_start] = temp

            back_list = []
            back_plot_dic = []
            for key in dic:
                index_list = list(range(key, dic[key] + 1))     # 下标列表
                data_part = data_analyse.loc[index_list]    # 根据下标列表获取数据值
                # 开始判断是否回勾
                if (data_part['voltage'].max() - data_part['voltage'].min()) < 0.2:  # 最大与最小相差小则弃掉
                    continue
                rolling_len = int(math.sqrt(len(data_part)))
                if rolling_len % 2 == 0:
                    rolling_len -= 1
                data_mean = pandas.DataFrame(data_part).rolling(window=rolling_len).mean().dropna()
                # plt.figure(figsize=(10,10))
                # plt.plot(data_mean['voltage'])
                # plt.show()

                data_part = data_part[4:]
                if len(data_part.index) == 0:
                    continue
                if data_part.iloc[0].voltage <= 0.5 * (float(top) - float(base)):  # 上升
                    data_sort = data_mean.sort_values(by='voltage', ascending=True)
                    flag = 1
                else:
                    data_sort = data_mean.sort_values(by='voltage', ascending=False)
                    flag = -1
                last_index = data_sort.index[0]
                back_part_list = []
                space_standard = int(rolling_len / 2) + 1   # 判定依据
                for index in data_sort.index[0:]:
                    if (last_index - index) > space_standard:
                        if (not back_list) or (last_index - back_list[-1]) > space_standard:
                            back_list.append(last_index)
                            back_part_list.append(last_index)
                    last_index = index
                if not back_part_list:
                    continue
                for x in back_part_list:    # 回勾数据
                    bplot = self.find_plot(data_part, x, flag)
                    if not bplot:
                        continue
                    back_plot_dic.append(bplot)

            max_plot = {}
            max_diff = 0
            if not back_plot_dic:
                return max_plot

            for a in back_plot_dic:
                if a["y2"] - a["y1"] > max_diff:
                    max_plot = a
                    max_diff = a["y2"] - a["y1"]
            return max_plot
        except Exception as err:
            raise Exception(err)

    def crosstalk(self, csv_path, base, top):
        """
              判断是否有串扰
              :param csv_path:csv文件路径
              :param base:低电平有效值
              :param top: 高电平有效值
              :return: 染回串扰的幅值
        """
        try:
            df = read_data(csv_path)

            # 串扰 < 200mV(高电平 / 低电平的峰峰值)
            lower = float(base) + 0.2
            topper = float(top) - 0.2
            if lower >= topper:
                raise Exception("错误的波形文件")

            data = pandas.DataFrame(df)  # 使用DataFrame获取数据
            data = data.reset_index()

            # 依据两套数据模板内容进行区分，兼容两套模板；
            if data.iloc[3, 1] == "Ampl" and data.iloc[3, 0] == "Time":
                data = data.iloc[4:, [0, 1]]    # 获取子表'坐标'和‘测试结果’列的数
            else:
                data = data.iloc[:, [1, 2]]

            data.columns = ['time', 'voltage']  # 设置纵坐标
            data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

            # 获取voltage在(lower,topper)之间的所有数据
            data_analyse = data[(data.voltage < lower) | (data.voltage > topper)]

            # 索引起始点
            data_start = 0
            # 当前行号
            data_current = 0
            # 索引终点
            data_end = 0
            # 所有的高低电平保存参数
            data_low = data_high = pandas.core.frame.DataFrame()
            src_length = int(len(data_analyse))

            while data_start < src_length:
                count = data_analyse.index[data_current] - data_current
                while data_end < src_length:
                    # 如果原数据索引有断层，则证明是一个新的波段
                    if data_analyse.index[data_end] - data_current == count:
                        data_end += 1
                        data_current += 1
                    else:
                        break
                data1 = data_analyse.iloc[data_start:data_end]

                # 先去除前20%的点防止过冲干扰
                data_length = int(len(data1) * 0.2)
                data1 = data1.iloc[data_length:len(data1)]
                # 重新建立索引
                data1 = data1.reset_index(drop=True)

                # 根据第一个点的大小判断是高电平还是低电平
                if data1.iloc[0].voltage <= 0.5 * (float(top) - float(base)):
                    # 找出第一个和最后一个低于有效值的位置
                    data3 = data1[(data1.voltage <= float(base))]
                    if len(data3) > 0:
                        data_low = pandas.concat([data_low, data1.iloc[min(data3.index):max(data3.index)]])
                else:
                    # 找出第一个和最后一个高于有效值的位置
                    data3 = data1[(data1.voltage >= top)]
                    if len(data3) > 0:
                        data_high = pandas.concat([data_high, data1.iloc[min(data3.index):max(data3.index)]])
                data_start = data_end

            if len(data_low) == 0:
                low_min = 0
                low_max = 0
            else:
                low_min = min(data_low.voltage.to_list())
                low_max = max(data_low.voltage.to_list())

            if len(data_high) == 0:
                high_min = 0
                high_max = 0
            else:
                high_min = min(data_high.voltage.to_list())
                high_max = max(data_high.voltage.to_list())

            measure_value = {'low_min': low_min, 'low_max': low_max,
                             'high_min': high_min,
                             'high_max': high_max}
            return measure_value
        except Exception as err:
            raise Exception(err)

    def find_plot(self, data, backindex, flag):
        coo_dic = {}
        deep_standard = 0
        if len(data) > 5000:
            deep_standard = 0.04
        if flag == 1:  # 上升
            row_num = data.index.get_loc(backindex)
            low_before_data = data[:row_num]
            y2 = low_before_data['voltage'].max()
            high_index = low_before_data['voltage'].idxmax()
            high_row = data.index.get_loc(high_index)
            high_after_data = data[high_row:]
            y1 = high_after_data['voltage'].min()
            if (y2 - y1) < deep_standard:
                return
            min_diff_y1 = 5  # 与y1最接近的值
            min_diff_y1_index = 0

            high_before_data = data[:high_row]
            high_before_data = high_before_data.iloc[::-1]  # 反向
            for index, row in high_before_data.iterrows():
                diff = math.fabs(row['voltage'] - y1)
                if diff < min_diff_y1:
                    min_diff_y1 = diff
                    min_diff_y1_index = index
                if row['voltage'] < y1:
                    break
            index1 = min_diff_y1_index
            x1 = data.loc[index1]['time']

            min_diff_y2 = 5  # 与y2最接近的值
            min_diff_y2_index = 0
            low_after_data = data[row_num:]
            for index, row in low_after_data.iterrows():
                diff = math.fabs(row['voltage'] - y2)
                if diff < min_diff_y2:
                    min_diff_y2 = diff
                    min_diff_y2_index = index
                if row['voltage'] > y2:
                    break
            index2 = min_diff_y2_index
            x2 = data.loc[index2]['time']
            coo_dic = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
        elif flag == -1:
            row_num = data.index.get_loc(backindex)
            high_before_data = data[:row_num]   # 获取回勾点之前的数据
            y1 = high_before_data['voltage'].min()
            low_index = high_before_data['voltage'].idxmin()
            low_row = data.index.get_loc(low_index)
            low_after_data = data[low_row:]
            y2 = low_after_data['voltage'].max()
            if (y2 - y1) < deep_standard:
                return

            low_before_data = data[:low_row]
            low_before_data = low_before_data.iloc[::-1]  # 反向
            # 获取齐平y2的值
            index1 = low_before_data.loc[low_before_data.voltage >= y2].index.tolist()[0]
            x1 = data.loc[index1]['time']
            high_after_data = data[row_num:]
            # 获取齐平y1的值
            index2 = high_after_data.loc[high_after_data.voltage >= y1].index.tolist()[0]
            x2 = data.loc[index2]['time']
            coo_dic = {"x1": x1, "x2": x2, "y1": y1, "y2": y2}
        return coo_dic


    def check_step(self, csv_path, base, top, threshold):
        """
        判断是否有台阶
        :param threshold: 低于阈值才算台阶
        :param top:
        :param base:
        :param csv_path:csv文件路径
        :return:
        """
        df = read_data(csv_path)

        lower = float(base) + 0.2
        # topper = base + 0.9 * (top - base)
        topper = float(top) - 0.2

        data = pandas.DataFrame(df)  # 使用DataFrame获取数据
        data = data.reset_index()

        if data.iloc[3, 1] == "Ampl" and data.iloc[3, 0] == "Time":
            data = data.iloc[4:, [0, 1]]  # 获取子表'坐标'和‘测试结果’列的数
        else:
            data = data.iloc[:, [1, 2]]

        # data = data.iloc[4:, [0, 1]]  # 获取子表'坐标'和‘测试结果’列的数
        data.columns = ['time', 'voltage']  # 设置纵坐标
        data = data.apply(pandas.to_numeric, errors='coerce')  # 将所有字符串转为数字

        # 获取voltage在(lower,topper)之间的所有数据
        data_analyse = data[(data.voltage > lower) & (data.voltage < topper)]
        #  取出连续片段的开始和结束加入字典的键和值
        dic = {}  # 字典，键为上升或下降区间的开始，值为结束
        temp_start = data_analyse.index[0]  # 记录开始位置，加入字典
        dic[temp_start] = 0
        temp = temp_start  # 临时变量记录索引
        for index in data_analyse.index[0:]:
            if (index - temp) > 1:
                dic[temp_start] = temp  # 临时加入字典
                temp_start = index
            temp = index
        dic[temp_start] = temp  # 最后一项加入字典

        coo_dic = []
        for key in dic:
            index_list = list(range(key, dic[key] + 1))
            data_part = data_analyse.loc[index_list]

            # 圆滑数据
            rolling_len = int(math.sqrt(len(data_part)))
            if rolling_len % 2 == 0:
                rolling_len -= 1
            data_mean = pandas.DataFrame(data_part).rolling(window=rolling_len).mean().dropna()
            length = len(data_part)

            # 如果点数小于10则不作台阶检测
            if length <= 10:
                continue
            # 每次取值十分之一
            counts = int(length / 10)
            if length <= 100:
                # 如果样本数小于100则每一步都进行计算
                stepping = 2
                counts = int(length / 3)
                # counts = 10
            else:
                # 如果样本数大于100则取百分之一小步进行计算
                stepping = 50

            sections = int(length / stepping)

            list_std = {}
            for i in range(sections):
                if i * stepping + counts > length:
                    break

                data_step_analyse = data_mean.head(i * stepping + counts).tail(counts)['voltage']

                # 如果最大值和最小值大于0.2v则不做台阶检测
                if (data_step_analyse.max() - data_step_analyse.min()) > 0.2:
                    continue

                # 数据归一化
                df_normalization = data_step_analyse / data_step_analyse.min()
                # 计算标准差
                std = df_normalization.std()
                if std < float(threshold):
                    list_std[key + i * stepping] = std

            if len(list_std) > 0:
                # 记录标准差最小位置
                max_index = min(list_std, key=list_std.get)
                # list1 = [max_index, max_index + counts, list_std[max_index]]
                list1 = [float(max_index), float(max_index + counts), data.loc[max_index].time, data.loc[max_index + counts].time,
                         list_std[max_index]]
                coo_dic.append(list1)
        return coo_dic


if __name__ == '__main__':
    try:
        path_test_1 = 'C1--Trace--CLK.csv'
        path_test_2 = 'C1--Trace--MOSI.csv'
        path_test_3 = 'C1--Trace--MISO.csv'
        path_test_4 = 'C1--Trace--CS.csv'
        path_test_5 = '20220401155257522087.csv'
        path_test_6 = 'Data.csv'
        path_test_7 = 'E:\\POST\\Data.csv'
        test_path = path_test_6
        #
        test = SpiSignalQuality()
        # print("========checkback result========")
        check_back = test.check_back(path_test_7, 0.12, 3.02)
        print(check_back)
        # cb_result = test.check_step(test_path, 0.03, 3, 0.01)
        # print(cb_result)
        # result = jsonify(result="OK", message=cb_result)
    except Exception as err:
        print(str(err))
# print("========crosstalk result========")
# ct_result = test.crosstalk(test_path, 0.0, 1.75)
# print(ct_result)
