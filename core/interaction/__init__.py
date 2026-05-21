from core.interaction.browser_interaction_engine import (
    build_interaction_plan,
    click_element,
    fill_input,
    hover_element,
    record_interaction,
    select_option,
    wait_for_selector,
)
from core.interaction.infinite_scroll_engine import extract_infinite_scroll
from core.interaction.interaction_graph_engine import (
    build_interaction_graph,
    interaction_graph_to_runtime_ir,
)
from core.interaction.interaction_replay_engine import replay_interactions
from core.interaction.interaction_replay_store import (
    load_interaction_replay,
    save_interaction_replay,
)
from core.interaction.modal_runtime_engine import close_modal, detect_modals
from core.interaction.pagination_engine import extract_paginated_content
from core.interaction.tab_runtime_engine import capture_tabs, switch_tab

__all__ = [
    "build_interaction_plan",
    "record_interaction",
    "click_element",
    "fill_input",
    "select_option",
    "hover_element",
    "wait_for_selector",
    "replay_interactions",
    "build_interaction_graph",
    "interaction_graph_to_runtime_ir",
    "extract_infinite_scroll",
    "extract_paginated_content",
    "detect_modals",
    "close_modal",
    "capture_tabs",
    "switch_tab",
    "save_interaction_replay",
    "load_interaction_replay",
]
