from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.objects.support.trigger_select import TS
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario


filename = "relics"
scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
                     scenario.player_manager, scenario.message_manager


print(tm)


# scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
