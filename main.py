import os
import sys
import ctypes
import numpy as np
from PIL import Image

# 加载C库
c_lib = ctypes.CDLL("./add_bayer.dll")
c_lib.add_bayer.restype = None
c_lib.add_bayer.argtypes = [
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.POINTER(ctypes.c_uint8),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int
]

def generate_Bayer_Matrix(n):
    '''生成Bayer矩阵'''
    if n == 2:
        return np.array([[0, 2], [3, 1]], dtype=np.uint8)
    else:
        smaller = generate_Bayer_Matrix(n // 2)
        return np.block([
            [4 * smaller, 4 * smaller + 2],
            [4 * smaller + 3, 4 * smaller + 1]
        ])

# 遍历当前目录中的文件
for filename in os.listdir('./'):
    filepath = os.path.join('./', filename)
    try:
        with Image.open(filepath) as img:
            im = img
            # 转换为灰度图像
            im = im.convert("L")
            # 将图像转换为numpy数组
            im_arr = np.array(im, dtype = np.uint8)
            # 生成Bayer矩阵
            bayer_matrix = generate_Bayer_Matrix(8)
            # 创建输出数组
            out = np.zeros_like(im_arr, dtype = np.uint8)
            
            # 将numpy数组转换为ctypes指针
            im_arr_ptr = im_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
            bayer_matrix_ptr = bayer_matrix.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
            out_ptr = out.ctypes.data_as(ctypes.POINTER(ctypes.c_uint8))
            
            # 调用C函数
            c_lib.add_bayer(
                im_arr_ptr,
                bayer_matrix_ptr,
                out_ptr,
                im_arr.shape[0],
                im_arr.shape[1],
                bayer_matrix.shape[0]
            )
            
            # 将结果转换为图像并保存
            result_im = Image.fromarray(out, mode='L')
            result_im.show()
            result_im.save('output.png')
            break  # 处理第一个图像后退出循环
    except IOError:
        pass

