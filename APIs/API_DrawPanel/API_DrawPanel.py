from typing import List
import Level
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

class PanelItem:

    def __init__(self, order):
        self.order = order
        self.view = None

    def setup(self):
        pass

    def should_draw(self):
        return True

    def get_height(self):
        return 0

    def draw(self, cur_x, cur_y):
        pass

    def __getattr__(self, attribute):
        # Redirect accesses to 
        return getattr(self.view, attribute)

class PanelHP(PanelItem):
    
    def get_height(self):
        return self.linesize

    def get_hp_color(self):
        hpcolor = (255, 255, 255)
        if self.game.p1.cur_hp <= 25:
            hpcolor = (255, 0, 0)
        return hpcolor

    def draw(self, cur_x, cur_y):
        hpcolor = self.get_hp_color()

        self.draw_string("%s %d/%d" % (RiftWizard.CHAR_HEART, self.game.p1.cur_hp, self.game.p1.max_hp), self.character_display, cur_x, cur_y, color=hpcolor)
        self.draw_string("%s" % RiftWizard.CHAR_HEART, self.character_display, cur_x, cur_y, (255, 0, 0))

class PanelShield(PanelItem):

    def get_height(self):
        return self.linesize

    def should_draw(self):
        return self.game.p1.shields

    def draw(self, cur_x, cur_y):
        self.draw_string("%s %d" % (RiftWizard.CHAR_SHIELD, self.game.p1.shields), self.character_display, cur_x, cur_y)
        self.draw_string("%s" % (RiftWizard.CHAR_SHIELD), self.character_display, cur_x, cur_y, color=RiftWizard.COLOR_SHIELD.to_tup())

class PanelXP(PanelItem):

    def get_height(self):
        return self.linesize

    def draw(self, cur_x, cur_y):
        self.draw_string("SP %d" % self.game.p1.xp, self.character_display, cur_x, cur_y, color=RiftWizard.COLOR_XP)

class PanelRealm(PanelItem):

    def get_height(self):
        return self.linesize

    def draw(self, cur_x, cur_y):
        self.draw_string("Realm %d" % self.game.level_num, self.character_display, cur_x, cur_y)

def get_spell_color(self: Level.Spell):
    return (255, 255, 255)

def get_cost_string(self: Level.Spell):
    cost_str = ""
    if self.max_charges:
        cost_str += "%2d" % self.cur_charges
    if self.caster.cool_downs.get(self, 0) > 0:
        cost_str += "(%d)" % self.caster.cool_downs.get(self, 0)
    return cost_str

Level.Spell.get_spell_color = get_spell_color
Level.Spell.get_cost_string = get_cost_string

class PanelSpells(PanelItem):

    def get_height(self):
        return self.linesize * (1 + len(self.game.p1.spells))

    def get_spell_color(self, spell):
        if spell == self.cur_spell:
            cur_color = (0, 255, 0)
        elif spell.can_pay_costs():
            cur_color = spell.get_spell_color()
        else:
            cur_color = (128, 128, 128)
        return cur_color

    def get_cost_string(self, spell: Level.Spell):
        return spell.get_cost_string()

    def draw(self, cur_x, cur_y):
        self.draw_string("Spells:", self.character_display, cur_x, cur_y)
        cur_y += self.linesize

        # Spells
        index = 1
        for spell in self.game.p1.spells:
            spell_number = (index) % 10
            mod_key = 'C' if index > 20 else 'S' if index > 10 else ''
            hotkey_str = "%s%d" % (mod_key, spell_number)

            cur_color = self.get_spell_color(spell)

            cost_str = self.get_cost_string(spell)
            
            name_fmt = "%%-%ds" % (19-len(cost_str))
            name_str = name_fmt % spell.name
            fmt = "%2s  %s%s" % (hotkey_str, name_str, cost_str)

            self.draw_string(fmt, self.character_display, cur_x, cur_y, cur_color, mouse_content=RiftWizard.SpellCharacterWrapper(spell), char_panel=True)
            self.draw_spell_icon(spell, self.character_display, cur_x + 38, cur_y)

            cur_y += self.linesize
            index += 1

