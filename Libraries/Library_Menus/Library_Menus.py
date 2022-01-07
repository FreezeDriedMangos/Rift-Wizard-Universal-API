
from collections import namedtuple
import pygame


####################################################
# Importing RiftWizard.py                          |
# Credit to trung on discord                       |
#                                                  |
#----------------------------------------------    |
import inspect #                                   |
def get_RiftWizard(): #                            |
    # Returns the RiftWizard.py module object      |
    for f in inspect.stack()[::-1]: #              |
        if "file 'RiftWizard.py'" in str(f): #     |
            return inspect.getmodule(f[0]) #       |
	 #                                             |
    return inspect.getmodule(f[0]) #               |
#                                                  |
RiftWizard = get_RiftWizard() #                    |
#                                                  |
#                                                  |
####################################################


class Menu():
	def __init__(self, pages):
		self.pages = pages
		self.cur_page_index = 0
		self.loops = False
		# self.can_scroll_pages_on_select_header = False

	def process_input(self, pygameview, up_keys, down_keys, left_keys, right_keys, confirm_keys):
		for event in pygameview.events:
			if event.type != pygame.KEYDOWN:
				continue

			cur_page = self.pages[self.cur_page_index]

			if event.key in right_keys:
				if cur_page.selected_subrow_index >= len(cur_page.rows[cur_page.selected_row_index].subrows)-1: # if the last subrow appears to be selected
					self.cur_page_index += 1
					if self.loops:
						self.cur_page_index %= len(self.pages)
					else:
						self.cur_page_index = min(self.cur_page_index, len(self.pages)-1)

					next_page = self.pages[self.cur_page_index]
					next_page.selected_row_index = cur_page.selected_row_index
					next_page.selected_subrow_index = 0

					continue # don't pass this event to the new cur_page
			
			if event.key in left_keys:
				if cur_page.selected_subrow_index == 0 or len(cur_page.rows[cur_page.selected_row_index].subrows) == 0: # if subrow 0 appears to be selected
					self.cur_page_index -= 1
					if self.loops:
						self.cur_page_index = self.cur_page_index if self.cur_page_index >= 0 else len(self.pages)-1
					else:
						self.cur_page_index = max(self.cur_page_index, 0)

					next_page = self.pages[self.cur_page_index]
					next_page.selected_row_index = cur_page.selected_row_index
					next_page.selected_subrow_index = len(next_page.rows[next_page.selected_row_index].subrows)-1

					continue # don't pass this event to the new cur_page

			cur_page.process_one_input_key(pygameview, event, up_keys, down_keys, left_keys, right_keys, confirm_keys)
			

		#
		# Mouse
		#

		cur_page = self.pages[self.cur_page_index]

		mouse_dx, mouse_dy = pygameview.get_mouse_rel()
		if mouse_dx or mouse_dy:
			pygameview.examine_target = None

			mx, my = pygameview.get_mouse_pos()
			for r, c in pygameview.ui_rects:
				if r.collidepoint((mx, my)):
					pygameview.examine_target = c.mouse_content

					# search for any subrow with mouse_content = c.mouse_content
					br = False
					for (row, row_index) in zip(cur_page.rows, range(0, len(cur_page.rows))):
						for (subrow, sub_row_index) in zip(row.subrows, range(0, len(row.subrows))):
							if subrow.mouse_content == pygameview.examine_target:
								cur_page.selected_row_index = row_index
								cur_page.selected_subrow_index = sub_row_index
								br = True
								break
						if br:
							break
					break


		for evt in pygameview.events:
			if not evt.type == pygame.MOUSEBUTTONDOWN:
				continue

			mx, my = pygameview.get_mouse_pos()
			for r, c in pygameview.ui_rects:
				if r.collidepoint((mx, my)):
					pygameview.examine_target = c.mouse_content

					if evt.button == pygame.BUTTON_LEFT:
						if c.on_confirm_callback:
							c.on_confirm_callback()

			
	def draw(self, pygameview, draw_pane, x, y):
		cur_page = self.pages[self.cur_page_index]
		cur_page.draw(pygameview, draw_pane, x, y)


