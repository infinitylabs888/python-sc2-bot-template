import sc2
from sc2 import BotAI, Race
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2, Point3


class CompetitiveBot(BotAI):
    NAME: str = "VoidRay"
    """This bot's name"""
    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    def __init__(self):
        ### Initiating built in Classes
        sc2.BotAI.__init__(self)

    async def on_start(self):
        print("Game started")
        self.draw_ramp_points()
        # Do things here before the game starts

    async def on_step(self, iteration):
        nexus = self.townhalls.ready.random
        # Assign tasks to workers 
        await self.distribute_workers()
       
        await self.get_coordinates(nexus)

        # Train new workers
        await self.train_workers(nexus)

        # Build More Supply Sources
        await self.add_new_supply(nexus)

        # Build Gateways
        await self.build_gateway(nexus)

        # Build Assimilators 
        vgs = self.vespene_geyser.closer_than(15, nexus)
        for vg in vgs:
            if self.can_afford(UnitTypeId.ASSIMILATOR):
                await self.build(UnitTypeId.ASSIMILATOR, vg)

        # Build Infantries
        await self.train_infantries(UnitTypeId.STALKER)
        await self.train_infantries(UnitTypeId.ZEALOT)

        # Build Cybernetic Core
        if (
            self.can_afford(UnitTypeId.CYBERNETICSCORE) 
            and not self.already_pending(UnitTypeId.CYBERNETICSCORE)
            and self.structures(UnitTypeId.CYBERNETICSCORE).amount < 1
        ):
            pylon = self.structures(UnitTypeId.PYLON).ready.random
            self.build(UnitTypeId.CYBERNETICSCORE, near=pylon)

        # Build Stalkers

        # Build Stargates

        # Build VoidRays

        # Attacks

        # Expand to new Bases
        if self.can_afford(UnitTypeId.NEXUS) and self.workers.amount > 21:
            self.expand_now()

    async def train_infantries(self, UnitType):
        for GW in self.structures(UnitTypeId.GATEWAY).ready.idle:
            if self.can_afford(UnitType):
                GW.train(UnitType)

        if self.units(UnitType).amount > 12:
            for unit in self.units(UnitType).ready.idle:
                targets = (self.enemy_units | self.enemy_structures).filter(lambda unit: unit.can_be_attacked)
                if targets:
                    target = targets.closest_to(unit)
                else:
                    unit.attack(self.enemy_start_locations[0])

    async def get_coordinates(self, nexus):
        NSPs = self.game_info.map_ramps
        print("There are ", len(NSPs), "RAMP in the Map")
        print("The Closet RAMP position is:\n", self.main_base_ramp)

        print(
            "Our starting position: \n", 
            "X:", nexus.position3d.x,"\n", 
            "Y:", nexus.position3d.y,"\n",  
            "Elevation:",nexus.position3d.z, "\n"
        )

    # CONSTANTLY ADDING MORE WORKERS
    async def train_workers(self, nexus):
        if (
            self.can_afford(UnitTypeId.PROBE)
            and nexus.is_idle
            and self.workers.amount < self.townhalls.amount * 22
        ):
            nexus.train(UnitTypeId.PROBE)
            

    # CONSTANTLY ADD MORE SUPPLIES UNTIL REACHING LIMITS
    async def add_new_supply(self, nexus):
        if (self.supply_left < 2 and self.already_pending(UnitTypeId.PYLON) == 0):
            if self.can_afford(UnitTypeId.PYLON):
                if self.supply_used > 16:
                    await self.build(UnitTypeId.PYLON, near=nexus)
                else:
                    await self.build(
                        UnitTypeId.PYLON, 
                        Point2((
                            self.main_base_ramp.top_center.x + 3,
                            self.main_base_ramp.top_center.y + 3,
                        ))
)
    # Build Infantry Training Buildings
    async def build_gateway(self, nexus):
        if self.can_afford(UnitTypeId.GATEWAY) and self.structures(UnitTypeId.GATEWAY).amount < 4:
            await self.build(UnitTypeId.GATEWAY, self.main_base_ramp.barracks_correct_placement)

    async def draw_ramp_points(self):
        for ramp in self.game_info.map_ramps:
            for p in ramp.points:
                h2 = self.get_terrain_z_height(p)
                pos = Point3((p.x, p.y, h2))
                color = Point3((255, 0, 0))
                if p in ramp.upper:
                    color = Point3((0, 255, 0))
                if p in ramp.upper2_for_ramp_wall:
                    color = Point3((0, 255, 255))
                if p in ramp.lower:
                    color = Point3((0, 0, 255))
                self._client.debug_box2_out(pos, half_vertex_length=0.25, color=color)



    def on_end(self, result):
        print("Game ended.")
        # Do things here after the game ends
