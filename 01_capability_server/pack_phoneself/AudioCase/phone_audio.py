# coding=utf-8
from PhoneSet.settings import Settings
from Demand.record_play import PlayAudio, RecordAudio
from Base.mobile_base import MobileBase


class PhoneSide(MobileBase):

    def __init__(self, device_id=None, play_path=None, record_path=None):
        super().__init__(device_id)
        self.pa = PlayAudio(self, play_path)
        self.ra = RecordAudio(self, record_path)
        self.play_path = play_path
        self.record_path = record_path
        self.case_date = {}
        self.date = {}

    def return_class_name(self):
        # 获取class name，包括子类
        return __class__

    def play_audio(self, volume_type, level, play_audio_file):
        """
        手机播放从PC端推送的音频文件
        :param volume_type: 播放器件类型，话筒, 扬声器, 闹钟, 蓝牙
        :param level:音量
        :param play_audio_file:音频名称
        :return:
        """
        self.pa.play_audio_by_qq(volume_type, level, play_audio_file)

    def record_audio(self):
        """手机录制音频"""
        self.ra.phone_record_audio()

    def stop_audio_record(self, audio_name):
        """停止OPPO录音软件并并推送文件到指定PC目录"""
        self.ra.phone_record_stop(audio_name)

    def alarm_ring(self):
        """闹铃铃声"""
        pass

    def telephone_ring(self, volume_type, level, audioName):
        """电话铃声"""
        self.set_volume(volume_type, level)
        Settings(self.device_id).goto_select_ring(audioName)

    def play_video(self, volume_type, level, play_video_file):
        """手机播放视频"""
        self.pa.play_video_oppo(volume_type, level, play_video_file)

    def stop_audio_video(self):
        """删除push到sdcard的音频文件，停止所有音频，视频的播放"""
        self.adb_comm_execute('adb shell rm -f /sdcard/%s' % self.pa.random_name)
        self.pa.stop_phone_play()

    def record_camera(self):
        """相机录制视频"""
        self.ra.phone_record_camera()

    def stop_camera_record(self, audio_name):
        """停止录制视频，并推送文件到指定PC目录"""
        self.ra.camera_record_stop(audio_name)

    def set_volume(self, volume_type, level):
        self.pa.volume.set_phone_volume(volume_type, level)

    def page_source(self):
        print(self.driver.info)


if __name__ == '__main__':
    PLAY_AUDIO_PATH = r'E:\\play_audio\\'
    RECORD_AUDIO_PATH = r'E:\\record_audio\\'
    side = PhoneSide('192.168.1.8', play_path=PLAY_AUDIO_PATH, record_path=RECORD_AUDIO_PATH)
    side.telephone_ring("第一次录音.mp3")
