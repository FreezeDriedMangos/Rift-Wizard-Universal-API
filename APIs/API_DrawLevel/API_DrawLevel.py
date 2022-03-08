import Level
import LevelGen
import CommonContent
#import RiftWizard
import Spells
import pygame
from collections import namedtuple
from typing import Dict, List, Set

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

TILE_TABLE_WIDTH = LevelGen.LEVEL_SIZE
TILE_TABLE_SIZE = TILE_TABLE_WIDTH * TILE_TABLE_WIDTH

class Layer:
    def __init__(self, order):
        self.order = order
        self.occluded_by: List[Layer] = []
        self.view = None

    ## Whether the layer should be drawn at all
    def should_draw(self):
        return True

    ## Called when the layer should be drawn
    def draw_layer(self):
        pass

    ## Called once for each tile before the layer is drawn
    def accept_tile(self, tile):
        pass

    ## Called once before the layer accepts any tiles, allowing you to reset stored data
    def reset(self):
        pass

    ## Whether a tile is occluded by this layer
    def occludes(self, x, y):
        return False

    ## Checks whether a tile on this layer is occluded by another layer
    def is_occluded(self, x, y):
        for layer in self.occluded_by:
            if layer.occludes(x, y):
                return True
        return False
    
    ## Returns the entire set of occluding tiles. You should hand-implement a faster version probably in subclasses.
    def get_occluding_set(self):
        occlusion : Set = set()
        for x in range(TILE_TABLE_WIDTH):
            for y in range(TILE_TABLE_WIDTH):
                occlusion = self.occludes(x,y)
        
        return occlusion

    def __getattr__(self, attribute):
        # Redirect accesses to 
        return getattr(self.view, attribute)

class LayerLOS (Layer):
    def __init__(self):
        super().__init__(500)

    def should_draw(self):
        keys = pygame.key.get_pressed()
        return any(k and keys[k] for k in self.key_binds[RiftWizard.KEY_BIND_LOS])

    def draw_layer(self):
        self.draw_los()
    
    def get_occluding_set(self):
        return None

class LayerThreat (Layer):
    def __init__(self):
        super().__init__(500)

    def should_draw(self):
        keys = pygame.key.get_pressed()
        return any(k and keys[k] for k in self.key_binds[RiftWizard.KEY_BIND_THREAT]) and self.game.is_awaiting_input()

    def draw_layer(self):
        self.draw_threat()
    
    def get_occluding_set(self):
        return None

class LayerSpellTarget (Layer):
    def __init__(self):
        super().__init__(500)

    def should_draw(self):
        return self.cur_spell

    def draw_layer(self):
        self.draw_targeting()
    
    def get_occluding_set(self):
        return None

class LayerOrbTarget (Layer):
    def __init__(self):
        super().__init__(700)
    
    def draw_layer(self):
        if isinstance(self.examine_target, Level.Unit):
            buff = self.examine_target.get_buff(Spells.OrbBuff)
            if buff and buff.dest:
                dest = buff.dest
                rect = (dest.x * RiftWizard.SPRITE_SIZE, dest.y * RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE)
                self.level_display.blit(self.hostile_los_image, (dest.x * RiftWizard.SPRITE_SIZE, dest.y * RiftWizard.SPRITE_SIZE))
    
    def get_occluding_set(self):
        return None

class LayerChannelTarget (Layer):
    def __init__(self):
        super().__init__(50)
    
    def draw_layer(self):
        if hasattr(self.examine_target, 'level') and hasattr(self.examine_target, 'x') and hasattr(self.examine_target, 'y'):
            if isinstance(self.examine_target, Level.Unit) and self.examine_target.cur_hp > 0:
                if self.examine_target.has_buff(Level.ChannelBuff):
                    b = self.examine_target.get_buff(Level.ChannelBuff)             
                    rect = (b.spell_target.x * RiftWizard.SPRITE_SIZE, b.spell_target.y * RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE)
                    color = (60, 0, 0)
                    # TODO- red target circle(or green if ally) instead of grey background block
                    # TODO- all impacted tiles of target
                    pygame.draw.rect(self.level_display, color, rect)
    
    def get_occluding_set(self):
        return None