class PanelItems(PanelItem):

    def get_height(self):
        return self.linesize * (1 + len(self.game.p1.items))

    def draw(self, cur_x, cur_y):
        self.draw_string("Items:", self.character_display, cur_x, cur_y)
        cur_y += self.linesize

        # Items
        index = 1
        for item in self.game.p1.items:

            hotkey_str = "A%d" % (index % 10)

            cur_color = (255, 255, 255)
            if item.spell == self.cur_spell:
                cur_color = (0, 255, 0)
            fmt = "%2s  %-17s%2d" % (hotkey_str, item.name, item.quantity)			

            self.draw_string(fmt, self.character_display, cur_x, cur_y, cur_color, mouse_content=item)
            self.draw_spell_icon(item, self.character_display, cur_x + 38, cur_y)

            cur_y += self.linesize
            index += 1

class PanelBuffs(PanelItem):

    def setup(self):
        self.status_effects = [b for b in self.game.p1.buffs if b.buff_type != RiftWizard.BUFF_TYPE_PASSIVE]
        self.counts = {}
        for effect in self.status_effects:
            if effect.name not in self.counts:
                self.counts[effect.name] = (effect, 0, 0, None)
            _, stacks, duration, color = self.counts[effect.name]
            stacks += 1
            duration = max(duration, effect.turns_left)

            self.counts[effect.name] = (effect, stacks, duration, effect.get_tooltip_color().to_tup())

    def get_height(self):
        return self.linesize * (2 + len(self.counts))

    def should_draw(self):
        return self.status_effects

    def draw(self, cur_x, cur_y):
        # Buffs
        
        cur_y += self.linesize
        self.draw_string("Status Effects:", self.character_display, cur_x, cur_y, (255, 255, 255))
        cur_y += self.linesize
        for buff_name, (buff, stacks, duration, color) in self.counts.items():
            fmt = buff_name
            if stacks > 1:
                fmt += ' x%d' % stacks
            if duration:
                fmt += ' (%d)' % duration
            self.draw_string(fmt, self.character_display, cur_x, cur_y, color, mouse_content=buff)
            cur_y += self.linesize

class PanelSkills(PanelItem):
    def setup(self):
        self.skills = [b for b in self.game.p1.buffs if b.buff_type == RiftWizard.BUFF_TYPE_PASSIVE and not b.prereq]
    
    def get_height(self): # This is scuffed. Might want to just make draw return the height.....
        height = self.linesize * 2
        cur_x = self.border_margin
        skill_x_max = self.character_display.get_width() - self.border_margin - 16
        for skill in self.skills:
            cur_x += 18
            if cur_x > skill_x_max:
                cur_x = self.border_margin
                height += self.linesize
        return height

    def should_draw(self):
        return self.skills

    def draw(self, cur_x, cur_y):
        cur_y += self.linesize

        self.draw_string("Skills:", self.character_display, cur_x, cur_y)
        cur_y += self.linesize

        skill_x_max = self.character_display.get_width() - self.border_margin - 16
        for skill in self.skills:
            self.draw_spell_icon(skill, self.character_display, cur_x, cur_y)
            cur_x += 18
            if cur_x > skill_x_max:
                cur_x = self.border_margin
                cur_y += self.linesize

class PanelSeperator(PanelItem):

    def __init__(self, order, lines=1):
        super().__init__(order)
        self.lines = lines

    def get_height(self):
        return self.linesize * self.lines

PANEL_HP = PanelHP(0)
PANEL_SHIELDS = PanelShield(100)
PANEL_XP = PanelXP(200)
PANEL_REALM = PanelRealm(300)
PANEL_SPELLS = PanelSpells(400)
PANEL_ITEMS = PanelItems(500)
PANEL_BUFFS = PanelBuffs(600)
PANEL_SKILLS = PanelSkills(700)

character_panels: List[PanelItem] = [
    PANEL_HP,
    PANEL_SHIELDS,
    PANEL_XP,
    PANEL_REALM,
    PanelSeperator(350),
    PANEL_SPELLS,
    PanelSeperator(450),
    PANEL_ITEMS,
    PANEL_BUFFS,
    PANEL_SKILLS
]

