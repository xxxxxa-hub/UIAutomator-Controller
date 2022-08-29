import serial
import serial.tools.list_ports
import time

sendCmd_Version = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x38, 0x36, 0x30, 0x30, 0x38, 0x38, 0x0D]  # 读版本号
sendCmd_SEL0_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x30, 0x33, 0x32,
                  0x0D]  # SEL0_L
sendCmd_SEL0_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x30, 0x30, 0x31, 0x30, 0x30, 0x33, 0x33,
                  0x0D]  # SEL0_H
sendCmd_SEL1_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x31, 0x30, 0x30, 0x30, 0x30, 0x33, 0x33,
                  0x0D]  # SEL1_L
sendCmd_SEL1_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x31, 0x30, 0x31, 0x30, 0x30, 0x33, 0x34,
                  0x0D]  # SEL1_H
sendCmd_SEL2_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x32, 0x30, 0x30, 0x30, 0x30, 0x33, 0x34,
                  0x0D]  # SEL2_L
sendCmd_SEL2_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x32, 0x30, 0x31, 0x30, 0x30, 0x33, 0x35,
                  0x0D]  # SEL2_H
sendCmd_OE0_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x33, 0x30, 0x30, 0x30, 0x30, 0x33, 0x35,
                 0x0D]  # OE0_L
sendCmd_OE0_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x33, 0x30, 0x31, 0x30, 0x30, 0x33, 0x36,
                 0x0D]  # OE0_H
sendCmd_OE1_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x34, 0x30, 0x30, 0x30, 0x30, 0x33, 0x36,
                 0x0D]  # OE1_L
sendCmd_OE1_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x34, 0x30, 0x31, 0x30, 0x30, 0x33, 0x37,
                 0x0D]  # OE1_H
sendCmd_OE2_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x35, 0x30, 0x30, 0x30, 0x30, 0x33, 0x37,
                 0x0D]  # OE2_L
sendCmd_OE2_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x35, 0x30, 0x31, 0x30, 0x30, 0x33, 0x38,
                 0x0D]  # OE2_H
sendCmd_C_B12_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x36, 0x30, 0x30, 0x30, 0x30, 0x33, 0x38,
                   0x0D]  # C_B12_L
sendCmd_C_B12_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x36, 0x30, 0x31, 0x30, 0x30, 0x33, 0x39,
                   0x0D]  # C_B12_H
sendCmd_OTG_CC_C_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x37, 0x30, 0x30, 0x30, 0x30, 0x33, 0x39,
                      0x0D]  # OTG_CC_C_L
sendCmd_OTG_CC_C_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x37, 0x30, 0x31, 0x30, 0x30, 0x33, 0x41,
                      0x0D]  # OTG_CC_C_H
sendCmd_OTG_VBUS_C_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x38, 0x30, 0x30, 0x30, 0x30, 0x33, 0x41,
                        0x0D]  # OTG_VBUS_C_L
sendCmd_OTG_VBUS_C_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x38, 0x30, 0x31, 0x30, 0x30, 0x33, 0x42,
                        0x0D]  # OTG_VBUS_C_H
sendCmd_SVOOC_MOS_C_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x39, 0x30, 0x30, 0x30, 0x30, 0x33, 0x42,
                         0x0D]  # SVOOC_MOS_C_L
sendCmd_SVOOC_MOS_C_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x39, 0x30, 0x31, 0x30, 0x30, 0x33, 0x43,
                         0x0D]  # SVOOC_MOS_C_H
sendCmd_Phone_mos_c_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x41, 0x30, 0x30, 0x30, 0x30, 0x33, 0x43,
                         0x0D]  # Phone_mos_c_L
sendCmd_Phone_mos_c_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x41, 0x30, 0x31, 0x30, 0x30, 0x33, 0x44,
                         0x0D]  # Phone_mos_c_H
sendCmd_PD_MOS_C_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x42, 0x30, 0x30, 0x30, 0x30, 0x33, 0x44,
                      0x0D]  # PD_MOS_C_L
sendCmd_PD_MOS_C_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x42, 0x30, 0x31, 0x30, 0x30, 0x33, 0x45,
                      0x0D]  # PD_MOS_C_H
sendCmd_QC_MOS_C_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x43, 0x30, 0x30, 0x30, 0x30, 0x33, 0x45,
                      0x0D]  # QC_MOS_C_L
sendCmd_QC_MOS_C_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x43, 0x30, 0x31, 0x30, 0x30, 0x33, 0x46,
                      0x0D]  # QC_MOS_C_H
sendCmd_SEL_DPDN_CC_L = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x44, 0x30, 0x30, 0x30, 0x30, 0x33, 0x46,
                         0x0D]  # SEL_DPDN_CC_L
sendCmd_SEL_DPDN_CC_H = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x33, 0x30, 0x30, 0x44, 0x30, 0x31, 0x30, 0x30, 0x34, 0x30,
                         0x0D]  # SEL_DPDN_CC_H

sendCmd_Ibus = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x41, 0x32, 0x30, 0x30, 0x41, 0x34, 0x0D]  # 查询Ibus值命令
sendCmd_Vbus = [0x7E, 0x30, 0x31, 0x30, 0x31, 0x41, 0x33, 0x30, 0x30, 0x41, 0x35, 0x0D]  # 查询Vbus值命令
byte_rcveMSG = []  # 接收到的上报数据


