
from AoE2ScenarioParser.local_config import folder_de
from AoE2ScenarioParser.scenarios.aoe2_scenario import AoE2Scenario
from AoE2ScenarioParser.datasets.effects import EffectId
from AoE2ScenarioParser.objects.data_objects.effect import Effect


class XsEffect(Effect):

    def __init__(self, xs: str):
        super().__init__(
            effect_type=EffectId.SCRIPT_CALL,
            ai_script_goal=-1,
            quantity=-1,
            tribute_list=-1,
            diplomacy=-1,
            object_list_unit_id=-1,
            source_player=-1,
            target_player=-1,
            technology=-1,
            string_id=-1,
            display_time=-1,
            trigger_id=-1,
            location_x=-1,
            location_y=-1,
            location_object_reference=-1,
            area_x1=-1,
            area_y1=-1,
            area_x2=-1,
            area_y2=-1,
            object_group=-1,
            object_type=-1,
            instruction_panel_position=-1,
            attack_stance=-1,
            time_unit=-1,
            enabled=-1,
            food=-1,
            wood=-1,
            stone=-1,
            gold=-1,
            item_id=-1,
            flash_object=-1,
            force_research_technology=-1,
            visibility_state=-1,
            scroll=-1,
            operation=-1,
            object_list_unit_id_2=-1,
            button_location=-1,
            ai_signal_value=-1,
            object_attributes=-1,
            variable=-1,
            timer=-1,
            facet=-1,
            play_sound=-1,
            player_color=-1,
            color_mood=-1,
            reset_timer=-1,
            object_state=-1,
            action_type=-1,
            message=xs,
            sound_name="",
        )

    @property
    def xs(self) -> str:
        return self.message

    @xs.setter
    def xs(self, value: str):
        self.message = value


filename = "aaaaa"
scenario = AoE2Scenario.from_file(f"{folder_de}{filename}.aoe2scenario")
tm, um, mm, xm, pm, msm = scenario.trigger_manager, scenario.unit_manager, scenario.map_manager, scenario.xs_manager, \
    scenario.player_manager, scenario.message_manager

trigger = tm.add_trigger('test')
trigger.effects.append(XsEffect("Some XS that should be in the effect now :)"))

scenario.write_to_file(f"{folder_de}{filename}_written.aoe2scenario")