class LayerSoulbound (Layer):
    def __init__(self):
        super().__init__(50)
    
    def draw_layer(self):
        if hasattr(self.examine_target, 'level') and hasattr(self.examine_target, 'x') and hasattr(self.examine_target, 'y'):
            if isinstance(self.examine_target, Level.Unit) and self.examine_target.cur_hp > 0:
                if self.examine_target.has_buff(CommonContent.Soulbound):
                    b = self.examine_target.get_buff(CommonContent.Soulbound)

                    rect = (b.guardian.x * RiftWizard.SPRITE_SIZE, b.guardian.y * RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE)
                    color = (60, 0, 0)
                    pygame.draw.rect(self.level_display, color, rect)
    
    def get_occluding_set(self):
        return None

class LayerEffects (Layer):

    def __init__(self):
        super().__init__(800)
        self.occlusion: Set = set()

    def draw_layer(self):
        for e in self.effects: 
            if not self.is_occluded(e.x, e.y):
                self.draw_effect(e)

    def reset(self):
        self.occlusion.clear()
        for effect in self.effects:
            self.occlusion.add((effect.x, effect.y))

    def occludes(self, x, y):
        return (x, y) in self.occlusion
    
    def get_occluding_set(self):
        return self.occlusion

class LayerTiles (Layer):

    def __init__(self):
        super().__init__(100)
        self.tiles: List[Level.Tile] = [None] * TILE_TABLE_SIZE
        self.partially_occluded_by: List[Layer] = []
        self.occlusion : List[bool] = [False] * TILE_TABLE_SIZE
        self.non_chasms : Set = set()

    def accept_tile(self, tile):
        index = tile.x + tile.y * TILE_TABLE_WIDTH
        self.tiles[index] = tile
        self.occlusion[index] = True
        
        if not tile.is_chasm:
            self.non_chasms.add((tile.x, tile.y))

    def draw_layer(self):
        # much faster to batch the blits together
        draw_tiles = []
        
        # ask the layers for the sets and then merge them ourselves here
        # for efficiency reasons
        occluded = self.non_chasms & LAYER_UNITS.get_occluding_set()
        
        partially_occluded = set()
        
        for layer in self.occluded_by:
            occluded |= layer.get_occluding_set()
        
        for layer in self.partially_occluded_by:
            partially_occluded |= layer.get_occluding_set()

        for tile in self.tiles:
            if not (tile.x, tile.y) in occluded:
                draw_tiles.append(self.build_draw_tile(tile, partial_occlude=(tile.x, tile.y) in partially_occluded))

        self.view.level_display.blits(draw_tiles)
    
    def build_draw_tile(self, tile, partial_occlude=False):
        x = tile.x * RiftWizard.SPRITE_SIZE
        y = tile.y * RiftWizard.SPRITE_SIZE
        
        if not tile.sprites:
            tile.sprites = [None, None]

        if not partial_occlude:
            if not tile.sprites[0]:
                tile.sprites[0] = self.make_tile_sprite(tile, 0)
            image = tile.sprites[0]
        else:
            if not tile.sprites[1]:
                tile.sprites[1] = self.make_tile_sprite(tile, 1)
            image = tile.sprites[1]
        
        return (image, (x,y))


    def reset(self):
        self.non_chasms.clear()
        for index in range(TILE_TABLE_SIZE):
            self.occlusion[index] = False
            self.tiles[index] = None

    def is_occluded(self, x, y, tile=None):
        if tile and not tile.is_chasm and LAYER_UNITS.occludes(x,y): # Tiles are also occluded by units if they're not chasmas
            return True
        
        # this used to be: return super().is_occluded(x, y)
        # i'm shocked that this matters that much but it saves a full
        # millisecond per frame on average
        for layer in self.occluded_by:
            if layer.occludes(x, y):
                return True
        return False

    def is_partially_occluded(self, x, y):
        for layer in self.partially_occluded_by:
            if layer.occludes(x, y):
                return True
        return False

    def occludes(self, x, y):
        return self.occlusion[tile.x + tile.y * TILE_TABLE_WIDTH]

class LayerProps (Layer):

    def __init__(self):
        super().__init__(120)
        self.props: List[Level.Prop] = []
        self.occlusion: Set = set()

    def accept_tile(self, tile):
        if tile.prop:
            self.props.append(tile.prop)
            self.occlusion.add((tile.x, tile.y))

    def draw_layer(self):
        for prop in self.props:
            if not self.is_occluded(prop.x, prop.y):
                self.draw_prop(prop)

    def reset(self):
        self.props.clear()
        self.occlusion.clear()

    def occludes(self, x, y):
        return (x, y) in self.occlusion
    
    def get_occluding_set(self):
        return self.occlusion


