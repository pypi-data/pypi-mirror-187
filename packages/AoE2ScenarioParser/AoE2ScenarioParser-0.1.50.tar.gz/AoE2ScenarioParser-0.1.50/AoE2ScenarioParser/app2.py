from typing import List

from ordered_set import OrderedSet

from AoE2ScenarioParser.datasets.terrains import TerrainId
from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.objects.data_objects.terrain_tile import TerrainTile
from AoE2ScenarioParser.objects.support import AreaPattern, Tile
from AoE2ScenarioParser.scenarios.aoe2_de_scenario import AoE2DEScenario

filename = "relics"
scenario = AoE2DEScenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

data_triggers = scenario.actions.load_data_triggers()

area_pattern: AreaPattern = data_triggers.areas['relics'][0]

chunks: List[OrderedSet[TerrainTile]] = area_pattern.use_pattern_grid(block_size=2).to_chunks(as_terrain=True)


x: Tile


for chunk in chunks:
    for tile in chunk:
        tile.terrain_id = TerrainId.BEACH_ICE

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