def make_menu_from_rows(rows, page_height, font, linesize, header_rows=[], footer_rows=[], add_page_count_footer=True, loopable=True):
	return Menu(make_pages(rows, page_height, font, linesize, header_rows= header_rows, footer_rows=footer_rows, add_page_count_footer=add_page_count_footer, loopable=loopable))

def make_single_page_menu_from_rows(rows, page_height):
	page = Page(rows, page_height)
	# page.draw_elipsis = True
	return Menu([page])

def make_menu_from_pages(pages):
	return Menu(page)

# def make_pages(rows, page_height):
# 	pages = []
# 	cur_page_rows = []
# 	cur_y = 0

# 	for row in rows:
# 		if row.height+cur_y > page_height:
# 		pages.append(Page(rows, page_height))
# 		cur_page_rows = []
# 		cur_y = 0
# 		cur_y += row.height
# 		cur_page_rows.append(row)

# 	return pages

# to make a menu that doesn't scroll and has pages instead
def make_pages(rows, page_height, font, linesize, header_rows=[], footer_rows=[], add_page_count_footer=True, loopable=True):
	if add_page_count_footer:
		prev_page_row = row_from_text('<<<', font, linesize)
		next_page_row = row_from_text('>>>', font, linesize)
		prev_page_row.selectable = True
		next_page_row.selectable = True

		footer_rows.append( MultiRow(next_page_row, row_from_text(" Page ww/ww ", font, linesize), next_page_row) )

	footer_height = sum(row.height for row in footer_rows)
	header_height = sum(row.height for row in header_rows)
	effective_page_height = page_height - header_height - footer_height

	pages = []
	cur_page_rows = []
	cur_y = 0

	rows.append(Row(1, 999999999)) # to force the rows the last page to be created in the for loop


	for row in rows:
		if row.height+cur_y > effective_page_height:
			pages.append(Page(header_rows+rows+footer_rows, page_height))
			cur_page_rows = []
			cur_y = 0

		cur_y += row.height
		cur_page_rows.append(row)

	# at this point, cur_page_rows should = [Row(1, 999999999)]

	if add_page_count_footer:
		if not loopable: 
			# remove the back arrow from the first page
			pages[0].rows[-1].subrows[0] = row_from_text("   ")
			# remove the forward arrow from the last page
			pages[-1].rows[-1].subrows[-1] = row_from_text("   ")

		# correct the page numbers
		for (page, i) in zip(pages, range(0, len(pages))):
			page_num = " "+str(i+1) if len(pages) >= 10 and i+1 < 10 else str(i+1)
			page.rows[-1].subrows[1].text = " " + "Page " + page_num + "/" + str(len(pages))

	return pages