def unit_build_blit(self, x, y):
    to_blit = []
    self.advance()

    if self.slide_frames:
        oldx = RiftWizard.SPRITE_SIZE * self.old_pos.x
        oldy = RiftWizard.SPRITE_SIZE * self.old_pos.y
        tween = self.slide_frames / float(RiftWizard.SLIDE_FRAMES)
        xdiff = oldx - x
        ydiff = oldy - y
        x += tween * xdiff
        y += tween * ydiff

    if self.hit_flash_colors and self.hit_flash_sub_frame < RiftWizard.HIT_FLASH_SUBFRAMES:
        flash_image = self.sheet.get_glow_frame(self.anim, self.anim_frame, self.hit_flash_colors[0], self.unit.sprite.face_left)
        to_blit.append((flash_image, (x, y)))
    elif self.unit.is_alive():
        frame_dict = self.sheet.anim_frames_flipped if self.unit.sprite.face_left else self.sheet.anim_frames

        frame = frame_dict[self.anim]
        if self.anim_frame >= len(frame):
            assert False, "Trying to render frame %d of anim %d on %s, impossible" % (self.anim_frame, self.anim, self.unit.name)
        to_draw = frame[self.anim_frame]
        to_blit.append((to_draw, (x, y)))
    
    if self.boss_glow:
        glow_image = self.sheet.get_glow_frame(self.anim, self.anim_frame, RiftWizard.Color(255, 80, 0), self.unit.sprite.face_left, outline=True)
        to_blit.append((glow_image, (x, y)))
    
    if self.hit_flash_colors:
        self.hit_flash_sub_frame += 1
        if self.hit_flash_sub_frame >= RiftWizard.HIT_FLASH_SUBFRAMES * 2:
            self.hit_flashes_shown += 1
            self.hit_flash_sub_frame = 0
            if self.hit_flashes_shown == RiftWizard.HIT_FLASH_FLASHES:
                self.hit_flash_colors = self.hit_flash_colors[1:]
                self.hit_flashes_shown = 0
                if not self.hit_flash_colors:
                    self.finished = self.is_death_flash
    
    return to_blit

class LayerUnits (Layer):

    def __init__(self):
        super().__init__(150)
        self.units: List[Level.Unit] = []
        self.occlusion: Set = set()
        self.friendly_image = RiftWizard.get_image(['friendly'])
        
        # used in build_draw_unit, but not reinitialized every time
        self.seen_types = set()

    def accept_tile(self, tile):
        if tile.unit:
            self.units.append(tile.unit)
            self.occlusion.add((tile.x, tile.y))

    def draw_layer(self):
        draw_units = []
        # healthbars mainly
        rects = []
        
        # ask the layers for the sets and then merge them ourselves here
        # for efficiency reasons
        if len(self.occluded_by) <= 0:
            for unit in self.units:
                new_units, new_rects = self.build_draw_unit(unit)
                draw_units += new_units
                rects += new_rects
        else:
            occluded = set()
        
            for layer in self.occluded_by:
                occluded |= layer.get_occluding_set()
        
            for unit in self.units:
                if not (unit.x, unit.y) in occluded:
                    new_units, new_rects = self.build_draw_unit(unit)
                    draw_units += new_units
                    rects += new_rects
        
        self.view.level_display.blits(draw_units)
        
        for color,rect in rects:
            pygame.draw.rect(self.view.level_display, color, rect)

    def build_draw_unit(self, u):
        x = u.x * RiftWizard.SPRITE_SIZE
        y = u.y * RiftWizard.SPRITE_SIZE
        rects = []

        if u.transform_asset_name:
            if not u.Transform_Anim:
                u.Transform_Anim = self.get_anim(u, forced_name=u.transform_asset_name)
            to_blit = unit_build_blit(u.Transform_Anim,x,y)
        else:
            if not u.Anim:
                u.Anim = self.get_anim(u)
            to_blit = unit_build_blit(u.Anim, x,y)

        # Friendlyness icon
        if not u.is_player_controlled and not Level.are_hostile(u, self.view.game.p1):
            image = self.friendly_image
            
            frame_num = 0
            num_frames = image.get_width() // RiftWizard.STATUS_ICON_SIZE
            frame_num = RiftWizard.cloud_frame_clock // RiftWizard.STATUS_SUBFRAMES % num_frames 
            source_rect = (RiftWizard.STATUS_ICON_SIZE*frame_num, 0, RiftWizard.STATUS_ICON_SIZE, RiftWizard.STATUS_ICON_SIZE)
            
            to_blit.append((image, (x + RiftWizard.SPRITE_SIZE - 4, y+1), source_rect))
        
        # Lifebar
        if u.cur_hp != u.max_hp:
            hp_percent = u.cur_hp / float(u.max_hp)
            max_bar = RiftWizard.SPRITE_SIZE - 2
            bar_pixels = int(hp_percent * max_bar)
            margin = (max_bar - bar_pixels) // 2
            rects.append(((255, 0, 0, 128), (x + 1 + margin, y+RiftWizard.SPRITE_SIZE-2, bar_pixels, 1)))

        # Draw Buffs
        status_effects = []
        
        self.seen_types.clear()
        for b in u.buffs:
            # Do not display icons for passives- aka, passive regeneration
            if b.buff_type == RiftWizard.BUFF_TYPE_PASSIVE:
                continue
            if b.asset == None:
                continue
            if type(b) in self.seen_types:
                continue
            self.seen_types.add(type(b))
            status_effects.append(b)

        if not status_effects:
            return (to_blit, rects)

        buff_x = x+1
        buff_index = RiftWizard.cloud_frame_clock // (RiftWizard.STATUS_SUBFRAMES * 4) % len(status_effects)
        
        b = status_effects[buff_index]

        image = None
        if not b.asset:
            image = RiftWizard.get_image(b.asset)
        
        if image:
            num_frames = image.get_width() // RiftWizard.STATUS_ICON_SIZE

            frame_num = RiftWizard.cloud_frame_clock // RiftWizard.STATUS_SUBFRAMES % num_frames 
            source_rect = (RiftWizard.STATUS_ICON_SIZE*frame_num, 0, RiftWizard.STATUS_ICON_SIZE, RiftWizard.STATUS_ICON_SIZE)
        
            to_blit.append((image, (buff_x, y+1), source_rect))
        else:
            color = b.color if b.color else RiftWizard.Color(255, 255, 255)
            rects.append((color.to_tup(), (buff_x, y+1, 3, 3)))
        
        return (to_blit, rects)

    def reset(self):
        self.units.clear()
        self.occlusion.clear()

    def occludes(self, x, y):
        return (x, y) in self.occlusion
    
    def get_occluding_set(self):
        return self.occlusion

