import Level
import mods.API_Universal.Libraries.Library_QuickPatch.Library_QuickPatch as Library_QuickPatch
import time, random
from typing import List

def unit_init(self, *args, **kwargs):
    self.haste = 0

Library_QuickPatch.patch_init(Level.Unit, unit_init)

class TurnAdvancer:

    def __init__(self, order):
        self.order = order
        self.level = None

    def setup(self):
        pass

    def advance(self):
        yield from ()

    def __getattr__(self, attribute):
        # Redirect accesses to 
        return getattr(self.level, attribute)

class TurnAdvancerSplit(TurnAdvancer):

    def __init__(self, order, splits):
        super().__init__(order)
        self.splits = splits

    def advance(self):
        for split in self.splits:
            yield from self.advance_split(split)

    def advance_split(self, split):
        yield from ()

class TurnUnits(TurnAdvancerSplit):

    def __init__(self, order):
        super().__init__(order, [True, False])

    def setup(self):
        # Store units to enforce summoning sickness
        self.turn_units = list(self.units)

    def advance_split(self, is_player_turn):
        units = [unit for unit in self.turn_units if unit.is_player_controlled == is_player_turn]
        random.shuffle(units)

        for unit in units:
            if not unit.is_alive():
                continue
            unit.pre_advance()
            finished_advance = False
            while not finished_advance:
                if unit.is_player_controlled and not unit.is_stunned() and not self.requested_action:
                    self.level.is_awaiting_input = True
                    yield
                finished_advance = unit.advance()
                if unit.haste and unit.is_alive():
                    finished_advance = False
                    unit.haste -= 1
                
                #yield
                yield from advance_spells(self)
            # Advance buffs after advancing spells
            unit.advance_buffs()
            yield from advance_spells(self)
            self.level.frame_units_moved += 1
            
            # Yield if the current advance frame is aboive the advance time budget
            if time.time() - self.frame_start_time > Level.MAX_ADVANCE_TIME:
                yield

class TurnClouds(TurnAdvancerSplit):

    def __init__(self, order):
        super().__init__(order, [True, False])

    def setup(self):
        pass

    def advance_split(self, is_player_turn):
        clouds = [cloud for cloud in self.clouds if cloud.owner.is_player_controlled == is_player_turn]
        if clouds:
            for cloud in clouds:
                if cloud.is_alive:
                    cloud.advance()
            yield from advance_spells(self)

class TurnProps(TurnAdvancer):
    def advance(self):
        for prop in list(self.props):
            prop.advance()
        yield from advance_spells(self)

def advance_spells(self: Level.Level):
    while self.can_advance_spells():
        yield self.advance_spells()

TURN_CLOUDS = TurnClouds(100)
TURN_UNITS = TurnUnits(200)
TURN_PROPS = TurnProps(300)

turn_advancers: List[TurnAdvancer] = [
    TURN_CLOUDS,
    TURN_UNITS,
    TURN_PROPS
]

def iter_frame(self: Level.Level, mark_turn_end=False):
    # An iterator representing the order of turns for all game objects
    while True:
        # Yield once per iteration if there are no units to prevent infinite loop
        if not self.units:
            yield
        self.turn_no += 1
        if any(u.team != Level.TEAM_PLAYER for u in self.units):
            self.next_log_turn()
            self.combat_log.debug("Level %d, Turn %d begins." % (self.level_no, self.turn_no))

        turn_advancers.sort(key=lambda x: x.order)
        for turn_advancer in turn_advancers:
            turn_advancer.level = self
            turn_advancer.setup()
            yield from turn_advancer.advance()
        
        if not Level.visual_mode:
            yield True