
from collections import namedtuple



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

	def process_input(self, pygameview):
		for event in pygameview.events:
			if right:
				if cur_page.selected_subrow_index >= len(cur_page.rows[curpage.selected_row_index].subrows)-1:
					# cur_page = next page
					continue # don't pass this event to the new cur_page
			
			if left:
				if cur_page.selected_subrow_index == 0 or len(curpage.rows[cur_page.selected_row_index].subrows) == 0:
					# cur_page = prev page
					continue # don't pass this event to the new cur_page

			# cur_page.process_one_input_key(event)


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
def make_pages(rows, page_height, font, header_rows=[], footer_rows=[], add_page_count_footer=True, loopable=True):
	if add_page_count_footer:
		prev_page_row = make_row_from_text('<<<', font)
		next_page_row = make_row_from_text('>>>', font)
		prev_page_row.selectable = True
		next_page_row.selectable = True

		footer_rows.append( MultiRow(next_page_row, make_row_from_text(" Page ww/ww ", font), next_page_row) )

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
		if sum(row.height for row in rows) > height:
			self.scrolls = True

		self.rows = []
		for row in rows:
			if not isinstance(row, MultiRow):
				self.rows.append(MultiRow(row))
			else
				self.rows.append(row)

		self.selected_row_index = 0
		self.selected_subrow_index = 0
		self.scroll_index = 0

	def process_one_input_key(self, pygameview, event, up_keys, down_keys, left_keys, right_keys):
		if evt.type != pygame.KEYDOWN:
			return

		if event.key in up_keys:
			self.selected_row_index = max(0, self.selected_row_index-1)
			
			if self.selected_row_index == self.scroll_index:
				self.scroll_index = max(0, self.scroll_index-1)
		if event.key in down_keys:
			self.selected_row_index = min(self.selected_row_index+1, len(self.rows)-1)
			
			if self.selected_row_index != len(self.rows)-1:
				next_row_index = min(self.selected_row_index+1, len(self.rows)-1)
				cur_height_to_selection = sum(row.height for row in self.rows[self.scroll_index:self.selected_row_index])
				if cur_height_to_selection + self.rows[next_row_index].height > self.height:
					self.scroll_index += 1

		if event.key in right_keys:
			self.selected_subrow_index += 1
			self.selected_subrow_index = min(self.selected_subrow_index, len(rows[selectedindex].subrows-1))
		if event.key in left_keys:
			max_subrow_index = min(len(self.rows[self.selected_row_index].subrows)-1, 0)
			if self.selected_subrow_index >= len(self.rows[self.selected_row_index].subrows)-1: # if it appears that the last subrow is already selected, change the max to the second to last subrow, so the left key appears to function as normal
				max_subrow_index = min(len(self.rows[self.selected_row_index].subrows)-2, 0)

			self.selected_subrow_index -= 1
			self.selected_subrow_index = max(0, min(self.selected_subrow_index, max_subrow_index))
		
		pygameview.examine_target = rows[selectedindex].subrows[min(selectedsubrowindex, len(rows[selectedindex].subrows))]
		

	def draw(self, pygameview, draw_pane, x, y):
		cur_y = y
		for row in self.rows[self.scroll_index:]:
			if cur_y >= self.height:
				return
			
			row.draw(x, cur_y)
			cur_y += row.height
	


Word = namedtuple("Word", "text color")
class Row():
	def __init__(self, width, height):
		self.width = width
		self.height = height
 
	def draw(self, pygameview, draw_pane, x, y):
		font = self.font
		linesize = self.font
		for line in self.lines:
			for word in line:
				pygameview.draw_string(word.text+" ", word.color, cur_x, cur_y mouse_content=self if self.selectable else None)


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
		RiftWizard.draw_spell_icon(self.spell, draw_pane, x, y, grey=False, animated=False):
		Row.draw(self, pygameview, draw_pane, x+16, y, font, linesize)


# for stuff like "<<< Page 3/7 >>>" which has two selectable buttons and one non selectable text on the same row
# can also be used to implement the key rebind screen and other grids
class MultiRow():
	def __init__(self, *args):
		self.subrows = args
		self.width = sum(subrow.width for subrow in self.subrows)
		self.height = max(subrow.height for subrow in self.subrows)

	def draw(self, pygameview, draw_pane, x, y):
		for row in self.subrows:
			row.draw(pygameview, draw_pane, x, y)
			x += row.width





	

# modified from RiftWizard.PyGameView.draw_wrapped_string
def string_to_words(string, width, font, linesize, color=(255, 255, 255), indent=False, extra_space=False):
	lines = string.split('\n')
	processed_lines = []

	cur_x = x
	cur_y = y
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
		cur_x = x
		assert(all(len(word) < chars_per_line) for word in words)

		while words:
			cur_color = color

			word = words.pop()
			if word != ' ':

				# Process complex tooltips- strip off the []s and look up the color
				if word and word[0] == '[' and word[-1] == ']':
					tokens = word[1:-1].split(':')
					if len(tokens) == 1:
						word = tokens[0] # todo- fmt attribute?
						cur_color = tooltip_colors[word.lower()].to_tup()
					elif len(tokens) == 2:
						word = tokens[0].replace('_', ' ')
						cur_color = tooltip_colors[tokens[1].lower()].to_tup()

				max_size = chars_left if word in [' ', '.', ','] else chars_left - 1
				if len(word) > max_size:
					cur_y += linesize
					num_lines += 1
					# Indent by one for next line
					cur_x = x + char_width
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



def row_from_size(width, height):
	return Row(width, height)

def row_from_text(text, font, linesize, width=None, height=0):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = Row(width, max(text_height, height))
	row.lines = lines
	row.font = font
	row.linesize = linesize
	return row

def row_from_text_and_icon(text, font, linesize, icon_asset, width=None, height=0):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = RowWithIcon(width, max(text_height, height))
	row.lines = lines
	row.icon_asset = icon_asset
	row.font = font
	row.linesize = linesize

	return row

# also works for items
def row_from_text_and_spell(text, font, linesize, spell, width=None, height=0):
	if width == None:
		width = font.size(text)[0]

	lines = string_to_words(text, width, font, linesize)
	text_height = len(lines)*linesize
	row = RowWithSpellIcon(width, max(text_height, height))
	row.lines = lines
	row.spell = spell
	row.font = font
	row.linesize = linesize

	return row