class LayerClouds (Layer):

    def __init__(self):
        super().__init__(200)
        self.clouds: List[Level.Cloud] = []
        self.occlusion: Set = set()

    def accept_tile(self, tile):
        if tile.cloud:
            self.clouds.append(tile.cloud)
            self.occlusion.add((tile.x, tile.y))

    def draw_layer(self):
        for cloud in self.clouds:
            if not self.is_occluded(cloud.x, cloud.y):
                self.draw_cloud(cloud)

    def reset(self):
        self.clouds.clear()
        self.occlusion.clear()

    def occludes(self, x, y):
        return (x, y) in self.occlusion
    
    def get_occluding_set(self):
        return self.occlusion
    
class LayerDeploy (Layer):

    def __init__(self):
        super().__init__(1000)

    def draw_layer(self):
        level = self.get_display_level()
        image = RiftWizard.get_image(["UI", "deploy_ok_animated"]) if level.can_stand(self.deploy_target.x, self.deploy_target.y, self.game.p1) else RiftWizard.get_image(["UI", "deploy_no_animated"])
        deploy_frames = image.get_width() // RiftWizard.SPRITE_SIZE
        deploy_frame = RiftWizard.idle_frame % deploy_frames
        self.level_display.blit(image, (self.deploy_target.x * RiftWizard.SPRITE_SIZE, self.deploy_target.y * RiftWizard.SPRITE_SIZE), (deploy_frame * RiftWizard.SPRITE_SIZE, 0, RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE))

    def should_draw(self):
        return self.game.deploying and self.deploy_target
    
    def get_occluding_set(self):
        return None

class LayerSelection (Layer):

    def __init__(self):
        super().__init__(110)
        self.selection = None

    def accept_tile(self, tile):
        if self.examine_target and (self.examine_target in [tile.unit, tile.cloud, tile.prop]):
            self.selection = self.examine_target

    def should_draw(self):
        return self.selection

    def draw_layer(self):
        rect = (self.selection.x * RiftWizard.SPRITE_SIZE, self.selection.y * RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE, RiftWizard.SPRITE_SIZE)
        color = (60, 60, 60)
        pygame.draw.rect(self.level_display, color, rect)

    def reset(self):
        self.selection = None
    
    def get_occluding_set(self):
        return None