class SerialPort:
    def __init__(self):
        # 获取系统串口端口号；
        plist = list(serial.tools.list_ports.comports())
        ports = None
        for i in range(len(plist)):
            if "USB-SERIAL CH340" in plist[i][1]:
                ports = plist[i][0]
        # 打开端口初始化；
        self.SER = serial.Serial(
            port=ports, baudrate=9600, bytesize=8, parity="N", stopbits=1, timeout=None, xonxoff=0, rtscts=0)
        if self.SER.is_open is False:
            self.SER.open()

    def port_send(self, send_data):
        """
        # 向串口发送数据
        :param send_data: 需要发送的数据
        :return:
        """
        if self.SER.is_open:
            self.SER.write(send_data)  # .encode("utf-8")
            time.sleep(0.2)
            response = self.SER.read_all()
            response = self.convert_hex(response)
            return response

    @staticmethod
    def convert_hex(string):
        """
        # 将结果转换成16进制
        :param string:需要转换的信息
        :return:
        """
        res = []
        result = []
        for item in string:
            res.append(item)
        for i in res:
            result.append(hex(i))
        return result

    def pc_on(self):
        """
        # PC 口开启连接
        :return: 开启连接请求返回值列表
        """
        open_list = [sendCmd_SEL_DPDN_CC_H, sendCmd_SEL_DPDN_CC_H, sendCmd_C_B12_H, sendCmd_Phone_mos_c_H,
                     sendCmd_OE0_L]
        response_list = []
        for com in open_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        time.sleep(1)
        return response_list

    def pc_off(self):
        """
        # PC 口断开连接
        :return:
        """
        off_list = [sendCmd_OE0_H, sendCmd_Phone_mos_c_L, sendCmd_C_B12_L, sendCmd_SEL_DPDN_CC_L, sendCmd_SEL_DPDN_CC_L]
        response_list = []
        for com in off_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        time.sleep(1)
        return response_list

    def pd_on(self):
        """
        # PD 口连接
        :return:
        """
        on_list = [sendCmd_SEL_DPDN_CC_H, sendCmd_C_B12_H, sendCmd_PD_MOS_C_H, sendCmd_SEL0_H, sendCmd_SEL2_H,
                   sendCmd_OE0_L, sendCmd_OE1_L, sendCmd_OE2_L]
        response_list = []
        for com in on_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def pd_off(self):
        """
        # PD 口断开连接
        :return:
        """
        off_list = [sendCmd_OE2_H, sendCmd_OE1_H, sendCmd_OE0_H, sendCmd_SEL2_L, sendCmd_SEL0_L, sendCmd_PD_MOS_C_L,
                    sendCmd_C_B12_L, sendCmd_SEL_DPDN_CC_L]
        response_list = []
        for com in off_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def qc_on(self):
        """
        # QC 口连接
        :return:
        """
        on_list = [sendCmd_SEL_DPDN_CC_H, sendCmd_C_B12_H, sendCmd_QC_MOS_C_H, sendCmd_SEL0_H, sendCmd_OE0_L,
                   sendCmd_OE1_L, sendCmd_OE2_L]
        response_list = []
        for com in on_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def qc_off(self):
        """
        # qc 口断开连接
        :return:
        """
        off_list = [sendCmd_OE2_H, sendCmd_OE1_H, sendCmd_OE0_H, sendCmd_SEL0_L, sendCmd_QC_MOS_C_L, sendCmd_C_B12_L,
                    sendCmd_SEL_DPDN_CC_L]
        response_list = []
        for com in off_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def otg_on(self):
        """
        # OTG 口连接
        :return:
        """
        on_list = [sendCmd_SEL_DPDN_CC_H, sendCmd_C_B12_H, sendCmd_OTG_CC_C_H, sendCmd_OTG_VBUS_C_H]
        response_list = []
        for com in on_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def otg_off(self):
        """
        # OTG 口断开连接
        :return:
        """
        off_list = [sendCmd_OTG_VBUS_C_L, sendCmd_OTG_CC_C_L, sendCmd_C_B12_L, sendCmd_SEL_DPDN_CC_L]
        response_list = []
        for com in off_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def svooc_on(self):
        """
        # SVOOC 口连接
        :return:
        """
        on_list = [sendCmd_SEL_DPDN_CC_H, sendCmd_C_B12_H, sendCmd_SVOOC_MOS_C_H, sendCmd_SEL0_H, sendCmd_SEL1_H,
                   sendCmd_OE0_L, sendCmd_OE1_L]
        response_list = []
        for com in on_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def svooc_off(self):
        """
        # SVOOC 口断开连接
        :return:
        """
        off_list = [sendCmd_OE1_H, sendCmd_OE0_H, sendCmd_SEL1_L, sendCmd_SEL0_L, sendCmd_SVOOC_MOS_C_L,
                    sendCmd_C_B12_L, sendCmd_SEL_DPDN_CC_L]
        response_list = []
        for com in off_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        return response_list

    def close_port(self):
        """
        # 关闭串口
        :return:
        """
        close_list = [sendCmd_Phone_mos_c_L, sendCmd_SVOOC_MOS_C_L, sendCmd_PD_MOS_C_L, sendCmd_QC_MOS_C_L,
                      sendCmd_OTG_VBUS_C_L, sendCmd_OE2_H, sendCmd_OE1_H, sendCmd_OE0_H, sendCmd_SEL_DPDN_CC_L,
                      sendCmd_SEL2_L, sendCmd_SEL1_L, sendCmd_SEL0_L, sendCmd_OTG_CC_C_L, sendCmd_C_B12_L]
        response_list = []
        for com in close_list:
            response = self.port_send(com)
            time.sleep(0.2)
            response_list.append(response)
        self.SER.close()    # 关闭串口
        return response_list


if __name__ == '__main__':
    cc = SerialPort()
    requ = cc.pc_on()
    # requ = cc.pc_off()
    print(requ)
