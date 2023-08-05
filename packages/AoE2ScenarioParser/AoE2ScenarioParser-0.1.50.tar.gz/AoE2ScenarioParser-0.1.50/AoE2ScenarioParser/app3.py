from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.sections.aoe2_file_section import SectionName

filename = "../CBFRONT_DE"
scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, mm, um, xm, pm, msgm = scenario.trigger_manager, scenario.map_manager, scenario.unit_manager, \
                     scenario.xs_manager, scenario.player_manager, scenario.message_manager

scenario.sections[SectionName.OPTIONS.value].per_player_number_of_disabled_techs = [0] * 16
scenario.sections[SectionName.OPTIONS.value].per_player_number_of_disabled_units = [0] * 16
scenario.sections[SectionName.OPTIONS.value].per_player_number_of_disabled_buildings = [0] * 16

# um.units = []
# tm.triggers = []
# mm.map_size = 0
# mm.map_size = 10

# scenario._debug_byte_structure_to_file('structure.txt')

filename = "empty2p"
scenario2 = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm2, mm2, um2, xm2, pm2, msgm2 = scenario2.trigger_manager, scenario2.map_manager, scenario2.unit_manager, \
                     scenario2.xs_manager, scenario2.player_manager, scenario2.message_manager

# tm2.triggers = [tm.triggers[0]]
tm2.triggers = tm.triggers
mm2.terrain = mm.terrain
um2.units = um.units
pm2.players = pm.players

msgm2.instructions = msgm.instructions
msgm2.hints = msgm.hints
msgm2.victory = msgm.victory
msgm2.loss = msgm.loss
msgm2.history = msgm.history
msgm2.scouts = msgm.scouts
msgm2.instructions_string_table_id = msgm.instructions_string_table_id
msgm2.hints_string_table_id = msgm.hints_string_table_id
msgm2.victory_string_table_id = msgm.victory_string_table_id
msgm2.loss_string_table_id = msgm.loss_string_table_id
msgm2.history_string_table_id = msgm.history_string_table_id
msgm2.scouts_string_table_id = msgm.scouts_string_table_id

scenario2.write_to_file(f"{folder_de}{filename}_output_new.aoe2scenario")
