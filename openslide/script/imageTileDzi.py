#--*-- coding:utf-8 --*--

import os
import time
import openslide
from openslide.deepzoom import DeepZoomGenerator

import matplotlib.pyplot as plt


from PIL import Image,ImageFile

#非病理图像太大时会触发DecompressionBombWarning报错
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

#读取图像，生成OpenSlide对象
def load_slide(imagePath):

	slide = openslide.open_slide(imagePath)

	#查看OpenSlide对象信息
	print('slide 每一层级的维度信息为：%s' % str(slide.level_dimensions))
	print('slide 的层级为: %d' % slide.level_count)

	return slide

#生成deepzoom
def generate_deepzoom(osr, tile_size, overlap, limit_bounds):
	zoomslide = DeepZoomGenerator(osr, tile_size, overlap, limit_bounds)
	
	print('生成的层数为：%d' % zoomslide.level_count)
	print('生成的tile总数为： %d ' % zoomslide.tile_count)
	print('每一层的瓦片块数为：%s' % str(zoomslide.level_tiles))
	print('每一层的维度信息为：%s' % str(zoomslide.level_dimensions))

	return zoomslide



#将生成的图块保存到目录中
def write_tiles(deepzoomslide, format, basename):
	for level in range(deepzoomslide.level_count):
		tiledir = os.path.join(tilePath, "%s_files" % basename, str(level))
		if not os.path.exists(tiledir):
			os.makedirs(tiledir)
		cols, rows = deepzoomslide.level_tiles[level]
		for row in range(rows):
			for col in range(cols):
				tilename = os.path.join(tiledir, '%d_%d.%s' %(col, row, format))
				if not os.path.exists(tilename):
					tile = deepzoomslide.get_tile(level, (col, row))
					tile.save(tilename)
										
#保存dzi文件
def write_dzi(deepzoomslide, format, basename):
	dziPath = tilePath + "%s.dzi" % basename
	with open(dziPath, 'w') as f:
		f.write(deepzoomslide.get_dzi(format))

if __name__ == '__main__':

	imagePath="/Users/xiaojiao/myWork/openslide/towerBabel.jpeg"
	tilePath="/Users/xiaojiao/myWork/openseadragon/towerBabel_1024/"

	timeStart = time.time()
	timeStr = time.strftime('%Y-%m-%d- %H:%M:%S',time.localtime(timeStart))
	print('start at %s ...' % timeStr)

	slide = load_slide(imagePath)
	#获取部分区域并显示
	#指定第二层级，从坐标（10，10）为左上角开始的长、宽分别为100，100的图像
	#region1 = slide.read_region((10,10), 2, (100,100))

	#plt.imshow(region1)
	#plt.show()

	tile_size = 1024
	overlap = 0
	limit_bounds = False
	
	zoomslide = generate_deepzoom(slide, tile_size, overlap, limit_bounds)
	
	basename = "tiles"
	format = "jpg"
	write_tiles(zoomslide, format, basename)
	write_dzi(zoomslide, format, basename)

	slide.close()
	timeEnd = time.time()
	timeStr = time.strftime('%Y-%m-%d- %H:%M:%S',time.localtime(timeEnd))
	print("runtime = %d seconds" % (timeEnd - timeStart))