def character_adjust(self: RiftWizard.PyGameView, num):
    scrollable = getattr(self, "character_panel_scrollable", False) # could __init__ hook to drop the getattr calls

    if scrollable:
        self.character_panel_scroll = getattr(self, "character_panel_scroll", 0) + num * self.linesize

        self.play_sound("menu_confirm")

def process_input_character(self: RiftWizard.PyGameView):

    for click in self.events:
        if click.type != pygame.MOUSEBUTTONDOWN:
            continue

        mx, my = self.get_mouse_pos()

        if mx > self.h_margin:
            continue

        if self.examine_target: #Examining something should scroll the right panel only
            continue

        if click.button == pygame.BUTTON_WHEELDOWN:
            character_adjust(self, 2)
        
        if click.button == pygame.BUTTON_WHEELUP:
            character_adjust(self, -2)

    pass

def get_character_scroll(self: RiftWizard.PyGameView):
    scroll = getattr(self, "character_panel_scroll", 0)

    panel_height = get_total_character_height(self)
    scrollable_height = self.character_display.get_height() - 2*self.border_margin - 3*self.linesize - 8
    max_scroll = panel_height - scrollable_height + self.linesize * 4 # A little buffer at the end

    scroll = max(scroll, 0)
    if max_scroll > 0:
        scroll = min(scroll, max_scroll)
    self.character_panel_scroll = scroll
    return scroll

def get_total_character_height(self: RiftWizard.PyGameView):
    height = 0

    for panel in character_panels:
        panel.view = self
        panel.setup()
        if panel.should_draw():
            height += panel.get_height()

    return height

def draw_character(self: RiftWizard.PyGameView):

    self.draw_panel(self.character_display)
    
    scrollable_width = self.character_display.get_width() - 2*self.border_margin
    scrollable_height = self.character_display.get_height() - 2*self.border_margin - 3*self.linesize - 8
    self.character_display.set_clip(pygame.Rect(self.border_margin, self.border_margin, scrollable_width, scrollable_height))

    self.char_panel_examine_lines = {}

    start_y = self.border_margin - get_character_scroll(self)

    cur_x = self.border_margin
    cur_y = start_y
    linesize = self.linesize

    character_panels.sort(key=lambda x: x.order)

    for panel in character_panels:
        panel.view = self
        panel.setup()
        if panel.should_draw():
            panel.draw(cur_x, cur_y)
            cur_y += panel.get_height()

    self.character_panel_scrollable = cur_y - start_y > scrollable_height

    cur_x = self.border_margin
    cur_y = self.character_display.get_height() - self.border_margin - 3*self.linesize

    self.character_display.set_clip(pygame.Rect(cur_x, cur_y, self.character_display.get_width() - self.border_margin - cur_x, self.character_display.get_height() - self.border_margin - cur_y))

    menu_keybind_str = pygame.key.name(self.key_binds[RiftWizard.KEY_BIND_ABORT][0]).upper()
    self.draw_string("Menu (%s)" % menu_keybind_str, self.character_display, cur_x, cur_y, mouse_content=RiftWizard.OPTIONS_TARGET)
    cur_y += linesize

    howto_keybind_str = pygame.key.name(self.key_binds[RiftWizard.KEY_BIND_HELP][0]).upper()
    self.draw_string("How to Play (%s)" % howto_keybind_str, self.character_display, cur_x, cur_y, mouse_content=RiftWizard.INSTRUCTIONS_TARGET)
    cur_y += linesize

    char_keybind_str = pygame.key.name(self.key_binds[RiftWizard.KEY_BIND_CHAR][0]).upper()
    color = self.game.p1.discount_tag.color.to_tup() if self.game.p1.discount_tag else (255, 255, 255)
    self.draw_string("Character Sheet (%s)" % char_keybind_str, self.character_display, cur_x, cur_y, color=color, mouse_content=RiftWizard.CHAR_SHEET_TARGET)

    self.character_display.set_clip(None)

    self.screen.blit(self.character_display, (0, 0))