class Page():
	def __init__(self, rows, height):
		self.width = rows[0].width
		self.height = height

		if sum(row.height for row in rows) > height:
			self.scrolls = True

		self.rows = []
		for row in rows:
			if not isinstance(row, MultiRow):
				self.rows.append(MultiRow(row))
			else:
				self.rows.append(row)

		self.selected_row_index = 0
		self.selected_subrow_index = 0
		self.scroll_index = 0
		self.second_to_last_row_drawn = None
		self.last_row_drawn = None

		selectable_rows = [index for (row, index) in zip(self.rows, range(len(self.rows))) if row.selectable] + [0]
		self.selected_row_index = selectable_rows[0]

		self.scroll_up_on_last_selectable_row = True
		self.scroll_down_on_last_selectable_row = True

		self.draw_elipsis = False

	def process_one_input_key(self, pygameview, event, up_keys, down_keys, left_keys, right_keys, confirm_keys):
		if event.type != pygame.KEYDOWN:
			return


		maxindex = len(self.rows)-1
		selectedindex = min(self.selected_row_index, maxindex)
		maxsubindex = len(self.rows[selectedindex].subrows)-1
		selectedsubindex = min(self.selected_subrow_index, maxsubindex)

		if not self.rows[selectedindex].subrows[selectedsubindex].selectable:
			subrows = self.rows[selectedindex].subrows[selectedsubindex:]
			selectable_subrows = [index for (subrow, index) in zip(subrows, range(selectedsubindex, selectedsubindex+len(subrows))) if subrow.selectable] + [selectedsubindex, selectedsubindex]
			selectedsubindex = selectable_subrows[0]

		# if nothing's selected in the menu, just select what we were last on
		if not self.rows[selectedindex].selectable or pygameview.examine_target != self.rows[selectedindex].subrows[selectedsubindex].mouse_content:
			selected_subrow = self.rows[selectedindex].subrows[min(selectedsubindex, len(self.rows[selectedindex].subrows))]
			if not selected_subrow.selectable:
				# options = [row for row in self.rows[selectedindex].subrows if row.selectable] + [selected_subrow]
				# selected_subrow = options[0]

				# ensure that a selectable subrow is selected
				rows = self.rows[selectedindex:]
				selectable_rows = [index for (row, index) in zip(rows, range(selectedindex, selectedindex+len(rows))) if row.selectable] + [selectedindex, selectedindex]
				self.selected_row_index = selectable_rows[0]
				selectedindex = self.selected_row_index
				
				subrows = self.rows[selectedindex].subrows[selectedsubindex:]
				selectable_subrows = [index for (subrow, index) in zip(subrows, range(selectedsubindex, selectedsubindex+len(subrows))) if subrow.selectable] + [selectedsubindex, selectedsubindex]
				self.selected_subrow_index = selectable_subrows[0]
				selectedsubindex = self.selected_subrow_index

				selected_subrow = self.rows[selectedindex].subrows[selectedsubindex]


			pygameview.examine_target = selected_subrow.mouse_content

			self.selected_row_index = selectedindex
			self.selected_subrow_index = selectedsubindex
			return

		if event.key in up_keys:
			rows = self.rows[:selectedindex]
			selectable_rows = [selectedindex] + [index for (row, index) in zip(rows, range(len(rows))) if row.selectable]
			# selectable_rows = [index for (row, index) in zip(rows, range(len(rows))) if row.selectable]
			self.selected_row_index = selectable_rows[-1]

			# if the previous row is offscreen, scroll up
			if self.selected_row_index == self.scroll_index:
				self.scroll_index = max(0, self.scroll_index-1)
			if self.scroll_up_on_last_selectable_row and selectedindex == self.selected_row_index:
				self.scroll_index = max(0, self.scroll_index-1)

		if event.key in down_keys:
			# self.selected_row_index = min(selectedindex+1, maxindex)
			rows = self.rows[selectedindex:]
			selectable_rows = [index for (row, index) in zip(rows, range(selectedindex, selectedindex+len(rows))) if row.selectable] + [selectedindex, selectedindex]
			self.selected_row_index = selectable_rows[1]

			# if the next row is off the screen, scroll down
			if self.selected_row_index < maxindex:
				# next_row_index = max(self.selected_row_index+1, len(self.rows)-1)
				# cur_height_to_selection = sum(row.height for row in self.rows[self.scroll_index:self.selected_row_index])
				# if cur_height_to_selection + self.rows[next_row_index].height > self.height: 
				# 	self.scroll_index += 1
				# 	print('height to selection: ' + str(cur_height_to_selection) + '   next row height: ' + str(self.rows[next_row_index].height) +'   page height: ' + str(self.height))
				on_last_selectable_row = selectedindex == self.selected_row_index
				if self.rows[selectedindex] == self.second_to_last_row_drawn or (self.scroll_down_on_last_selectable_row and on_last_selectable_row and self.last_row_drawn != self.rows[-1]):
					self.scroll_index += 1


		selectedindex = min(self.selected_row_index, maxindex)
		maxsubindex = len(self.rows[selectedindex].subrows)-1
		selectedsubindex = min(self.selected_subrow_index, maxsubindex)
		if not self.rows[selectedindex].subrows[selectedsubindex].selectable:
			subrows = self.rows[selectedindex].subrows[selectedsubindex:]
			selectable_subrows = [index for (subrow, index) in zip(subrows, range(selectedsubindex, selectedsubindex+len(subrows))) if subrow.selectable] + [selectedsubindex, selectedsubindex]
			selectedsubindex = selectable_subrows[0]


		if event.key in right_keys:
			subrows = self.rows[selectedindex].subrows[selectedsubindex:]
			selectable_subrows = [index for (subrow, index) in zip(subrows, range(selectedsubindex, selectedsubindex+len(subrows))) if subrow.selectable] + [selectedsubindex, selectedsubindex]
			self.selected_subrow_index = selectable_subrows[1]
			selectedsubindex = self.selected_subrow_index

			# self.selected_subrow_index = min(selectedsubindex+1, maxsubindex)

		if event.key in left_keys:
			subrows = self.rows[selectedindex].subrows[:selectedsubindex]
			selectable_subrows = [selectedsubindex] + [index for (subrow, index) in zip(subrows, range(len(subrows))) if subrow.selectable] 
			self.selected_subrow_index = selectable_subrows[-1]
			selectedsubindex = self.selected_subrow_index

			# self.selected_subrow_index = max(0, selectedsubindex-1)

		selected_row = self.rows[selectedindex].subrows[min(selectedsubindex, len(self.rows[selectedindex].subrows))]

		if selected_row.on_select_callback:
			selected_row.on_select_callback()

		if event.key in confirm_keys and selected_row.on_confirm_callback:
			selected_row.on_confirm_callback()
		
		pygameview.examine_target = selected_row.mouse_content
		

	def draw(self, pygameview, draw_pane, x, y):
		cur_y = y
		cur_x = x

		first_row_index = self.scroll_index

		if self.draw_elipsis and self.scroll_index != 0:
			pygameview.draw_string("...", draw_pane, cur_x, cur_y)
			cur_y += pygameview.linesize
			first_row_index += 1

		for row in self.rows[first_row_index:]:
			if cur_y >= self.height:
				return
			
			if self.draw_elipsis and row.height + cur_y >= self.height:
				pygameview.draw_string("...", draw_pane, cur_x, cur_y)
				cur_y += pygameview.linesize
			else:
				if row.center: 
					cur_x += self.width//2
				row.draw(pygameview, draw_pane, cur_x, cur_y)
				cur_y += row.height
				cur_x = x
			

			self.second_to_last_row_drawn = self.last_row_drawn
			self.last_row_drawn = row
	


