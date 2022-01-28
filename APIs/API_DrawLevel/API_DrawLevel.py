import Level
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
        return any(layer.occludes(x, y) for layer in self.occluded_by)

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

class LayerThreat (Layer):
    def __init__(self):
        super().__init__(500)

    def should_draw(self):
        keys = pygame.key.get_pressed()
        return any(k and keys[k] for k in self.key_binds[RiftWizard.KEY_BIND_THREAT]) and self.game.is_awaiting_input()

    def draw_layer(self):
        self.draw_threat()

class LayerSpellTarget (Layer):
    def __init__(self):
        super().__init__(500)

    def should_draw(self):
        return self.cur_spell

    def draw_layer(self):	
        self.draw_targeting()

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

class LayerTiles (Layer):

    def __init__(self):
        super().__init__(100)
        self.tiles: List[Level.Tile] = []
        self.partially_occluded_by: List[Layer] = []
        self.occlusion: Set = set()

    def accept_tile(self, tile):
        self.tiles.append(tile)
        self.occlusion.add((tile.x, tile.y))

    def draw_layer(self):
        for tile in self.tiles:
            should_draw_tile = True
            if self.is_occluded(tile.x, tile.y, tile=tile):
                should_draw_tile = False
            if should_draw_tile:
                partial_occulde = self.is_partially_occluded(tile.x, tile.y)
                self.draw_tile(tile, partial_occulde=partial_occulde)

    def reset(self):
        self.tiles.clear()
        self.occlusion.clear()

    def is_occluded(self, x, y, tile=None):
        if tile and not tile.is_chasm and LAYER_UNITS.occludes(x,y): # Tiles are also occluded by units if they're not chasmas
            return True
        return super().is_occluded(x, y)

    def is_partially_occluded(self, x, y):
        return any(layer.occludes(x, y) for layer in self.partially_occluded_by)

    def occludes(self, x, y):
        return (x, y) in self.occlusion

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

class LayerUnits (Layer):

    def __init__(self):
        super().__init__(150)
        self.units: List[Level.Unit] = []
        self.occlusion: Set = set()

    def accept_tile(self, tile):
        if tile.unit:
            self.units.append(tile.unit)
            self.occlusion.add((tile.x, tile.y))

    def draw_layer(self):
        for unit in self.units:
            if not self.is_occluded(unit.x, unit.y):
                self.draw_unit(unit)

    def reset(self):
        self.units.clear()
        self.occlusion.clear()

    def occludes(self, x, y):
        return (x, y) in self.occlusion

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
