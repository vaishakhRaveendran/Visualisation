import pygame
import random
import math
pygame.init()


#CLASS OF VARIABLES
class DrawInformation:
	BLACK = 0, 0, 0
	WHITE = 183, 196, 208
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = WHITE

	GRADIENTS = [
		(238, 227, 203),
		(215, 192, 174),
		(150, 126, 118)
	]

	FONT = pygame.font.SysFont('arial', 30)
	LARGE_FONT = pygame.font.SysFont('arial', 40)

	SIDE_PAD = 120
	TOP_PAD = 150

	def __init__(self, width, height, lst):
		self.width = width
		self.height = height

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Xenon")
		self.set_list(lst)

	def set_list(self, lst):
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)


	title = draw_info.LARGE_FONT.render(f"{algo_name}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))


	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting", 1, draw_info.BLACK)
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))

	
	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort |S -Selection Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	
	

	draw_list(draw_info)
	pygame.display.update()


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst
 #clearing only the portion of screen which is being used for sorting.
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		#redrawing
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

 #Finding the leftTop(x,y)for each block
	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

		color = draw_info.GRADIENTS[i % 3]
  #manually recoloring blocks that is being sorted.
		if i in color_positions:
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

	if clear_bg:#if we have redrawn some portion make sure that we update. 
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)
		lst.append(val)

	return lst


def selection_sort(draw_info,ascending=True):
  lst=draw_info.lst
  size = len(lst)
  for i in range(size-1):
      smallIndex = i
      for j in range(i, size):
          if lst[j] < lst[smallIndex]:
              smallIndex = j
      lst[i], lst[smallIndex] = lst[smallIndex], lst[i]
      draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True) 
      yield True
  return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				#in this block itself we are going to manually draw the blocks sorted.Redraw entire blocks and color present blocks
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True
				#pausing the bubble sort function everytime a swap happens.Wait for calling this next time
				#this helps to retain control over reset and exit while the program runs.


	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)
	draw_info = DrawInformation(1000, 800, lst)
	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None

	while run:
		clock.tick(60)

  #Continously calling the generatoru next method if sorting is true.
		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				#storing the generator object when the sorting algorithm is called.
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"
			elif event.key == pygame.K_s and not sorting:
				sorting_algorithm = selection_sort
				sorting_algo_name = "Selection Sort"


	pygame.quit()


if __name__ == "__main__":
	main()