Word = namedtuple("Word", "text color")
class Row():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.on_confirm_callback = None
		self.center = False
		self.on_select_callback = None
		self.selectable = False
		self.mouse_content = self
 
	def draw(self, pygameview, draw_pane, x, y):
		if not hasattr(self, 'font'):
			return
		font = self.font
		linesize = self.font
		cur_x = x
		cur_y = y
		for line in self.lines:
			cur_x = x
			if self.center:
				cur_x -= sum(self.font.size(word.text+" ")[0] for word in line)//2

			for word in line:
				old_linesize = pygameview.linesize
				pygameview.linesize = self.linesize
				pygameview.draw_string(word.text+" ", draw_pane, cur_x, cur_y, color=word.color, mouse_content=self.mouse_content if self.selectable else None, font=self.font)
				pygameview.linesize = old_linesize

				cur_x += self.font.size(word.text+" ")[0]
			
			cur_y += self.linesize

	def set_text(self, text):
		self.lines = string_to_words(text, self.width, self.font, self.linesize)


class RowWithIcon(Row):
	def draw(self, pygameview, draw_pane, x, y):
		# draw icon
		icon = RiftWizard.get_image(self.icon_asset, alphafy=True)
		if icon:
			surface.blit(icon, (x, y))

		Row.draw(self, pygameview, draw_pane, x+icon.get_width(), y)
	
class RowWithSpellIcon(Row):
	def draw(self, pygameview, draw_pane, x, y):
		# draw icon
		RiftWizard.draw_spell_icon(self.spell, draw_pane, x, y, grey=False, animated=False)
		Row.draw(self, pygameview, draw_pane, x+16, y)


# for stuff like "<<< Page 3/7 >>>" which has two selectable buttons and one non selectable text on the same row
# can also be used to implement the key rebind screen and other grids
class MultiRow():
	def __init__(self, *args):
		self.subrows = args
		self.width = sum(subrow.width for subrow in self.subrows)
		self.height = max(subrow.height for subrow in self.subrows)
		self.center = args[0].center

		self.selectable = any(row.selectable for row in self.subrows)

	def draw(self, pygameview, draw_pane, x, y):
		for row in self.subrows:
			row.draw(pygameview, draw_pane, x, y)
			x += row.width

	def on_confirm_callback():
		for row in self.subrows:
			if row.on_confirm_callback:
				row.on_confirm_callback()

	def on_select_callback():
		for row in self.subrows:
			if row.on_select_callback:
				row.on_select_callback()




