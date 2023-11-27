# coding:utf-8
from PIL import Image
import piexif


def get_gps_info(image_path):
    """
    获取图片的gps信息
    :param image_path:
    :return:
    """
    img = Image.open(image_path)
    exif_data = img._getexif()
    if exif_data and piexif.ImageIFD.GPSTag in exif_data:
        return exif_data[piexif.ImageIFD.GPSTag]
    else:
        return None


def add_gps_info(image_path, lat, lng, alt):
    """
    设置图片的gps信息，并保存新图片
    :param image_path:
    :param lat:
    :param lng:
    :return:
    """
    img = Image.open(image_path)
    if 'exif' in img.info:
        exif_dict = piexif.load(img.info['exif'])
    else:
        exif_dict = {}
    gps_ifd = {piexif.GPSIFD.GPSLatitudeRef: 'N',
               piexif.GPSIFD.GPSLatitude: ((lat, 1), (0, 1), (0, 1)),
               piexif.GPSIFD.GPSLongitudeRef: 'E',
               piexif.GPSIFD.GPSLongitude: ((lng, 1), (0, 1), (0, 1)),
               piexif.GPSIFD.GPSAltitude: (alt, 10000)}

    exif_dict['GPS'] = gps_ifd

    exif_bytes = piexif.dump(exif_dict)
    img.save(image_path[: -4] + '_addgps' + image_path[-4:], exif=exif_bytes)


def add_gps_info_test(image_path, lat, lng, alt):
    # 测试用例
    # image_path = '../file/detection/detection_{150}_addgps.jpg'
    # image_path = '../file/gps/001.jpg'
    gps_info = get_gps_info(image_path)
    if gps_info is None:
        print('No GPS info found. Adding GPS info...')
        # add_gps_info(image_path[: -4] + '_addgps' + image_path[-4 :], 37.7749, 122.4194)  # 添加旧金山的经纬度
        # add_gps_info(image_path, 37.7749, 122.4194)  # 添加旧金山的经纬度
        add_gps_info(image_path, lat, lng, alt)  # 添加旧金山的经纬度
    else:
        print('GPS info:', gps_info)


if __name__ == '__main__':
    image_path = '../file/detection/detection_{145}_{2023-06-29 09:38:27}_addgps.jpg'
    image_path = '../file/gps/002.jpg'
    lat = 37
    lng = 122
    alt = 144
    add_gps_info_test(image_path, lat, lng, alt)