import Level
import time, random

def advance_spells(self: Level.Level):
    while self.can_advance_spells():
        yield self.advance_spells()

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
        # Cache unit list here to enforce summoning delay
        turn_units = list(self.units)
        for is_player_turn in [True, False]:
            clouds = [cloud for cloud in self.clouds if cloud.owner.is_player_controlled == is_player_turn]
            if clouds:
                for cloud in clouds:
                    if cloud.is_alive:
                        cloud.advance()
                yield from advance_spells(self)
            units = [unit for unit in turn_units if unit.is_player_controlled == is_player_turn]
            random.shuffle(units)
            for unit in units:
                if not unit.is_alive():
                    continue
                unit.pre_advance()
                finished_advance = False
                while not finished_advance:
                    if unit.is_player_controlled and not unit.is_stunned() and not self.requested_action:
                        self.is_awaiting_input = True
                        yield
                    finished_advance = unit.advance()
                    
                #yield
                yield from advance_spells(self)
                # Advance buffs after advancing spells
                unit.advance_buffs()
                yield from advance_spells(self)
                self.frame_units_moved += 1
                
                # Yield if the current advance frame is aboive the advance time budget
                if time.time() - self.frame_start_time > Level.MAX_ADVANCE_TIME:
                    yield
        # Advance all props similtaneously
        for prop in list(self.props):
            prop.advance()
        # In the unlikely event that that created effects, advance them
        yield from advance_spells(self)
        if not Level.visual_mode:
            yield True