import re

# modified from RiftWizard.PyGameView.draw_wrapped_string
def string_to_words(string, width, font, linesize, color=(255, 255, 255), indent=False, extra_space=False):
	lines = string.split('\n')
	processed_lines = [[]]

	cur_x = 0
	cur_y = 0
	# linesize = linesize
	tooltip_colors = RiftWizard.tooltip_colors
	num_lines = 0

	char_width = font.size('w')[0]
	chars_per_line = width // char_width
	for line in lines:
		#words = line.split(' ')
		# This regex separates periods, spaces, commas, and tokens
		exp = '[\[\]:|\w\|\'|%|-]+|.| |,'
		words = re.findall(exp, line)
		words.reverse()
		cur_line = "" 
		chars_left = chars_per_line

		# Start each line all the way to the left
		cur_x = 0
		assert(all(len(word) < chars_per_line) for word in words)

		while words:
			cur_color = color

			word = words.pop()
			if word != ' ':

				# Process complex tooltips- strip off the []s and look up the color
				if word and word[0] == '[' and word[-1] == ']':
					original_word = word
					try:
						tokens = word[1:-1].split(':')
						if len(tokens) == 1:
							word = tokens[0] # todo- fmt attribute?
							cur_color = tooltip_colors[word.lower()].to_tup()
						elif len(tokens) == 2:
							word = tokens[0].replace('_', ' ')
							cur_color = tooltip_colors[tokens[1].lower()].to_tup()
					except:
						word = original_word

				max_size = chars_left if word in [' ', '.', ','] else chars_left - 1
				if len(word) > max_size:
					cur_y += linesize
					num_lines += 1
					# Indent by one for next line
					cur_x = 0 + char_width
					chars_left = chars_per_line

				# self.draw_string(word, surface, cur_x, cur_y, cur_color, content_width=width)	
				processed_lines[-1].append(Word(word, cur_color))			
			
			cur_x += (len(word)) * char_width
			chars_left -= len(word)

		cur_y += linesize
		num_lines += 1
		if extra_space:
			cur_y += linesize
			num_lines += 1
			processed_lines.append([Word(" ", color)])	

	return processed_lines



def row_from_size(width, height, custom_draw_function=None, selectable=False, on_confirm_callback=None, center=False, mouse_content=None):
	row = Row(width, height)
	if custom_draw_function:
		row.draw = custom_draw_function

	row.selectable = selectable
	row.on_confirm_callback = on_confirm_callback
	row.center = center

	if mouse_content != None:
		row.mouse_content = mouse_content

	return row

def row_from_text(text, font, linesize, width=None, height=0, selectable=False, on_confirm_callback=None, center=False):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = Row(width, max(text_height, height))
	row.lines = lines
	row.font = font
	row.linesize = linesize
	row.selectable = selectable
	row.on_confirm_callback = on_confirm_callback
	row.center = center

	return row

def row_from_text_and_icon(text, font, linesize, icon_asset, width=None, height=0, selectable=False, on_confirm_callback=None, center=False):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = RowWithIcon(width, max(text_height, height))
	row.lines = lines
	row.icon_asset = icon_asset
	row.font = font
	row.linesize = linesize
	row.selectable = selectable
	row.on_confirm_callback = on_confirm_callback
	row.center = center

	return row

# also works for items
def row_from_text_and_spell(text, font, linesize, spell, width=None, height=0, selectable=False, on_confirm_callback=None, center=False):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = RowWithSpellIcon(width, max(text_height, height))
	row.lines = lines
	row.spell = spell
	row.font = font
	row.linesize = linesize
	row.selectable = selectable
	row.on_confirm_callback = on_confirm_callback

	return row

# also works for items
def row_from_spell(spell, font, linesize, width=None, height=0, selectable=False, on_confirm_callback=None, center=False):
	return row_from_text_and_spell(spell.name, font, linesize, spell, width=width, height=height, selectable=selectable, on_confirm_callback=on_confirm_callback, center=center)


