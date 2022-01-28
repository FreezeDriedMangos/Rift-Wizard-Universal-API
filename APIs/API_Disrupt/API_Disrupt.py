import Level

def disrupt_default(self, caster):
	self.level_gen_params = caster.level.gen_params.make_child_generator()
	self.description = self.level_gen_params.get_description()
	self.next_level = None
	caster.level.flash(self.x, self.y, Level.Tags.Arcane.color)

def disrupt_portals_cast_instant(self, x, y):
	gates = [tile.prop for tile in self.caster.level.iter_tiles() if isinstance(tile.prop, Level.Portal)]
	for gate in gates:
		gate.disrupt(self.caster)