LAYER_SOULBOUND = LayerSoulbound()
LAYER_SPELL_TARGET = LayerSpellTarget()
LAYER_CHANNEL_TARGET = LayerChannelTarget()
LAYER_ORB_TARGET = LayerOrbTarget()
LAYER_THREAT = LayerThreat()
LAYER_LOS = LayerLOS()
LAYER_TILES = LayerTiles()
LAYER_UNITS = LayerUnits()
LAYER_PROPS = LayerProps()
LAYER_EFFECTS = LayerEffects()
LAYER_CLOUDS = LayerClouds()
LAYER_DEPLOY = LayerDeploy()
LAYER_SELECTION = LayerSelection()

LAYER_TILES.occluded_by = [LAYER_PROPS]
LAYER_TILES.partially_occluded_by = [LAYER_EFFECTS, LAYER_UNITS]
LAYER_PROPS.occluded_by = [LAYER_UNITS, LAYER_EFFECTS, LAYER_CLOUDS]

layers: List[Layer] = [
    LAYER_SOULBOUND,
    LAYER_SPELL_TARGET,
    LAYER_CHANNEL_TARGET,
    LAYER_ORB_TARGET,
    LAYER_THREAT,
    LAYER_LOS,
    LAYER_EFFECTS,
    LAYER_TILES,
    LAYER_UNITS,
    LAYER_PROPS,
    LAYER_CLOUDS,
    LAYER_DEPLOY,
    LAYER_SELECTION
]

def draw_level(self):
    if self.gameover_frames >= 8:
        return

    level = self.get_display_level()
    self.level_display.fill((0, 0, 0))

    layers.sort(key = lambda x: x.order)

    for layer in layers:
        layer.view = self
        layer.reset()
    
    #Transform and drain the levels effects
    to_remove = []
    for effect in level.effects:
        if not hasattr(effect, 'graphic'):
            graphic = self.get_effect(effect)
            if not graphic:
                to_remove.append(effect)
                continue

            effect.graphic = graphic
            graphic.level_effect = effect
            # Queue buff effects, instantly play other effects

            # Damage effects can replace damage effects
            # Buff effects queue after everything
            # Damage effects queue after buff effects
            queued_colors = [
                Level.Tags.Buff_Apply.color,
                Level.Tags.Debuff_Apply.color,
                Level.Tags.Shield_Apply.color,
                Level.Tags.Shield_Expire.color,
            ]
            if hasattr(effect, 'color') and effect.color in queued_colors:
                self.queue_effect(graphic)
            else:
                self.effects.append(graphic)
            
    # Kill sound effects
    for effect in to_remove:
        level.effects.remove(effect)

    # Draw the board
    self.advance_queued_effects()

    if self.game.next_level:
        self.deploy_anim_frames += 1
        self.deploy_anim_frames = min(self.deploy_anim_frames, self.get_max_deploy_frames())
    elif self.game.prev_next_level and self.deploy_anim_frames > 0:
        self.deploy_anim_frames -= 1

    def get_level(i, j):
        if not self.deploy_anim_frames:
            return self.game.cur_level

        cur_radius = RiftWizard.DEPLOY_SPEED*self.deploy_anim_frames
        if abs(i-self.game.p1.x) + abs(j-self.game.p1.y) > cur_radius:
            return self.game.cur_level
        else:
            return self.game.next_level or self.game.prev_next_level


    for i in range(0, RiftWizard.LEVEL_SIZE):
        for j in range(0, RiftWizard.LEVEL_SIZE):
            
            level = get_level(i, j)
    
            tile = level.tiles[i][j]

            for layer in layers:
                layer.accept_tile(tile)

    for layer in layers:
        if layer.should_draw():
            layer.draw_layer()
    
    for e in self.effects:
        if e.finished:
            if hasattr(e, 'level_effect'):
                # Sometimes this will fail if you transfer to the next level
                # Whatever (itll be garbage collected with the level anyway)
                if e.level_effect in self.game.cur_level.effects:
                    self.game.cur_level.effects.remove(e.level_effect)
                elif self.game.next_level and e.level_effect in self.game.next_level.effects:
                    self.game.next_level.effects.remove(e.level_effect)

    self.effects = [e for e in self.effects if not e.finished]

    # Blit to main screen
    pygame.transform.scale(self.whole_level_display, (self.screen.get_width(), self.screen.get_height()), self.screen)
